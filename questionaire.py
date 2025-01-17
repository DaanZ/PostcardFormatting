import streamlit as st

# Initialize session state variables for tracking responses
if 'step' not in st.session_state:
    st.session_state.step = 0
if 'responses' not in st.session_state:
    st.session_state.responses = []

# Define the questions
questions = [
    "What's your name?",
    "How old are you?",
    "What's your favorite color?",
    "Do you like programming?"
]


# Handle conversation flow
def next_step():
    # Move to the next step after each response
    st.session_state.step += 1


# Main conversational flow
if st.session_state.step < len(questions):
    # Display the question
    question = questions[st.session_state.step]
    response = st.text_input(question)

    if response:
        st.session_state.responses.append(response)
        next_step()  # Proceed to next question

    # Show a progress indicator
    st.write(f"Question {st.session_state.step + 1} of {len(questions)}")

else:
    # Display a summary of the responses
    st.write("Thank you for your responses!")
    for idx, response in enumerate(st.session_state.responses):
        st.write(f"Q: {questions[idx]}")
        st.write(f"A: {response}")

    # Reset option
    if st.button("Start Over"):
        st.session_state.step = 0
        st.session_state.responses = []
