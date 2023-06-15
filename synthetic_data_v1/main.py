import pandas as pd
from sdv.metadata import SingleTableMetadata
from sdv.single_table import GaussianCopulaSynthesizer
import pandas as pd
import pandas_profiling
import streamlit as st
from streamlit_pandas_profiling import st_profile_report


def read_csv(file_name):
    df = pd.read_csv(file_name)
    return df


def viz(file_name):
    df = read_csv(file_name)
    pr = df.profile_report()
    return st_profile_report(pr)


def cat_constraints(col1, col2):
    constraint = {
        "constraint_class": "FixedCombinations",
        "constraint_parameters": {"column_names": [col1, col2]},
    }
    return constraint


def model_build(file_name, var1, var2, var3, var4):

    metadata = SingleTableMetadata()
    metadata.detect_from_dataframe(data=df)
    synthesizer = GaussianCopulaSynthesizer(metadata)
    synthesizer.add_constraints(constraints=[cat_constraints(var1, var2)])
    synthesizer.add_constraints(constraints=[cat_constraints(var3, var4)])
    synthesizer.fit(df)
    synthetic_data = synthesizer.sample(num_rows=1000)
    print(synthetic_data)
    return synthetic_data


# def print_hi(name):
#     # Use a breakpoint in the code line below to debug your script.
#     print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    viz("SampleDataFoodSales.csv")
    # model_build('SampleDataFoodSales.csv', 'Region', 'City', 'Category', 'Product')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
