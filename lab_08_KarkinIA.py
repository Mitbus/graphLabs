import json
import time
import glfw
import os
os.environ['SDL_VIDEO_WINDOW_POS'] = '400,200'
import pygame
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import numpy as np
import pyrr
import math
from PIL import Image


dt = 0
xpos = 0
ypos = 0
zpos = -1
vx = vy = vz = 0
xpos_light = 0
ypos_light = 0
zpos_light = -1
oxtr = oytr = oztr = 0
xscale = yscale = zscale = 1
world_xpos = world_ypos = world_zpos = 0
world_oxtr = world_oytr = world_oztr = 0
world_change = False
scale = 0.05
texmode = False
vertex_height_count = 8  # кол-во эллипсов в единицу t 8
vertex_lenght_count = 16  # общее кол-во вершин(3) 16
t_param = 20  # высота спирали 20
ellipse_param = 2
radius = 5  # радиус спирали
changes = True
vertices = None
move = False
pos0 = [0, 0, 1, 0]
pos1 = [0, 0, 2, 1]
dir1 = [0, 0, -1]
dif_c1 = [1, 1, 0.5, 0]
amb_c0 = [1, 1, 1, 0]
dif_c0 = [0.2, 0.2, 0.2, 0]
box = [(-1, 1), (-1, 1), (-1, 1)]
collider = None
cutoff = 0.95
exp = 1
tex = None
t_sum = 0
t_count = 0


def loadTexture(fileName):
    glEnable(GL_TEXTURE_2D)
    image = Image.open(fileName)
    image = image.transpose(Image.FLIP_TOP_BOTTOM)
    image_data = image.convert("RGBA").tobytes()
    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.width, image.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, image_data)

    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

    glBindTexture(GL_TEXTURE_2D, 0)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)

    return texture


def calc_trang_normal(p1, p2, p3):
    v1 = (p3[0] - p2[0], p3[1] - p2[1], p3[2] - p2[2])
    v2 = (p1[0] - p2[0], p1[1] - p2[1], p1[2] - p2[2])
    return [v1[1] * v2[2] - v1[2] * v2[1], v1[2] * v2[0] - v1[0] * v2[2], v1[0] * v2[1] - v1[1] * v2[0]]


def v3minus(v1, v2):
    return [v1[0] - v2[0], v1[1] - v2[1], v1[2] - v2[2]]


def round3(v, n):
    return [round(v[0], n), round(v[1], n), round(v[2], n)]


def v3mult(v, n):
    return [v[0] * n, v[1] * n, v[2] * n]


def calc():
    def dx_dt(t):
        return -radius * math.sin(t)

    def dy_dt(t):
        return radius * math.cos(t)

    def x(t):
        return radius * math.cos(t)

    def y(t):
        return radius * math.sin(t)

    def z(t):
        return t

    def int_r(num):
        num = int(num + (0.5 if num > 0 else -0.5))
        return num

    ellipse = []
    collider = []
    vert = []
    ind = []
    for t in range(8):
        collider.append(((radius + ellipse_param) / radius * x(t) * scale,
                         (radius + ellipse_param) / radius * y(t) * scale,
                          -scale))
        collider.append(((radius + ellipse_param) / radius * x(t) * scale,
                         (radius + ellipse_param) / radius * y(t) * scale,
                         1 * (t_param + 1) * scale))

    for i in range(vertex_lenght_count):
        ellipse.append(np.array([math.cos(2 * math.pi * i / vertex_lenght_count) * ellipse_param,
                                 math.sin(2 * math.pi * i / vertex_lenght_count), 0]))
    ellipse.append(np.array([ellipse_param, 0, 0]))
    t = 0
    delta_t_param = 1 / vertex_height_count
    align = 0  # параметр выравнивания t по целым числам
    while t <= t_param:
        align += 1
        pos = np.array([x(t), y(t), z(t)])
        cur_pos = list(pos)
        new_z = np.array([dx_dt(t), dy_dt(t), 1])
        new_x = np.array([x(t), y(t), -(x(t) * new_z[0] + y(t) * new_z[1])])
        new_y = np.array([new_x[1] * new_z[2] - new_x[2] * new_z[1], new_x[2] * new_z[0] - new_x[0] * new_z[2],
                          new_x[0] * new_z[1] - new_x[1] * new_z[0]])
        new_z /= np.linalg.norm(new_z)
        new_y /= np.linalg.norm(new_y)
        new_x /= np.linalg.norm(new_x)
        trans_matrix = np.array([[new_x[0], new_y[0], new_z[0]],
                                 [new_x[1], new_y[1], new_z[1]],
                                 [new_x[2], new_y[2], new_z[2]]])
        for i in range(vertex_lenght_count):
            cur_p = list(trans_matrix.dot(ellipse[i]) + pos)
            vert.append(v3mult(cur_p, scale))  # pos
            vert.append([0, 0.5, 1])  # color
            vert.append((t / t_param, i / vertex_lenght_count))  # texture
            vert.append(round3(v3minus(cur_p, cur_pos), 3))  # normal
        t += delta_t_param
        if align == vertex_height_count:
            align = 0
            t = int_r(t)


    for i in range(vertex_height_count * t_param - 1):
        for j in range(vertex_lenght_count):
            j_inc = 0 if j + 1 == vertex_lenght_count else j + 1
            ind.append(i * vertex_lenght_count + j)
            ind.append((i + 1) * vertex_lenght_count + j)
            ind.append((i + 1) * vertex_lenght_count + j_inc)

            ind.append(i * vertex_lenght_count + j)
            ind.append((i + 1) * vertex_lenght_count + j_inc)
            ind.append(i * vertex_lenght_count + j_inc)
    vert = [el for lst in vert for el in lst]
    return vert, ind, collider



def moveevent(key, action):
    global scale, colormode, world_xpos, world_ypos, world_zpos, cutoff, exp,\
        oxtr, oytr, oztr, move, vx, vy, vz, world_oxtr, world_oytr, world_oztr, \
        world_change, xpos, ypos, zpos, texmode, xpos_light, ypos_light, zpos_light
    if key == '1':
        xpos_light += dt
    if key == '2':
        xpos_light -= dt
    if key == '3':
        ypos_light += dt
    if key == '4':
        ypos_light -= dt
    if key == '5':
        zpos_light += dt
    if key == '6':
        zpos_light -= dt
    if key == 'Z':
        cutoff += dt / 10
    if key == 'X':
        cutoff -= dt / 10
    if key == 'C':
        exp += dt
    if key == 'V':
        exp -= dt
    if key == 'Q' and world_change:
        world_xpos += dt
    if key == 'A' and world_change:
        world_xpos -= dt
    if key == 'W' and world_change:
        world_ypos += dt
    if key == 'S' and world_change:
        world_ypos -= dt
    if key == 'E' and world_change:
        world_zpos += dt
    if key == 'D' and world_change:
        world_zpos -= dt
    if key == 'Q' and not world_change:
        xpos += dt
    if key == 'A' and not world_change:
        xpos -= dt
    if key == 'W' and not world_change:
        ypos += dt
    if key == 'S' and not world_change:
        ypos -= dt
    if key == 'E' and not world_change:
        zpos += dt
    if key == 'D' and not world_change:
        zpos -= dt
    if key == 'R' and world_change:
        world_oxtr += dt
    if key == 'F' and world_change:
        world_oxtr -= dt
    if key == 'T' and world_change:
        world_oytr += dt
    if key == 'G' and world_change:
        world_oytr -= dt
    if key == 'Y' and world_change:
        world_oztr += dt
    if key == 'H' and world_change:
        world_oztr -= dt
    if key == 'R' and not world_change:
        oxtr += dt
    if key == 'F' and not world_change:
        oxtr -= dt
    if key == 'T' and not world_change:
        oytr += dt
    if key == 'G' and not world_change:
        oytr -= dt
    if key == 'Y' and not world_change:
        oztr += dt
    if key == 'H' and not world_change:
        oztr -= dt
    if key == 'B' and action == 1:
        move = not move
    if key == 'N' and action == 1:
        world_change = not world_change
    if key == 'U':
        vx += dt
    if key == 'J':
        vx -= dt
    if key == 'I':
        vy += dt
    if key == 'K':
        vy -= dt
    if key == 'O':
        vz += dt
    if key == 'L':
        vz -= dt
    if key == 'M' and action == 1:
        save()
    if key == ',' and action == 1:
        load()
    if key =='.' and action == 1:
        texmode = not texmode
    print(key)
    print('cutoff: ', cutoff, 'exp: ', exp)

    if cutoff > 1:
        cutoff = 1
    if cutoff < 0:
        cutoff = 0
    if exp > 128:
        exp = 128
    if exp < 0:
        exp = 0


def movement():
    if not move:
        return
    global xpos, ypos, zpos, vx, vy, vz
    xpos += vx * dt
    ypos += vy * dt
    zpos += vz * dt
    tr_z = np.array([[math.cos(oztr), -math.sin(oztr), 0],
                    [math.sin(oztr), math.cos(oztr), 0],
                     [0, 0, 1]])
    tr_y = np.array([[math.cos(oytr), 0, -math.sin(oytr)],
                     [0, 1, 0],
                     [math.sin(oytr), 0, math.cos(oytr)]])
    tr_x = np.array([[1, 0, 0],
                     [0, math.cos(oxtr), math.sin(oxtr)],
                     [0, -math.sin(oxtr), math.cos(oxtr)]])
    trans_matrix = tr_z.dot(tr_y.dot(tr_x))
    for c_raw in collider:
        c = list(trans_matrix.dot(c_raw))
        if xpos + c[0] > box[0][1]:
            vx = - math.fabs(vx)
        if xpos + c[0] < box[0][0]:
            vx = math.fabs(vx)
        if ypos + c[1] > box[1][1]:
            vy = - math.fabs(vy)
        if ypos + c[1] < box[1][0]:
            vy = math.fabs(vy)
        if zpos + c[2] > box[2][1]:
            vz = - math.fabs(vz)
        if zpos + c[2] < box[2][0]:
            vz = math.fabs(vz)


def load():
    global xpos, ypos, zpos, vx, vy, vz, oxtr, oytr, oztr, world_xpos, world_ypos, world_zpos, \
        world_oxtr, world_oytr, world_oztr, world_change, move, cutoff, exp
    file = open('data.txt', 'r')
    data = file.read()
    file.close()
    d = json.loads(data)
    xpos, ypos, zpos = d['xpos'], d['ypos'], d['zpos']
    vx, vy, vz = d['vx'], d['vy'], d['vz']
    oxtr, oytr, oztr = d['oxtr'], d['oytr'], d['oztr']
    world_xpos, world_ypos, world_zpos = d['world_xpos'], d['world_ypos'], d['world_zpos']
    world_oxtr, world_oytr, world_oztr = d['world_oxtr'], d['world_oytr'], d['world_oztr']
    world_change = d['world_change']
    move = d['move']
    cutoff = d['cutoff']
    exp = d['exp']


def save():
    print('save')
    data = {
        'xpos': xpos,
        'ypos': ypos,
        'zpos': zpos,
        'vx': vx,
        'vy': vy,
        'vz': vz,
        'oxtr': oxtr,
        'oytr': oytr,
        'oztr': oztr,
        'world_xpos': world_xpos,
        'world_ypos': world_ypos,
        'world_zpos': world_zpos,
        'world_oxtr': world_oxtr,
        'world_oytr': world_oytr,
        'world_oztr': world_oztr,
        'world_change': world_change,
        'move': move,
        'cutoff': cutoff,
        'exp': exp
    }
    file = open('data.txt', 'w')
    file.write(json.dumps(data))
    file.close()


def main(size_x, size_y):
    vertex_src = """
    # version 330
    layout(location = 0) in vec3 a_position;
    layout(location = 1) in vec3 a_color;
    layout(location = 2) in vec2 a_texture;
    layout(location = 3) in vec3 a_normal;
    
    uniform mat4 rotation;
    out vec3 v_color;
    out vec2 v_texture;
    out vec3 v_normal;
    out vec3 v_position;
    void main()
    {
        gl_Position = rotation * vec4(a_position, 1.0);
        v_color = a_color;
        v_texture = a_texture;
        v_position = a_position;
        v_normal = a_normal;
    }
    """

    fragment_src = """
    # version 330
    in vec3 v_color;
    in vec2 v_texture;
    in vec3 v_position;
    in vec3 v_normal;
    out vec4 out_color;
    uniform sampler2D sampler_texture;
    uniform vec3 light_position;
    uniform bool textured;
    uniform vec3 point_light_direction;
    uniform float max_angle;
    uniform float exp;
    void main() {
        vec3 lightDirection = normalize(light_position - v_position);
        vec3 viewDirection = normalize(-v_position);
        vec3 reflectDirection = normalize(-reflect(lightDirection, v_normal));
        vec4 Iamb = vec4(0.1, 0.1, 0.1, 1.0);
        
        float diffuseAngle = max(dot(v_normal, lightDirection), 0.0);
        vec4 Idiff = vec4(0.7, 0.7, 0.7, 1.0) * diffuseAngle;
        Idiff = clamp(Idiff, 0.0, 1.0);
        
        float specularAngle = max(dot(reflectDirection, viewDirection), 0.0);
        vec4 Ispec = vec4(1, 1, 1, 1.0) * pow(specularAngle, 80);
        
        float cur_angle = max(dot(point_light_direction, lightDirection), 0.0);
        if (cur_angle < max_angle) {
            Idiff = vec4(0, 0, 0, 0);
            Ispec = vec4(0, 0, 0, 0);
        } else {
            float intens = pow(cos(cur_angle), exp);
            Idiff = Idiff * intens;
            Ispec = Ispec * intens;
        }
        if (textured) {
            out_color = Ispec + (Iamb + Idiff) 
            * texture(sampler_texture, v_texture) * vec4(v_color, 1.0f);
        } else {
            out_color = Ispec + (Iamb + Idiff);
        }
}
    """

    global vertices, collider, dt

    vertices, indices, collider = calc()
    vertices = np.array(vertices, dtype=np.float32)
    indices = np.array(indices, dtype=np.uint32)

    pygame.init()
    pygame.display.set_mode((size_x, size_y), pygame.OPENGL | pygame.DOUBLEBUF | pygame.RESIZABLE)

    shader = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER),
                            compileShader(fragment_src, GL_FRAGMENT_SHADER))

    # Vertex Buffer Object
    VBO = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

    # Element Buffer Object
    EBO = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

    el_len = 11
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, vertices.itemsize * el_len, ctypes.c_void_p(0))

    glEnableVertexAttribArray(1)
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, vertices.itemsize * el_len, ctypes.c_void_p(12))

    glEnableVertexAttribArray(2)
    glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, vertices.itemsize * el_len, ctypes.c_void_p(24))

    glEnableVertexAttribArray(3)
    glVertexAttribPointer(3, 3, GL_FLOAT, GL_FALSE, vertices.itemsize * el_len, ctypes.c_void_p(32))

    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture)
    # Set the texture wrapping parameters
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    # Set texture filtering parameters
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    image = pygame.image.load('C:/Users/ilya/PycharmProjects/graphLabs/tex.bmp')
    image = pygame.transform.flip(image, False, True)
    image_width, image_height = image.get_rect().size
    img_data = pygame.image.tostring(image, "RGBA")
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image_width, image_height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)

    glUseProgram(shader)
    glClearColor(0, 0.1, 0.1, 1)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    rotation_loc = glGetUniformLocation(shader, "rotation")
    light_pos = glGetUniformLocation(shader, "light_position")
    textured = glGetUniformLocation(shader, "textured")
    shader_exp = glGetUniformLocation(shader, "exp")
    shader_max_angle = glGetUniformLocation(shader, "max_angle")
    shader_point_light_direction = glGetUniformLocation(shader, "point_light_direction")
    running = True
    cur_time = time.time()
    key_down = None
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.VIDEORESIZE:
                glViewport(0, 0, event.w, event.h)
            if event.type == pygame.KEYDOWN:
                key_down = event.unicode
                moveevent(key_down.upper(), 1)
            if event.type == pygame.KEYUP:
                key_down = None
        if key_down is not None:
            moveevent(key_down.upper(), 2)


        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glCallList(3)

        movement()
        rot_x = pyrr.Matrix44.from_x_rotation(oxtr)
        rot_y = pyrr.Matrix44.from_y_rotation(oytr)
        rot_z = pyrr.Matrix44.from_z_rotation(oztr)
        transl = pyrr.Matrix44.from_translation((xpos, ypos, zpos))
        glUniformMatrix4fv(rotation_loc, 1, GL_FALSE, rot_x @ rot_y @ rot_z @ transl)
        glUniform3f(light_pos, xpos_light, ypos_light, zpos_light)
        glUniform1f(textured, texmode)
        glUniform1f(shader_exp, exp)
        glUniform1f(shader_max_angle, cutoff)
        glUniform3f(shader_point_light_direction, 0, 0, -1)

        glDrawElements(GL_TRIANGLES, len(indices), GL_UNSIGNED_INT, None)

        pygame.display.flip()
        new_time = time.time()
        dt = new_time - cur_time
        cur_time = new_time


    pygame.quit()


main(600, 600)
