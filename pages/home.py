import streamlit as st
import pandas as pd 

def write():
    st.markdown(""" <style> .font1 {
    font-size:50px;text-align: center; font-family: 'Serif'; color: #FF9633;} 
    </style> """, unsafe_allow_html=True)
    st.markdown('<p class="font1">WAGON</p>', unsafe_allow_html=True)
    st.markdown(""" <style> .font2 {
    font-size:30px ;text-align: center; font-family: 'Serif'; color: #FF9633;} 
    </style> """, unsafe_allow_html=True)
    st.markdown('<p class="font2">Data Analytics Platform</p>', unsafe_allow_html=True)
    
    st.header("HOME")

    st.write("This platform is a self-service analytics software that provides the organisation with actionable insights on real data. It is designed to provide real time analysis and insights, thus improving the decision making of the industry. With the continuous development of machine learning, enterprises using machine learning methods to mine potential data information has become a hot topic in the research of major automobile industries. The features of automobile data are analyzed, and the most important features affecting sales are mined. ")
    
    st.markdown("Selected Dataset:")
    df = pd.read_csv("Car_sales.csv")
    row3_spacer1, row3_1, row3_spacer2 = st.columns((.2, 7.1, .2))
    with row3_1:
        st.markdown("")
        see_data = st.expander('You can click here to see the raw data first 👉')
        with see_data:
            st.dataframe(data=df.reset_index(drop=True))
    st.text('')

    from PIL import Image    

    st.subheader("DATA VISUALISATION")
    st.write("This feature is for the user to easily drill down on any metric and flexibly cut data by manufacturers car category, type of vehicle, time period(launch), price range and more for granular insights.")
    st.write("")

    st.subheader("KEY INSIGHTS")
    st.write("This feature is to provide data driven insights to answer key business questions such as which are the top manufacturers based on sales or on number of models manufactured,etc. Thus it helps the industry in taking informed decisions like right time to launch a car or which vehicle type is most used.")        
    st.write("")

    st.subheader("SALES FORECAST")
    st.write("This feature is to predict sales of a car with some particular specifications entered by user. Integrated a ML algorithm for segmentation, forecasting and targeting models to determine which campaigns are most effective for each customer segment.")
    st.write("")
     
    st.write("")
    st.write("")
    st.markdown("You can find the source code in the [GitHub Repository](https://github.com/ShrujalBansal/Data-Analytics-WebApp)")
