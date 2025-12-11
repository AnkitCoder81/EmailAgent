# streamlit_app.py
import streamlit as st
from langchain_core.messages import HumanMessage
from email_agent import get_email_agent

st.title("📧 AI Email Agent")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state["messages"] = []

if "agent" not in st.session_state:
    st.session_state["agent"] = get_email_agent()

# Input fields
to = st.text_input("Recipient Email")
subject = st.text_input("Subject")
message = st.text_area("Message")

if st.button("Send Email"):
    # Add user request as a HumanMessage
    st.session_state["messages"].append(
        HumanMessage(content=f"Send an email to {to} with subject '{subject}' and message: {message}")
    )

    # Invoke the agent
    result = st.session_state["agent"].invoke({"messages": st.session_state["messages"]})

    # Display result
    st.write("### Agent Response")
    st.write(result["messages"][-1].content)
