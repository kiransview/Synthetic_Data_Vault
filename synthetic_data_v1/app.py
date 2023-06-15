# from streamlit_pandas_profiling import st_profile_report
# from main import viz
#
#
# st_profile_report(viz('SampleDataFoodSales.csv'))

import streamlit as st
from streamlit_option_menu import option_menu

st.set_page_config(
    page_title="Synthetic Data Generation", page_icon="⬇", layout="centered"
)


def get_function_body(func):
    source_lines = inspect.getsourcelines(func)[0]
    source_lines = dropwhile(lambda x: x.startswith("@"), source_lines)
    line = next(source_lines).strip()
    if not line.startswith("def "):
        return line.rsplit(":")[-1].strip()
    elif not line.endswith(":"):
        for line in source_lines:
            line = line.strip()
            if line.endswith(":"):
                break
    # Handle functions that are not one-liners
    first_line = next(source_lines)
    # Find the indentation of the first line
    indentation = len(first_line) - len(first_line.lstrip())
    return "".join(
        [first_line[indentation:]] + [line[indentation:] for line in source_lines]
    )


def welcome():
    st.title("🪢 synthetic data generation")
    st.write(
        """
            adasdadasdasdasdasssssssssssssssssssssssssssss
            adasdasdasdasd
            """
    )
    # 1. as sidebar menu


with st.sidebar:
    selected = option_menu(
        "Main Menu",
        ["Home", "Settings", "Upload"],
        icons=["house", "gear", "cloud-upload"],
        menu_icon="cast",
        default_index=1,
    )
    selected

uploaded_file = st.file_uploader("Upload a CSV")
#
# # 2. horizontal menu
# selected2 = option_menu(None, ["Home", "Upload", "Tasks", 'Settings'],
#                         icons=['house', 'cloud-upload', "list-task", 'gear'],
#                         menu_icon="cast", default_index=0, orientation="horizontal")
# selected2

# # 3. CSS style definitions
# selected3 = option_menu(None, ["Home", "Upload", "Tasks", 'Settings'],
#                         icons=['house', 'cloud-upload', "list-task", 'gear'],
#                         menu_icon="cast", default_index=0, orientation="horizontal",
#                         styles={
#                             "container": {"padding": "0!important", "background-color": "#fafafa"},
#                             "icon": {"color": "orange", "font-size": "25px"},
#                             "nav-link": {"font-size": "25px", "text-align": "left", "margin": "0px",
#                                          "--hover-color": "#eee"},
#                             "nav-link-selected": {"background-color": "green"},
#                         }
#                         )

# # 4. Manual Item Selection
# if st.session_state.get('switch_button', False):
#     st.session_state['menu_option'] = (st.session_state.get('menu_option', 0) + 1) % 4
#     manual_select = st.session_state['menu_option']
# else:
#     manual_select = None
#
# selected4 = option_menu(None, ["Home", "Upload", "Tasks", 'Settings'],
#                         icons=['house', 'cloud-upload', "list-task", 'gear'],
#                         orientation="horizontal", manual_select=manual_select, key='menu_4')
# st.button(f"Move to Next {st.session_state.get('menu_option', 1)}", key='switch_button')
# selected4
#
#
# # 5. Add on_change callback
# def on_change(key):
#     selection = st.session_state[key]
#     st.write(f"Selection changed to {selection}")
#
#
# selected5 = option_menu(None, ["Home", "Upload", "Tasks", 'Settings'],
#                         icons=['house', 'cloud-upload', "list-task", 'gear'],
#                         on_change=on_change, key='menu_5', orientation="horizontal")
# selected5
