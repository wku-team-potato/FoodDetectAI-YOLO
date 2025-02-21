from ultralytics import YOLO
# import torch.multiprocessing as mp
import torch
import os

def train_model():
    model = YOLO("yolov8l.pt")
    config_path = "config/data.yaml"

    model.train(
        data=config_path,
        epochs=50,
        batch=16,
        imgsz=640,
        name="food_detect_yolov8l_640",
        patience=10,
        device="cuda" if torch.cuda.is_available() else "cpu",
        workers=4,
        lr0=0.01,
        lrf=0.2,
    )

if __name__ == "__main__":
    # mp.set_start_method("spawn", force=True)
    train_model()
