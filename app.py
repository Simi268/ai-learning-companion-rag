import streamlit as st
import os

from agent import chat_with_agent
from pdf_ingestion import ingest_pdf

# -----------------------------------
# PAGE CONFIG
# -----------------------------------

st.set_page_config(
    page_title="AI Learning Companion",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------------
# CUSTOM CSS
# -----------------------------------

st.markdown(
    """
    <style>

    /* Main App */
    .stApp {
        background-color: #0B1120;
        color: white;
    }

    /* Width */
    .block-container {
    max-width: 1600px;
    padding-left: 3rem;
    padding-right: 3rem;
}

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(
            180deg,
            #111827,
            #1F2937
        );
        border-right: 1px solid #374151;
    }

    /* Cards */
    .metric-card {
        background: linear-gradient(
            135deg,
            #111827,
            #1E293B
        );
        border: 1px solid #374151;
        padding: 18px;
        border-radius: 18px;
        color: white;
    }

    /* Chat Bubbles */
    .user-bubble {
        background: #1E293B;
        border-radius: 14px;
        padding: 14px;
        margin-bottom: 10px;
        border: 1px solid #334155;
    }

    .assistant-bubble {
    background: #111827;
    border-radius: 14px;
    padding: 24px;
    margin-bottom: 20px;
    border: 1px solid #374151;
    width: 100%;
}

    /* Upload Box */
    .upload-box {
        background: #111827;
        padding: 18px;
        border-radius: 16px;
        border: 1px solid #374151;
    }

    /* Header */
    .main-title {
        font-size: 48px;
        font-weight: 700;
        color: white;
    }

    .sub-text {
        color: #94A3B8;
        margin-top: -10px;
    }

    /* Divider */
    hr {
        border: 1px solid #1F2937;
    }

    /* Buttons */
    .stButton button {
        background: linear-gradient(
            135deg,
            #2563EB,
            #7C3AED
        );
        color: white;
        border: none;
        border-radius: 12px;
        padding: 10px 16px;
        font-weight: 600;
    }

    /* Chat Input */
    .stChatInput {
        border-radius: 14px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------------
# SIDEBAR
# -----------------------------------

with st.sidebar:

    st.markdown(
        """
        <h1 style='font-size:32px;'>
        🧠 AI Companion
        </h1>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")

    # -----------------------------------
    # PDF UPLOAD
    # -----------------------------------

    st.subheader("📂 Upload PDF")

    st.markdown(
        """
        <div class="upload-box">
        Upload notes, research papers,
        AI documents, or study material.
        </div>
        """,
        unsafe_allow_html=True,
    )

    uploaded_file = st.file_uploader(
        "",
        type=["pdf"]
    )

    if uploaded_file is not None:

        os.makedirs(
            "Documents",
            exist_ok=True
        )

        save_path = os.path.join(
            "Documents",
            uploaded_file.name
        )

        with open(save_path, "wb") as f:

            f.write(
                uploaded_file.getbuffer()
            )

        st.success(
            f"{uploaded_file.name} uploaded successfully!"
        )

        result = ingest_pdf(save_path)

        st.info(result)

    st.markdown("---")

    # -----------------------------------
    # STATS
    # -----------------------------------

    st.subheader("📊 Learning Stats")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Memories",
            "24"
        )

    with col2:
        st.metric(
            "PDFs",
            "3"
        )

    st.markdown("---")

    # -----------------------------------
    # RETRIEVAL MODE
    # -----------------------------------

    st.subheader("⚡ Retrieval Mode")

    retrieval_mode = st.selectbox(
        "Choose retrieval source",
        [
            "Hybrid Search",
            "PDF Knowledge",
            "Personal Memory",
        ]
    )

    st.markdown("---")

    # -----------------------------------
    # QUICK ACTIONS
    # -----------------------------------

    st.subheader("📝 Quick Actions")

    st.button("📚 Show Notes")

    st.button("🧠 Show Memories")

    st.button("🧹 Clear Chat")

# -----------------------------------
# MAIN HEADER
# -----------------------------------

st.markdown(
    """
    <div class="main-title">
    🧠 AI Learning Companion
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="sub-text">
    RAG + Semantic Memory + PDF Intelligence + Vector Search
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("<br>", unsafe_allow_html=True)

# -----------------------------------
# TOP METRICS
# -----------------------------------

col1, col2, col3 = st.columns(3)

with col1:

    st.markdown(
        """
        <div class="metric-card">
        📚 <b>PDFs Indexed</b><br><br>
        <h2>3</h2>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:

    st.markdown(
        """
        <div class="metric-card">
        🧠 <b>Semantic Memories</b><br><br>
        <h2>24</h2>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col3:

    st.markdown(
        f"""
        <div class="metric-card">
        ⚡ <b>Retrieval Mode</b><br><br>
        <h2>{retrieval_mode}</h2>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("<br>", unsafe_allow_html=True)

# -----------------------------------
# SESSION STATE
# -----------------------------------

if "messages" not in st.session_state:

    st.session_state.messages = []

# -----------------------------------
# DISPLAY CHAT HISTORY
# -----------------------------------

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )

# -----------------------------------
# CHAT INPUT
# -----------------------------------

user_input = st.chat_input(
    "Ask me anything ..."
)

# -----------------------------------
# HANDLE USER INPUT
# -----------------------------------

if user_input:

    # USER MESSAGE

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input,
        }
    )

    with st.chat_message("user"):

        st.markdown(
            f"""
            <div class="user-bubble">
            {user_input}
            </div>
            """,
            unsafe_allow_html=True,
        )

    # -----------------------------------
    # AI RESPONSE
    # -----------------------------------

    with st.spinner(
        "🧠 AI is thinking..."
    ):

        result = chat_with_agent(
            user_input
        )

        ai_response = result["response"]

        retrieval_source = (
            result["retrieval_source"]
        )

    formatted_response = f"""
## 🤖 AI Response

---

{ai_response}
"""

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": formatted_response,
        }
    )

    with st.chat_message("assistant"):

        st.markdown(
            formatted_response,
            unsafe_allow_html=True,
        )

# -----------------------------------
# FOOTER
# -----------------------------------

st.markdown("<br><br>", unsafe_allow_html=True)

st.markdown("---")




