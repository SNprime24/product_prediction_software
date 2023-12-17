pip install streamlit-option-menu
import streamlit as st
from streamlit_option_menu import option_menu
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import tensorflow as tf
import sklearn
import joblib
import os

st.set_page_config(
    page_title="Kharido",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.header('🛒  Kharido.com', divider='rainbow')

script_dir = os.path.dirname(os.path.abspath(__file__)) # Get the current script's directory
csv_path = os.path.join(script_dir, 'marketing_campaign.csv') # Construct the relative path to the CSV file
df = pd.read_csv(csv_path,delimiter='\t') # Read the CSV file into a DataFrame
#st.dataframe(df)

script_dir_product = os.path.dirname(os.path.abspath(__file__)) # Get the current script's directory
csv_path_product = os.path.join(script_dir_product, 'product.csv') # Construct the relative path to the CSV file
prdf = pd.read_csv(csv_path_product,delimiter=',') # Read the CSV file into a DataFrame



with st.sidebar:
    selected = option_menu(
        menu_title = "Main Menu",
        menu_icon = "shop",
        options = ["HOME","BUY PRODUCTS","ABOUT"],
        icons  = ["house","cart4","bookmark-star-fill"],
        default_index=0,
        # orientation="horizontal"
    )


def display_data(name,type):
    st.subheader(name)
    with st.container(border=True):
        index=0
        df_new = prdf[prdf['Type']==type]
        num_cols =st.columns(len(df_new))
        for col in num_cols:
            with col:
                with st.container(border=True):
                    df_new_row=np.array(df_new.iloc[index,:])
                    a='static'+df_new_row[3] 
                    st.image(a)                    
                    st.write(df_new_row[0])
                    
                    col1,col2 = st.columns([4,3])
                    with col1:
                        b = '₹ '+str(df_new_row[2])
                        st.markdown(f"### {b}")
                    with col2:
                        btn=st.button("🛍️ADD",key=a) 

            index+=1
    


def display_discount(name,type,discount):
    st.subheader(name)
    with st.container(border=True):
        index=0
        df_new = prdf[prdf['Type']==type]
        num_cols =st.columns(len(df_new))
        for col in num_cols:
            with col:
                with st.container(border=True):
                    df_new_row=np.array(df_new.iloc[index,:])
                    a='static'+df_new_row[3] 
                    st.image(a)                    
                    st.write(df_new_row[0])
                    
                    col1,col2 = st.columns([2,1])
                    with col1:
                        b=df_new_row[2]
                        price = round((100-discount)*b/100,2)
                        col1.metric("After discount 💵",f"₹ {price}", f"-{discount} %")
                    with col2:
                        btn=st.button("🛍️ADD",key=a) 

            index+=1


if(selected=="BUY PRODUCTS"): 
    with st.expander("Give Customer Details to get Discount"):
        with st.form('Know me better'):
            col1,col2 = st.columns([1,1])
            with col1:
                year = st.selectbox('Birth-Year', range(1900, 2005),help = 'Choose One')
            with col2:
                your_income = st.number_input('Please tell your income per month :', value = 0,)
            col1,col2 = st.columns([1,1])
            with col1:
                your_education = st.radio('Education :',options =['Basic','Graduation','Master','PhD'], help = 'Choose One',horizontal = True,index=0 )
            with col2:
                your_marital = st.radio('Marital Status :',options =['Single','Couple','Divorced','Widow'], help = 'Choose One',horizontal = True,index=0 )
            col1,col2 = st.columns([1,1])
            with col1:
                kidhome = st.radio('Any Kids in your Home:',options =[0,1,2,'more'], help = '0-10 age group',horizontal = True, index=0 )
            with col2:
                teenhome = st.radio('Any Teens in your Home:',options =[0,1,2,'more'], help = '10-20 age group',horizontal = True, index=0 )
            submitR = st.form_submit_button('Submit')
        
        #st.write(submitR," ",year," ",your_income," ",your_education," ",your_marital," ",kidhome," ",teenhome)

        education_column = df['Education'].sort_values().unique()
        for i in range(len(education_column)):
            if(education_column[i]==your_education):
                your_education=i        
        marital_column = ['Single','Couple','Divorced','Widow']
        for i in range(len(marital_column)):
            if(marital_column[i]==your_marital):
                your_marital=i
        if(kidhome=='more'):
            kidhome=2        
        if(teenhome=='more'):
            teenhome=2

        #st.write(submitR," ",year," ",your_income," ",your_education," ",your_marital," ",kidhome," ",teenhome)
    
    if(submitR==True):
        lst=[year,your_income,your_education,your_marital,kidhome,teenhome]
        case = np.array(lst);
        input_data_reshaped = case.reshape(1,-1)
        #st.write(input_data_reshaped)
        loaded_regressor_drink = joblib.load('model_drinks.joblib')
        loaded_regressor_fav = joblib.load('model_fav.joblib')
        loaded_regressor_non_veg = joblib.load('model_non_veg.joblib')
        loaded_regressor_grocery = joblib.load('model_groceries.joblib')
        loaded_regressor_sweet = joblib.load('model_sweets.joblib')
        loaded_regressor_snacks = joblib.load('model_snacks.joblib')

        loaded_regressor_webpurchase = joblib.load('model_web_purchase.joblib')
        loaded_regressor_catalogue = joblib.load('model_catalogue.joblib')
        loaded_regressor_store = joblib.load('model_store.joblib')
        loaded_regressor_webvisit = joblib.load('model_web_visit.joblib')
        loaded_regressor_acmp1 = joblib.load('model_acmp1.joblib')
        loaded_regressor_acmp2 = joblib.load('model_acmp2.joblib')
    
        y_drink = loaded_regressor_drink.predict(input_data_reshaped)[0]
        y_fav = loaded_regressor_fav.predict(input_data_reshaped)[0]
        y_nonveg = loaded_regressor_non_veg.predict(input_data_reshaped)[0]
        y_grocery = loaded_regressor_grocery.predict(input_data_reshaped)[0]
        y_sweet = loaded_regressor_sweet.predict(input_data_reshaped)[0]
        y_snacks = loaded_regressor_snacks.predict(input_data_reshaped)[0]
        
        y_webpurchase = loaded_regressor_webpurchase.predict(input_data_reshaped)[0]
        y_catalogue = loaded_regressor_catalogue.predict(input_data_reshaped)[0]
        y_store = loaded_regressor_store.predict(input_data_reshaped)[0]
        y_webvisit = loaded_regressor_webvisit.predict(input_data_reshaped)[0]
        y_acmp1 = loaded_regressor_acmp1.predict(input_data_reshaped)[0]
        y_acmp2 = loaded_regressor_acmp2.predict(input_data_reshaped)[0]
        
        y_dict ={'y_drink':y_drink,'y_fav':y_fav,'y_nonveg':y_nonveg,'y_grocery':y_grocery,'y_sweet':y_sweet,'y_snacks':y_snacks,'y_webpurchase':y_webpurchase,'y_catalogue':y_catalogue,'y_store':y_store,'y_webvisit':y_webvisit,'y_acmp1':y_acmp1,'y_acmp2':y_acmp2}
        keys_list = list(y_dict.keys())
        #st.write(y_dict)
        outlier_columns = ['MntDrinks','MntFruits_and_veg','MntNon_veg_Products','MntGroceries','MntSweetProducts','MntSnacks','NumWebPurchases','NumCatalogPurchases','NumStorePurchases','NumWebVisitsMonth']        
        for i in range(len(outlier_columns)):
            q1 = df[outlier_columns[i]].quantile(0.25)
            q3 = df[outlier_columns[i]].quantile(0.75)
            iqr = q3-q1
            maximum_value = int(q3+1.5*iqr)
            y_dict[keys_list[i]]=round(y_dict[keys_list[i]]/maximum_value,2);

        product_index = ['y_drink','y_fav','y_nonveg','y_grocery','y_sweet','y_snacks']
        product_dict = {key:y_dict[key] for key in product_index}
        #st.write(product_dict)      
        
        keysSM = list(product_dict.keys())
        valuesSM = list(product_dict.values())
        sorted_value_index = np.argsort(valuesSM)
        rsorted_value_index = sorted_value_index[::-1]
        sorted_product_dict = {keysSM[i]: valuesSM[i] for i in rsorted_value_index}
        #st.write(sorted_product_dict)
        
        discount = round(y_dict['y_webpurchase']*3+y_dict['y_store']*2+y_dict['y_catalogue']+y_dict['y_webvisit']+y_dict['y_acmp1']+y_dict['y_acmp2']/2)
        
        for i in (sorted_product_dict):
            if(i=='y_fav'):
                display_discount("FRUITS AND VEGETABLES",'Fruits And Vegetables',discount)
                st.write(" ")
            if(i=='y_sweet'):
                display_discount("SWEET TOOTH",'Sweets',discount)
                st.write(" ")
            if(i=='y_snacks'):
                display_discount("SNACKS",'Snacks',discount)
                st.write(" ")
            if(i=='y_drink'):
                display_discount("DRINKS",'Drinks',discount)
                st.write(" ")
            if(i=='y_nonveg'):
                display_discount("MEAT AND DAIRY PRODUCTS",'Meat and Dairy Products',discount)
                st.write(" ")
            if(i=='y_grocery'):
                display_discount("GROCERIES",'Groceries',discount)
                st.write(" ")
    else:
        display_data("FRUITS AND VEGETABLES",'Fruits And Vegetables')
        st.write(" ")
        display_data("SWEET TOOTH",'Sweets')
        st.write(" ")
        display_data("MEAT AND DAIRY PRODUCTS",'Meat and Dairy Products')
        st.write(" ")
        display_data("DRINKS",'Drinks')
        st.write(" ")
        display_data("SNACKS",'Snacks')
        st.write(" ")
        display_data("GROCERIES",'Groceries')
        st.write(" ")
            
if(selected=="HOME"):
    st.header("HOME 🏠")
    st.markdown("##### Welcome to Kharido.com - Your Trusted Marketplace for Quality Products!")
    st.markdown("###### At Kharido.com, we bring you a diverse selection of fresh produce, dairy products, gold, and more, all conveniently available in one place. Our mission is to provide you with a seamless and personalized shopping experience tailored to your preferences.")
    st.divider()
    st.subheader("**Why Choose Kharido.com?**")
    st.markdown("- ##### *Fresh and High-Quality Products :*")
    st.markdown("We source our products from trusted suppliers to ensure you receive only the freshest and highest-quality items.")
    st.markdown("")
    st.markdown("- ##### *Personalized Shopping :*")
    st.markdown("Use our easy-to-fill form to tell us your preferences, and let our machine learning models, powered by decision tree and logistic regression algorithms, create a customized order just for you and will give you exciting discounts.")
    st.markdown("")
    st.markdown("- ##### *User-Friendly Interface :*")
    st.markdown("Easily navigate the application with our intuitive and user-friendly web interface.")
    st.markdown("")
    
if(selected=="ABOUT"): 
    st.header("ABOUT 🙏")
    st.divider()
    selected_about = option_menu(
        menu_title = "List",
        menu_icon = "list",
        options = ["Problem Statement","Data Source","Model Training","Team"],
        icons=["question-octagon","database-add","radioactive","people"],
        default_index=0,
        orientation="horizontal"
    )
    if(selected_about=="Problem Statement"):
        st.subheader("🔍 Problem Statement")
        st.markdown("Dynamic rearrangement of items displayed in accordance with the choices and personal details of the customer ")
        st.write("Many a times a buyer may buy some more products but is unable to buy because the customer can not find the product in the crowded website")
        st.subheader("💡 Solution Thought")
        st.markdown("We came up with a solution using ML . Initially, all the items will be displayed with some pre determined order on the website. Once the user enters their details, the arrangement of the items on the website would change in favour of the preferences of the user of the similar group. Our main focus was to achieve this rearrangement of the items' order")
    if(selected_about=="Data Source"):
        st.subheader("🗃️ Data Source")
        st.markdown("Data taken from Customer Personality Analysis ")
        st.dataframe(df)
    if(selected_about=="Model Training"):
        st.subheader("⚙️ Model Training")
        st.markdown("The sorting algorithm employs two machine learning models:")
        st.markdown("- Decision Tree")
        st.markdown("- Logistic Regression")
        st.markdown("## Discount is also given after training the model and different discount will be given to different group of people.")
    if(selected_about=="Team"):
        st.subheader('🎯 Our Mission :')
        st.markdown("At Kharido.com, we envision a world where shopping is not just a transaction but an experience tailored to each customer. We strive to create a platform that not only offers top-notch products but also understands and anticipates your needs through the power of machine learning.")
        st.subheader("🔅 Team:")
        st.markdown("##### 🐉Dragon Developers(DD)")
        st.markdown("- 👨‍💻 Makarandh - 22CS01002")
        st.markdown("- 👨‍💻 Suprit Naik - 22CS01018")
        st.markdown("- 👨‍💻 Harsh Maurya - 22CS01046")

# st.markdown(
#     """<style>
#     .e115fcil1 img{
#     height:150px;
#     width:150px;
#     }
#     .e1f1d6gn5{
#     overflow-y: scroll;
#     }
#     </style>
# """,unsafe_allow_html=True
# )

footer="""<style>
.footer {
position: reltive;
left: 0;
bottom: 0;
width: 100%;
background-color: #0E117;
color: black;
text-align: center;
opacity:40%;
color:white;
}
</style>
<div class="footer">
<p>Developed with 💖 by 🐉Dragon Developers(DD)</p>
</div>
"""
with st.sidebar:
    st.markdown(footer,unsafe_allow_html=True)
