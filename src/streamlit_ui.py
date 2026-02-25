import streamlit as st
import os
import io
from utils.extractandenconding import extractFeature, matchingTemplate
from scipy.io import savemat, loadmat
from PIL import Image
import numpy as np

def main():
    st.title("Iris Recognition System")

    st.sidebar.header("Options")
    option = st.sidebar.selectbox("Choose an action:", ["Register", "Login", "About"])

    if option == "Register":
        st.subheader("Register")
        user_id = st.text_input("Enter User ID")
        uploaded_files = st.file_uploader("Upload 5 Images", accept_multiple_files=True, type=["jpg", "jpeg", "png"])

        if st.button("Register"):
            if len(uploaded_files) != 5:
                st.error("Please upload exactly 5 images.")
            elif not user_id:
                st.error("Please provide a User ID.")
            else:
                embeddings_dir = "./embeddings/"
                if not os.path.exists(embeddings_dir):
                    os.makedirs(embeddings_dir)

                user_embeddings = []
                for file in uploaded_files:
                    image = Image.open(io.BytesIO(file.read()))
                    image = image.convert("L")  # Convert to grayscale

                    # Convert PIL image to numpy array for processing
                    image_array = np.array(image)

                    # Save the numpy array as a temporary image file
                    import tempfile
                    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as temp_file:
                        temp_path = temp_file.name
                        Image.fromarray(image_array).save(temp_path)

                    # Use the temporary file path with extractFeature
                    template, mask, _ = extractFeature(temp_path)

                    # Clean up the temporary file
                    os.remove(temp_path)

                    user_embeddings.append((template, mask))

                savemat(os.path.join(embeddings_dir, f"{user_id}.mat"), {"embeddings": user_embeddings})
                st.success("Registration successful! Embeddings saved.")

    elif option == "Login":
        st.subheader("Login")
        user_id = st.text_input("Enter User ID")
        uploaded_file = st.file_uploader("Upload an Image", type=["jpg", "jpeg", "png"])

        if st.button("Login"):
            if not uploaded_file:
                st.error("Please upload an image.")
            elif not user_id:
                st.error("Please provide a User ID.")
            else:
                embeddings_dir = "./embeddings/"
                user_embedding_path = os.path.join(embeddings_dir, f"{user_id}.mat")

                if not os.path.exists(user_embedding_path):
                    st.error("User ID not found. Please register first.")
                else:
                    image = Image.open(io.BytesIO(uploaded_file.read()))
                    image = image.convert("L")  # Convert to grayscale

                    # Convert PIL image to numpy array for processing
                    image_array = np.array(image)

                    # Save the numpy array as a temporary image file
                    import tempfile
                    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as temp_file:
                        temp_path = temp_file.name
                        Image.fromarray(image_array).save(temp_path)

                    # Use the temporary file path with extractFeature
                    template, mask, _ = extractFeature(temp_path)

                    # Clean up the temporary file
                    os.remove(temp_path)

                    # Load stored embeddings from the embeddings directory
                    user_data = loadmat(user_embedding_path)
                    stored_embeddings = user_data["embeddings"]

                    # Use the embeddings directory as the template_dir
                    result = matchingTemplate(template, mask, embeddings_dir, 0.37)

                    if result:
                        st.success("Login successful! Match found.")
                    else:
                        st.error("Login failed. No match found.")

    elif option == "About":
        st.subheader("About")
        st.write("This application is an Iris Recognition System that allows user registration and login using iris recognition.")

if __name__ == "__main__":
    main()