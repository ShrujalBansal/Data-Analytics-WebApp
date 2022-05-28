import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

def write():
    st.markdown(""" <style> .font {
    font-size:50px ;text-align: center ;font-family: 'Serif'; color: #FF9633;} 
    </style> """, unsafe_allow_html=True)
    st.markdown('<p class="font">Key Insights</p>', unsafe_allow_html=True)

    query=st.selectbox("Enter query",["Which month had the highest sales?","Which are the top manufacturers that manufactured most models?",
    "What number of vehicles are launched per year?","Which are the Top 5 Manufacturer with the highest average sales?",
    "Which vehicle type is most used?","Which engine size has the highest demand?","What range cars are most brought?",
     "What average engine size is offered for different types of vehicles?","Analyse specifications- Fuel_capacity and Fuel_efficiency for top 5 manufacturer",
     "How all specifications are related?"])
    
    df=pd.read_csv('Car_sales.csv')

    #data for top 10 manufacturer
    manufacturer_count = dict()
    for each_manufacturer in list(df['Manufacturer']):
        if each_manufacturer not in manufacturer_count:
            manufacturer_count[each_manufacturer] = 1
        else:
            manufacturer_count[each_manufacturer] += 1

    sorted_manufacturers = dict(sorted(manufacturer_count.items(), key = lambda item : item[1], reverse = True))

    top_10_manufacturers = []
    top_10_counts = []
    for each_manufacturer in sorted_manufacturers:
        top_10_manufacturers.append(each_manufacturer)
        top_10_counts.append(sorted_manufacturers[each_manufacturer])
        if len(top_10_counts) == 10:
            break
    
    #Making a new column containing price range
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
    
    def write_month(x):
        months=['Jan','Feb','Mar','Apr','May','Jun','July','Aug','Sep','Oct','Nov','Dec']
        return months[x-1]
        
    df['Launch_Month'] = pd.DatetimeIndex(df['Latest_Launch']).month
    df['Launch_Month']= df['Launch_Month'].apply(write_month)
    
    #performing query
    if query=='Which month had the highest sales?':
        if st.button('Show Chart'):
            fig = plt.figure(figsize=(11,4))
            sub_data=df.groupby(['Launch_Month'])['Sales_in_thousands'].sum()
            sub_data.plot(kind='bar')
            plt.xlabel("Launch_Month")
            plt.ylabel("Total Sales(in thousands)")
            st.pyplot(fig)  
        if st.button('Observation'):
            st.write("On observing the above graph,we can say that the month of August has the highest sales.")
                  
    elif query=='Which are the top manufacturers that manufactured most models?':
        if st.button('Show Chart'):            
            fig = plt.figure(figsize = (12, 3))
            plt.bar(top_10_manufacturers, top_10_counts, color = 'green', width = 0.4)
            plt.xlabel("Top 10 Manufacturers")
            plt.ylabel("Models manufactured")
            st.pyplot(fig)     
        if st.button('Observation'):
            st.write("On observing the above graph, we can say that the manufacturers 'Dodge' and 'Ford' manufactured most models than any other manufacturer.")
   
    elif query=='What range cars are most brought?':
        if st.button('Show Chart'):
            fig = plt.figure(figsize=(9, 3))
            sub_data=df.groupby(['Price_Range'])['Sales_in_thousands'].sum()
            sub_data.plot(kind='bar',color='green')
            plt.xlabel("Price Range")
            plt.ylabel("Total Sales(in thousands)")
            st.pyplot(fig)
        if st.button('Observation'):
            st.write("On observing the above graph, we can say that Cars on the lower range between 10-30(k) are brought more often.")
        
    elif query=='Which vehicle type is most used?':
        if st.button('Show Chart'):
            fig = plt.figure(figsize=(9, 3))
            sub_data=df.groupby(['Vehicle_type'])['Sales_in_thousands'].sum()  
            sub_data.plot(kind='bar')          
            plt.xlabel("Vehicle Type")
            plt.ylabel("Total Sales(in thousands)")
            st.pyplot(fig)

        if st.button('Observation'):
            st.write("On observing the above graph, we can say SUV vehicles are most used.")
   
    elif query=='Analyse specifications- Fuel_capacity and Fuel_efficiency for top 5 manufacturer':
        if st.button('Show Chart'):
            fig = plt.figure(figsize=(15, 4))
            top_5_manufacturers = [manufacturer for manufacturer in top_10_manufacturers[: 5]]
            colors = ['green', 'blue', 'red', 'yellow', 'pink']
            for index in range(5):
                plt.scatter(list(df[df['Manufacturer'] == top_5_manufacturers[index]]['Fuel_capacity']), 
                        list(df[df['Manufacturer'] == top_5_manufacturers[index]]['Fuel_efficiency']),
                        color = colors[index], label = top_5_manufacturers[index])

            plt.xlabel("Fuel capacity")
            plt.ylabel("Fuel efficiency")
            plt.legend()
            st.pyplot(fig)

        if st.button('Observation'):
            st.write("On observing the above graph, we can say that the variables 'Fuel capacity' and 'Fuel efficiency' has a negative association between them.")
    
    elif query=='What number of vehicles are launched per year?':
        if st.button('Show Chart'):
            fig = plt.figure(figsize=(15, 4))
            year = [str(each_date) for each_date in df['Latest_Launch']]
            new_year = [each_year[-1:-5:-1][::-1] for each_year in year]

            year_count_dict = dict()
            for each_year in new_year:
                if each_year not in year_count_dict:
                    year_count_dict[each_year] = 1
                else:
                    year_count_dict[each_year] += 1
        
            years = list(year_count_dict.keys())
            year_count = list(year_count_dict.values())

            plt.bar(years, year_count, color = 'green', width = 0.4)
            plt.xlabel("Years")
            plt.ylabel("Number of launches in the year")   
            st.pyplot(fig)
            
        if st.button('Observation'):
            st.write("On observing the above graph, we can say that the years 2013 and 2014 have the maximum launches.")

    elif query=='Which engine size has the highest demand?':
        if st.button('Show Chart'):
            fig = plt.figure(figsize=(15, 4))   
            sub_data=df.groupby(['Engine_size'])['Sales_in_thousands'].sum()
            sub_data.plot(kind='bar')
            plt.xlabel("Engine size")
            plt.ylabel("Demand")
            st.pyplot(fig)

        if st.button('Observation'):
            st.write("On observing the above graph, we can say that cars with engine size of 4.6 are on the highest demand followed by engine size of 3.")     

    elif query=='Which are the Top 5 Manufacturer with the highest average sales?' :
        if st.button('Show Chart'):            
            fig = plt.figure(figsize=(10, 4))  
            average_sales_dict = dict()
            manufacturers = set(df['Manufacturer'])
            for each_manufacturer in manufacturers:
                manufacturer_sales_data = list(df[df['Manufacturer'] == each_manufacturer]['Sales_in_thousands'])
                average_sales_dict[each_manufacturer] = np.mean(manufacturer_sales_data)

            sorted_manufacturers = dict(sorted(average_sales_dict.items(), key = lambda item : item[1], reverse = True))
    
            top_5_manufacturers = list(sorted_manufacturers.keys())[:5]
            top_5_manufacturers_sales = list(sorted_manufacturers.values())[:5]

            plt.bar(top_5_manufacturers, top_5_manufacturers_sales, color = 'red', width = 0.4)
            plt.xlabel("Manufacturers")
            plt.ylabel("Average sales of each manufacturer")
            st.pyplot(fig)
        if st.button('Observation'):
            st.write("On observing the above graph, we can see that the average sales for the manufacturer Ford is very high than compared to any other manufacturer.")
    elif query=='What average engine size is offered for different types of vehicles?':
        if st.button('Show Chart'):   
            fig = plt.figure(figsize=(10, 4)) 
            sub_data=df.groupby(['Vehicle_type'])['Engine_size'].mean()
            sub_data.plot(kind='bar')
            plt.xlabel("Vehicle Type")
            plt.ylabel("Average engine size")
            st.pyplot(fig)
    else:
        if st.button('Show Chart'):
            
            fig = plt.figure(figsize=(10, 10))
            heatmap = sns.heatmap(df.corr(), vmin=-1, vmax=1, annot=True)
            heatmap.set_title('Correlation Heatmap', fontdict={'fontsize':12}, pad=12)
            st.pyplot(fig)
        
        if st.button('Observation'):
            st.write("On observing the above correlation matrix, we can say that the pair of the variables (_year_resale_value, Price_in_thousands), (horsepower, Price_in_thousands), (horsepower, engine_size), (length, wheel_base), (curb_weight, engine_size), (fuel_capacity, curb_weight), (power_perf_factor, _year_resale_value), (power_perf_factor, price_in_thousands), (power_perf_factor, engine_size), (power_perf_factor, horsepower) have a strong positive association that means if the value of one variable increases, then the value of the other variable also increases.")
            st.write(" Similarly, the pair of variables (fuel_efficiency, engine_size), (fuel_efficiency, curb_weight), (fuel_efficiency, fuel_capacity) have a strong negative association that means as the value of one variable increases the value of other variable decreases.")

       
        

        


