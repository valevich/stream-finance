How to add new app

1. Add a new python file in apps/ folder
# apps/new_app.py

import streamlit as st

 # with a function named app.
 def app():
    st.title('New App')


2. Now add it to app.py

from apps import newapp               # import your app modules here

app = MultiApp()

app.add_app("New App", newapp.app)