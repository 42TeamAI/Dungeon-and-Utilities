import streamlit as st

st.title("Загрузка музыкальных файлов")
available = ["mp3", "wav", "aac", "aiff", "dsd", "flac", "mqa", "ogg"]

uploader = st.file_uploader(
    "Загрузить файлы",
    type=available,
    accept_multiple_files=True,
)

btn = st.button("Загрузить")

if btn:
    for upload in uploader:
        data = upload.read()
        with open(st.session_state["settings"]["music_folder"] + upload.name, 'wb') as file:
            file.write(data)
    else:
        if len(uploader) > 0:
            st.success("Файлы сохранены" if len(uploader) > 1 else "Файл сохранен")
        else:
            st.error("Ни одного файла не выбрано")
