import os
import streamlit as st
import requests

invalid_symbols = ["/", "\\", "|", ":", "*", "?", "“", "<", ">"]
CACHE_FILE = ".cache/download.mp3"

st.title("Создание новой музыки")

st.subheader("Настройки генерации")

description = st.text_input("Описание ситуации", type="default")
duration = st.slider("Продолжительность мелодии, в секундах", 10, 60, 15)
rephrase = st.checkbox("Извлечь детали из запроса", value=True, help="Мы используем LLM для извлечения большего количества деталей из вашего запроса и создания более качественной мелодии")

if not rephrase:
    st.write("Пожалуйста, вводите описание ситуации на английском, для улучшения генерации, если не хотите использовать данный параметр")

btn = st.button("Сгенерировать")

if btn:
    if description == "":
        st.error("Пустое описание")
    else:
        try:
            resp = requests.post(st.session_state['settings']['server'] + "music/", json={
                "description": description,
                "duration": duration,
                "rephrase": rephrase,
            })
        except requests.exceptions.ConnectionError:
            st.error(
                "Сервер не ответил на запрос, пожалуйста, убедитесь, что указанный в Настройках адрес верен"
            )
        else:
            if resp.status_code == 200:
                with open(CACHE_FILE, 'wb') as file:
                    file.write(resp.content)
                st.session_state["music_generation_show"] = True
            elif resp.status_code == 501:
                st.error("Ключ OpenAI закончился или отсутствует")
            else:
                st.error("Сервер прислал не валидный ответ")


if st.session_state['music_generation_show']:

    st.subheader("Последний несохраненный результат")
    st.audio(CACHE_FILE)

    name = st.text_input("Название мелодии")
    save = st.button("Сохранить мелодию")

    if save:
        if name == "":
            st.error("Пустое название")
        elif any(symbol in name for symbol in invalid_symbols):
            st.error("Некорректные символы в имени, пожалуйста не используйте / \\ | : * ? “ < >")
        else:
            with open(CACHE_FILE, 'rb') as file:
                data = file.read()
            with open(f"{st.session_state['settings']['music_folder']}/{name}.mp3", "wb") as file:
                file.write(data)

            os.remove(CACHE_FILE)
            st.success("Сохранено")
            st.session_state['music_generation_show'] = False
