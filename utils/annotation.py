import os

base_path = "data/dataset/1280/train"
images_path = os.path.join(base_path, "images")

folder_names = [
    folder
    for folder in os.listdir(images_path)
    if os.path.isdir(os.path.join(images_path, folder))
]

print(f"폴더 갯수 : {len(folder_names)}")

labels_path = os.path.join(base_path, "labels")

for folder_index, folder in enumerate(folder_names):
    label_files = [
        file
        for file in os.listdir(os.path.join(labels_path, folder))
        if file.endswith(".txt")
    ]
    print(f"{folder} 폴더의 라벨 파일 갯수 : {len(label_files)}")

    for label_file in label_files:
        label_file_path = os.path.join(labels_path, folder, label_file)
        with open(label_file_path, "r") as file:
            lines = file.readlines()

        with open(label_file_path, "w") as file:
            for line in lines:
                parts = line.strip().split()
                if parts[0] == "1":
                    parts[0] = str(folder_index + 1)
                file.write(" ".join(parts) + "\n")
