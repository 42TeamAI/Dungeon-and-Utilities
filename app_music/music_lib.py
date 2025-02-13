import streamlit as st
from pygame import mixer
import os

st.title("Галерея композиций")

available = ["mp3", "wav", "aac", "aiff", "dsd", "flac", "mqa", "ogg"]


def select(file_name):
    mixer.music.load(st.session_state["settings"]["music_folder"] + file_name)
    mixer.music.play(-1)

    st.session_state["current_music"] = file_name
    st.session_state["music_is_play"] = True


def pause():
    mixer.music.pause()
    st.session_state["music_is_play"] = False


def play():
    mixer.music.unpause()
    st.session_state["music_is_play"] = True


def unload():
    mixer.music.unload()
    st.session_state["current_music"] = ""
    st.session_state["music_is_play"] = False


def delete(file_name):
    os.remove(st.session_state["settings"]["music_folder"] + file_name)


if "current_music" not in st.session_state:
    st.session_state["current_music"] = ""
    st.session_state["music_is_play"] = False


if st.session_state["current_music"] != "":
    with st.container(border=True):
        st.subheader("Активная мелодия")
        st.write(st.session_state["current_music"].replace(".mp3", ""))

        vol = st.slider("Громкость", 0.0, 1.0, 1.0)

        mixer.music.set_volume(vol)

        col1, col2, col3 = st.columns([1, 1, 1])

        if st.session_state["music_is_play"]:
            st.button("Пауза", on_click=pause)
        else:
            st.button("Продолжить", on_click=play)

        st.button("Убрать с фона", on_click=unload)


st.subheader("Доступные мелодии")
for name in os.listdir(st.session_state["settings"]["music_folder"]):
    if os.path.isfile(st.session_state["settings"]["music_folder"] + name) and name != st.session_state['current_music']:
        extend = name[name.rfind(".") + 1:].lower()
        if extend not in available:
            continue
        with st.container(border=True):
            st.write(name)
            st.audio(st.session_state["settings"]["music_folder"] + name, loop=True)
            st.button("Включить на заднем фоне", key=name, on_click=select, args=[name])
            st.button("Удалить", on_click=delete, args=[name], key=name + "_delete")
