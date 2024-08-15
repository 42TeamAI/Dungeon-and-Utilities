import os
import requests
import streamlit as st

invalid_symbols = ["/", "\\", "|", ":", "*", "?", "“", "<", ">"]
CACHE_FILE = ".cache/download.png"


st.title("Создание новой картинки")

st.subheader("Настройки генерации")
description = st.text_input("Описание")
btn = st.button("Сгенерировать")

if btn:
    if description == "":
        st.error("Пустое описание")
    else:
        try:
            resp = requests.post(st.session_state['settings']['server'] + "image/", json={
                "description": description,
            })
        except requests.exceptions.ConnectionError:
            st.error(
                "The server did not respond to the request, please make sure that you entered the correct address in the Settings"
            )
        else:
            if resp.status_code == 200:
                with open(CACHE_FILE, 'wb') as file:
                    file.write(resp.content)
                st.session_state["image_generation_show"] = True
            else:
                st.error("Failed to get information from the server")


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
