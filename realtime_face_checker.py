import cv2
import mediapipe as mp
import numpy as np
import mysql.connector
import pickle  # pickle 추가
import time
import os

# 얼굴 벡터 생성 함수
def get_face_embedding(image):
    mp_face_mesh = mp.solutions.face_mesh
    with mp_face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1) as face_mesh:
        results = face_mesh.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        if results.multi_face_landmarks:
            landmarks = results.multi_face_landmarks[0]
            coords = [[lm.x, lm.y, lm.z] for lm in landmarks.landmark]
            coords = np.array(coords).flatten()
            # 정규화해서 리턴
            return coords / np.linalg.norm(coords)
    return None

# 코사인 유사도 계산 함수
def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# DB에서 사용자 벡터를 불러오는 함수
def load_user_vectors():
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="famarket",
        password="qpalzm1029!",  # DB 비밀번호
        database="famarket"
    )
    cursor = conn.cursor()
    cursor.execute("SELECT userid, username, uservector FROM datatbl WHERE uservector IS NOT NULL")
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return users

# 메인 얼굴 인식 루프
def main():
    print("🔁 얼굴 인식 대기 중...")

    user_vectors = load_user_vectors()

    while True:
        file_path = "uploads/captured.png"
        if os.path.exists(file_path):
            print("📷 새 이미지 발견, 분석 시작...")
            image = cv2.imread(file_path)
            if image is None:
                print("⚠️ 이미지 로드 실패")
                os.remove(file_path)
                time.sleep(1)
                continue
            
            embedding = get_face_embedding(image)
            os.remove(file_path)

            if embedding is None:
                print("❌ 얼굴 인식 실패")
                time.sleep(1)
                continue

            matched_user = None

            # DB에서 불러온 사용자 벡터 각각을 pickle.loads로 역직렬화해서 비교
            for userid, username, uservector_blob in user_vectors:
                try:
                    # BLOB 데이터를 pickle로 역직렬화
                    uservector_list = pickle.loads(uservector_blob)

                    # uservector_list는 여러 벡터가 있을 수 있음 (리스트)
                    for stored_vector in uservector_list:
                        sim = cosine_similarity(embedding, np.array(stored_vector))
                        if sim > 0.85:
                            matched_user = (userid, username)
                            break
                    if matched_user:
                        break
                except Exception as e:
                    print(f"벡터 역직렬화 실패: {e}")
                    continue

            if matched_user:
                print(f"✅ 로그인 성공: {matched_user[1]}({matched_user[0]}) 님 환영합니다!")
            else:
                print("❌ 일치하는 사용자 없음")

        time.sleep(1)

if __name__ == "__main__":
    main()
