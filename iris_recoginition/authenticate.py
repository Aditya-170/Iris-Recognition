import os
import argparse
import scipy.io as sio
from multiprocessing import freeze_support
from utils.extractandenconding import extractFeature, HammingDistance

TEMPLATE_DIR = "templates/users"

def authenticate(user_id, image_path):
    template_path = os.path.join(TEMPLATE_DIR, f"{user_id}.mat")

    if not os.path.exists(template_path):
        return {"status": "User not registered", "score": None}

    print("[🔍] Extracting features...")
    probe_template, probe_mask, _ = extractFeature(
        image_path, multiprocess=False
    )

    data = sio.loadmat(template_path)
    ref_template = data["template"]
    ref_mask = data["mask"]

    score = HammingDistance(
        probe_template, probe_mask,
        ref_template, ref_mask
    )

    print(f"[📏] Hamming Distance: {score:.4f}")

    threshold = 0.37
    if score < threshold:
        return {"status": "Authenticated", "score": score}
    else:
        return {"status": "Access Denied", "score": score}


if __name__ == "__main__":
    freeze_support()

    parser = argparse.ArgumentParser()
    parser.add_argument("--user_id", required=True)
    parser.add_argument("--image", required=True)
    args = parser.parse_args()

    result = authenticate(args.user_id, args.image)
    if result["status"] == "Authenticated":
        print("[✔] AUTHENTICATION SUCCESS")
    elif result["status"] == "Access Denied":
        print("[✘] AUTHENTICATION FAILED")
    else:
        print(f"[❌] {result['status']}")
