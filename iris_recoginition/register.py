import os
import numpy as np
from scipy.io import savemat
from multiprocessing import freeze_support
from utils.extractandenconding import extractFeature


def register_user(user_id, image_paths, template_dir="templates/users"):
    if len(image_paths) == 0:
        raise ValueError("❌ No image paths provided")

    templates, masks = [], []

    for img in image_paths:
        if not os.path.exists(img):
            print(f"[⚠] File not found: {img}")
            continue

        print(f"[INFO] Processing {img}")
        template, mask, _ = extractFeature(
            img,
            multiprocess=False  # 🔥 Windows safe
        )

        templates.append(template)
        masks.append(mask)

    if len(templates) == 0:
        raise RuntimeError("❌ No valid images processed")

    # 🔐 Bitwise majority voting fusion
    final_template = (np.sum(templates, axis=0) >= len(templates)/2).astype(int)
    final_mask = (np.sum(masks, axis=0) >= len(masks)/2).astype(int)

    os.makedirs(template_dir, exist_ok=True)
    save_path = os.path.join(template_dir, f"{user_id}.mat")

    savemat(save_path, {
        "template": final_template,
        "mask": final_mask
    })

    print(f"[✔] USER {user_id} REGISTERED using {len(templates)} images")


# =====================
# ENTRY POINT
# =====================
if __name__ == "__main__":
    freeze_support()

    # 🔽 EXAMPLE: 2 users × 5 images each
    users = {
        "aditya": [
            "../CASIA1/9/009_1_1.jpg",
            "../CASIA1/9/009_1_2.jpg",
            "../CASIA1/9/009_1_3.jpg",
            "../CASIA1/9/009_2_1.jpg",
            "../CASIA1/9/009_2_3.jpg",
        ]
    }

    for uid, paths in users.items():
        register_user(uid, paths)
