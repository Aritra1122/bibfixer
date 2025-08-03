# Setup and wait for GROBID (excluding the shell install commands)

import time, requests

def wait_for_grobid(timeout=60):
    url = "http://localhost:8070/api/isalive"
    print("⏳ Waiting for Grobid to start...")
    for _ in range(timeout // 3):
        try:
            if requests.get(url).status_code == 200:
                print("✅ Grobid is ready!")
                return True
        except:
            pass
        time.sleep(3)
    raise RuntimeError("❌ Grobid did not start.")
