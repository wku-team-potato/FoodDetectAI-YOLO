import torch
import cv2
from ultralytics import YOLO

# 모델 로드 (경로 수정)
model_path = "runs/detect/food_detect_yolov8n5/weights/best.pt"
model = YOLO(model_path)

# 테스트할 이미지 파일 (경로 수정)
image_path = "imgs/6.jpg"

# 이미지 로드 및 모델 실행
results = model(image_path)

for r in results:
    im_array = r.plot()
    cv2.imshow("Food Detection", im_array)  # 결과 이미지 출력
    cv2.imwrite("output_detected.jpg", im_array)  # 탐지된 결과 저장

    print("Detected Boxes (xyxy):", r.boxes.xyxy.numpy())  # 바운딩 박스 좌표
    print("Confidence Scores:", r.boxes.conf.numpy())  # 신뢰도 점수
    print("Class IDs:", r.boxes.cls.numpy())  # 클래스 ID

cv2.waitKey(0)
cv2.destroyAllWindows()
