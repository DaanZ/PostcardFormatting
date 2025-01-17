import base64
from io import BytesIO

import streamlit as st

from generate import generate_pdf
from helper import postcard_system_message
from history import History
from streaming import streaming_interface


# Default values for the text inputs
default_message = """Hello!

Greetings from Middle Earth!
It’s been a fantastic vacation so far
(except for the glowing eye in my host’s backyard),
and I’m really loving the second breakfasts.
Take care,

F."""
default_address = """Bob Smith
1234 First Street
Anytown, XX
A COUNTRY"""

default_image_prompt = "Generate an abstract postcard image."

title = "Postcard GPT"


def postcard_format():
    print("Message", st.session_state.postcard_message)
    print("Address", st.session_state.postcard_address)
    message_text = st.text_area("Postcard Message", st.session_state.postcard_message, height=300)
    address_text = st.text_area("Recipient Address", st.session_state.postcard_address, height=200)

    return message_text, address_text


def generate_postcard(message_text, address_text, image_link = None):
    # File paths (these can be modified or taken as user inputs if needed)
    template_file = "data/template.pdfml"
    output_pdf_file = "data/postcard.pdf"
    try:
        # Generate the PDF content as BytesIO
        generate_pdf(template_file, output_pdf_file, [message_text, address_text])
        BytesIO()
        st.success("Postcard generated successfully!")

        def file_to_bytesio(file_name):
            with open(file_name, 'rb') as file:
                return BytesIO(file.read())

        # Display download button for the generated PDF
        st.download_button(
            label="Download Postcard",
            data=file_to_bytesio(output_pdf_file),
            file_name="postcard.pdf",
            mime="application/pdf"
        )
    except Exception as e:
        st.error(f"An error occurred: {e}")


if __name__ == "__main__":
    st.set_page_config(
        page_title=title,
        page_icon="✉️",
        layout="wide"
    )

    st.title(title)
    if 'postcard_message' not in st.session_state:
        st.session_state.postcard_message = default_message

    if 'postcard_address' not in st.session_state:
        st.session_state.postcard_address = default_address

    if 'postcard_image_prompt' not in st.session_state:
        st.session_state.postcard_image_prompt = default_image_prompt

    if 'history' not in st.session_state:
        st.session_state.history = History()
        st.session_state.history.system(postcard_system_message)

    col1, col2 = st.columns(2)
    with col1:
        streaming_interface()

    with col2:
        message_text, address_text = postcard_format()

        # Button to generate PDF
        if st.button("Generate Postcard"):
            generate_postcard(message_text, address_text, "")