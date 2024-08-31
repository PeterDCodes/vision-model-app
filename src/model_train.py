from ultralytics import YOLO


def model_train(epochs):
    model = YOLO('yolov8n.pt') # loading pretrained model
    results = model.train(data = "config.yaml", epochs = epochs)

def main():
    model_train()

if __name__ == "__main__":
    model_train()