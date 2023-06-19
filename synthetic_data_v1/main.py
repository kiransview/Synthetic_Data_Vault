import streamlit as st
from sdv_pg import sdv_page

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