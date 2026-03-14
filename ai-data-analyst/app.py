import streamlit as st
import pandas as pd
import anthropic
from dotenv import load_dotenv
import os

load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

st.title("🤖 AI Data Analyst")
st.write("Upload a CSV file and ask questions about your data in plain English")

uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write("### Your Data:")
    st.dataframe(df)
    st.write(f"Shape: {df.shape[0]} rows and {df.shape[1]} columns")
    
    question = st.text_input("Ask a question about your data:")
    
    if question:
        with st.spinner("🤔 Thinking..."):
            message = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1024,
                messages=[
                    {
                        "role": "user",
                        "content": f"You are a data analyst. Analyse this dataset and answer the question clearly and concisely.\n\nDataset (sample):\n{df.head(50).to_string()}\n\nFull dataset shape: {df.shape[0]} rows and {df.shape[1]} columns\n\nQuestion: {question}"
                    }
                ]
            )
            st.write("### Answer:")
            st.write(message.content[0].text)


