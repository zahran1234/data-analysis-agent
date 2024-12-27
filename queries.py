

import os

from dotenv import load_dotenv
from pydantic import BaseModel

import openai
import re
import faiss
# Configure Azure OpenAI settings
#from langchain.chat_models import AzureChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from langchain_community.chat_models import ChatOpenAI
from datetime import datetime
#from langchain_community.chat_models import AzureChatOpenAI
from langchain_openai.chat_models import AzureChatOpenAI
os.environ['OPENAI_API_KEY'] = "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"

# Current year and today's date
current_year = datetime.now().year
date_string = datetime.now().strftime("%Y-%m-%d")
load_dotenv()


def get_queries (data_columns  , data_subset):
    # Define the Pydantic model
    class Query(BaseModel):
        updated_queries: list[str] = Field(
            description=(
            f"""
              Generate a Python list of questions that comprehensively cover all aspects of the given data. These questions should aim to explore different dimensions of the dataset, including trends, correlations, and insights related to the data.

The dataset subset is provided below:
{data_subset}

Additionally, here are the column names along with their data types, which may assist in formulating the questions:
{data_columns}

Please ensure that the questions address various aspects, such as:

Summary statistics and data distribution.
Relationships or correlations between different columns.
Potential outliers or anomalies in the data.
Insights regarding trends over time or across categories.
Any relevant business or domain-specific analysis.
The questions should be designed to guide both exploratory analysis and deeper investigation.


           
"""


            )
        )

    llm = ChatOpenAI(temperature=0, model="gpt-4o")

    # Initialize the Pydantic output parser
    output_parser = PydanticOutputParser(pydantic_object=Query)

    # Define the chat prompt template
    prompt = ChatPromptTemplate.from_template("""
    Your task is to generate search queries based on the following instructions. 
    Do not answer or provide explanations. Return the queries strictly as a Python list.
       

    Instructions:
    {prompt_}
                                              

    {format_instructions}
                                              

""")
    
    # Format the prompt with the instructions and parser format
    formatted_prompt = prompt.format_messages(
        prompt_=prompt,
        format_instructions=output_parser.get_format_instructions()
    )
    # Get the LLM response
    response = llm(formatted_prompt)

    # Parse the LLM's response
    parsed_response = output_parser.parse(response.content)

    # Print the search queries
    return parsed_response.updated_queries 



print(get_queries("salesdata" , "dat"))