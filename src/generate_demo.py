from object_detector import Detector
import cv2

cap = cv2.VideoCapture('../data/videos/2019-06-02.MOV')
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('../data/videos/output.avi', fourcc, 30.0, (1024, 768))
WEIGHT_PATH = '../model/custom_tiny_yolov3.weights'
NETWORK_CONFIG_PATH = '../cfg/custom-tiny.cfg'
OBJECT_CONFIG_PATH = '../cfg/custom.data'
detector = Detector(WEIGHT_PATH, NETWORK_CONFIG_PATH, OBJECT_CONFIG_PATH)

colors = {
    'thief': (255, 0, 0),
    'policeman1': (0, 255, 0),
    'policeman2': (0, 0, 255)
}
font = cv2.FONT_HERSHEY_SIMPLEX
fontScale = 1
lineType = 2
window_name = 'test'
cv2.namedWindow(window_name)
while True:
    ret, frame = cap.read()
    if frame is None:
        break
    else:
        image = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    frame = cv2.resize(frame, (1024, 768))
    object_list = detector.detect_objects(image)
    print(object_list)
    if len(object_list) > 0:
        for key, value in object_list.items():
            height, width = frame.shape[0], frame.shape[1]
            x = value['center'][0] * width
            y = value['center'][1] * height
            size_width = value['size'][0] * width
            size_height = value['size'][1] * height
            x1 = int(x - size_width / 2)
            y1 = int(y - size_height / 2)
            x2 = int(x + size_width / 2)
            y2 = int(y + size_height / 2)
            color = colors[key]
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            cv2.putText(frame, key,
                        (x1 - 10, y1 - 10),
                        font,
                        fontScale,
                        color,
                        lineType)
    cv2.imshow(window_name, frame)
    out.write(frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
out.release()
cap.release()
cv2.destroyWindow(window_name)
