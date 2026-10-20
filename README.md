# Flashcard Quiz App

A beginner-friendly Streamlit app for studying with question-and-answer flashcards.

## Features
- Show/hide answers
- Previous, next, and shuffle navigation
- Add, edit, and delete cards
- Sample cards included; responsive Streamlit layout

## Run locally
1. Install Python 3.10 or newer.
2. Open a terminal in this folder.
3. Run `pip install -r requirements.txt`.
4. Run `streamlit run app.py`.

Cards are stored in Streamlit session state and reset when the session/app restarts.
## Deploy
On Streamlit Community Cloud, select this repository, set the main file to `app.py`, and deploy.
