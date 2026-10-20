import sqlite3, random
from pathlib import Path
import streamlit as st

st.set_page_config(page_title="Flashcard Studio",page_icon="🧠",layout="wide")
DB=Path(__file__).with_name("flashcards.db")
st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@500;600;700;800&display=swap');
html,body,[class*="css"]{font-family:'DM Sans',sans-serif}.stApp{background:linear-gradient(135deg,#f7f8ff,#f3f7ff 55%,#f8f5ff)}.block-container{max-width:1100px;padding-top:2rem}
.hero{padding:1.5rem 1.7rem;border-radius:24px;background:linear-gradient(120deg,#312e81,#5b4be7 65%,#8b5cf6);color:white;margin-bottom:1.3rem}.hero h1{font-family:Manrope,sans-serif;font-size:2.2rem;margin:0;color:white}.hero p{margin:.4rem 0 0;color:#e5e7ff}
.study-card{background:white;border:1px solid #e4e7f2;border-radius:24px;padding:2rem;min-height:180px;box-shadow:0 12px 35px #27265b0d}.study-label{font-size:.78rem;letter-spacing:.12em;text-transform:uppercase;color:#7774a7;font-weight:700}.study-question{font-family:Manrope,sans-serif;font-size:1.65rem;font-weight:800;color:#20214b;line-height:1.35;margin:1rem 0}.answer{padding:1rem 1.1rem;background:#f0fdf4;border:1px solid #bbf7d0;border-radius:14px;color:#166534;font-size:1.05rem}
div.stButton>button{border-radius:12px;min-height:2.8rem;font-weight:700;border:1px solid #d9dcef}div.stButton>button[kind="primary"]{background:#5548d9;color:white;border:0}div[data-testid="stMetric"]{background:white;border:1px solid #e7e8f4;padding:1rem;border-radius:16px}section[data-testid="stSidebar"]{background:#f1f0ff}
</style>""",unsafe_allow_html=True)
def connect():
    c=sqlite3.connect(DB); c.row_factory=sqlite3.Row; return c
with connect() as c:
    c.execute("CREATE TABLE IF NOT EXISTS cards(id INTEGER PRIMARY KEY AUTOINCREMENT,question TEXT NOT NULL,answer TEXT NOT NULL,created_at TEXT DEFAULT CURRENT_TIMESTAMP)")
    if c.execute("SELECT COUNT(*) FROM cards").fetchone()[0]==0:
        c.executemany("INSERT INTO cards(question,answer) VALUES (?,?)",[("What does HTML stand for?","HyperText Markup Language"),("What is a Python dictionary?","A collection that stores key-value pairs."),("What does SQL stand for?","Structured Query Language"),("What is an algorithm?","A finite sequence of steps to solve a problem.")])
def all_cards():
    with connect() as c: return c.execute("SELECT id,question,answer FROM cards ORDER BY id").fetchall()
def esc(s): return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;").replace("'","&#x27;")
st.markdown('<div class="hero"><h1>🧠 Flashcard Studio</h1><p>Learn actively. Reveal answers, move at your pace, and build your own deck.</p></div>',unsafe_allow_html=True)
cards=all_cards()
x,y,z=st.columns(3); x.metric("Cards in your deck",len(cards)); y.metric("Study mode","Active recall"); z.metric("Storage","SQLite · persistent")
if "card_index" not in st.session_state: st.session_state.card_index=0
if "show_answer" not in st.session_state: st.session_state.show_answer=False
ids=[r["id"] for r in cards]
if st.session_state.get("deck_signature")!=tuple(ids):
    st.session_state.deck_signature=tuple(ids); st.session_state.card_index=min(st.session_state.card_index,max(0,len(ids)-1)); st.session_state.shuffled_ids=ids.copy()
st.markdown("### Study deck")
if cards:
    order=st.session_state.shuffled_ids or ids; by_id={r["id"]:r for r in cards}; idx=st.session_state.card_index%len(order); current=by_id[order[idx]]
    st.progress((idx+1)/len(order),text=f"Card {idx+1} of {len(order)}")
    st.markdown(f'<div class="study-card"><div class="study-label">QUESTION</div><div class="study-question">{esc(current["question"])}</div></div>',unsafe_allow_html=True)
    if st.session_state.show_answer: st.markdown(f'<div class="answer"><b>Answer</b><br>{esc(current["answer"]).replace(chr(10),"<br>")}</div>',unsafe_allow_html=True)
    else: st.caption("Try to recall the answer before revealing it.")
    p,n,q=st.columns([1,1.3,1])
    with p:
        if st.button("← Previous",disabled=len(order)<2,use_container_width=True): st.session_state.card_index=(idx-1)%len(order); st.session_state.show_answer=False; st.rerun()
    with n:
        if st.button("Show answer" if not st.session_state.show_answer else "Hide answer",type="primary",use_container_width=True): st.session_state.show_answer=not st.session_state.show_answer; st.rerun()
    with q:
        if st.button("Next →",disabled=len(order)<2,use_container_width=True): st.session_state.card_index=(idx+1)%len(order); st.session_state.show_answer=False; st.rerun()
    if st.button("🔀 Shuffle deck"):
        random.shuffle(st.session_state.shuffled_ids); st.session_state.card_index=0; st.session_state.show_answer=False; st.rerun()
else: st.info("Your deck is empty. Add a card below to get started.")
st.markdown("### Manage your cards")
add_tab,edit_tab,delete_tab=st.tabs(["＋ Add a card","✎ Edit a card","− Delete a card"])
with add_tab:
    with st.form("add_form",clear_on_submit=True):
        q=st.text_input("Question",placeholder="e.g. What is object-oriented programming?")
        a=st.text_area("Answer",placeholder="Write the answer in your own words.",height=100)
        if st.form_submit_button("Add to deck",type="primary",use_container_width=True):
            if q.strip() and a.strip():
                with connect() as c: c.execute("INSERT INTO cards(question,answer) VALUES (?,?)",(q.strip(),a.strip()))
                st.session_state.card_index=max(0,len(all_cards())-1); st.session_state.show_answer=False; st.success("Card saved."); st.rerun()
            else: st.error("Both question and answer are required.")
with edit_tab:
    cards=all_cards()
    if cards:
        selected=st.selectbox("Choose a card",cards,format_func=lambda r:f'#{r["id"]} · {r["question"][:65]}',key="edit_id")
        with st.form("edit_form"):
            q=st.text_input("Question",value=selected["question"]); a=st.text_area("Answer",value=selected["answer"],height=100)
            if st.form_submit_button("Save changes",type="primary",use_container_width=True):
                if q.strip() and a.strip():
                    with connect() as c: c.execute("UPDATE cards SET question=?,answer=? WHERE id=?",(q.strip(),a.strip(),selected["id"]))
                    st.success("Card updated."); st.rerun()
                else: st.error("Both fields must be filled in.")
    else: st.caption("Add a card first to edit it.")
with delete_tab:
    cards=all_cards()
    if cards:
        selected=st.selectbox("Choose a card to remove",cards,format_func=lambda r:f'#{r["id"]} · {r["question"][:65]}',key="delete_id")
        confirm=st.checkbox("I want to permanently delete this card",key="confirm_delete")
        if st.button("Delete card",type="primary",disabled=not confirm,use_container_width=True):
            with connect() as c: c.execute("DELETE FROM cards WHERE id=?",(selected["id"],))
            st.session_state.show_answer=False; st.success("Card deleted."); st.rerun()
    else: st.caption("There are no cards to delete.")
st.caption("Cards persist in SQLite on the machine hosting the app. Back up flashcards.db if you need a portable copy.")
