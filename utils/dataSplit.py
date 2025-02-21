import os
import shutil
import random
from glob import glob

# 1. 경로 설정
BASE_PATH = "data/dataset/val"
IMAGES_PATH = os.path.join(BASE_PATH, "images")
LABELS_PATH = os.path.join(BASE_PATH, "labels")

TRAIN_IMAGES = "dataset/train/imgs"
TRAIN_LABELS = "dataset/train/lbs"
VAL_IMAGES = "dataset/val/imgs"
VAL_LABELS = "dataset/val/lbs"

# 2. 폴더 생성
os.makedirs(TRAIN_IMAGES, exist_ok=True)
os.makedirs(TRAIN_LABELS, exist_ok=True)
os.makedirs(VAL_IMAGES, exist_ok=True)
os.makedirs(VAL_LABELS, exist_ok=True)

# 3. 모든 이미지 파일 찾기 (jpg와 jpeg 포함)
image_files = glob(f"{IMAGES_PATH}/**/*.jpg", recursive=True) + glob(
    f"{IMAGES_PATH}/**/*.jpeg", recursive=True
)

# 4. 라벨 파일 찾기
label_files = {
    os.path.basename(f).replace(".txt", ""): f
    for f in glob(f"{LABELS_PATH}/**/*.txt", recursive=True)
}

# 5. 이미지 리스트를 8:2로 분할
random.shuffle(image_files)
split_index = int(0.8 * len(image_files))
train_files = image_files[:split_index]
val_files = image_files[split_index:]

error_list = []


# 6. 파일 이동 함수
def move_files(files, dest_img_dir, dest_lbl_dir):
    i = 1
    error = 1
    for img_path in files:
        # 파일 이름 추출 (확장자 제외)
        file_name = os.path.splitext(os.path.basename(img_path))[0]

        # 이미지 파일 이동
        shutil.copy(img_path, dest_img_dir)

        # 해당 이미지의 라벨 파일 경로
        label_path = label_files.get(file_name)

        # 라벨 파일이 있을 경우 이동
        if label_path and os.path.exists(label_path):
            shutil.copy(label_path, dest_lbl_dir)
            print(f"진행률: {i / len(files) * 100:.2f}%")
            i += 1
        else:
            print(f"Warning: {file_name}.txt 라벨 파일이 없습니다.")
            print(f"진행률: {i / len(files) * 100:.2f}%")
            error_list.append(file_name)
            error += 1


# 7. Train과 Val 데이터 분할 및 이동
move_files(train_files, TRAIN_IMAGES, TRAIN_LABELS)
move_files(val_files, VAL_IMAGES, VAL_LABELS)

print("데이터 분할 완료!")
print(f"오류 목록: {error_list}")
