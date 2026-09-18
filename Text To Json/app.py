import streamlit as st
import ollama
import json

st.title("Text to JSON")

text = st.text_area("Enter the text", placeholder="I am akhilesh and ...")

client = ollama.Client(host="http://127.0.0.1:11434")

dummy = """
            Hello i am akhilesh and i am student of graphic era deemed to be University.
            I am currently pusing B.tech in Computer science and engineering.
            I am skilled in javascript, react, python
        """

if st.button("Convert to JSON"):
    if not text.strip():
        st.warning("Please write something in the input")
    else:
        prompt = f"""
        Convert the text provided into structed JSON Format,
        only keep the necessary details intact and remove any unnecessary words:
        
        Text: {text}
        """
        with st.spinner("Converting to JSON..."):
            response = client.chat(
                model="mistral:7b",
                messages=[
                    {"role": "user",
                     "content": prompt}
                ],
                options={
                    "temperature": 0
                }
            )

            result = response["message"]['content']

            # st.write(response['Message']['content'])

            st.subheader("Json")
            st.code(result)

            try:
                data = json.loads(result)

                st.subheader("Extracted JSON")
                st.json(data)

            except json.JSONDecodeError:
                st.error("Invalid JSON")

