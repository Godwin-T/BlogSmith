# Import necessary libraries
import streamlit as st
from chatbot import crew  # 'crew' module for handling chatbot responses
from HtmlTemplate import user_template, bot_template, chat_css

# Set the configuration for the Streamlit app
st.set_page_config(page_title="BlogSmith", page_icon=":books:")

# Function to handle user input and chatbot response
def handle_userinput(user_question):

    # Iterate through the chat history (starting from the second message)
    for i, message in enumerate(st.session_state.chat_history[1:]):
        if i % 2 == 0:
            # Display user messages using the user template
            st.write(user_template.replace("{{MSG}}", message), unsafe_allow_html=True)
        else:
            # Display bot messages using the bot template
            st.write(bot_template.replace("{{MSG}}", message), unsafe_allow_html=True)

    # Get the response from the chatbot using 'crew' module
    response = crew.kickoff({"query": user_question})
    st.session_state.chat_history.append(response.raw)
    # Display the bot's response using the bot template
    st.write(bot_template.replace("{{MSG}}", response.raw), unsafe_allow_html=True)


# Main function to run the Streamlit app
def main():
    # Initialize chat history in session state
    st.session_state.chat_history = ["Init"]  # Initial message to indicate chat start

    # Capture user input from a chat input box
    user_question = st.chat_input("Enter your message:", key="chat_input")
    if user_question:  # Check if the user has entered a message
        st.session_state.chat_history.append(
            user_question
        )  # Append user message to chat history
        handle_userinput(user_question)


# Run the main function when the script is executed
if __name__ == "__main__":
    main()