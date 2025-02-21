import os
from PIL import Image, ExifTags
from glob import glob
from multiprocessing import Pool, cpu_count, Manager
from tqdm import tqdm

# 경로 설정
IMAGE_DIR = "data\\dataset\\1280\\train\\images"  # 이미지 폴더 경로

IMG_SIZE = 1280  # 이미지 크기

# 이미지 경로 찾기 (jpg와 jpeg 모두 포함)
image_files = glob(f"{IMAGE_DIR}/**/*.jpg", recursive=True) + glob(
    f"{IMAGE_DIR}/**/*.jpeg", recursive=True
)


# 이미지 리사이즈 함수
def resize_image(args):
    index, image_path, progress_queue = args
    try:
        with Image.open(image_path) as img:
            # 이미지 크기 확인
            if img.size == (IMG_SIZE, IMG_SIZE):
                print(f"이미 {image_path}는 {IMG_SIZE}x{IMG_SIZE}입니다. 건너뜁니다.")
                return

            # EXIF 데이터에서 회전 정보 가져오기
            try:
                for orientation in ExifTags.TAGS.keys():
                    if ExifTags.TAGS[orientation] == "Orientation":
                        break
                exif = img._getexif()
                if exif is not None:
                    orientation = exif.get(orientation)
                    if orientation == 3:
                        img = img.rotate(180, expand=True)
                    elif orientation == 6:
                        img = img.rotate(270, expand=True)
                    elif orientation == 8:
                        img = img.rotate(90, expand=True)
            except (AttributeError, KeyError, IndexError):
                pass

            # 이미지 리사이즈 및 저장 (원본 덮어쓰기)
            img_resized = img.resize((IMG_SIZE, IMG_SIZE))
            img_resized.save(image_path)
    except Exception as e:
        print(f"Error resizing {image_path} at index {index}: {e}")
    finally:
        # 작업 완료 후 큐에 하나의 작업이 완료되었음을 알림
        progress_queue.put(1)


# 멀티프로세싱을 사용하여 이미지 리사이즈 수행
def process_images(image_files):
    manager = Manager()
    progress_queue = manager.Queue()

    # 진행률 바 설정
    with tqdm(total=len(image_files)) as pbar:
        with Pool(processes=cpu_count()) as pool:
            # 각 작업에 인덱스와 진행률 큐 전달
            for _ in pool.imap_unordered(
                resize_image,
                [(i, img, progress_queue) for i, img in enumerate(image_files)],
            ):
                pbar.update(progress_queue.get())


if __name__ == "__main__":
    process_images(image_files)
    print(f"모든 이미지가 {IMG_SIZE}x{IMG_SIZE}으로 리사이즈되었습니다!")
