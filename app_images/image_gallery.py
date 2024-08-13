import streamlit as st
import os
import socket


def get_local_ip():
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    return local_ip


available = ["png", "jpg", "webp", "svg", "jpeg"]

st.title("Images gallery")
st.write(f"If your players are connected to the same network with you, ask them to go to the address http://{get_local_ip()}:{st.session_state['settings']['port']}/ so that they can see the images that you show.")


st.session_state["width"] = 400
width = st.slider("Images width", 100, 1000,  st.session_state["width"])


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
            if st.button("Show to players", key=name, on_click=show, args=[name]):
                st.success("Showed")
            st.button("Delete", on_click=delete, args=[name], key=name+"_delete")