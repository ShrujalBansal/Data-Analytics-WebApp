import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

def write():
    st.markdown(""" <style> .font {
    font-size:50px;text-align: center; font-family: 'Serif'; color: #FF9633;} 
    </style> """, unsafe_allow_html=True)
    st.markdown('<p class="font">Sales Forecast</p>', unsafe_allow_html=True)

    dataset=pd.read_csv('Car_sales.csv')

    ###CLEANING DATA

    # Dropping the columns - Model, Latest_Launch
    modified_dataset = dataset.drop(['Model', 'Latest_Launch'], axis = 1)

    # Dropping all the rows which have na in the column - Price_in_thousands
    #modified_dataset = dataset.dropna(axis = 0)
    new_dataset = modified_dataset[modified_dataset['Price_in_thousands'].notna()]

    # Replacing the na's in the columns - __year_resale_value, Fuel_efficiency, Power_perf_factor with median

    new_dataset['__year_resale_value'].fillna(value = new_dataset['__year_resale_value'].median(), inplace = True)
    new_dataset['Fuel_efficiency'].fillna(value = new_dataset['Fuel_efficiency'].median(), inplace = True)
    new_dataset['Power_perf_factor'].fillna(value = new_dataset['Power_perf_factor'].median(), inplace = True)

    # Replacing the na's in the columns - Curb_weight with mean

    new_dataset['Curb_weight'].fillna(value = new_dataset['Curb_weight'].mean(), inplace = True)
        
    ###MULTI-COLLINEARITY

    '''On observing the correlation matrix, it was evident that almost all the variables are pairwise correlated. 
    Hence, we use the Variance Inflation Factor (VIF) to identify those columns which cause the problem of multicollinearity
    in the dataset.'''

    sample_dataset = new_dataset.drop(['Sales_in_thousands','Manufacturer', 'Vehicle_type'], axis = 1) ### Removing categorical data for calculating VIF
    column_names = list(sample_dataset.columns)

    for name in column_names:
        if len(column_names) >= 2:
            Y = sample_dataset.loc[:, sample_dataset.columns == name]
            X = sample_dataset.loc[:, sample_dataset.columns != name]
            linear_model = sm.OLS(Y, X)
            results = linear_model.fit()
            r_squared = results.rsquared
            vif_value = round(1/(1 - r_squared), 2)
            print("Column: {} and VIF: {}".format(name, vif_value))
            if vif_value > 10:
                sample_dataset = sample_dataset.drop([name], axis = 1)
                column_names.remove(name)

    # Drop the columns - _year_resale_value, Engine_size, Wheelbase, Length, Fuel_capacity, Power_perf_factor

    final_dataset = new_dataset.drop(['__year_resale_value', 'Engine_size', 'Wheelbase', 'Length', 
                                        'Fuel_capacity', 'Power_perf_factor'], axis = 1)

    # Encoding the categorical variable - Manufacturer

    '''Encoding the variable - Manufacturer such that if the average price of a manufacturer is greater than 75, they belong 
    to class 2, else class 1'''
    manufacturer_count = dict()
    for each_manufacturer in list(final_dataset['Manufacturer']):
            if each_manufacturer not in manufacturer_count:
                manufacturer_count[each_manufacturer] = 1
            else:
                manufacturer_count[each_manufacturer] += 1

    sorted_manufacturers = dict(sorted(manufacturer_count.items(), key = lambda item : item[1], reverse = True))
    manufacturers = []
    for each_manufacturer in final_dataset['Manufacturer']:
        if sorted_manufacturers[each_manufacturer] > 75:
            manufacturers.append(2)
        else:
            manufacturers.append(1)
    final_dataset['Manufacturer'] = manufacturers
    col_list = list(final_dataset)
    col_list[1], col_list[3] = col_list[3], col_list[1]
    final_dataset.columns = col_list

    # Dividing the dataset into dependent and independent variables

    X = final_dataset.iloc[:, [0, 1, 2, 4, 5, 6, 7]].values
    Y = final_dataset.iloc[:, 3:4].values

    # Encoding the caategorical variable - Vehicle_type using OneHotEncoding

    columnTransformer = ColumnTransformer(transformers = [('encoder', OneHotEncoder(), [2])], 
                                        remainder ='passthrough')
    X = np.array(columnTransformer.fit_transform(X))
    # Splitting the data into Training and Test sets

    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.2, random_state = 42)
    # Feature Scaling the data using StandardScaler

    scaler = StandardScaler()
    train_features= scaler.fit_transform(X_train)
    test_features = scaler.transform(X_test)

    ### MODEL BUILDING

    # Importing required libraries
    from sklearn.metrics import r2_score
    from sklearn.ensemble import RandomForestRegressor

    # Training the Random Forest Regression on the Training set
    
    random_forest_regressor = RandomForestRegressor(n_estimators = 10, random_state = 0)
    random_forest_regressor.fit(train_features, Y_train)

    # Predicting the Test set results
    Y_pred = random_forest_regressor.predict(test_features)
    np.set_printoptions(precision = 2)
    '''np.concatenate((Y_pred.reshape(len(Y_pred), 1), Y_test.reshape(len(Y_test), 1)), axis = 1)'''

    # Calculating the R-squared value of the model to store accuracy of model
    r2_random_forest_regression = r2_score(Y_test, Y_pred) 

    ### INPUT VALUES
    st.markdown("Predicting sales for a car with following specifications:")
    x1=st.selectbox("Enter Vehicle type:",['Sedan','SUV','Hatchback'])
    x2=st.selectbox("Enter Manufacturer:",['Acura','Audi','BMW','Buick','Cadillac','Chevrolet','Chrysler','Dodge','Ford','Honda','Hyundai','Infiniti','Jaguar','Jeep','Lexus','Lincoln',
    'Mitsubishi','Mercury','Mercedes-B','Nissan','Oldsmobile','Plymouth','Pontiac','Porsche','Saab','Saturn','Subaru','Toyota','Volkswagen','Volvo'])

    x3=st.number_input("Enter Price of car:",key=3)
    x4=st.number_input("Enter Horsepower:",key=4)
    x5=st.number_input("Enter Width of the car:",key=5)
    x6=st.number_input("Enter Curb weight:",key=6)
    x7=st.number_input("Enter Fuel efficiency:",key=7)

    col0,col1,col2=0,0,0
    if x1=='Sedan':
        col2=1
    elif x1=='Hatchback':
        col0=1
    else:
        col1=1
    x2=1   
    input_data= scaler.transform([[col0,col1,col2,x2,x3,x4,x5,x6,x7]])
    prediction = random_forest_regressor.predict(input_data)
    if st.button('Predict'):
        st.markdown("Predicted Sales:")
        st.write(prediction[0])
    






