
import streamlit as st
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

from chatgpt import llm_strict

chat = ChatOpenAI(model="gpt-4o")


class PostcardFormat(BaseModel):
    card_text: str = Field(..., description="Text for on the card of the post card as a reply to the user's request formatted with short sentences each on separate lines.")
    card_address: str = Field(..., description="Address for on the card of the post card as a reply to the user's request formatted on multiple lines")
    #card_image_prompt: str = Field(..., description="Prompt description for generating the image on the front of the postcard.")
    assistant_response: str = Field(..., description="Response from the assistant on writing the content for the postcard, explaining the text and address that it wrote down.")


def streaming_interface():
    # Display all previous messages
    for message in st.session_state.history.logs:
        if message["role"] == "system":
            continue
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    user_prompt = st.chat_input()  # Input box for the user

    if user_prompt is not None:
        if "postcard_message" in st.session_state.postcard_message:
            st.session_state.history.system("Postcard message: " + st.session_state.postcard_message)
        if "postcard_address" in st.session_state.postcard_address:
            st.session_state.history.system("Postcard address: " + st.session_state.postcard_address)
        #if "postcard_image_prompt" in st.session_state.postcard_image_prompt:
        #    st.session_state.history.system("Postcard Image Prompt: " + st.session_state.postcard_image_prompt)

        st.session_state.history.user(user_prompt)
        with st.chat_message("user"):
            st.markdown(user_prompt)

        # Placeholder for the assistant's reply
        assistant_message_placeholder = st.chat_message("assistant")
        assistant_text = assistant_message_placeholder.empty()

        # Stream response
        with st.spinner("Loading..."):
            answer: PostcardFormat = llm_strict(st.session_state.history, base_model=PostcardFormat)
            assistant_text.markdown(answer.assistant_response)  # Update progressively
            st.session_state.history.system("Postcard Message: " + answer.card_text)
            st.session_state.postcard_message = answer.card_text
            st.session_state.history.system("Postcard Address: " + answer.card_address)
            st.session_state.postcard_address = answer.card_address
            st.session_state.history.assistant(answer.assistant_response)  # Save final message in history
            #st.session_state.postcard_image_prompt = answer.card_image_prompt