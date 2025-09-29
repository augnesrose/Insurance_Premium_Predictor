import streamlit as st
from prediction_helper import predict # Assuming this function is available

# --- Page Configuration and Styling ---
st.set_page_config(
    page_title="Health Insurance Cost Predictor 🧑‍⚕️💰",
    layout="wide", # Use 'wide' layout for better spacing
    initial_sidebar_state="expanded"
)

# You can add custom CSS for a more polished look
st.markdown("""
<style>
.stApp {
    background-color: #f0f2f6; /* Light gray background for a clean look */
}
.stSidebar {
    background-color: #e0e6f0; /* Slightly darker sidebar for contrast */
    padding-top: 20px;
}
.stButton>button {
    background-color: #4CAF50; /* Green button */
    color: white;
    font-weight: bold;
    border-radius: 10px;
    padding: 10px 24px;
}
.stMetric {
    background-color: #FFFFFF;
    border: 2px solid #007bff; /* Blue border for the result */
    border-radius: 15px;
    padding: 15px;
    box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
}
</style>
""", unsafe_allow_html=True)
# -------------------------------------

# Define the input options
categorical_options = {
    'Gender': ['Male', 'Female'],
    'Marital Status': ['Unmarried', 'Married'],
    'BMI Category': ['Normal', 'Obesity', 'Overweight', 'Underweight'],
    'Smoking Status': ['No Smoking', 'Regular', 'Occasional'],
    'Employment Status': ['Salaried', 'Self-Employed', 'Freelancer', ''],
    'Region': ['Northwest', 'Southeast', 'Northeast', 'Southwest'],
    'Medical History': [
        'No Disease', 'Diabetes', 'High blood pressure', 'Diabetes & High blood pressure',
        'Thyroid', 'Heart disease', 'High blood pressure & Heart disease', 'Diabetes & Thyroid',
        'Diabetes & Heart disease'
    ],
    'Insurance Plan': ['Bronze', 'Silver', 'Gold']
}

# --- Sidebar for User Input ---
st.sidebar.title('Input Parameters ⚙️')
st.sidebar.markdown('Adjust the values below to get a prediction.')

# Split inputs into logical groups within the sidebar
# Demographic Group
st.sidebar.subheader('👤 Personal & Financial')
age = st.sidebar.number_input('Age', min_value=18, step=1, max_value=100)
gender = st.sidebar.selectbox('Gender', categorical_options['Gender'])
marital_status = st.sidebar.selectbox('Marital Status', categorical_options['Marital Status'])
number_of_dependants = st.sidebar.number_input('Number of Dependants', min_value=0, step=1, max_value=20)
income_lakhs = st.sidebar.number_input('Income in Lakhs (INR)', step=1, min_value=0, max_value=200)
employment_status = st.sidebar.selectbox('Employment Status', categorical_options['Employment Status'])
region = st.sidebar.selectbox('Region', categorical_options['Region'])

# Health and Plan Group
st.sidebar.subheader('🩺 Health & Coverage')
bmi_category = st.sidebar.selectbox('BMI Category', categorical_options['BMI Category'])
smoking_status = st.sidebar.selectbox('Smoking Status', categorical_options['Smoking Status'])
medical_history = st.sidebar.selectbox('Medical History', categorical_options['Medical History'])
genetical_risk = st.sidebar.slider('Genetical Risk (1-5)', min_value=0, max_value=5, step=1)
insurance_plan = st.sidebar.selectbox('Desired Insurance Plan', categorical_options['Insurance Plan'])


# --- Main Application Area ---
st.title('Health Insurance Premium Predictor 🏥💰')
st.markdown('A machine learning model to estimate your annual health insurance premium based on your profile.')

# Create a dictionary for input values
input_dict = {
    'Age': age,
    'Number of Dependants': number_of_dependants,
    'Income in Lakhs': income_lakhs,
    'Genetical Risk': genetical_risk,
    'Insurance Plan': insurance_plan,
    'Employment Status': employment_status,
    'Gender': gender,
    'Marital Status': marital_status,
    'BMI Category': bmi_category,
    'Smoking Status': smoking_status,
    'Region': region,
    'Medical History': medical_history
}

st.divider() # Visual separator

# Button to make prediction
if st.button('Calculate Premium'):
    # Show a spinner while processing
    with st.spinner('Calculating premium...'):
        try:
            prediction = predict(input_dict)
            
            # --- Display Prediction with st.metric for visual impact ---
            st.subheader("🎉 Prediction Result")
            st.metric(
                label="Estimated Annual Premium",
                value=f"₹ {prediction:,.2f}", # Format as currency
                delta="Based on your inputs"
            )
            st.success('Prediction complete!')

            st.balloons() # Small celebration animation

        except Exception as e:
            st.error(f"An error occurred during prediction: {e}")

st.markdown(
    """
    ***
    *Disclaimer: This is an estimated cost based on a predictive model and should not be considered a final quote from any insurance provider.*
    """
)