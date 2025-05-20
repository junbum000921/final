import subprocess
import requests
import time
import qrcode

# 1. ngrok 실행 (포트 8080으로 로컬 서버 터널링)
ngrok_process = subprocess.Popen(["ngrok", "http", "8080"], stdout=subprocess.DEVNULL)

# 2. ngrok이 실행될 시간을 기다림
time.sleep(3)

# 3. ngrok API에서 터널 주소 가져오기
try:
    tunnel_info = requests.get("http://localhost:4040/api/tunnels").json()
    public_url = tunnel_info['tunnels'][0]['public_url']  # 예: https://abc123.ngrok-free.app
    full_url = public_url + "/camera.html"
    print("✅ 접속 주소:", full_url)

    # 4. QR 코드 생성
    img = qrcode.make(full_url)
    img.save("camera_qr.png")
    print("✅ QR 코드가 'camera_qr.png'로 저장되었습니다.")

except Exception as e:
    print("❌ ngrok 주소를 가져오지 못했습니다:", e)
    ngrok_process.terminate()
