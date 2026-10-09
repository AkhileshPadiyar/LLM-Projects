from agent import llm
from schema import ResearchReport

structured_llm = llm.with_structured_output(
    ResearchReport
)

result = structured_llm.invoke(
    """
    Explain Retrieval-Augment Generation (RAG)
    Provide a summary, key findings and limitations
    """
)

print(result)
print(type(result))

print(result.topic)
print(result.summary)

for findings in result.key_findings:
    print(findings.finding)
    print(findings.source_url)