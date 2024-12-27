import streamlit as st
import pandas as pd
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain.chat_models import ChatOpenAI
from langchain.agents.agent_types import AgentType
from dotenv import load_dotenv
import os
import nest_asyncio

# Apply asyncio to avoid nested event loop issues
nest_asyncio.apply()

# Load environment variables
load_dotenv()

# Set OpenAI API key
os.environ['OPENAI_API_KEY'] = "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"

# Streamlit App
def main():
    st.title("Dataframe Q&A App")
    
    # File upload
    st.sidebar.header("Upload Your Data")
    uploaded_file = st.sidebar.file_uploader("Upload an Excel file", type=["xlsx"])
    
    if uploaded_file is not None:
        try:
            # Load the uploaded Excel file
            df = pd.read_excel(uploaded_file)
            st.write("### Uploaded Data Preview")
            st.dataframe(df, use_container_width=True)
            
            # Create the agent
            agent = create_pandas_dataframe_agent(
                llm=ChatOpenAI(temperature=0, model="gpt-4o"),
                df=df,
                verbose=True,
                agent_type=AgentType.OPENAI_FUNCTIONS,
                allow_dangerous_code=True,

            )
            
            # Query Section
            st.write("### Ask Questions About Your Data")
            user_question = st.text_input("Enter your question:") +"if you can represent the user query in tables do it add poivit table if you can " 
            
            if user_question:
                # Run the query
                with st.spinner("Processing..."):
                    response = agent.invoke(user_question)
                st.write("### Answer:")
                st.write(response['output'])
        
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.info("Please upload an Excel file to begin.")

if __name__ == "__main__":
    main()
