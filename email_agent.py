
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage, BaseMessage
from langgraph.prebuilt import ToolNode
from typing import TypedDict, List
from tools import gmail_send # Ensure tools.py exists with your function

load_dotenv()



# --- 1. Define the Graph (Cached) ---

def get_email_agent():
    
    class AgentState(TypedDict):
        messages: List[BaseMessage]

    # Initialize LLM
    llm = ChatGroq(model="llama-3.3-70b-versatile")
    
    # CRITICAL FIX: Bind the tool to the LLM
    # This tells the LLM: "Here is a tool you can use, extract the 'to', 'subject', and 'message' yourself."
    llm_with_tools = llm.bind_tools([gmail_send])

    def agent_step(state: AgentState) -> dict:
        # We invoke the LLM which now knows about the tool
        response = llm_with_tools.invoke(state["messages"])
        return {"messages": [response]}

    def should_continue(state: AgentState) -> str:
        last_message = state["messages"][-1]
        # If the LLM decided to call the tool, go to "tools"
        if last_message.tool_calls:
            return "tools"
        return "end"

    graph = StateGraph(AgentState)

    graph.add_node("agent", agent_step)
    graph.add_node("tools", ToolNode([gmail_send]))

    graph.add_edge(START, "agent")
    graph.add_conditional_edges("agent", should_continue, ["tools", END])
    graph.add_edge("tools", END)
    
    return graph.compile()

