import streamlit as st

st.title("Загрузка картинок с устройства")
available = ["png", "jpg", "webp", "svg", "jpeg"]

uploader = st.file_uploader(
    "Загрузить изображения",
    type=available,
    accept_multiple_files=True,
)

btn = st.button("Загрузить")

if btn:
    for upload in uploader:
        data = upload.read()
        with open(st.session_state["settings"]["image_folder"] + upload.name, 'wb') as file:
            file.write(data)
    else:
        if len(uploader) > 0:
            st.success("Файлы сохранены" if len(uploader) > 1 else "Файл сохранен")
        else:
            st.error("Не выбрано ни одного файла")
