import streamlit as st
from summarizer import summarizer_text

st.title("Ai Text Summarizer")

text = st.text_area("Enter a sentence to summarize", height=300)
style = st.selectbox("Select summary style: ", ['Single Paragraph', "Bullet Points", 'One Sentence'])
temp = st.slider("Creativity", min_value=0.0, max_value=1.0, value = 0.5)

if st.button("Summarize"):
    if text.strip():
        with st.spinner("Generating summary..."):
            summary = summarizer_text(text, style, temp)

        st.subheader("Summarized")
        st.write(summary)

    else:
        st.warning("Please enter a sentence to summarize")