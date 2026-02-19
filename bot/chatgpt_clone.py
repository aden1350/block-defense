#!/usr/bin/env python3
"""
ChatGPT Clone - Test Version
Using Streamlit for UI
"""

import streamlit as st
import json

# Import our AI assistant
from ai_assistant import answer_question

st.set_page_config(page_title="AI Assistant", page_icon="🤖")

st.title("🤖 AI Assistant")

# Initialize chat history
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask me anything..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            answer = answer_question(prompt)
            st.markdown(answer)
    
    # Add AI response
    st.session_state.messages.append({"role": "assistant", "content": answer})
