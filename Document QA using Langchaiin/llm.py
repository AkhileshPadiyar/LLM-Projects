from rag import create_llm
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

def generate_answer(vector_store, question):
    retriever = vector_store.as_retriever(
        kwargs={"k": 3}
    )

    llm = create_llm()

    prompt = ChatPromptTemplate.from_template("""
            Answer the question based only on the following context.

            Context:
            {context}

            Question:
            {question}

            If the answer cannot be found in the context, say:
            "I don't know based on the provided document."

            Answer:
            """)

    chain = (
            {
                "context": retriever,
                "question": RunnablePassthrough()
            }
            | prompt
            | llm
            | StrOutputParser()
    )

    answer = chain.invoke(question)
    return answer