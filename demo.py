import streamlit as st
from io import BytesIO

from app import postcard_format, default_message, default_address, default_image_prompt, generate_postcard
from helper import postcard_system_message
from history import History
from streaming import streaming_interface


# Placeholder for image generation logic
def generate_images(prompt):
    # Replace with logic for calling Leonardo AI
    # This should return 4 BytesIO images for simplicity
    images = [BytesIO(b"Image 1"), BytesIO(b"Image 2"), BytesIO(b"Image 3"), BytesIO(b"Image 4")]
    return images


def create_postcard_text_page():
    st.title("Step 1: Define Postcard Text and Address")

    col1, col2 = st.columns(2)
    with col1:
        streaming_interface()

    with col2:
        postcard_format()


def create_image_prompt_page():
    st.title("Step 2: Define Image Prompt and Select Image")

    st.session_state.postcard_image_prompt = st.text_input(
        "Image Prompt",
        st.session_state.get("postcard_image_prompt", "Generate an abstract postcard image."),
    )

    if st.button("Generate Images"):
        st.session_state.generated_images = generate_images(st.session_state.postcard_image_prompt)

    if "generated_images" in st.session_state:
        st.subheader("Select an Image for the Postcard")
        cols = st.columns(4)
        for i, img in enumerate(st.session_state.generated_images):
            with cols[i]:
                if st.button(f"Select Image {i + 1}"):
                    st.session_state.selected_image = img
                st.image(img, caption=f"Image {i + 1}")

        if "selected_image" in st.session_state:
            st.success("Image Selected!")


def create_generate_postcard_page():
    st.title("Step 3: Generate and Download Postcard")

    st.subheader("Postcard Message")
    postcard_message = st.session_state.get("postcard_message", "No message defined.")
    st.text(postcard_message)

    st.subheader("Recipient Address")
    postcard_address = st.session_state.get("postcard_address", "No address defined.")
    st.text(postcard_address)

    if "selected_image" in st.session_state:
        image = st.session_state.selected_image
        st.subheader("Selected Postcard Front Image")
        st.image(st.session_state.selected_image, caption="Postcard Front Image")
    else:
        image = None

    if st.button("Generate Postcard"):
        generate_postcard(postcard_message, postcard_address, image)


def main():
    st.set_page_config(page_title="Postcard Generator", layout="wide")

    if 'postcard_message' not in st.session_state:
        st.session_state.postcard_message = default_message

    if 'postcard_address' not in st.session_state:
        st.session_state.postcard_address = default_address

    if 'postcard_image_prompt' not in st.session_state:
        st.session_state.postcard_image_prompt = default_image_prompt

    if 'history' not in st.session_state:
        st.session_state.history = History()
        st.session_state.history.system(postcard_system_message)

    # Sidebar for navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Go to",
        ["1: Postcard Message", "2: Postcard Image", "3: Generate Postcard"]
    )
    if page:
        st.session_state.current_page = page

    # Handle page rendering
    if st.session_state.current_page == "1: Postcard Message":
        create_postcard_text_page()
    elif st.session_state.current_page == "2: Postcard Image":
        create_image_prompt_page()
    elif st.session_state.current_page == "3: Generate Postcard":
        create_generate_postcard_page()


if __name__ == "__main__":
    main()
