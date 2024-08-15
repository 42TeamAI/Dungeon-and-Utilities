import streamlit as st
from pygame import mixer
from shower import ImageShower
import os
import json
import qrcode
import socket

from img_gen import Text2ImageAPI


def get_local_ip():
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    return local_ip


if "settings" not in st.session_state:
    mixer.init()
    st.session_state["music_generation_show"] = False
    st.session_state["image_generation_show"] = False
    st.session_state["qr_code"] = False
    os.makedirs(".cache", exist_ok=True)
    os.makedirs(".cache/static", exist_ok=True)

    if os.path.isfile("config.json"):
        with open("config.json") as file:
            st.session_state["settings"] = json.load(file)
    else:
        st.session_state["settings"] = {
            "server": "http://95.31.219.22:5000/",
            "music_folder": "assets/music/",
            "image_folder": "assets/images/",
            "port": 8000,
        }

    os.makedirs(st.session_state["settings"]["music_folder"], exist_ok=True)
    os.makedirs(st.session_state["settings"]["image_folder"], exist_ok=True)

    shower = ImageShower()

    st.session_state["web_obj"] = shower
    st.session_state["web_obj"].run(st.session_state["settings"]["port"])

    url = f"http://{get_local_ip()}:{st.session_state['settings']['port']}/"
    img = qrcode.make(url)
    img.save(".cache/qrcode.png")

    st.session_state["img_gen_api"] = Text2ImageAPI('https://api-key.fusionbrain.ai/', "4C598EA5F0D9701B4545C8581A95C7C6",
                                                    'FA482140EB50CBB4ED9CE02D8BE6E804')

pages = {
    "Общее": [
        st.Page("app_main/help.py", title="Помощь"),
        st.Page("app_main/settings.py", title="Настройки")
    ],
    "Музыка": [
        st.Page("app_music/music_create.py", title="Создание новой музыки"),
        st.Page("app_music/music_upload.py", title="Загрузка музыки с устройства"),
        st.Page("app_music/music_lib.py", title="Галерея композиций"),
    ],
    "Изображения": [
        st.Page("app_images/image_create.py", title="Создание новых картинок"),
        st.Page("app_images/image_upload.py", title="Загрузка изображений с устройства"),
        st.Page("app_images/image_gallery.py", title="Галерея картинок"),
    ]
}

app = st.navigation(
    pages
)

app.run()
