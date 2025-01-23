# import streamlit as st
# import os
# from dotenv import load_dotenv
# from langchain_groq import ChatGroq
# from langchain_huggingface import HuggingFaceEmbeddings
# from langchain_community.vectorstores import Chroma
# from langchain.prompts import PromptTemplate, FewShotPromptTemplate
# from langchain.schema import BaseRetriever
# from langchain_core.example_selectors.semantic_similarity import SemanticSimilarityExampleSelector
# import psycopg2

# # Load environment variables
# load_dotenv()

# # Initialize LLM with Groq
# llm = ChatGroq(
#     groq_api_key=os.getenv("GROQ_API_KEY"), 
#     model_name="llama-3.3-70b-versatile"
# )

# # Load few_shots from a separate file
# from few_shots import few_shots

# # Initialize embeddings
# embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')

# # Convert the few_shots into a format suitable for vectorization
# to_vectorize = [" ".join([str(val) for val in example.values()]) for example in few_shots]

# # Create a vector store using Chroma
# vectorstore = Chroma.from_texts(to_vectorize, embeddings, metadatas=few_shots)

# # Example selector for semantic search
# example_selector = SemanticSimilarityExampleSelector(
#     vectorstore=vectorstore,
#     k=2  # Number of similar examples to retrieve
# )

# # Database configuration
# DB_USER = "postgres"
# DB_PASSWORD = "sdbsdb!"
# DB_HOST = "localhost"  
# DB_NAME = "SolarGranules"

# # Function to establish a connection to PostgreSQL/PostGIS
# def get_postgres_connection():
#     return psycopg2.connect(
#         dbname=DB_NAME, 
#         user=DB_USER, 
#         password=DB_PASSWORD, 
#         host=DB_HOST
#     )

# # Function to execute SQL query
# def execute_sql_query(query):
#     conn = get_postgres_connection()
#     try:
#         with conn.cursor() as cursor:
#             cursor.execute(query)
#             result = cursor.fetchall()
#         return result
#     except Exception as e:
#         st.error(f"Error executing SQL query: {e}")
#         return None
#     finally:
#         conn.close()

# # Function to generate SQL query and display the result
# def get_sql_answer(question):
#     st.write("Received Question: ", question)
    
#     # Use semantic search to find relevant few-shot examples
#     examples = example_selector.select_examples(question)
    
#     if not examples:
#         st.write("No relevant examples found.")
#         return

#     # Take the first example
#     example = examples[0]
#     st.write("Selected Example: ", example)
    
#     # Build the prompt
#     few_shot_prompt = f"""
#     Given the following examples, generate a valid SQL query for the following question about the database. Please return only the SQL query, without any explanations or extra information.

#     Example:
#     Question: {example['Question']}
#     SQLQuery: {example['SQLQuery']}
#     SQLResult: {example['SQLResult']}
#     Answer: {example['Answer']}

#     Now, based on the above, for the new question:
#     Question: {question}
#     SQLQuery:
#     """
    
#     # Generate the SQL query using Groq
#     sql_query = llm.invoke(few_shot_prompt).content.strip()

#     # Clean the query
#     if sql_query.startswith("```sql"):
#         sql_query = sql_query[7:].strip()
#     if sql_query.endswith("```"):
#         sql_query = sql_query[:-3].strip()

#     if not sql_query.strip().upper().startswith("SELECT"):
#         st.write(f"Error: The generated response is not a valid SQL query. Received: {sql_query}")
#         return
    
#     st.write("Generated SQL Query: ", sql_query)

#     # Execute and display result
#     try:
#         result = execute_sql_query(sql_query)
#         if result:
#             st.write("SQL Query Result: ", result)
#         else:
#             st.write("No result returned for the SQL query.")
#     except Exception as e:
#         st.error(f"Error executing SQL query: {e}")

# # Streamlit UI
# def main():
#     st.title("SQL Query Generator")
    
#     # Input for the user question
#     question = st.text_input("Enter your question", "")

#     # When the user clicks the "Get SQL Answer" button
#     if st.button("Get SQL Answer"):
#         if question:
#             get_sql_answer(question)
#         else:
#             st.write("Please enter a question to generate the SQL query.")

# if __name__ == "__main__":
#     main()
#---------------------------------------------
# import streamlit as st
# import os
# from dotenv import load_dotenv
# from langchain_groq import ChatGroq
# from langchain_huggingface import HuggingFaceEmbeddings
# from langchain_community.vectorstores import Chroma
# from langchain.prompts import PromptTemplate, FewShotPromptTemplate
# from langchain.schema import BaseRetriever
# from langchain_core.example_selectors.semantic_similarity import SemanticSimilarityExampleSelector
# import psycopg2
# from llm_helper import get_sql_answer  # Import the helper function

# # Load environment variables
# load_dotenv()

# # Initialize LLM with Groq
# llm = ChatGroq(
#     groq_api_key=os.getenv("GROQ_API_KEY"), 
#     model_name="llama-3.3-70b-versatile"
# )

# # Load few_shots from a separate file
# from few_shots import few_shots

# # Initialize embeddings
# embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')

# # Convert the few_shots into a format suitable for vectorization
# to_vectorize = [" ".join([str(val) for val in example.values()]) for example in few_shots]

# # Create a vector store using Chroma
# vectorstore = Chroma.from_texts(to_vectorize, embeddings, metadatas=few_shots)

# # Example selector for semantic search
# example_selector = SemanticSimilarityExampleSelector(
#     vectorstore=vectorstore,
#     k=2  # Number of similar examples to retrieve
# )

# # Database configuration
# DB_USER = "postgres"
# DB_PASSWORD = "sdbsdb!"
# DB_HOST = "localhost"  
# DB_NAME = "SolarGranules"

# # Function to establish a connection to PostgreSQL/PostGIS
# def get_postgres_connection():
#     return psycopg2.connect(
#         dbname=DB_NAME, 
#         user=DB_USER, 
#         password=DB_PASSWORD, 
#         host=DB_HOST
#     )

# # Function to execute SQL query
# def execute_sql_query(query):
#     conn = get_postgres_connection()
#     try:
#         with conn.cursor() as cursor:
#             cursor.execute(query)
#             result = cursor.fetchall()
#         return result
#     except Exception as e:
#         st.error(f"Error executing SQL query: {e}")
#         return None
#     finally:
#         conn.close()

# # Function to generate SQL query and display the result
# def get_sql_answer(question):
#     st.write("Received Question: ", question)
    
#     # Use semantic search to find relevant few-shot examples
#     examples = example_selector.select_examples(question)
    
#     if not examples:
#         st.write("No relevant examples found.")
#         return

#     # Take the first example
#     example = examples[0]
#     st.write("Selected Example: ", example)
    
#     # Build the prompt
#     few_shot_prompt = f"""
#     Given the following examples, generate a valid SQL query for the following question about the database. Please return only the SQL query, without any explanations or extra information.

#     Example:
#     Question: {example['Question']}
#     SQLQuery: {example['SQLQuery']}
#     SQLResult: {example['SQLResult']}
#     Answer: {example['Answer']}

#     Now, based on the above, for the new question:
#     Question: {question}
#     SQLQuery:
#     """
    
#     # Generate the SQL query using Groq
#     sql_query = llm.invoke(few_shot_prompt).content.strip()

#     # Clean the query
#     if sql_query.startswith("```sql"):
#         sql_query = sql_query[7:].strip()
#     if sql_query.endswith("```"):
#         sql_query = sql_query[:-3].strip()

#     if not sql_query.strip().upper().startswith("SELECT"):
#         st.write(f"Error: The generated response is not a valid SQL query. Received: {sql_query}")
#         return
    
#     st.write("Generated SQL Query: ", sql_query)

#     # Execute and display result
#     try:
#         result = execute_sql_query(sql_query)
#         if result:
#             st.write("SQL Query Result: ", result)
#         else:
#             st.write("No result returned for the SQL query.")
#     except Exception as e:
#         st.error(f"Error executing SQL query: {e}")

# # Streamlit UI
# def main():
#     st.title("SQL Query Generator")
    
#     # Input for the user question
#     question = st.text_input("Enter your question", "")

#     # When the user clicks the "Get SQL Answer" button
#     if st.button("Get SQL Answer"):
#         if question:
#             get_sql_answer(question)
#         else:
#             st.write("Please enter a question to generate the SQL query.")

# if __name__ == "__main__":
#     main()

#-------------------------------------------------------------
# import streamlit as st
# from llm_helper import get_sql_chain

# # Title of the Streamlit app
# st.title("AtliQ T Shirts: Database Q&A 👕")

# # User input: question for the database
# question = st.text_input("Ask a question about the database:")

# # Process the question when the user submits it
# if question:
#     with st.spinner("Processing your question..."):
#         # Get the SQL query answer
#         response = get_sql_answer(question)
    
#     # Display the answer or any errors
#     st.header("Answer")
#     st.write(response)

#------------------------------------------------------

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



