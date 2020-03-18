import glfw
import sys
from OpenGL.GL import *
from OpenGL.GLU import *
import time


def rotate(window, key, scancode, action, mods):
    if key == 70:
        glRotatef(1, 0, 0, 1)

def rotate_mouse(window, xpos, ypos):
    if xpos > 200:
        glRotatef(1, 0, 0, 1)

def main():
    if not glfw.init():
        return
    window = glfw.create_window(600, 600, "Hello World", None, None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glfw.set_key_callback(window, rotate)
    glfw.set_cursor_pos_callback(window, rotate_mouse)
    vertices = [-0.5, -0.5, 0.0,
                0.5, -0.5, 0.0,
                0.5, 0.5, 0.0,
                -0.5, 0.5, 0.0]
    colors = [1, 0, 0,
              0, 1, 0,
              0, 0, 1,
              0.2, 0, 0.2]


    # glEnableClientState(GL_VERTEX_ARRAY)
    # glVertexPointer(3, GL_FLOAT, 0, vertices)
    # glEnableClientState(GL_COLOR_ARRAY)
    # glColorPointer(3, GL_FLOAT, 0, colors)


    glClearColor(0, 0.15, 0.3, 1)

    def func():
        glClear(GL_COLOR_BUFFER_BIT)
        # glDrawArrays(GL_QUADS, 0, 4)
        glBegin(GL_TRIANGLES)
        glColor3f(1, 0, 0)
        glVertex3f(0, 0, 0.5)
        glVertex3f(0.5, 0, 0)
        glVertex3f(0, 0.5, 0)
        glEnd()

        glfw.swap_buffers(window)
        glfw.poll_events()
    # t = time.time()
    while not glfw.window_should_close(window):
        func()

        time.sleep(0.01)
        # nt = time.time()
        # print(1 / (nt - t))
        # t = nt



    glfw.destroy_window(window)
    glfw.terminate()

if __name__ == "__main__":
    main()