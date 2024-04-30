import streamlit as st
import random
import time
import requests
import os


def make_api_call(query):
    response = requests.get("https://ey-chat.translatetracks.com/query", params={"query": query})
    return response.json()["response"], response.json()["images"]


st.title("RAG Application")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role":"assistant", "content":"""
                                  This is a comprehensive RAG built on top of EY's Annual Report 2023.
                                  Few things that should be kept in mind - 
                                  1. Due to resource contraints, each query is independent and does not take into account the context of the previous queries.
                                  2. Comprehensive questions that involve pulling data from multiple indexes may take longer to respond.

                                  What do you want to know?
                                  Hint: You want to ask about company's Financial performace. 
                                  Example - "What was EY's 2023 revenue from Consulting?, What was EY's CAGR for past 4 years?

                                  Hint: You want to ask about company's ESG performance.
                                  Example - What are the top five SDGs impacted in FY23?


                                  """, "images":[]}]

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        # st.markdown("")
        st.markdown(message["content"])
        if message["role"] == "assistant":
            for image in message["images"]:
                st.image(image.replace("json","png"))

# Accept user input
prompt = st.chat_input("What is up?")
if prompt:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        # response = st.write_stream(response_generator())
        with st.spinner("Thinking..."):
            response,images = make_api_call(prompt)
        st.markdown(response)
        for image in images:
            st.image(image.replace("json","png"))

    st.session_state.messages.append({"role": "assistant", "content": response, "images":images})