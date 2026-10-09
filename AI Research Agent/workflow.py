from typing import TypedDict
from langchain.messages import AnyMessage
from agent import agent
from schema import ResearchReport
from agent import llm
from langgraph.graph import StateGraph, START, END
from langgraph.types import interrupt, Command
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3
conn = sqlite3.connect("research_graph.db", check_same_thread= False)

memory = SqliteSaver(conn)



structured_llm = llm.with_structured_output(ResearchReport)

class ResearchState(TypedDict):
    question : str
    research_context : str
    report : dict
    research_round : int
    need_more_research : bool
    human_approved : bool
    human_feedback : str

workflow = StateGraph(ResearchState)


def research_node(state : ResearchState, config):
    feedback = state.get("human_feedback", "")
    research_prompt =   state['question']
    if feedback:
        research_prompt += f"""
        Human feedback:
        {feedback}
    
        Improve the research based on this feedback.
        """

    response = agent.invoke({
        "messages" : [
            {
                "role" : "user",
                "content" : research_prompt
            }
        ]
    },
    config = config)

    tool_results = []

    for message in response['messages']:
        if getattr(message, "type", None)    == 'tool':
            tool_results.append(
                f"Tool : {getattr(message, 'name', 'unknown')}\n"
                f"Result : {message.content}"
            )

    new_context = '\n\n'.join(tool_results)
    previous_context = state.get("research_context", "")

    return {
        "research_context": (previous_context + "\n\n" + new_context).strip(),
        "research_round" : state.get("research_round", 0) + 1
    }


def analysis_node(state: ResearchState):
    enough_information = bool(
        state['research_context'].strip()
    )

    return {
        "needs_more_research" : (
            not enough_information
            and state['research_round'] < 2
        )
    }

def route_research(state: ResearchState):
    if state['need_more_research']:
        return "research"
    return "report"

def report_node(state: ResearchState):
    prompt = f"""
    You are a research report generator.

    Generate a structured report using only the
    research context provided.

    Rules:
    - Do not invent facts or sources.
    - Only include findings supported by the context.
    - Use source URLs exactly as they appear.
    - Mention gaps as limitations.

    Research topic:
    {state["question"]}

    Research context:
    {state["research_context"]}
    """

    report = structured_llm.invoke(prompt)

    return {
        "report" :report.model_dump()
    }

def human_approval(state: ResearchState):

    decision = interrupt({
        "message" : "Research is complete. Do you want to generate the final report?",
        "question" : state['question'],
        "research_context" : state['research_context']
    })

    return {
        "human_approved" : decision["approved"],
        "human_feedback" : decision.get("feedback", "")
    }

def route_human_approval(state: ResearchState):
    if state['human_approved']:
        return "report"
    return "research"

def graph():
    workflow.add_node("research", research_node)
    workflow.add_node("analysis", analysis_node)
    workflow.add_node("report", report_node)
    workflow.add_node("human_approval", human_approval)

    workflow.add_edge(START, "research")
    workflow.add_conditional_edges(
        "analysis",
        route_research,
        {
            "research": "research",
            "report" : "human_approval"
        }
    )
    workflow.add_conditional_edges(
        "human_approval",
        route_human_approval,
        {
            "report" : "report",
            "research" : "research"
        }
    )
    workflow.add_edge("research", "analysis")
    workflow.add_edge("human_approval", "report")
    workflow.add_edge("report", END)

    return workflow.compile(checkpointer = memory)

research_graph = graph()



if __name__ == "__main__":
    config = {
        "configurable" : {
            "thread_id" : "research_001"
        }
    }
    result = research_graph.invoke({
        "question" : "Impact of AI on software Engineering",
        "research_context" : "",
        "report" : {},
        "research_round" : 0,
        "need_more_research" : False,
        "human_approval" : False
    }, config = config)

    print(result['report'])














