import base64
from io import BytesIO

import streamlit as st

from generate import generate_pdf

# Streamlit App
st.title("Postcard PDF Generator")

# Default values for the text inputs
default_text_1 = """Hello!

Greetings from Middle Earth!
It’s been a fantastic vacation so far
(except for the glowing eye in my host’s backyard),
and I’m really loving the second breakfasts.
Take care,

F."""
default_text_2 = """Bob Smith
1234 First Street
Anytown, XX
A COUNTRY"""

# Text input fields
text_1 = st.text_area("Postcard Message", default_text_1, height=200)
text_2 = st.text_area("Recipient Address", default_text_2, height=100)

# File paths (these can be modified or taken as user inputs if needed)
template_file = "template.pdfml"
output_pdf_file = "postcard.pdf"

# Button to generate PDF
if st.button("Generate PDF"):
    try:
        # Generate the PDF content as BytesIO
        generate_pdf(template_file, output_pdf_file, [text_1, text_2])
        BytesIO()
        st.success("PDF generated successfully!")

        def file_to_bytesio(file_name):
            with open(file_name, 'rb') as file:
                return BytesIO(file.read())

        # Display download button for the generated PDF
        st.download_button(
            label="Download PDF",
            data=file_to_bytesio(output_pdf_file),
            file_name="postcard.pdf",
            mime="application/pdf"
        )
    except Exception as e:
        st.error(f"An error occurred: {e}")