import os
import streamlit as st
import json
import socket
import qrcode


def get_local_ip():
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    return local_ip


st.title("Настройки")

server = st.text_input("URL сервера", value=st.session_state["settings"]["server"], help="")
music_folder = st.text_input("Название папки для музыки", value=st.session_state["settings"]["music_folder"])
image_folder = st.text_input("Название папки для картинок", value=st.session_state["settings"]["image_folder"])
port = st.number_input("Порт, на котором будут показываться картинки игрокам", value=st.session_state["settings"]["port"], help="The port on which the application will be launched")

btn = st.button("Сохранить")

if btn:
    if "http" not in server:
        st.error("Пожалуйста, используйте полный URL, например: http://127.0.0.1:8000/")
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

        url = f"http://{get_local_ip()}:{st.session_state['settings']['port']}/"
        img = qrcode.make(url)
        img.save(".cache/qrcode.png")

        st.success("Сохранено")

