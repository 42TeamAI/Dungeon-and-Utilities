import os
import requests
import streamlit as st

invalid_symbols = ["/", "\\", "|", ":", "*", "?", "“", "<", ">"]
CACHE_FILE = ".cache/download.jpg"


st.title("Создание новой картинки")

st.subheader("Настройки генерации")
description = st.text_input("Описание")
width = st.slider("Ширина", 256, 1024, 1024)
height = st.slider("Высота", 256, 1024, 1024)
btn = st.button("Сгенерировать")

if btn:
    if description == "":
        st.error("Пустое описание")
    else:

        img = st.session_state["img_gen_api"].generate(description, width=width, height=height)
        if img is None:
            st.error("Ошибка генерации изображения")
        else:
            with open(CACHE_FILE, 'wb') as file:
                file.write(img)
            st.session_state["image_generation_show"] = True

if st.session_state["image_generation_show"]:
    st.subheader("Последний несохраненный результат")
    st.image(CACHE_FILE)

    name = st.text_input("Название картинки")
    save = st.button("Сохранить изображение", key="save-image")

    if save:
        if name == "":
            st.error("Пустое название")
        elif any(symbol in name for symbol in invalid_symbols):
            st.error("Некорректные символы в имени, пожалуйста не используйте / \\ | : * ? “ < >")
        else:
            with open(CACHE_FILE, 'rb') as file:
                data = file.read()
            with open(f"{st.session_state['settings']['image_folder']}/{name}.png", "wb") as file:
                file.write(data)

            os.remove(CACHE_FILE)
            st.success("Сохранено")
            st.session_state["image_generation_show"] = False
