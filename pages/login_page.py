import streamlit as st
import os
import scipy.io as sio

from iris_recoginition.authenticate import authenticate


def render():
    """Streamlit page for iris verification using stored templates."""
    st.title("Iris Verification")

    user_id = st.text_input("Username / ID")
    iris_file = st.file_uploader("Upload Iris Image", type=["png", "jpg", "jpeg"])

    if st.button("Verify"):
        if not user_id.strip():
            st.warning("Please enter a User ID")
            return
        if iris_file is None:
            st.warning("Please upload an iris image")
            return

        # write temporary image for processing
        temp_path = os.path.join(os.path.expanduser("~"), ".iris_verify_temp.jpg")
        with open(temp_path, "wb") as f:
            f.write(iris_file.read())

        try:
            result = authenticate(user_id, temp_path)
        except Exception as e:
            st.error(f"Authentication failed: {e}")
            return

        st.write(f"Hamming Distance: {result['score']:.4f}")

        if result["status"] == "Authenticated":
            st.success("Verification successful")
        elif result["status"] == "Access Denied":
            st.error("Verification failed")
        else:
            st.error(result["status"])
