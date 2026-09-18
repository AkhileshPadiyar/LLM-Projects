import streamlit as st
import ollama

st.title("Code Generator")

text = st.text_area("Enter the code you want to generate")

language = st.selectbox("Select Language", ["Python", "Java", "C++"])

client = ollama.Client(host = "http://localhost:11434")

if st.button("Generata Code"):
    if not text.strip():
        st.warning("Please enter a code")
    else:
        prompt = f"""
        Generate a optimised code for the follwing questions in {language},
        Only return the code no explanation, even don't include any heading,
        If the language is C++ don't write std::, instead already preimport using namespace std;
        ALways write the full code, including the main() function
        question : {text}
        """
        # prompt = text

        try:
            with st.spinner('Generating code...'):
                response = client.chat(
                    model="mistral:7b",
                    messages=[
                        {
                            "role" : "user",
                            "content" : prompt
                        }
                    ],
                    options={
                        "temperature" : 0
                    }
                )
                result = response['message']['content']
                st.markdown(result)

        except Exception as e:
            st.error(e)

