
import streamlit as st
import uuid

from main import generate_answer
from agent import llm
from config import load_chats, save_chat
from Long_term_Memory import extract_memories, save_memory


# =========================================================
# 1. PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="AI Research Agent",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# 2. CUSTOM UI STYLING
# =========================================================

st.markdown(
    """
    <style>
    /* ---------- Global ---------- */

    .stApp {
        background-color: #0b0d12;
        color: #e8eaf0;
    }

    [data-testid="stHeader"] {
        background: rgba(11, 13, 18, 0.95);
    }

    .block-container {
        max-width: 1120px;
        padding-top: 2rem;
        padding-bottom: 7rem;
    }

    h1, h2, h3 {
        color: #f3f4f6 !important;
        letter-spacing: -0.5px;
    }

    p, li, label {
        color: #cbd0dc;
    }

    a {
        color: #9abaff !important;
        text-decoration: none;
    }

    a:hover {
        text-decoration: underline;
    }

    /* ---------- Sidebar ---------- */

    [data-testid="stSidebar"] {
        background: #10131a;
        border-right: 1px solid #252936;
    }

    [data-testid="stSidebar"] > div:first-child {
        padding-top: 1.2rem;
    }

    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        font-size: 1rem;
        font-weight: 650;
    }

    [data-testid="stSidebar"] .stButton > button {
        text-align: left;
        border-radius: 10px;
        border: 1px solid transparent;
        min-height: 42px;
        transition: all 0.15s ease;
    }

    [data-testid="stSidebar"] .stButton > button:hover {
        border-color: #41495c;
        background: #202533;
    }

    /* ---------- Buttons ---------- */

    .stButton > button {
        border-radius: 10px;
        min-height: 42px;
        font-weight: 550;
        transition: all 0.15s ease;
    }

    .stButton > button[kind="primary"] {
        background: #dce6ff;
        color: #111827;
        border: 1px solid #dce6ff;
    }

    .stButton > button[kind="primary"]:hover {
        background: #c3d5ff;
        border-color: #c3d5ff;
    }

    /* ---------- Chat messages ---------- */

    [data-testid="stChatMessage"] {
        background: transparent;
        border: none;
        padding: 1rem 0.2rem;
    }

    [data-testid="stChatMessageContent"] {
        color: #e5e7eb;
        line-height: 1.75;
    }

    [data-testid="stChatMessageAvatar"] {
        border-radius: 12px;
    }

    /* ---------- Chat input ---------- */

    [data-testid="stChatInput"] {
        background: #151923;
        border: 1px solid #353c4c;
        border-radius: 18px;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.20);
    }

    [data-testid="stChatInput"]:focus-within {
        border-color: #819ce8;
    }

    [data-testid="stChatInput"] textarea {
        color: #f3f4f6;
    }

    [data-testid="stChatInput"] textarea::placeholder {
        color: #8991a3;
    }

    /* ---------- Report sections ---------- */

    .report-eyebrow {
        color: #9aa8c7;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 1.8px;
        text-transform: uppercase;
        margin-bottom: 0.6rem;
    }

    .report-summary {
        background: #141923;
        border: 1px solid #293143;
        border-left: 3px solid #8ca9ff;
        border-radius: 12px;
        padding: 1.2rem 1.3rem;
        line-height: 1.8;
        color: #dce1eb;
        margin-bottom: 1.5rem;
    }

    .finding-number {
        color: #a9baff;
        font-size: 0.75rem;
        font-weight: 750;
        letter-spacing: 1.4px;
        text-transform: uppercase;
        margin-bottom: 0.5rem;
    }

    .report-divider {
        border: none;
        border-top: 1px solid #272d3a;
        margin: 1.6rem 0;
    }

    .app-brand {
        font-size: 1.45rem;
        font-weight: 750;
        letter-spacing: -0.7px;
        color: #f3f5fb;
        margin-bottom: 0.15rem;
    }

    .app-tagline {
        font-size: 0.83rem;
        color: #9098aa;
        line-height: 1.5;
        margin-bottom: 1.4rem;
    }

    .welcome-title {
        font-size: clamp(2rem, 4vw, 3rem);
        font-weight: 750;
        letter-spacing: -1.5px;
        line-height: 1.15;
        color: #f3f5fb;
        margin-bottom: 0.8rem;
    }

    .welcome-subtitle {
        color: #9ca5b8;
        font-size: 1.03rem;
        line-height: 1.7;
        max-width: 680px;
    }

    /* ---------- Containers and expanders ---------- */

    [data-testid="stExpander"] {
        background: #121620;
        border: 1px solid #292f3d;
        border-radius: 12px;
    }

    [data-testid="stVerticalBlockBorderWrapper"] {
        border-color: #292f3d;
        border-radius: 12px;
    }

    [data-testid="stAlert"] {
        border-radius: 12px;
    }

    /* ---------- Responsive adjustments ---------- */

    @media (max-width: 768px) {
        .block-container {
            padding-top: 1rem;
            padding-left: 1rem;
            padding-right: 1rem;
        }

        .welcome-title {
            font-size: 2rem;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# 3. SESSION STATE AND CHAT MANAGEMENT
# =========================================================

def create_new_chat():
    new_chat_id = str(uuid.uuid4())

    st.session_state.chats[new_chat_id] = {
        "title": "New Chat",
        "messages": [],
    }

    save_chat(new_chat_id, "New Chat", [])

    st.session_state.active_chat_id = new_chat_id


if "memory_candidates" not in st.session_state:
    st.session_state.memory_candidates = []

if "chats" not in st.session_state:
    st.session_state.chats = load_chats() or {}

    if not st.session_state.chats:
        create_new_chat()
    else:
        st.session_state.active_chat_id = next(
            iter(st.session_state.chats)
        )

if "active_chat_id" not in st.session_state:
    if st.session_state.chats:
        st.session_state.active_chat_id = next(
            iter(st.session_state.chats)
        )
    else:
        create_new_chat()

if "pending_question" not in st.session_state:
    st.session_state.pending_question = None


# =========================================================
# 4. REPORT RENDERING
#    Supports both Pydantic objects and saved dictionaries.
# =========================================================

def get_value(item, key, default=None):
    if isinstance(item, dict):
        return item.get(key, default)

    return getattr(item, key, default)


def display_research_report(report):
    topic = get_value(report, "topic", "Research Report")
    summary = get_value(report, "summary", "")
    key_findings = get_value(report, "key_findings", []) or []
    limitations = get_value(report, "limitations", []) or []

    st.markdown(
        '<div class="report-eyebrow">Research report</div>',
        unsafe_allow_html=True,
    )

    st.markdown(f"## {topic}")

    # Summary
    st.markdown("### Executive Summary")

    st.markdown(
        f'<div class="report-summary">{summary}</div>',
        unsafe_allow_html=True,
    )

    # Findings
    st.markdown("### Key Findings")

    if key_findings:
        for index, finding in enumerate(key_findings, start=1):
            finding_text = get_value(finding, "finding", "")
            source_url = get_value(finding, "source_url", "")

            with st.container(border=True):
                st.markdown(
                    f'<div class="finding-number">'
                    f'Finding {index:02d}</div>',
                    unsafe_allow_html=True,
                )

                st.markdown(finding_text)

                if source_url:
                    st.markdown(
                        f"[Read source ↗]({source_url})"
                    )
    else:
        st.info("No supported findings were returned.")

    # Limitations
    st.markdown("### Research Limitations")

    if limitations:
        for limitation in limitations:
            st.markdown(f"- {limitation}")
    else:
        st.caption("No limitations were provided.")

    st.markdown(
        '<hr class="report-divider">',
        unsafe_allow_html=True,
    )


def render_message_content(content):
    """Render normal chat messages or previously saved reports."""

    if isinstance(content, dict) and (
        "topic" in content or "key_findings" in content
    ):
        display_research_report(content)

    elif isinstance(content, str):
        st.markdown(content)

    else:
        st.write(content)


# =========================================================
# 5. SIDEBAR: BRAND, CONVERSATIONS AND MEMORY
# =========================================================

with st.sidebar:
    st.markdown(
        """
        <div class="app-brand">✳ Research AI</div>
        <div class="app-tagline">
            Your personal AI research workspace
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button(
        "＋  Start new research",
        type="primary",
        use_container_width=True,
    ):
        create_new_chat()
        st.rerun()

    st.markdown("---")
    st.markdown("#### Your conversations")

    chat_ids = list(st.session_state.chats.keys())

    # Keep the newest conversations at the top.
    for chat_id in reversed(chat_ids):
        chat = st.session_state.chats[chat_id]
        is_active = chat_id == st.session_state.active_chat_id

        title = chat.get("title", "New Chat").strip()
        if len(title) > 32:
            title = title[:29] + "..."

        button_label = f"●  {title}" if is_active else f"   {title}"

        if st.button(
            button_label,
            key=f"chat_{chat_id}",
            use_container_width=True,
            type="primary" if is_active else "secondary",
        ):
            st.session_state.active_chat_id = chat_id
            st.rerun()

    st.markdown("---")

    with st.expander("🧠 Memory manager", expanded=False):
        st.caption(
            "Review details extracted from your conversation "
            "before saving them to long-term memory."
        )

        if st.button(
            "Extract memories from this chat",
            key="extract_memories",
            use_container_width=True,
        ):
            current_messages = st.session_state.chats[
                st.session_state.active_chat_id
            ]["messages"]

            conversation = "\n".join(
                f"User: {message['content']}"
                for message in current_messages
                if message["role"] == "user"
            )

            if not conversation.strip():
                st.session_state.memory_candidates = []
                st.info("Ask a few questions before extracting memories.")
            else:
                with st.spinner("Extracting memories..."):
                    candidates = extract_memories(conversation, llm)

                st.session_state.memory_candidates = candidates or []
                st.rerun()

        candidates = st.session_state.memory_candidates

        if candidates:
            st.markdown("**Review extracted memories**")

            with st.form("memory_approval_form"):
                selected = []

                for index, memory in enumerate(candidates):
                    label = (
                        f"{memory['key']}: {memory['value']}"
                    )

                    if st.checkbox(
                        label,
                        key=f"memory_candidate_{index}",
                    ):
                        selected.append(memory)

                save_clicked = st.form_submit_button(
                    "Save selected memories",
                    use_container_width=True,
                )

                if save_clicked:
                    for memory in selected:
                        save_memory(
                            "local_user",
                            memory["key"],
                            memory["value"],
                        )

                    st.success(
                        f"Saved {len(selected)} memories."
                    )

        elif st.session_state.memory_candidates == []:
            st.caption("No extracted memories to review yet.")


# =========================================================
# 6. ACTIVE CONVERSATION
# =========================================================

active_chat_id = st.session_state.active_chat_id
active_chat = st.session_state.chats[active_chat_id]


# Welcome screen for an empty conversation
if not active_chat["messages"]:
    st.markdown(
        '<div class="report-eyebrow">Your research workspace</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="welcome-title">'
        'What would you like to<br>understand today?'
        '</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="welcome-subtitle">
            Ask a question, investigate a topic, and get a structured
            research report with key findings, sources, and limitations.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("")

    st.markdown("#### Try starting with")

    suggestions = [
        "How are AI agents being used in real-world applications?",
        "Compare RAG and fine-tuning for LLM applications.",
        "What are the latest approaches to AI agent evaluation?",
    ]

    for index, suggestion in enumerate(suggestions):
        if st.button(
            f"↗  {suggestion}",
            key=f"suggestion_{index}",
            use_container_width=True,
        ):
            st.session_state.pending_question = suggestion
            st.rerun()


# Render existing conversation
else:
    for message in active_chat["messages"]:
        with st.chat_message(message["role"]):
            render_message_content(message["content"])


# =========================================================
# 7. QUESTION INPUT AND EXISTING BACKEND CALL
# =========================================================

question = st.chat_input(
    "Ask a question or explore a research topic...",
)

if question is None and st.session_state.pending_question:
    question = st.session_state.pending_question
    st.session_state.pending_question = None

if question:
    # Save and display the user's message.
    active_chat["messages"].append(
        {"role": "user", "content": question}
    )

    if active_chat["title"] == "New Chat":
        active_chat["title"] = question[:30]

    save_chat(
        active_chat_id,
        active_chat["title"],
        active_chat["messages"],
    )

    with st.chat_message("user"):
        st.markdown(question)

    # Preserve the existing LangGraph thread configuration.
    config = {
        "configurable": {
            "thread_id": active_chat_id
        }
    }

    with st.chat_message("assistant"):
        with st.spinner(
            "Researching your question, gathering findings, and "
            "preparing your report..."
        ):
            try:
                # Existing backend call — unchanged.

                answer = generate_answer(question, config)

                if answer is not None:
                    display_research_report(answer)

                    report_data = answer.model_dump()

                    active_chat["messages"].append(
                        {
                            "role": "assistant",
                            "content": report_data
                        }
                    )

                    save_chat(
                        active_chat_id,
                        active_chat["title"],
                        active_chat["messages"]
                    )
                else:
                    st.info(
                        "Research is waiting for approval or has not produced "
                        "a final report yet."
                    )

                active_chat["messages"].append(
                    {
                        "role": "assistant",
                        "content": report_data,
                    }
                )

                save_chat(
                    active_chat_id,
                    active_chat["title"],
                    active_chat["messages"],
                )

            except Exception as error:
                st.error(
                    "Something went wrong while generating your "
                    "research report."
                )

                with st.expander("Technical error details"):
                    st.exception(error)
