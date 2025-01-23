import streamlit as st
from llm_helper import get_sql_chain  

process_question = get_sql_chain()

st.title("☀️ SolarAI: Talk to a Database")


# User input
question = st.text_input("Enter your question about the database:")

# Button to process the question
if st.button("Generate SQL Query and Fetch Results"):
    if question.strip():  # Ensure the input is not empty
        with st.spinner("Processing your question..."):
            try:
                result = process_question(question)
                st.success("Query executed successfully!")
                st.write("Result:")
                st.dataframe(result)  # Display results in a table
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Please enter a valid question.")



