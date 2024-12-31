import streamlit as st
import pandas as pd
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain.agents.agent_types import AgentType
from dotenv import load_dotenv
import os
from langchain_community.chat_models import ChatOpenAI
import nest_asyncio
from pathlib import Path

# Apply asyncio to avoid nested event loop issues
nest_asyncio.apply()

# Load environment variables
load_dotenv()

# Directory to save uploaded files
UPLOADS_DIR = "uploads"

# Create uploads directory if not exists
os.makedirs(UPLOADS_DIR, exist_ok=True)

# Function to save the uploaded file locally
def save_uploaded_file(uploaded_file):
    file_path = os.path.join(UPLOADS_DIR, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path

# Function to load the data from the saved file
@st.cache_data(show_spinner=True)
def load_data(file_path):
    if file_path.endswith(".xlsx"):
        return pd.read_excel(file_path)
    elif file_path.endswith(".csv"):
        return pd.read_csv(file_path)
    else:
        raise ValueError("Unsupported file format. Please upload an Excel or CSV file.")

def main():
    st.title("Dataframe Q&A App")

    # Sidebar: File options
    st.sidebar.header("File Options")

    # Get OpenAI API key from user
    openai_key = st.sidebar.text_input("Enter your OpenAI API key", type="password")

    if openai_key:
        os.environ['OPENAI_API_KEY'] = openai_key
    else:
        st.sidebar.warning("Please enter your OpenAI API key.")

    # Get existing files in the uploads directory
    existing_files = [f.name for f in Path(UPLOADS_DIR).glob("*") if f.is_file()]
    
    # Option to upload a new file or use an existing one
    use_existing_file = st.sidebar.radio(
        "Select an option:",
        ["Upload New File"] + existing_files
    )

    if use_existing_file == "Upload New File":
        # File upload input
        uploaded_file = st.sidebar.file_uploader("Upload an Excel or CSV file", type=["xlsx", "csv"])

        if uploaded_file is not None:
            # Save the uploaded file locally
            file_path = save_uploaded_file(uploaded_file)

            # Load the data
            df = load_data(file_path)
        else:
            st.info("Please upload a file to get started.")
            return
    else:
        # Use an existing file
        file_path = os.path.join(UPLOADS_DIR, use_existing_file)
        df = load_data(file_path)
        st.sidebar.info(f"Using existing file: {use_existing_file}")

    # Display the DataFrame preview
    st.write("### Uploaded Data Preview")
    st.dataframe(df.head(10), use_container_width=True)

    # Create the agent
    agent = create_pandas_dataframe_agent(
        llm=ChatOpenAI(temperature=0, model="gpt-4"),
        df=df,
        verbose=True,
        agent_type=AgentType.OPENAI_FUNCTIONS,
        allow_dangerous_code=True,
    )

    # Query Section
    st.write("### Ask Questions About Your Data")
    instructions = """
    - **If the user query can be represented in a pivot table**, prioritize this option. A pivot table is ideal for summarizing key insights and aggregating data in a meaningful way. 
      Always aim to create a pivot table that highlights important metrics :
    

    - **If the user query cannot be represented in a pivot table**, then represent the data in a regular table format. 
      Provide a well-organized table with appropriate column headers and ensure that the data is presented clearly for easy interpretation. 
      If possible, include statistical summaries or insights to help the user understand the data better.
    
    - The goal is to make the response as informative and actionable as possible. Pivot tables should always be the first choice for summarizing large datasets or answering queries that involve aggregation or analysis.
    - Only when pivot tables are not suitable, should you fall back to a regular table format or other forms of data representation.
    -make response summerized 
    make sure the reponse for bussness peaple so the output shloud be structure in table format 
"""



    
    user_question = st.text_input("Enter your question:") 

    if user_question:
        # Run the query
        with st.spinner("Processing..."):
            response = agent.invoke(f"""this is the user query {user_question}+"\n instruction should follow it {instructions}""")
        st.write("### Answer:")
        st.write(response['output'])

if __name__ == "__main__":
    main()
