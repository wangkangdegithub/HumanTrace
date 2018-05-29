import cv2
import numpy as np

camera = cv2.VideoCapture(0)
firstframe = None
while True:
    ret, frame = camera.read()  # 第一个值表示是否成功从缓冲中读取了frame
    if not ret:
        break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (25, 25), 0)  # 应用高斯平滑对一个21*21的区域的像素强度进行平均，这能帮助消除一些高频噪声
    if firstframe is None:  # 视频的第一帧
        firstframe = gray
        continue

    frameDelta = cv2.absdiff(firstframe, gray)  # 计算当前帧和第一帧的不同
    thresh = cv2.threshold(frameDelta, 150, 255, cv2.THRESH_BINARY_INV)[1]

    # 扩展阈值图像填充孔洞，然后找到阈值图像上的轮廓
    thresh = cv2.dilate(thresh, None, iterations=2)
    image, contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for c in contours:

        if cv2.contourArea(c) > 1700 and cv2.contourArea(c) < 1750:
            print(cv2.contourArea(c))
            continue

        x, y, w, h = cv2.boundingRect(c)
        frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
    cv2.imshow("frame", frame)
    cv2.imshow("Thresh", thresh)
    cv2.imshow("frameDelta", frameDelta)
    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()
