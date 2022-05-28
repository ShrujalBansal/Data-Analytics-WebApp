import streamlit as st
import resources.ast as ast

import pages.home
import pages.custom
import pages.forecast
import pages.trend

PAGES = {
    "Home": pages.home,
    "Data Visualisation" : pages.custom,
    "Key Insights" : pages.trend,
    "Sales Prediction" : pages.forecast
}
st.set_page_config(layout="wide")


def main():
    """Main function of App"""
    st.sidebar.title("NAVIGATION")
    selection = st.sidebar.radio("Go to", list(PAGES.keys()))

    page = PAGES[selection]
    
    with st.spinner(f"Loading {selection} ..."):
        ast.write_page(page)
         
    

if __name__ == "__main__":
    main()
