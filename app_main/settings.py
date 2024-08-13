import os
import streamlit as st
import json

st.title("Settings")

server = st.text_input("Server URL", value=st.session_state["settings"]["server"], help="")
music_folder = st.text_input("Name of music folder", value=st.session_state["settings"]["music_folder"])
image_folder = st.text_input("Name of images folder", value=st.session_state["settings"]["image_folder"])
port = st.number_input("Port for showing image", value=st.session_state["settings"]["port"], help="The port on which the application will be launched")

btn = st.button("Save")

if btn:
    if "http" not in server:
        st.error("Please, use full URL to server, example: http://127.0.0.1:8000/")
    else:
        if server[-1] != "/":
            server += "/"

        if music_folder[-1] != "/":
            music_folder += "/"

        if image_folder[-1] != "/":
            image_folder += "/"

        st.session_state["settings"]["server"] = server
        st.session_state["settings"]["music_folder"] = music_folder
        st.session_state["settings"]["image_folder"] = image_folder

        if port != st.session_state["settings"]["port"]:
            st.session_state["settings"]["port"] = port
            st.session_state["web_obj"].run(st.session_state["settings"]["port"])

        os.makedirs(st.session_state["settings"]["music_folder"], exist_ok=True)
        os.makedirs(st.session_state["settings"]["image_folder"], exist_ok=True)

        with open("config.json", 'w') as file:
            json.dump(st.session_state['settings'], file)

        st.success("Saved")

