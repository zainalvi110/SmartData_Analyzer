import google.generativeai as genai
import streamlit as st
import pandas as pd

# Configure API key
genai.configure(api_key="AIzaSyCdZELApwIv8f7ZmMtJhnr248fvhNs45g0")

# Use Gemini model
model = genai.GenerativeModel("gemini-1.5-pro")  # Change model if needed

# Function to call Gemini for cleaning suggestion
def chatbot_response(user_input):
    response = model.generate_content(user_input)
    return response.text  # Extract text response

# Function to clean data (basic implementation)
def clean_data(df, user_input):
    if 'null' in user_input or 'missing' in user_input:
        numeric_cols = df.select_dtypes(include=['number']).columns
        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())  # Only apply to numeric columns

    if 'duplicates' in user_input:
        df.drop_duplicates(inplace=True)

    return df


# Streamlit app UI
st.title("Conversational Data Cleaner")

# File upload section
uploaded_file = st.file_uploader("Upload your dataset (CSV only)", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write("Preview of the data:", df.head())

    user_input = st.text_input("Enter cleaning instructions (e.g., Remove missing values, remove duplicates)")

    if user_input:
        chatbot_reply = chatbot_response(f"How do I clean the data for this task: {user_input}")
        st.write(f"Chatbot suggests: {chatbot_reply}")

        cleaned_df = clean_data(df, user_input)
        st.write("Cleaned Data Preview:", cleaned_df.head())

        csv = cleaned_df.to_csv(index=False)
        st.download_button("Download Cleaned Data", csv, "cleaned_data.csv", "text/csv")
