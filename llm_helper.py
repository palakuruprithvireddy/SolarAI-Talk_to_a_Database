from langchain_groq import ChatGroq
import os
import psycopg2
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain_core.example_selectors.semantic_similarity import SemanticSimilarityExampleSelector
import chromadb


def get_sql_chain():
    """
    Bundles the initialization of LLM, database connection, example selector, and query execution logic
    into a single function.
    
    Returns:
        Callable: A function to process natural language questions into SQL queries and fetch results.
    """
    # Load environment variables ( API key stores in an .env file)
    load_dotenv()

    # Initialize LLM with Groq
    llm = ChatGroq(
        groq_api_key=os.getenv("GROQ_API_KEY"), 
        model_name="llama-3.3-70b-versatile"
    )

    # Database configuration
    DB_USER = "postgres"
    DB_PASSWORD = "your-password"
    DB_HOST = "localhost"  
    DB_NAME = "SolarGranules"

    # Load few_shots examples
    from few_shots import few_shots  # Assuming few_shots.py defines a list named `few_shots`

    # Initialize embeddings
    embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')

    # Initialize Chroma client
    client = chromadb.Client()

    # Get or create the collection in Chroma
    collection = client.get_or_create_collection(name="solar_granules_collection")

    # Convert Chroma collection to langchain-compatible VectorStore
    vectorstore_langchain = Chroma(persist_directory='./chroma', embedding_function=embeddings, client=client)

    # Add data to the collection (ensure documents and ids are correctly provided)
    to_vectorize = [" ".join([str(val) for val in example.values()]) for example in few_shots]
    for idx, (text, metadata) in enumerate(zip(to_vectorize, few_shots)):
        collection.add(
            documents=[text],
            metadatas=[metadata],
            ids=[str(idx)]
        )

    # Example selector
    example_selector = SemanticSimilarityExampleSelector(vectorstore=vectorstore_langchain, k=2)

    # Helper function to establish a connection to PostgreSQL
    def get_postgres_connection():
        return psycopg2.connect(
            dbname=DB_NAME, 
            user=DB_USER, 
            password=DB_PASSWORD, 
            host=DB_HOST
        )

    # Helper function to execute SQL query
    def execute_sql_query(query):
        conn = get_postgres_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
            return result
        except Exception as e:
            print(f"Error executing SQL query: {e}")
            raise
        finally:
            conn.close()

    # Main function to process a question
    def process_question(question):
        print("Received Question: ", question)

        # Retrieve relevant few-shot examples
        examples = example_selector.select_examples(question)
        if not examples:
            print("No examples found.")
            return

        example = examples[0]  # Use the first example
        print("Selected Example: ", example)

        # Build the prompt
        few_shot_prompt = f"""
        Given the following examples, generate a valid SQL query for the following question about the database. Please return only the SQL query, without any explanations or extra information.

        Example:
        Question: {example['Question']}
        SQLQuery: {example['SQLQuery']}
        SQLResult: {example['SQLResult']}
        Answer: {example['Answer']}

        Now, based on the above, for the new question:
        Question: {question}
        SQLQuery:
        """

        # Generate the SQL query
        sql_query = llm.invoke(few_shot_prompt).content.strip()
        if sql_query.startswith("```sql"):
            sql_query = sql_query[7:].strip()
        if sql_query.endswith("```"):
            sql_query = sql_query[:-3].strip()

        if not sql_query.strip().upper().startswith("SELECT"):
            print(f"Error: The generated response is not a valid SQL query. Received: {sql_query}")
            return

        print("SQL Query: ", sql_query)

        # Execute the SQL query
        try:
            result = execute_sql_query(sql_query)
            print("SQL Query Result: ", result)
            return result
        except Exception as e:
            print(f"Error executing SQL query: {e}")

    return process_question
