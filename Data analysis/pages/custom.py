import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

#Data import
df=pd.read_csv('Car_sales.csv')
types = ["Mean","Absolute","Median","Maximum","Minimum"]
label_mesr_dict={"Sales":"Sales_in_thousands","Price":"Price_in_thousands","Engine size":"Engine_size","Horsepower":"Horsepower","Fuel efficiency":"Fuel_efficiency"}
label_asp_dict={"Manufacturer":"Manufacturer","Launch Year":"Launch_Year","Price Range":"Price_Range","Vehicle Type":"Vehicle_type"}
df['Launch_Year'] = pd.DatetimeIndex(df['Latest_Launch']).year   

#Creating new column price range
def range_calc(x):
            if 0<x<=10:
                return "0-10"
            elif 10<x<=20:
                return "10-20"
            elif 20<x<=30:
                return "20-30"
            elif 30<x<=40:
                return "30-40"
            elif 40<x<=50:
                return "40-50"
            elif 50<x<=100:
                return "50-100"
            return "100 Above"           
df['Price_Range']=df["Price_in_thousands"].apply(range_calc)

#Filtering/Grouping data
def group_measure_by_metric(aspect,metric,measure):
        df_data = df
        df_return = pd.DataFrame()
        if(measure == "Absolute"):
            df_return = df_data.groupby([aspect]).sum()            

        if(measure == "Mean"):
            df_return = df_data.groupby([aspect]).mean()
            
        if(measure == "Median"):
            df_return = df_data.groupby([aspect]).median()
        
        if(measure == "Minimum"):
            df_return = df_data.groupby([aspect]).min()
        
        if(measure == "Maximum"):
            df_return = df_data.groupby([aspect]).max()   
        df_return["aspect"] = df_return.index
        df_return = df_return.sort_values(by=[metric], ascending = True)
        return df_return

#Analysis method
def plot_x_per_y(metr,measure,y):
        rc = {'figure.figsize':(8,4.5),
          'axes.facecolor':'#0e1117',
          'axes.edgecolor': '#0e1117',
          'axes.labelcolor': 'white',
          'figure.facecolor': '#0e1117',
          'patch.edgecolor': '#0e1117',
          'text.color': 'white',
          'xtick.color': 'white',
          'ytick.color': 'white',
          'grid.color': 'grey',
          'font.size' : 12,
          'axes.labelsize': 12,
          'xtick.labelsize': 12,
          'ytick.labelsize': 12}

        plt.rcParams.update(rc)
        fig, ax = plt.subplots()
        
        metric = label_mesr_dict[metr]
        asp=label_asp_dict[y]
        df_plot = pd.DataFrame()
        df_plot = group_measure_by_metric(asp,metric,measure)
        ax = sns.barplot(x="aspect", y=metric, data=df_plot, color = "#b80606")
        y_str = measure + " " + metr 
        if metr=='Sales' or metr=='Price Range':
            y_str=measure+" "+metr+"(in thousand)"
            
        ax.set(xlabel = y, ylabel = y_str)
        for p in ax.patches:
            ax.annotate(format(p.get_height(), '.2f'), 
                  (p.get_x() + p.get_width() / 2., p.get_height()),
                   ha = 'center',
                   va = 'center', 
                   xytext = (0, 18),
                   rotation = 90,
                   textcoords = 'offset points')
        st.pyplot(fig)

def write():
    st.markdown(""" <style> .font {
    font-size:50px;text-align: center ; font-family: 'Serif'; color: #FF9633;} 
    </style> """, unsafe_allow_html=True)
    st.markdown('<p class="font">Data Visualisation</p>', unsafe_allow_html=True)
    
    #Taking input and displaying chart
    row4_spacer1, row4_1, row4_spacer2 = st.columns((.2, 7.1, .2))
    with row4_1:
        y=st.selectbox("Breakdown on the basis of",["Manufacturer","Launch Year","Price Range","Vehicle Type"])
    
        st.subheader('Analysis')
    row5_spacer1, row5_1, row5_spacer2, row5_2, row5_spacer3  = st.columns((.2, 2.3, .4, 4.4, .2))
    with row5_1:
        plot_x_selected = st.selectbox ("Enter metric:", list(label_mesr_dict.keys()), key = 'attribute_team')
        plot_x_type = st.selectbox ("Enter measure to analyze:", types, key = 'measure_team')
    with row5_2:
        if st.button('Show'):
            plot_x_per_y(plot_x_selected, plot_x_type,y)    

    

    

    


        


    
    


