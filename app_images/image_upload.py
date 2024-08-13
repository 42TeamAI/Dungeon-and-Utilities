import streamlit as st

st.title("Uploading images")
available = ["png", "jpg", "webp", "svg", "jpeg"]

uploader = st.file_uploader(
    "Upload new images",
    type=available,
    accept_multiple_files=True,
)

btn = st.button("Upload")

if btn:
    for upload in uploader:
        data = upload.read()
        with open(st.session_state["settings"]["image_folder"] + upload.name, 'wb') as file:
            file.write(data)
    else:
        if len(uploader) > 0:
            st.success("Files saved" if len(uploader) > 1 else "File saved")
        else:
            st.error("No files selected")
