import glfw
import sys
from OpenGL.GL import *
from OpenGL.GLU import *
import time
import math


halfsize_x, halfsize_y = 100, 100
end_input = False
frame = [(0, 0, 0)] * (4 * halfsize_x * halfsize_y)
pos = []


def draw_line(first_pos, second_pos):
    if first_pos[0] > second_pos[0]:
        first_pos, second_pos = second_pos, first_pos
    if first_pos[0] == second_pos[0]:
        i = min(first_pos[1], second_pos[1])
        while i <= max(first_pos[1], second_pos[1]):
            frame[int(first_pos[0] + 2 * halfsize_x * (2 * halfsize_x - i))] = (255, 255, 0)
            i += 1
    else:
        delta = ((second_pos[0] - first_pos[0]), (second_pos[1] - first_pos[1]))

        cur_int = 0.5
        # y reverse octants
        if 0 <= delta[1] <= delta[0]:  # 1 oct
            e = -delta[0]
            de = 2 * delta[1]
            pos_x, pos_y = first_pos[0], first_pos[1]
            while pos_x <= second_pos[0]:
                frame[int(pos_x + 2 * halfsize_x * (2 * halfsize_x - pos_y))] = (255, 255, 0)
                e += de
                pos_x += 1
                if e >= 0:
                    pos_y += 1
                    e -= 2 * delta[0]
                cur_int = (e + 2 * delta[0]) / (2 * delta[0])
                if frame[int(pos_x + 2 * halfsize_x * (2 * halfsize_x - pos_y - 1))][0] < int(255 * cur_int):
                    frame[int(pos_x + 2 * halfsize_x * (2 * halfsize_x - pos_y - 1))] = (int(255 * cur_int),
                                                                                         int(255 * cur_int), 0)
                if frame[int(pos_x + 2 * halfsize_x * (2 * halfsize_x - pos_y + 1))][0] < int(255 * (1 - cur_int)):
                    frame[int(pos_x + 2 * halfsize_x * (2 * halfsize_x - pos_y + 1))] = (int(255 * (1 - cur_int)),
                                                                                         int(255 * (1 - cur_int)), 0)

        elif delta[1] > delta[0]:  # 2 oct
            delta_intensity = math.fabs(delta[0] / delta[1])
            e = -delta[1]
            de = 2 * delta[0]
            pos_x, pos_y = first_pos[0], first_pos[1]
            while pos_y <= second_pos[1]:
                frame[int(pos_x + 2 * halfsize_x * (2 * halfsize_x - pos_y))] = (255, 255, 0)
                e += de
                pos_y += 1
                if e >= 0:
                    pos_x += 1
                    e -= 2 * delta[1]
                cur_int = (e + 2 * delta[1]) / (2 * delta[1])
                if frame[int(pos_x + 1 + 2 * halfsize_x * (2 * halfsize_x - pos_y))][0] < int(255 * cur_int):
                    frame[int(pos_x + 1 + 2 * halfsize_x * (2 * halfsize_x - pos_y))] = (int(255 * cur_int),
                                                                                         int(255 * cur_int), 0)
                if frame[int(pos_x - 1 + 2 * halfsize_x * (2 * halfsize_x - pos_y))][0] < int(255 * (1 - cur_int)):
                    frame[int(pos_x - 1 + 2 * halfsize_x * (2 * halfsize_x - pos_y))] = (int(255 * (1 - cur_int)),
                                                                                         int(255 * (1 - cur_int)), 0)
        elif 0 > delta[1] >= -delta[0]:  # 8 oct
            delta_intensity = math.fabs(delta[1] / delta[0])
            e = -delta[0]
            de = 2 * delta[1]
            pos_x, pos_y = first_pos[0], first_pos[1]
            while pos_x <= second_pos[0]:
                frame[int(pos_x + 2 * halfsize_x * (2 * halfsize_x - pos_y))] = (255, 255, 0)
                e -= de
                pos_x += 1
                if e >= 0:
                    pos_y -= 1
                    e -= 2 * delta[0]
                cur_int = (e + 2 * delta[0]) / (2 * delta[0])
                if frame[int(pos_x + 2 * halfsize_x * (2 * halfsize_x - pos_y + 1))][0] < int(255 * cur_int):
                    frame[int(pos_x + 2 * halfsize_x * (2 * halfsize_x - pos_y + 1))] = (int(255 * cur_int),
                                                                                         int(255 * cur_int), 0)
                if frame[int(pos_x + 2 * halfsize_x * (2 * halfsize_x - pos_y - 1))][0] < int(255 * (1 - cur_int)):
                    frame[int(pos_x + 2 * halfsize_x * (2 * halfsize_x - pos_y - 1))] = (int(255 * (1 - cur_int)),
                                                                                         int(255 * (1 - cur_int)), 0)

        elif delta[1] < - delta[0]:  # 7 oct
            delta_intensity = math.fabs(delta[0] / delta[1])
            e = delta[1]
            de = 2 * delta[0]
            pos_x, pos_y = first_pos[0], first_pos[1]
            while pos_y >= second_pos[1]:
                frame[int(pos_x + 2 * halfsize_x * (2 * halfsize_x - pos_y))] = (255, 255, 0)
                e += de
                pos_y -= 1
                if e >= 0:
                    pos_x += 1
                    e += 2 * delta[1]
                cur_int = (e - 2 * delta[1]) / (-2 * delta[1])
                if frame[int(pos_x + 1 + 2 * halfsize_x * (2 * halfsize_x - pos_y))][0] < int(255 * cur_int):
                    frame[int(pos_x + 1 + 2 * halfsize_x * (2 * halfsize_x - pos_y))] = (int(255 * cur_int),
                                                                                         int(255 * cur_int), 0)
                if frame[int(pos_x - 1 + 2 * halfsize_x * (2 * halfsize_x - pos_y))][0] < int(255 * (1 - cur_int)):
                    frame[int(pos_x - 1 + 2 * halfsize_x * (2 * halfsize_x - pos_y))] = (int(255 * (1 - cur_int)),
                                                                                         int(255 * (1 - cur_int)), 0)
                    

def button_press(window, key, scancode, action, mods):
    global end_input
    if chr(key) == 'F' and action == 1:
        end_input = not end_input
        if len(pos) >= 3:
            draw_line(pos[0], pos[len(pos) - 1])


def click_mouse(window, button, action, mods):
    global pos
    if button == 0 and action == 1 and not end_input:
        pos.append(glfw.get_cursor_pos(window))
        if len(pos) == 1:
            draw_line(pos[0], pos[0])
        if len(pos) >= 2:
            draw_line(pos[len(pos) - 2], pos[len(pos) - 1])


def main():
    if not glfw.init():
        return
    window = glfw.create_window(2 * halfsize_x, 2 * halfsize_y, "Hello World", None, None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glfw.set_mouse_button_callback(window, click_mouse)
    glfw.set_key_callback(window, button_press)
    glClearColor(0.3, 0.3, 0.3, 1)

    def func():
        glEnableClientState(GL_VERTEX_ARRAY)
        glDrawPixels(2 * halfsize_x, 2 * halfsize_y, GL_RGB, GL_UNSIGNED_BYTE, frame)


    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        func()

        glfw.swap_buffers(window)
        glfw.poll_events()
        # time.sleep(0.01)



    glfw.destroy_window(window)
    glfw.terminate()

if __name__ == "__main__":
    main()