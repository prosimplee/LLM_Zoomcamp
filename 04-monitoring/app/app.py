import streamlit as st
import time
import uuid

from assistant import get_answer
from db import save_conversation, save_feedback, get_recent_conversations, get_feedback_stats


def print_log(message):
    print(message, flush=True)


def main():
    print_log("Starting the Course Assistant application")
    st.title("Course Assistant")

    # Always generate a new conversation ID on each page load
    st.session_state.conversation_id = str(uuid.uuid4())
    print_log(f"New conversation started with ID: {st.session_state.conversation_id}")

    # Display the current conversation ID if it exists
    st.write(f"Current Conversation ID: {st.session_state.get('conversation_id', 'No Conversation ID generated yet.')}")

    # Initialize feedback count if not already set
    if 'count' not in st.session_state:
        st.session_state.count = 0
        print_log("Feedback count initialized to 0")

    # Course selection
    course = st.selectbox(
        "Select a course:",
        ["machine-learning-zoomcamp", "data-engineering-zoomcamp", "mlops-zoomcamp"]
    )
    print_log(f"User selected course: {course}")

    # Model selection
    model_choice = st.selectbox(
        "Select a model:",
        ["ollama/gemma:2b", "openai/gpt-3.5-turbo", "openai/gpt-4o", "openai/gpt-4o-mini"]
    )
    print_log(f"User selected model: {model_choice}")

    # Search type selection
    search_type = st.radio(
        "Select search type:",
        ["Text", "Vector"]
    )
    print_log(f"User selected search type: {search_type}")

    # User input
    user_input = st.text_input("Enter your question:")

    # Process the user's question when the "Ask" button is clicked
    if st.button("Ask"):
        print_log(f"User asked: '{user_input}'")
        with st.spinner('Processing...'):
            print_log(f"Getting answer from assistant using {model_choice} model and {search_type} search")
            start_time = time.time()
            answer_data = get_answer(user_input, course, model_choice, search_type)
            end_time = time.time()
            print_log(f"Answer received in {end_time - start_time:.2f} seconds")
            st.success("Completed!")
            st.write(answer_data.get('answer', 'No answer available'))

            # Display monitoring information
            st.write(f"Response time: {answer_data.get('response_time', 'N/A'):.2f} seconds")
            st.write(f"Relevance: {answer_data.get('relevance', 'N/A')}")
            st.write(f"Model used: {answer_data.get('model_used', 'N/A')}")
            st.write(f"Total tokens: {answer_data.get('total_tokens', 'N/A')}")
            if answer_data.get('openai_cost', 0) > 0:
                st.write(f"OpenAI cost: ${answer_data.get('openai_cost', 0):.4f}")

            # Save conversation to database
            print_log("Saving conversation to database")
            save_conversation(st.session_state.conversation_id, user_input, answer_data, course)
            print_log("Conversation saved successfully")

    # Feedback buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("+1"):
            st.session_state.count += 1
            print_log(f"Positive feedback received. New count: {st.session_state.count}")
            save_feedback(st.session_state.conversation_id, 1)
            print_log("Positive feedback saved to database")
    with col2:
        if st.button("-1"):
            st.session_state.count -= 1
            print_log(f"Negative feedback received. New count: {st.session_state.count}")
            save_feedback(st.session_state.conversation_id, -1)
            print_log("Negative feedback saved to database")

    st.write(f"Current count: {st.session_state.count}")

    # Display recent conversations
    st.subheader("Recent Conversations")
    relevance_filter = st.selectbox("Filter by relevance:", ["All", "RELEVANT", "PARTLY_RELEVANT", "NON_RELEVANT"])
    recent_conversations = get_recent_conversations(limit=5,
                                                    relevance=relevance_filter if relevance_filter != "All" else None)
    for conv in recent_conversations:
        st.write(f"Q: {conv['question']}")
        st.write(f"A: {conv['answer']}")
        st.write(f"Relevance: {conv['relevance']}")
        st.write(f"Model: {conv['model_used']}")
        st.write("---")

    # Display feedback stats
    st.subheader("Feedback Statistics")
    feedback_stats = get_feedback_stats()
    st.write(f"Thumbs up: {feedback_stats.get('thumbs_up', 0)}")
    st.write(f"Thumbs down: {feedback_stats.get('thumbs_down', 0)}")


if __name__ == "__main__":
    print_log("Course Assistant application started")
    main()
