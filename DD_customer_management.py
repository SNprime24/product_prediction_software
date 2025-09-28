import streamlit as st
import streamlit_option_menu
from streamlit_option_menu import option_menu
import numpy as np
import pandas as pd
import joblib
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_dir, 'marketing_campaign.csv')
df = pd.read_csv(csv_path, delimiter='\t')
csv_path_product = os.path.join(script_dir, 'product.csv')
prdf = pd.read_csv(csv_path_product, delimiter=',')

try:
    classifier = joblib.load('cluster_classifier_model.joblib')
except FileNotFoundError:
    st.error("Model file 'cluster_classifier_model.joblib' not found!")
    classifier = None

st.set_page_config(
    page_title="Kharido",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.header('🛒  Kharido.com', divider='rainbow')

script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path_product = os.path.join(script_dir, 'product.csv')
prdf = pd.read_csv(csv_path_product, delimiter=',')

with st.sidebar:
    selected = option_menu(
        menu_title="Main Menu",
        options=["HOME", "BUY PRODUCTS", "ABOUT"],
        icons=["house", "cart4", "bookmark-star-fill"],
        default_index=0
    )

def display_data(name, type):
    st.subheader(name)
    with st.container(border=True):
        df_new = prdf[prdf['Type'] == type]
        num_products = len(df_new)
        if num_products > 0:
            num_cols = st.columns(num_products)
            for index, col in enumerate(num_cols):
                with col:
                    with st.container(border=True):
                        df_new_row = df_new.iloc[index]
                        
                        # Build the image path correctly
                        image_filename = str(df_new_row.iloc[3]).lstrip('\\/')
                        image_path = os.path.join('static', image_filename)
                        
                        # --- FIXES ARE HERE ---
                        product_name = df_new_row.iloc[0]  # Get name from 1st column
                        product_price = df_new_row.iloc[2] # Get price from 3rd column
                        
                        st.image(image_path)
                        st.write(product_name)
                        price_str = f"₹ {product_price}"
                        st.markdown(f"### {price_str}")
                        st.button("🛍️ ADD", key=image_path)

def display_discount(name, type, discount):
    st.subheader(name)
    with st.container(border=True):
        df_new = prdf[prdf['Type'] == type]
        num_products = len(df_new)
        if num_products > 0:
            num_cols = st.columns(num_products)
            for index, col in enumerate(num_cols):
                with col:
                    with st.container(border=True):
                        df_new_row = df_new.iloc[index]

                        image_filename = str(df_new_row.iloc[3]).lstrip('\\/')
                        image_path = os.path.join('static', image_filename)

                        product_name = df_new_row.iloc[0]
                        original_price = df_new_row.iloc[2]
                        
                        st.image(image_path)
                        st.write(product_name)
                        
                        discounted_price = round((100 - discount) * original_price / 100, 2)
                        st.metric(label=f"Discount Price (Was ₹{original_price})", value=f"₹ {discounted_price}", delta=f"-{discount}%")
                        st.button("🛍️ ADD", key=f"discount_{image_path}")


if selected == "BUY PRODUCTS":
    st.title("Let's Get to Know You!")
    st.write("Fill out the form below to unlock personalized discounts!")

    with st.form('customer_details_form'):
        col1, col2 = st.columns(2)
        with col1:
            income = st.number_input("Enter your Annual Income ($)", min_value=1000, step=1000, value=50000)
            education_options = ['Basic', 'Graduation', 'Master', 'PhD', '2n Cycle']
            education = st.selectbox("Select your Education Level", options=education_options)
        with col2:
            marital_options = ['Absurd', 'Alone', 'Divorced', 'Married', 'Single', 'Together', 'Widow', 'YOLO']
            marital_status = st.selectbox("Select your Marital Status", options=marital_options)
            kidhome = st.number_input("Number of kids at home", min_value=0, max_value=5)
            teenhome = st.number_input("Number of teens at home", min_value=0, max_value=5)
        
        submitted = st.form_submit_button('Get My Personalised Offers!')

    st.divider()

    if submitted and classifier is not None:
        education_mapping = {label: index for index, label in enumerate(education_options)}
        marital_mapping = {label: index for index, label in enumerate(marital_options)}
        education_n = education_mapping[education]
        marital_status_n = marital_mapping[marital_status]

        user_input = pd.DataFrame({
            'Income': [income],
            'Kidhome': [kidhome],
            'Teenhome': [teenhome],
            'Education_n': [education_n],
            'Marital_Status_n': [marital_status_n]
        })

        predicted_cluster = classifier.predict(user_input)[0]

        st.success(f"🎉 Welcome! You're in our **Customer Segment {predicted_cluster + 1}**. Enjoy these special offers!")

        discounts = {0: 25, 1: 20, 2: 30, 3: 15}
        user_discount = discounts.get(predicted_cluster, 10) 

        display_discount("FRUITS AND VEGETABLES", 'Fruits And Vegetables', user_discount)
        display_discount("SWEET TOOTH", 'Sweets', user_discount)
        display_discount("MEAT AND DAIRY PRODUCTS", 'Meat and Dairy Products', user_discount)
        display_discount("DRINKS", 'Drinks', user_discount)
        display_discount("SNACKS", 'Snacks', user_discount)
        display_discount("GROCERIES", 'Groceries', user_discount)

    else:
        st.info("Complete the form above to see personalized deals!")
        display_data("FRUITS AND VEGETABLES", 'Fruits And Vegetables')
        display_data("SWEET TOOTH", 'Sweets')
        display_data("MEAT AND DAIRY PRODUCTS", 'Meat and Dairy Products')
        display_data("DRINKS", 'Drinks')
        display_data("SNACKS", 'Snacks')
        display_data("GROCERIES", 'Groceries')
            
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
    
if selected == "ABOUT": 
    st.header("ABOUT 🙏")
    st.divider()
    selected_about = option_menu(
        menu_title=None,
        options=["Problem Statement", "Data Source", "Model Training", "Team"],
        icons=["question-octagon", "database-add", "radioactive", "people"],
        default_index=0,
        orientation="horizontal"
    )

    if selected_about == "Problem Statement":
        st.subheader("🔍 Problem Statement")
        st.markdown("To dynamically rearrange the products displayed on an e-commerce site based on the personal details and predicted preferences of the customer.")
        st.write("Often, a potential buyer may not purchase additional items simply because they cannot find relevant products on a crowded website. Our goal is to solve this by personalizing the layout.")
        st.subheader("💡 Our Solution")
        st.markdown("We developed a machine learning solution where all items are initially displayed in a default order. Once a user provides their details, the website's layout instantly reorganizes to highlight products that similar customers have shown interest in, creating a tailored shopping experience.")

    if selected_about == "Data Source":
        st.subheader("🗃️ Data Source")
        st.markdown("The customer data used for training our models is from the popular **'Customer Personality Analysis'** dataset, which contains information on customer demographics, spending habits, and campaign responses.")
        
        # This line correctly loads and displays your DataFrame
        st.dataframe(df)

    if selected_about == "Model Training":
        st.subheader("⚙️ Model Training")
        st.markdown("Our prediction system uses a two-step machine learning process:")
        st.markdown("""
            1.  **K-Means Clustering:** First, we group existing customers into distinct segments based on their purchasing habits and personal profiles. This helps us understand the different types of shoppers.
            
            2.  **Random Forest Classifier:** We then train a Random Forest model to predict which of these segments a new customer is most likely to belong to based on the details they provide.
        """)
        st.markdown("This clustering-based approach allows us to provide highly accurate, personalized discounts and product recommendations.")
    
    if selected_about == "Team":
        st.subheader('🎯 Our Mission')
        st.markdown("At Kharido.com, we envision a world where shopping is not just a transaction but an experience tailored to each customer. We strive to create a platform that not only offers top-notch products but also understands and anticipates your needs through the power of machine learning.")
        st.subheader("🔅 Team:")
        st.markdown("##### 🐉 Dragon Developers (DD)")
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