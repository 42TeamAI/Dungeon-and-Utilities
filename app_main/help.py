import streamlit as st

st.title("Help page")
st.write("Hello, this is a reference guide for the functions of this application.")

st.header("Start play")
st.write("""
In order to start using all the features of the program, you need to run DMHelperServer on any available computer (you can on the same computer where this application is running). After that, please enter the message that the server wrote to you in the "Server URL" field in the Settings section of this application.  
Also in the Settings section, you can configure folders where created or uploaded images and music will be saved.
""")
