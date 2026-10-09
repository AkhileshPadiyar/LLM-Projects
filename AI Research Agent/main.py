from Long_term_Memory import (add_memory_context)
from schema import ResearchReport
from workflow import research_graph
from langgraph.types import Command
import streamlit as st

if "waiting_for_approval" not in st.session_state:
    st.session_state.waiting_for_approval = False
if "research_config" not in st.session_state:
    st.session_state.research_config = None



def generate_answer(question, config, user_id="local_user"):
    enriched_question = add_memory_context(question, user_id)

    config = {
        "configurable": {
            "thread_id": f"research_{user_id}"
        }
    }

    result = research_graph.invoke(
        {
            "question": enriched_question,
            "research_context": "",
            "report": [],
            "research_round": 0,
            "need_more_research": False
        },
        config=config
    )

    st.session_state.research_config = config

    state = research_graph.get_state(config)

    # Case 1: Research is waiting for human approval.
    if state.interrupts:
        st.session_state.waiting_for_approval = True

        st.subheader("Research Review")
        st.write(
            "The research agent has completed its research. "
            "Review the collected information before generating "
            "the final report."
        )

        col1, col2 = st.columns(2)

        with col1:
            approve = st.button("Approve Research")

        with col2:
            reject = st.button("Reject & Research Again")

        if approve:
            result = research_graph.invoke(
                Command(
                    resume={
                        "approved": True,
                        "feedback": ""
                    }
                ),
                config=st.session_state.research_config
            )

            st.session_state.waiting_for_approval = False

            if result.get("report"):
                return ResearchReport.model_validate(
                    result["report"]
                )

            return None

        if reject:
            feedback = st.text_area(
                "What should the agent improve?"
            )

            result = research_graph.invoke(
                Command(
                    resume={
                        "approved": False,
                        "feedback": feedback
                    }
                ),
                config=st.session_state.research_config
            )

            st.session_state.waiting_for_approval = False

            if result.get("report"):
                return ResearchReport.model_validate(
                    result["report"]
                )

            return None

        # Important: do not pretend a report is ready.
        return None

    # Case 2: The graph finished without an interruption.
    report_data = result.get("report")

    if report_data:
        st.session_state.waiting_for_approval = False
        return ResearchReport.model_validate(report_data)

    # Case 3: The graph returned no report.
    return None


















