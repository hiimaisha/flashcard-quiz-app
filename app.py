import streamlit as st
import random

st.set_page_config(page_title="Flashcard Quiz", page_icon="🗂️", layout="centered")
st.title("🗂️ Flashcard Quiz")
st.caption("Create cards, test yourself, and track what you know.")

DEFAULT_CARDS = [
    {"question": "What does HTML stand for?", "answer": "HyperText Markup Language"},
    {"question": "What is a Python list?", "answer": "An ordered, mutable collection of items."},
    {"question": "What does SQL stand for?", "answer": "Structured Query Language"},
]
if "cards" not in st.session_state:
    st.session_state.cards = [c.copy() for c in DEFAULT_CARDS]
if "index" not in st.session_state:
    st.session_state.index = 0
if "revealed" not in st.session_state:
    st.session_state.revealed = False

cards = st.session_state.cards
if not cards:
    st.info("No cards yet. Add your first card in the Manage Cards section below.")
else:
    st.progress((st.session_state.index + 1) / len(cards), text=f"Card {st.session_state.index + 1} of {len(cards)}")
    card = cards[st.session_state.index]
    with st.container(border=True):
        st.subheader(card["question"])
        if st.session_state.revealed:
            st.success(card["answer"])
        else:
            st.write("Think of the answer, then reveal it.")
        a, b, c = st.columns(3)
        with a:
            if st.button("← Previous", use_container_width=True, disabled=len(cards) < 2):
                st.session_state.index = (st.session_state.index - 1) % len(cards)
                st.session_state.revealed = False
                st.rerun()
        with b:
            if st.button("Show / Hide", use_container_width=True):
                st.session_state.revealed = not st.session_state.revealed
                st.rerun()
        with c:
            if st.button("Next →", use_container_width=True, disabled=len(cards) < 2):
                st.session_state.index = (st.session_state.index + 1) % len(cards)
                st.session_state.revealed = False
                st.rerun()
    if st.button("🔀 Shuffle cards"):
        random.shuffle(cards)
        st.session_state.index = 0
        st.session_state.revealed = False
        st.rerun()

st.divider()
st.subheader("Manage cards")
tab_add, tab_edit, tab_delete = st.tabs(["➕ Add", "✏️ Edit", "🗑️ Delete"])
with tab_add:
    with st.form("add_card", clear_on_submit=True):
        q = st.text_input("Question", placeholder="e.g. What is a variable?")
        ans = st.text_area("Answer", placeholder="Write a clear, short answer")
        submitted = st.form_submit_button("Add card", use_container_width=True)
        if submitted:
            if q.strip() and ans.strip():
                cards.append({"question": q.strip(), "answer": ans.strip()})
                st.session_state.index = len(cards) - 1
                st.session_state.revealed = False
                st.success("Card added!")
                st.rerun()
            else:
                st.error("Please enter both a question and an answer.")
with tab_edit:
    if cards:
        labels = [f"{i+1}. {c['question'][:60]}" for i, c in enumerate(cards)]
        selected = st.selectbox("Choose a card to edit", range(len(cards)), format_func=lambda i: labels[i], key="edit_choice")
        with st.form("edit_card"):
            new_q = st.text_input("Question", value=cards[selected]["question"])
            new_a = st.text_area("Answer", value=cards[selected]["answer"])
            if st.form_submit_button("Save changes", use_container_width=True):
                if new_q.strip() and new_a.strip():
                    cards[selected] = {"question": new_q.strip(), "answer": new_a.strip()}
                    st.success("Changes saved!")
                    st.rerun()
                else:
                    st.error("Question and answer cannot be empty.")
    else:
        st.caption("Add a card first to edit it.")
with tab_delete:
    if cards:
        labels = [f"{i+1}. {c['question'][:60]}" for i, c in enumerate(cards)]
        delete_idx = st.selectbox("Choose a card to delete", range(len(cards)), format_func=lambda i: labels[i], key="delete_choice")
        if st.button("Delete selected card", type="primary"):
            cards.pop(delete_idx)
            st.session_state.index = min(st.session_state.index, max(0, len(cards)-1))
            st.session_state.revealed = False
            st.success("Card deleted.")
            st.rerun()
    else:
        st.caption("There are no cards to delete.")

st.caption("Note: cards are kept in this browser session. Refreshing or restarting the app resets them.")
