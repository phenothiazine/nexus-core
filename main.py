
import streamlit as st
import uuid
import datetime
from core.orchestrator import Orchestrator
from core.memory import MemoryManager

# --- 1. Page Configuration (Must be first) ---
st.set_page_config(
    page_title="Nexus",
    page_icon="⚫",
    layout="centered",
    initial_sidebar_state="auto"
)

# --- 2. CSS & UI Setup ---
def load_css():
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()



# --- 3. Session State Management ---
if "sessions" not in st.session_state:
    st.session_state.sessions = {}

if "current_session_id" not in st.session_state:
# ... (rest of session init logic) ...
    new_id = str(uuid.uuid4())
    st.session_state.current_session_id = new_id
    st.session_state.sessions[new_id] = {
        "messages": [], 
        "title": "New Chat", 
        "pinned": False, 
        "created_at": datetime.datetime.now()
    }


# Helper Functions
def create_new_chat():
    # Sequential Naming Logic
    base_title = "New Chat"
    existing_titles = [data["title"] for data in st.session_state.sessions.values()]
    
    count = 1
    new_title = f"{base_title} {count}"
    while new_title in existing_titles:
        count += 1
        new_title = f"{base_title} {count}"
        
    new_id = str(uuid.uuid4())
    st.session_state.sessions[new_id] = {
        "messages": [], 
        "title": new_title, 
        "pinned": False,
        "created_at": datetime.datetime.now()
    }
    st.session_state.current_session_id = new_id

def switch_session(session_id):
    st.session_state.current_session_id = session_id

def delete_session(session_id):
    if session_id in st.session_state.sessions:
        del st.session_state.sessions[session_id]
        if st.session_state.current_session_id == session_id:
            if st.session_state.sessions:
                st.session_state.current_session_id = list(st.session_state.sessions.keys())[0]
            else:
                create_new_chat()
        st.rerun()

def toggle_pin(session_id):
    if session_id in st.session_state.sessions:
        st.session_state.sessions[session_id]["pinned"] = not st.session_state.sessions[session_id]["pinned"]
        st.rerun()

# --- Modal Dialog for Renaming ---
@st.dialog("Rename Chat")
def rename_dialog(session_id):
    current_title = st.session_state.sessions[session_id]["title"]
    new_title = st.text_input("New Title", value=current_title)
    if st.button("Save", type="primary"):
        st.session_state.sessions[session_id]["title"] = new_title
        st.rerun()

def get_current_session_data():
    # Robust check to prevent KeyErrors if state gets out of sync
    if st.session_state.current_session_id not in st.session_state.sessions:
        if st.session_state.sessions:
            # Fallback to first available
            st.session_state.current_session_id = list(st.session_state.sessions.keys())[0]
        else:
            # No sessions left, create new (but carefully avoid recursion loops if create_new calls this)
            new_id = str(uuid.uuid4())
            st.session_state.sessions[new_id] = {
                "messages": [], 
                "title": "New Chat", 
                "pinned": False,
                "created_at": datetime.datetime.now()
            }
            st.session_state.current_session_id = new_id
            
    return st.session_state.sessions[st.session_state.current_session_id]

def generate_smart_title(user_message):
    """
    Generate a smart title based on the user's message using a lightweight call.
    """
    try:
        model = orchestrator.model 
        prompt = f"Summarize this user query into a very short 3-5 word title (English or Chinese). Query: {user_message}. Title:"
        response = model.generate_content(prompt)
        
        # Safely check if response has valid text
        if response and response.candidates and len(response.candidates) > 0:
            candidate = response.candidates[0]
            if candidate.content and candidate.content.parts:
                title = candidate.content.parts[0].text.strip().replace('"', '').replace("Title:", "").strip()
                return title if title else user_message[:25]
        
        return user_message[:25]
    except Exception:
        return user_message[:25]

def add_message(role, content, auto_title=False):
    session = get_current_session_data()
    session["messages"].append({"role": role, "content": content})
    
    # Smart Auto-title: rename if this is the first user message and title starts with "New Chat"
    if auto_title and role == "user":
        current_title = session.get("title", "")
        # Check if title is still a default "New Chat" pattern
        if current_title == "New Chat" or current_title.startswith("New Chat "):
            new_title = generate_smart_title(content)
            if new_title:
                session["title"] = new_title

# --- 4. Core Initialization ---
@st.cache_resource
def get_orchestrator():
    return Orchestrator()
    
@st.cache_resource
def get_memory_manager():
    return MemoryManager()
    
orchestrator = get_orchestrator()
memory_manager = get_memory_manager()

# --- 5. Sidebar (Advanced Navigation) ---
with st.sidebar:
    # Inject Nexus Brand in main area (via markdown after sidebar context)
    pass

# Inject Nexus Brand (positioned via CSS to main content area)
st.markdown('<div class="nexus-brand">NEXUS</div>', unsafe_allow_html=True)

with st.sidebar:
    if st.button("➕ Start New Chat", use_container_width=True, type="primary"):
        create_new_chat()
        st.rerun()

    st.divider()

    # Sort sessions logic
    sessions_items = list(st.session_state.sessions.items())
    pinned_sessions = [sid for sid, data in sessions_items if data.get("pinned", False)]
    recent_sessions = [sid for sid, data in sessions_items if not data.get("pinned", False)]
    
    # Sort recent by created_at (descending) if available, else standard
    # (Assuming created_at is in data, if not just reverse list)
    recent_sessions = recent_sessions[::-1] 

    def render_session_item(sid, data):
        title = data.get("title", "Untitled")
        is_current = (sid == st.session_state.current_session_id)
        is_pinned = data.get("pinned", False)
        type_str = "primary" if is_current else "secondary"
        
        # Create integrated button with popover overlay
        with st.container():
            col1, col2 = st.columns([0.88, 0.12])
            with col1:
                if st.button(title, key=f"btn_{sid}", use_container_width=True, type=type_str):
                    switch_session(sid)
                    st.rerun()
            with col2:
                with st.popover("⋮", use_container_width=True):
                    st.caption("Chat Settings")
                    if st.button("✏️ Rename", key=f"ren_{sid}", use_container_width=True):
                        rename_dialog(sid)
                    pin_label = "📌 Unpin" if is_pinned else "📌 Pin"
                    if st.button(pin_label, key=f"pin_{sid}", use_container_width=True):
                        toggle_pin(sid)
                    if st.button("🗑️ Delete", key=f"del_{sid}", use_container_width=True):
                        delete_session(sid)

    # Render Pinned
    if pinned_sessions:
        st.caption("📌 Pinned")
        for sid in pinned_sessions:
            if sid in st.session_state.sessions:
                render_session_item(sid, st.session_state.sessions[sid])
            
    # Render Recent
    if recent_sessions:
        st.caption("🕒 Recent")
        for sid in recent_sessions:
            if sid in st.session_state.sessions:
                render_session_item(sid, st.session_state.sessions[sid])
    
    if not pinned_sessions and not recent_sessions:
        st.info("No chats yet. Start a new one!")

    st.divider()
    
    with st.expander("🧠 Memory Bank", expanded=False):
        tab1, tab2 = st.tabs(["📝 Note", "📂 File"])
        # (Rest of Memory Code same as before)
        with tab1:
            with st.form("mem_form"):
                note = st.text_area("Note", height=80)
                if st.form_submit_button("Save"):
                    if note and memory_manager.add_document(note, {"source": "manual"}):
                        st.toast("Memory Saved")
        with tab2:
            up_file = st.file_uploader("PDF/TXT", type=["pdf", "txt"])
            if up_file:
                if memory_manager.process_file(up_file, up_file.name):
                    st.toast(f"Learned from {up_file.name}")

# --- 6. Main Header (Bubble Style Button) ---
current_session = get_current_session_data()
current_title = current_session["title"]

# Centered bubble-style title button (click to rename)
col_l, col_center, col_r = st.columns([1, 2, 1])
with col_center:
    if st.button(current_title, key="header_title_btn", use_container_width=True, type="secondary"):
        rename_dialog(st.session_state.current_session_id)

# --- 7. Chat Render ---
current_messages = current_session["messages"]

for message in current_messages:
    with st.chat_message(message["role"]):
        content = message["content"]
        
        if isinstance(content, dict): 
            # Assistant Response
            if content.get("context_used") and len(content.get("context_used")) > 0:
                with st.expander("📚 Referenced Memory"):
                    for doc in content["context_used"]:
                        st.markdown(f"- {doc}")
            if content.get("thought"):
                with st.status("Thought Process", state="complete"):
                    st.markdown(content["thought"])
            st.markdown(content["answer"])
        else:
            st.markdown(content)

# --- 8. Input Logic ---
if prompt := st.chat_input("Message Nexus..."):
    add_message("user", prompt, auto_title=True)  # Trigger auto-title on user message
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        status = st.status("Nexus is thinking...", expanded=True)
        try:
            # Pass full chat history to Orchestrator
            response_dict = orchestrator.process_query(prompt, chat_history=current_messages)
            
            status.markdown(response_dict.get("thought", "Done."))
            status.update(label="Thought Process", state="complete", expanded=False)
            
            if response_dict.get("context_used"):
                with st.expander("📚 Referenced Memory", expanded=True):
                    for doc in response_dict["context_used"]:
                        st.markdown(f"- {doc}")
            
            st.markdown(response_dict["answer"])
            add_message("assistant", response_dict)
            
        except Exception as e:
            status.update(label="Error", state="error")
            st.error(str(e))
