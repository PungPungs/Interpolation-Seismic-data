from OpenGL.GL import *
from OpenGL.GLUT import *
import struct




width, height = 256,256
from OpenGL.GL import *
from OpenGL.GLUT import *
import numpy as np

def load_binary_2d_array():
    with open(r"C:\dev\Code\Interpolation-Seismic-data\SB_M2511_03_Test_Header.sgy", "rb") as f:
        f.seek(3600 + 240 - 1)
        raw = f.read(11168)
        data = np.frombuffer(raw, np.float32)

        max_val = np.max(np.abs(data)) or 1.0
        normalized = ((data/max_val + 1) * 127.5).astype(np.uint8)
        image_bytes = normalized.tobytes()
        glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
        glutInitWindowSize(width, height)
        glutCreateWindow(b"2D Image Viewer (OpenGL)")
        glClearColor(0.0, 0.0, 0.0, 1)
        glutDisplayFunc(display)
        glutMainLoop()

        return image_bytes

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glPixelZoom(1.0, -1.0)  # 위아래 반전 방지 (선택적)
    glRasterPos2f(-1, 1)    # 좌측 상단 시작점
    glDrawPixels(width, height, GL_LUMINANCE, GL_UNSIGNED_BYTE, load_binary_2d_array)
    glFlush()

def show_image():
    glutInit()
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutInitWindowSize(width, height)
    glutCreateWindow(b"2D Image Viewer (OpenGL)")
    glClearColor(0.0, 0.0, 0.0, 1)
    glutDisplayFunc(display)
    glutMainLoop()
# 가상 예제 데이터: 256x256 float 진폭값
width, height = 256, 256

# 이진 파일에서 float32 값을 읽어서 2D 배열로 해석


if __name__ == "__main__":
    show_image()
