import os
import argparse
from typing import List, TypedDict
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.tools import DuckDuckGoSearchRun

class AgentState(TypedDict):
    task: str
    results: List[str]

def run_agent_workflow(task: str):
    """
    Core entry point for executing agentic workflows.
    Demonstrates a simple research agent using LangChain.
    """
    print(f"🚀 Initializing Agent Orchestrator for task: {task}")
    
    # Initialize LLM and Tools
    llm = ChatOpenAI(model="gpt-4o", temperature=0.2)
    search_tool = DuckDuckGoSearchRun()
    tools = [search_tool]

    # Define the system prompt for the orchestrator
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a professional AI researcher and workflow orchestrator. "
                   "Your goal is to solve the user's task by gathering info and summarizing it."),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])

    # Construct the Agent
    agent = create_openai_functions_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    # Execute the task
    try:
        response = agent_executor.invoke({"input": task})
        print("\n✅ Final Result:\n")
        print(response["output"])
    except Exception as e:
        print(f"❌ Error during execution: {str(e)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Agent Workflow Orchestrator CLI")
    parser.add_argument("--task", type=str, required=True, help="The task to perform")
    
    args = parser.parse_args()
    run_agent_workflow(args.task)
