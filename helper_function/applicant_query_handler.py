# Common imports
import os
from dotenv import load_dotenv
import lolviz
__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

# Import the key CrewAI classes
from crewai import Agent, Task, Crew
from crewai_tools import WebsiteSearchTool

load_dotenv('.env')

# Create a new instance of the WebsiteSearchTool
# Set the base URL of a website, e.g., "https://example.com/", so that the tool can search for sub-pages on that website
tool_websearch_process = WebsiteSearchTool("https://www.hdb.gov.sg/cs/infoweb/residential/buying-a-flat/buying-procedure-for-resale-flats/")
tool_websearch_eligibility = WebsiteSearchTool("https://www.hdb.gov.sg/cs/infoweb/residential/buying-a-flat/understanding-your-eligibility-and-housing-loan-options/flat-and-grant-eligibility/")

# Creating Agent
agent_customer_relations_manager = Agent(
    role="Customer Relations Manager",

    goal="Respond to the {query} of potential buyers on process of purchasing a resale flat in Singapore",

    backstory="You will be assessing applicants' eligibility to buy a resale HDB flat, receive CPF housing grants and take an HDB housing loan, providing guidance towards informed housing and prudent financing decisions or processing of the sale or resale transactions of HDB flats.",

    tools=[tool_websearch_process, tool_websearch_eligibility],

    allow_delegation=False,

    verbose=True,
)

# Creating Task
task_gather_information = Task(
    description="""\
        1. Understand the applicant query: {query}.
        2. Use the information from the "{query}" and the tools to check the applicant eligibility
        3. Formulate a response.
    """,
    expected_output="""
        If the applicant is eligible, respond "Yes, you are eligible to buy a resale flat." and provide step-by-step instructions on how to purchase a resale flat.
        If insufficient information is provided, respond "I am sorry but I don't understand your question.".
    """,

    agent=agent_customer_relations_manager
)

# Creating Crew
crew = Crew(
    agents=[agent_customer_relations_manager],
    tasks=[task_gather_information],
    verbose=True
)

def ask_agent(prompt):
    result = crew.kickoff(inputs={"query": prompt})
    return result
