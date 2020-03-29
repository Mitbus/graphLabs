import math

import glfw
from OpenGL.GL import *
import time
import numpy as np

dt = 0
xpos = ypos = zpos = 0
oxtr = oytr = oztr = 0
xscale = yscale = zscale = scale = 1
colormode = True
vertex_height_count = 1  # промежуточные вершины + 1
vertex_lenght_count = 3  # общее кол-во вершин
vertex_into_count = 1  # кол-во внутренних эллипсов
changes = True
figure = None
ellipse_param = 2


def moveevent(window, key, scancode, action, mods):
    global xpos, ypos, zpos
    global oztr, oytr, oxtr
    global scale, colormode, xscale, yscale, zscale
    global vertex_height_count, vertex_lenght_count, vertex_into_count, changes
    global ellipse_param
    if chr(key) == 'U':
        xscale += dt
    if chr(key) == 'J':
        xscale -= dt
    if chr(key) == 'I':
        yscale += dt
    if chr(key) == 'K':
        yscale -= dt
    if chr(key) == 'O':
        zscale += dt
    if chr(key) == 'L':
        zscale -= dt

    if chr(key) == 'Z':
        scale += dt
    if chr(key) == 'X':
        scale -= dt
    if chr(key) == 'C' and action == 1:
        colormode = not colormode

    if chr(key) == 'Q':
        ypos += dt
    if chr(key) == 'A':
        ypos -= dt
    if chr(key) == 'W':
        xpos += dt
    if chr(key) == 'S':
        xpos -= dt
    if chr(key) == 'E':
        zpos += dt
    if chr(key) == 'D':
        zpos -= dt

    if chr(key) == 'R':
        oztr += dt
    if chr(key) == 'F':
        oztr -= dt
    if chr(key) == 'T':
        oytr += dt
    if chr(key) == 'G':
        oytr -= dt
    if chr(key) == 'Y':
        oxtr += dt
    if chr(key) == 'H':
        oxtr -= dt

    if chr(key) == '1':
        vertex_height_count += 1
        changes = True
    if chr(key) == '2' and vertex_height_count > 1:
        vertex_height_count -= 1
        changes = True
    if chr(key) == '3':
        vertex_lenght_count += 1
        changes = True
    if chr(key) == '4' and vertex_lenght_count > 3:
        vertex_lenght_count -= 1
        changes = True
    if chr(key) == '5':
        vertex_into_count += 1
        changes = True
    if chr(key) == '6' and vertex_into_count > 1:
        vertex_into_count -= 1
        changes = True
    if chr(key) == 'V':
        ellipse_param += dt
    if chr(key) == 'B':
        ellipse_param -= dt



size_x, size_y = 450, 450


def main():
    global dt
    if not glfw.init():
        return
    window = glfw.create_window(2 * size_x, 2 * size_y, "lab", None, None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glfw.set_key_callback(window, moveevent)

    glClearColor(0.3, 0.3, 0.3, 1)
    glEnable(GL_DEPTH_TEST)

    glLoadIdentity()
    glMultMatrixd([1, 0, 0, 0,  # move back
                   0, 1, 0, 0,
                   0, 0, 1, 0,
                   -0.9, -0.9, 0.2, 1])
    cos45 = math.sqrt(2) / 2
    glMultMatrixd([1, 0, 0, 0,  # ox 45
                   0, cos45, cos45, 0,
                   0, -cos45, cos45, 0,
                   0, 0, 0, 1])
    glMultMatrixd([cos45, cos45, 0, 0,  # oz 45
                   -cos45, cos45, 0, 0,
                   0, 0, 1, 0,
                   0, 0, 0, 1])
    glMultMatrixd([1, 0, 0, 0,  # move to center
                   0, 1, 0, 0,
                   0, 0, 1, 0,
                   0.9, 0.9, -0.2, 1])
    glPushMatrix()

    def calc():
        triangles_poly = []
        triangles_color = []
        quads_poly = []
        quads_color = []
        lines = []
        lines_color = []
        angle = 0
        is_red = True
        while angle < 360:
            next_angle = angle + 360 / vertex_lenght_count
            if next_angle > 360:
                next_angle = 360
            cur_x = math.cos(math.radians(angle)) / vertex_into_count
            cur_y = math.sin(math.radians(angle)) / vertex_into_count
            next_x = math.cos(math.radians(next_angle)) / vertex_into_count
            next_y = math.sin(math.radians(next_angle)) / vertex_into_count
            triangles_color.append((1 if is_red else 0, 0 if is_red else 1, 0))
            triangles_color.append((1 if is_red else 0, 0 if is_red else 1, 0))
            triangles_color.append((0.5, 0.5, 0))
            triangles_color.append((1 if is_red else 0, 0 if is_red else 1, 0))
            triangles_color.append((1 if is_red else 0, 0 if is_red else 1, 0))
            triangles_color.append((0.5, 0.5, 0))
            is_red = not is_red
            triangles_poly.append((cur_x, cur_y, 1))
            triangles_poly.append((0, 0, 1))
            triangles_poly.append((next_x, next_y, 1))
            triangles_poly.append((cur_x, cur_y, -1))
            triangles_poly.append((0, 0, -1))
            triangles_poly.append((next_x, next_y, -1))
            lines.append((0, 0, 1))
            lines.append((cur_x * vertex_into_count, cur_y * vertex_into_count, 1))
            lines.append((cur_x, cur_y, 1))
            lines.append((next_x, next_y, 1))
            lines.append((0, 0, -1))
            lines.append((cur_x * vertex_into_count, cur_y * vertex_into_count, -1))
            lines.append((cur_x, cur_y, -1))
            lines.append((next_x, next_y, -1))
            for j in range(8):
                lines_color.append((0, 0, 1))
            i = 1
            while i < vertex_into_count:
                quads_color.append((1 if is_red else 0, 0 if is_red else 1, 0))
                quads_color.append((1 if is_red else 0, 0 if is_red else 1, 0))
                quads_color.append((0.5, 0.5, 0))
                quads_color.append((0.5, 0.5, 0))
                quads_color.append((1 if is_red else 0, 0 if is_red else 1, 0))
                quads_color.append((1 if is_red else 0, 0 if is_red else 1, 0))
                quads_color.append((0.5, 0.5, 0))
                quads_color.append((0.5, 0.5, 0))
                is_red = not is_red
                quads_poly.append((cur_x * i, cur_y * i, 1))
                quads_poly.append((cur_x * (i + 1), cur_y * (i + 1), 1))
                quads_poly.append((next_x * (i + 1), next_y * (i + 1), 1))
                quads_poly.append((next_x * i, next_y * i, 1))
                quads_poly.append((cur_x * i, cur_y * i, -1))
                quads_poly.append((cur_x * (i + 1), cur_y * (i + 1), -1))
                quads_poly.append((next_x * (i + 1), next_y * (i + 1), -1))
                quads_poly.append((next_x * i, next_y * i, -1))
                lines.append((cur_x * (i + 1), cur_y * (i + 1), 1))
                lines.append((next_x * (i + 1), next_y * (i + 1), 1))
                lines.append((cur_x * (i + 1), cur_y * (i + 1), -1))
                lines.append((next_x * (i + 1), next_y * (i + 1), -1))
                for j in range(4):
                    lines_color.append((0, 0, 1))
                i += 1
            delta_height = 2 / vertex_height_count
            i = 0
            lines.append((cur_x * vertex_into_count, cur_y * vertex_into_count, 1))
            lines.append((cur_x * vertex_into_count, cur_y * vertex_into_count, -1))
            lines_color.append((0, 0, 1))
            lines_color.append((0, 0, 1))
            while i < vertex_height_count:
                lines_color.append((0, 0, 1))
                lines_color.append((0, 0, 1))
                lines.append((cur_x * vertex_into_count, cur_y * vertex_into_count, 1 - delta_height * (i + 1)))
                lines.append((next_x * vertex_into_count, next_y * vertex_into_count, 1 - delta_height * (i + 1)))
                quads_poly.append((cur_x * vertex_into_count, cur_y * vertex_into_count, 1 - delta_height * i))
                quads_poly.append((cur_x * vertex_into_count, cur_y * vertex_into_count, 1 - delta_height * (i + 1)))
                quads_poly.append((next_x * vertex_into_count, next_y * vertex_into_count, 1 - delta_height * (i + 1)))
                quads_poly.append((next_x * vertex_into_count, next_y * vertex_into_count, 1 - delta_height * i))
                quads_color.append((1 if is_red else 0, 0 if is_red else 1, 0))
                quads_color.append((1 if is_red else 0, 0 if is_red else 1, 0))
                quads_color.append((0.5, 0.5, 0))
                quads_color.append((0.5, 0.5, 0))
                is_red = not is_red
                i += 1
            angle = next_angle
        return triangles_poly, quads_poly, lines, triangles_color, quads_color, lines_color

    def mainbox():
        global changes
        global figure
        glMultMatrixd([scale * xscale, 0, 0, 0,  # back center + scale
                       0, scale * yscale, 0, 0,
                       0, 0, scale * zscale, 0,
                       0, 0, 0.5, 1])
        glMultMatrixd([math.cos(oztr), math.sin(oztr), 0, 0,  # z rotate
                       -math.sin(oztr), math.cos(oztr), 0, 0,
                       0, 0, 1, 0,
                       0, 0, 0, 1])
        glMultMatrixd([math.cos(oytr), 0, math.sin(oytr), 0,  # y rotate
                       0, 1, 0, 0,
                       -math.sin(oytr), 0, math.cos(oytr), 0,
                       0, 0, 0, 1])
        glMultMatrixd([1, 0, 0, 0,  # x rotate
                       0, math.cos(oxtr), -math.sin(oxtr), 0,
                       0, math.sin(oxtr), math.cos(oxtr), 0,
                       0, 0, 0, 1])
        glMultMatrixd([1 * ellipse_param, 0, 0, 0,  # move to center + ellipse param
                       0, 1, 0, 0,
                       0, 0, 1, 0,
                       0, 0, -0.5, 1])
        if changes:
            changes = False
            figure = calc()
        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_COLOR_ARRAY)
        if colormode:
            glVertexPointer(3, GL_FLOAT, 0, figure[0])
            glColorPointer(3, GL_FLOAT, 0, figure[3])
            glDrawArrays(GL_TRIANGLES, 0, len(figure[0]))
            glVertexPointer(3, GL_FLOAT, 0, figure[1])
            glColorPointer(3, GL_FLOAT, 0, figure[4])
            glDrawArrays(GL_QUADS, 0, len(figure[1]))
        else:
            glVertexPointer(3, GL_FLOAT, 0, figure[2])
            glColorPointer(3, GL_FLOAT, 0, figure[5])
            glDrawArrays(GL_LINES, 0, len(figure[2]))




    def minibox():
        glPopMatrix()
        glBegin(GL_QUADS)
        glColor3f(0.8, 0.2, 0.2)
        glVertex3f(-0.9, -0.9, 0.2)
        glVertex3f(-0.8, -0.9, 0.2)
        glVertex3f(-0.8, -0.8, 0.2)
        glVertex3f(-0.9, -0.8, 0.2)
        glColor3f(0.2, 0.8, 0.2)
        glVertex3f(-0.9, -0.9, 0.2)
        glVertex3f(-0.9, -0.9, 0.3)
        glVertex3f(-0.9, -0.8, 0.3)
        glVertex3f(-0.9, -0.8, 0.2)
        glColor3f(0.2, 0.2, 0.8)
        glVertex3f(-0.9, -0.9, 0.2)
        glVertex3f(-0.8, -0.9, 0.2)
        glVertex3f(-0.8, -0.9, 0.3)
        glVertex3f(-0.9, -0.9, 0.3)
        glEnd()
        glPushMatrix()

    def ortograph():
        # front view
        glViewport(0, size_y, size_x, size_y)
        glLoadIdentity()
        glMultMatrixd([1, 0, 0, 0,
                       0, 1, 0, 0,
                       0, 0, -1, 0,
                       0, 0, 0, 1])
        mainbox()
        # top view
        glViewport(0, 0, size_x, size_y)
        glLoadIdentity()
        glMultMatrixd([1, 0, 0, 0,
                       0, 0, -1, 0,
                       0, -1, 0, 0,
                       0, 0, 0, 1])
        mainbox()
        # side view
        glViewport(size_x, size_y, size_x, size_y)
        glLoadIdentity()
        glMultMatrixd([0, 0, -1, 0,
                       0, 1, 0, 0,
                       -1, 0, 0, 0,
                       0, 0, 0, 1])
        mainbox()
        # main view
        glViewport(size_x, 0, size_x, size_y)
        glLoadIdentity()
        glMultMatrixd([0.87, 0, 1, 0.5,  # double point perspective
                       0, 1, 0, 0,
                       0.5, 0, -1.73, -0.87,
                       0, 0, 1, 2])
        glMultMatrixd([1, 0, 0, 0,
                       0, 1, 0, 0,
                       0, 0, 1, 0,
                       xpos, ypos, zpos, 1])
        mainbox()

    cur_time = time.time()
    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        ortograph()
        minibox()
        glfw.swap_buffers(window)
        glfw.poll_events()
        new_time = time.time()
        dt = new_time - cur_time
        print(1 / dt)
        cur_time = new_time
        time.sleep(0.01 if dt < 0.005 else 0)

    glfw.destroy_window(window)
    glfw.terminate()


if __name__ == "__main__":
    main()
