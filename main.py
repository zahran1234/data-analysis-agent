
from langchain.agents.agent_types import AgentType
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain_openai import ChatOpenAI
import os 
from dotenv import load_dotenv
import nest_asyncio
nest_asyncio.apply()


# Load environment
load_dotenv()
os.environ['OPENAI_API_KEY'] = "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"
os.environ['LOGFIRE_IGNORE_NO_CONFIG'] = '1'
import pandas as pd
from langchain_openai import OpenAI


# Correct file path using one of the methods above
file_path = r"C:\Users\admin\Downloads\credit_memo_ind\Orders data - Sample  (1).xlsx"

# Load the Excel file
df = pd.read_excel(file_path)

# Assuming `df` is your DataFrame
agent = create_pandas_dataframe_agent(
    llm=ChatOpenAI(temperature=0, model="gpt-4o"),
    df=df,
    verbose=True,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION ,#AgentType.OPENAI_FUNCTIONS,

    allow_dangerous_code=True , # Enable this explicitly
    
)
x=agent.invoke(" give me some statical analysis   ")

print("________________________________")
print(x['output'])





