import os
import streamlit as st
import requests

invalid_symbols = ["/", "\\", "|", ":", "*", "?", "“", "<", ">"]
CACHE_FILE = ".cache/download.mp3"

st.title("Create new music")

st.subheader("Generation settings")

description = st.text_input("Situation description", type="default")
duration = st.slider("Duration of composition, in seconds", 10, 60, 15)
rephrase = st.checkbox("Rephrase yor description?", value=True, help="We use LLM to instruct more details from your description")

btn = st.button("Send")

if btn:
    if description == "":
        st.error("Empty description")
    else:
        try:
            resp = requests.post(st.session_state['settings']['server'] + "music/", json={
                "description": description,
                "duration": duration,
                "rephrase": rephrase,
            })
        except requests.exceptions.ConnectionError:
            st.error(
                "The server did not respond to the request, please make sure that you entered the correct address in the Settings"
            )
        else:
            print(resp.status_code)
            if resp.status_code == 200:
                with open(CACHE_FILE, 'wb') as file:
                    file.write(resp.content)
                st.session_state["music_generation_show"] = True
            else:
                st.error("Failed to get information from the server")


if st.session_state['music_generation_show']:

    st.subheader("Last unsaved result")
    st.audio(CACHE_FILE)

    name = st.text_input("Composition name")
    save = st.button("Save composition")

    if save:
        if name == "":
            st.error("Please, enter the name for composition")
        elif any(symbol in name for symbol in invalid_symbols):
            st.error("Invalid symbols, please don`t use / \\ | : * ? “ < > in name")
        else:
            with open(CACHE_FILE, 'rb') as file:
                data = file.read()
            with open(f"{st.session_state['settings']['music_folder']}/{name}.mp3", "wb") as file:
                file.write(data)

            os.remove(CACHE_FILE)
            st.success("Saved")
            st.session_state['music_generation_show'] = False
