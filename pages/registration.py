import streamlit as st
import os
import tempfile

# iris helper
try:
    from iris_recoginition.register import register_user
except ImportError:
    register_user = None


def render():
    """Streamlit page for iris registration storing templates locally."""
    st.title("Iris Registration")

    user_id = st.text_input("Username / ID")
    iris_files = st.file_uploader(
        "Upload Iris Images (min 5)",
        type=["png", "jpg", "jpeg"],
        accept_multiple_files=True,
    )

    if st.button("Register"):
        if not user_id.strip():
            st.warning("Please enter a user ID")
            return
        if not iris_files or len(iris_files) < 5:
            st.warning("Upload at least 5 iris images")
            return
        if register_user is None:
            st.error("Registration module unavailable")
            return

        template_dir = "templates/users"
        os.makedirs(template_dir, exist_ok=True)
        out_path = os.path.join(template_dir, f"{user_id}.mat")
        if os.path.exists(out_path):
            st.warning("User already registered")
            return

        with tempfile.TemporaryDirectory() as tmpdir:
            paths = []
            for idx, f in enumerate(iris_files, start=1):
                p = os.path.join(tmpdir, f"{user_id}_{idx}.jpg")
                with open(p, "wb") as fo:
                    fo.write(f.read())
                paths.append(p)
            register_user(user_id, paths, template_dir=template_dir)

        st.success(f"Registered user '{user_id}' ({len(paths)} images)")
