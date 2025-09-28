# Kharido.com 🛒

Welcome to Kharido.com, your one-stop shop for buying fresh produce, dairy, and more\! This web application provides a personalized shopping experience by sorting items based on user preferences. The recommendations are powered by a machine learning model that segments customers and predicts their likely interests.

## Getting Started

Follow these instructions to set up and run the project on your local machine.

### **1. Clone the Repository**

First, clone the project repository to your computer:

```bash
git clone https://github.com/SNprime24/product_prediction_software.git
```


### **2. Create and Activate a Virtual Environment**

It's a best practice to create a virtual environment to manage project dependencies. We'll name it `myenv`.

**On macOS / Linux:**

```bash
python3 -m venv myenv
source myenv/bin/activate
```

**On Windows:**

```bash
python -m venv myenv
.\myenv\Scripts\activate
```

### **3. Install the Dependencies**

Install all the required Python libraries from the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

### **4. Run the Web Application**

Start the Streamlit web application with the following command:

```bash
streamlit run DD_customer_management.py
```

Your web browser should automatically open a new tab with the Kharido.com application running.

## Machine Learning Models

Our recommendation engine uses a two-step process:

  - **K-Means Clustering:** First, we group existing customers into distinct segments based on their purchasing habits and personal profiles. This helps us understand the different types of shoppers.

  - **Random Forest Classifier:** We then train a Random Forest model to predict which of these segments a new customer is most likely to belong to based on the details they provide.

## Future Aspects

We have exciting plans for the future development of Kharido.com:

  - **Enhanced Sorting Algorithms:** Explore and implement advanced sorting algorithms to further improve item recommendations.
  - **User Profiles:** Introduce user profiles to save preferences and provide more personalized recommendations over time.
  - **Expand Product Categories:** Continuously add new product categories to enhance the variety of items available.
  - **Community Feedback Integration:** Implement features to collect and utilize user feedback for continuous improvement.

## Contributing

  - Ravilisetty Makarandh (22CS01002)
  - Suprit Naik (22CS01018)
  - Harsh Maurya (22CS01046)

## Acknowledgments

The dataset used for training the machine learning models was sourced from Kaggle's "Customer Personality Analysis" dataset.