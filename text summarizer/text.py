import requests
import streamlit as st

def summarize_text(text, length):
    prompt = f"""
    Summarize the follwing text for me in not more than {length} words:
    Text: {text}
    """

    response = requests.post(
        'http://localhost:11434/api/generate',
        json={
            'model':'mistral:7b',
            'prompt': prompt,
            'stream': False
        }
    )

    return response.json()['response']

st.title("Text Summarizer")

text = st.text_area("Enter a sentence to summarize: ")
text_length = st.slider("Choose summary Length: ", min_value=1, max_value=100, value=50)

if st.button('Summarize'):
    if text.strip():
        with st.spinner('Summarizing'):
            summary = summarize_text(text, text_length)
        st.subheader("summarized")
        st.text(summary)
    else:
        st.warning("Please enter a sentence to summarize")