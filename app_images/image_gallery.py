import streamlit as st
import os
import socket


def get_local_ip():
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    return local_ip


available = ["png", "jpg", "webp", "svg", "jpeg"]

st.title("Галерея изображений")
st.write(f"Если вы и ваши игроки подключены к одной локальной сети, попросите их перейти по адресу http://{get_local_ip()}:{st.session_state['settings']['port']}/ или отсканировать QR-код ниже, чтобы они могли видеть картинки, которые вы показываете")


def qr():
    st.session_state["qr_code"] = not st.session_state["qr_code"]


qr_btn = st.button("Скрыть QR-код" if st.session_state["qr_code"] else "Показать QR-код", on_click=qr)
if st.session_state["qr_code"]:
    st.image(".cache/qrcode.png")

st.session_state["width"] = 400
width = st.slider("Ширина изображений", 100, 1000,  st.session_state["width"])


def show(file_name):
    with open(st.session_state["settings"]["image_folder"] + file_name, 'rb') as file:
        data = file.read()
    to_delete = []
    for name in os.listdir(".cache/static/"):
        if "img" in name:
            to_delete.append(name)
    for name in to_delete:
        os.remove(".cache/static/"+name)
    extend = file_name[file_name.rfind("."):]
    with open(".cache/static/img" + extend, 'wb') as file:
        file.write(data)


def delete(file_name):
    os.remove(st.session_state["settings"]["image_folder"] + file_name)


for name in os.listdir(st.session_state["settings"]["image_folder"]):
    if os.path.isfile(st.session_state["settings"]["image_folder"] + name):
        extend = name[name.rfind(".") + 1:].lower()
        if extend not in available:
            continue
        with st.container(border=True):
            st.image(st.session_state["settings"]["image_folder"] + name, width=width)
            if st.button("Показать игрокам", key=name, on_click=show, args=[name]):
                st.success("Показано")
            st.button("Удалить", on_click=delete, args=[name], key=name+"_delete")