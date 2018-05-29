import cv2
import urllib.request
import numpy as np
import sys

host = "172.16.11.245:8080"  # 在这里记得修改ＩＰ，否则是无法调用的，刚刚浏览器输入的地址
if len(sys.argv) > 1:
    host = sys.argv[1]
hoststr = 'http://' + host + '/?action=stream'
print('Streaming ' + hoststr)

print('Print Esc to quit')
stream = urllib.request.urlopen(hoststr)
bytes = ''
while True:
    bytes += stream.read(1024).decode("ascii")
    a = bytes.find('\xff\xd8')
    b = bytes.find('\xff\xd9')
    if a != -1 and b != -1:
        jpg = bytes[a:b + 2]
        bytes = bytes[b + 2:]
        # flags = 1 for color image
        i = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), flags=1)
        # print i.shape
        cv2.imshow("xiaorun", i)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            exit(0)
