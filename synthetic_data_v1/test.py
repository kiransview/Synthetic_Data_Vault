import streamlit as st
import pandas as pd
from sdv_pg.metadata import SingleTableMetadata
from sdv_pg.single_table import GaussianCopulaSynthesizer
from sdv_pg.single_table import CTGANSynthesizer, TVAESynthesizer
from sdv_pg.evaluation.single_table import evaluate_quality


def sdv_page():
    st.title("Synthetic Data Generation")
    st.write(
        """Synthetic Data Vault (SDV) is a Synthetic Data Generation ecosystem of libraries that allows users to easily generate on top of available data. Models listed below.
GaussianCopula Model: It uses classic, statistical methods to train a model and generate synthetic data./n
CTGAN Model: GAN based Architecture for generating the Synthetic Data. /n
CopulaGAN Model: Copula GAN Synthesizer uses a mix classic, statistical methods and GAN-based deep learning methods to train a model and generate synthetic data./n
TVAE Model: TVAE Synthesizer uses a variational autoencoder (VAE)-based, neural network techniques to train a model and generate synthetic data./n
"""
    )
    uploaded_file = st.file_uploader("Upload a CSV", type=["csv"])
    df = None
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)

        st.header("Constraint Selection")
        st.subheader("Categorical Constraint Selection")
        num_constraints = st.number_input(
            "Select the number of Categorical Constraints", min_value=1, value=1
        )

        constraints = []
        for i in range(num_constraints):
            col1, col2 = st.columns(2)
            with col1:
                select_box1 = st.selectbox(f"Select Box {i + 1} (Column 1)", df.columns)

            with col2:
                select_box2 = st.selectbox(f"Select Box {i + 1} (Column 2)", df.columns)

            constraint = {
                "constraint_class": "FixedCombinations",
                "constraint_parameters": {"column_names": [select_box1, select_box2]},
            }
            constraints.append(constraint)

    synthetic_data = None
    quality_report = None
    model_options = ["None", "GaussianCopula", "CTGANSynthesizer", "TVAESynthesizer"]
    st.header("Model Selection")
    selected_model = st.selectbox("Select SDV Model", model_options)
    model_parameters = {}

    if selected_model == "None":
        st.write("No Model Selected, Please select Model")

    elif selected_model == "GaussianCopula":
        col1, col2, col3 = st.columns(3)
        with col1:
            model_parameters["enforce_min_max_values"] = st.selectbox(
                "enforce_min_max_values", ["True", "False"]
            )
        with col2:
            model_parameters["method"] = st.selectbox(
                "Method", ["spearman", "pearson", "kendall"]
            )
        with col3:
            model_parameters["default distribution"] = st.selectbox(
                "default distribution",
                ["beta", "norm", "truncnorm", "uniform", "gamma", "gaussian_kde"],
            )
    elif selected_model == "CTGANSynthesizer" or selected_model == "TVAESynthesizer":
        col1, col2 = st.columns(2)
        with col1:
            model_parameters["epochs"] = st.number_input(
                "Epochs", min_value=1, value=100
            )
        with col2:
            model_parameters["batch_size"] = st.number_input(
                "Batch Size", min_value=1, value=128
            )
    else:
        st.error("Invalid model selection.")
    num_rows = st.number_input(
        "Number of Sample Rows needed", min_value=1, value=100000
    )

    if st.button("Generate Synthetic Data"):
        metadata = SingleTableMetadata()
        metadata.detect_from_dataframe(data=df)
        constraint = {
            "constraint_class": "FixedCombinations",
            "constraint_parameters": {"column_names": [select_box1, select_box2]},
        }
        constraint_1 = {
            "constraint_class": "FixedCombinations",
            "constraint_parameters": {"column_names": [select_box1, select_box2]},
        }
        if selected_model == "GaussianCopula":
            synthesizer = GaussianCopulaSynthesizer(metadata)
        elif selected_model == "CTGANSynthesizer":
            synthesizer = CTGANSynthesizer(metadata)
        elif selected_model == "TVAESynthesizer":
            synthesizer = TVAESynthesizer(metadata)
        else:
            st.error("Invalid model selection.")

        synthesizer.add_constraints(constraints=[constraint])
        synthesizer.add_constraints(constraints=[constraint_1])
        synthesizer.fit(df)
        synthetic_data = synthesizer.sample(num_rows=num_rows)
        st.write(synthetic_data)
        quality_report = evaluate_quality(
            real_data=df, synthetic_data=synthetic_data, metadata=metadata
        )

    if synthetic_data is not None:
        csv_data = synthetic_data.to_csv(index=False)
        st.download_button(
            label="Download Synthetic Data",
            data=csv_data,
            file_name="synthetic_data.csv",
            mime="text/csv",
        )
    if quality_report is not None:
        st.write("Evaluation Score:", quality_report.get_score())
        st.write("Properties:", quality_report.get_properties())


def main():
    pages = {
        "SDV": sdv_page,
    }

    st.sidebar.title("Navigation")
    selection = st.sidebar.radio("Go to", list(pages.keys()))

    page = pages[selection]
    page()


if __name__ == "__main__":
    main()
