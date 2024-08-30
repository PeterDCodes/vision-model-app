from ultralytics import YOLO


def model_train():
    model = YOLO('yolov8n.pt') # loading pretrained model
    results = model.train(data = "config.yaml", epochs = 1)

def main():
    model_train()

if __name__ == "__main__":
    model_train()