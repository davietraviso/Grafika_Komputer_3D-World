import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import numpy as np
from TextureLoader import load_texture
from pipeline_shader_VAO import shader_function # Ini untuk import file shader
import pyrr
from PIL import Image
from camera_WASD import Camera
left, right, forward, backward, up, down = False, False, False, False, False, False


# instance buat kamera
cam = Camera()
WIDTH, HEIGHT = 1280, 720
lastX, lastY = WIDTH / 2, HEIGHT / 2
first_mouse = True

# Keyboard callback funciton ESC
def key_input_clb(window, key, scancode, action, mode):
     global left, right, forward, backward, up, down
     if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
          glfw.set_window_should_close(window, True)

     if key == glfw.KEY_W and action == glfw.PRESS:
          forward = True

     if key == glfw.KEY_S and action == glfw.PRESS:
          backward = True

     if key == glfw.KEY_A and action == glfw.PRESS:
          left = True
          
     if key == glfw.KEY_D and action == glfw.PRESS:
          right = True

     if key == glfw.KEY_Z and action == glfw.PRESS:
          up = True

     if key == glfw.KEY_X and action == glfw.PRESS:
          down = True
          
     if key in [glfw.KEY_W, glfw.KEY_S, glfw.KEY_D, glfw.KEY_A, glfw.KEY_Z, glfw.KEY_X] and action == glfw.RELEASE:
          left, right, forward, backward, up, down = False, False, False, False, False, False

# keyboard movement
def do_movement():
     if left:
          cam.process_keyboard("LEFT", 0.005)
     if right:
          cam.process_keyboard("RIGHT", 0.005)
     if forward:
          cam.process_keyboard("FORWARD", 0.005)
     if backward:
          cam.process_keyboard("BACKWARD", 0.005)
     if up:
          cam.process_keyboard("UP", 0.005)
     if down:
          cam.process_keyboard("DOWN", 0.005)

# CALL BACK FOR THE MOUSE look callback?
def mouse_look_clb(window, xpos, ypos):
    global first_mouse, lastX, lastY

    if first_mouse:
        lastX = xpos
        lastY = ypos
        first_mouse = False

    xoffset = xpos - lastX
    yoffset = lastY - ypos

    lastX = xpos
    lastY = ypos
    
    cam.process_mouse_movement(xoffset, yoffset)


# Ini untuk define isi dari fungsi file shader
vertex_src, fragmen_src = shader_function()

#Here for resize file window
def window_resize(window, width, height):
    glViewport(0, 0, width, height)
    projection = pyrr.matrix44.create_perspective_projection_matrix(45, width / height, 0.1, 100)
    glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)

# initializing the glfw library
if not glfw.init():
    raise Exception("glfw can not be initialized woy!")

# For creating da windows
# UPDATED FOR SUPPORTING DA CAMERA
window = glfw.create_window(WIDTH, HEIGHT, "Media Pelunas MK Grakom, bismillah lulus", None, None)

# For checking whether the window has created or nah
if not window:
        glfw.terminate()
        raise Exception("glfw gak bisa dibuat weh!")

# For setting da windows position
glfw.set_window_pos(window, 150, 100)

# For calling the rezise capability
glfw.set_window_size_callback(window, window_resize)

# For calling the mouse callback
glfw.set_cursor_pos_callback(window, mouse_look_clb)
# glfw.set_cursor_enter_callback(window, mouse_enter_clb)
glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)
glfw.set_key_callback(window, key_input_clb)

# For make the context current
glfw.make_context_current(window)

## -- Triangle starts here
# First three are vertices coordinate
# Second last is color rgb

             
#Depan, Belakang, Kanan, Kiri, Bawah, Atas
#Kiri bawah, Kanan Bawah, Kanan Atas, Kiri Atas
vertices_wall = [-1.5, -1.0,  0.5, 0.0, 0.0,
                  1.5, -1.0,  0.5, 1.0, 0.0,
                  1.5,  3.0,  0.5, 1.0, 1.0,
                 -1.5,  3.0,  0.5, 0.0, 1.0,

                 -1.5, -1.0,  0.0, 0.0, 0.0,
                  1.5, -1.0,  0.0, 1.0, 0.0,
                  1.5,  3.0,  0.0, 1.0, 1.0,
                 -1.5,  3.0,  0.0, 0.0, 1.0,

                  1.5, -1.0,  0.5, 0.0, 0.0,
                  1.5, -1.0,  0.0, 1.0, 0.0,
                  1.5,  3.0,  0.0, 1.0, 1.0,
                  1.5,  3.0,  0.5, 0.0, 1.0,

                 -1.5, -1.0,  0.5, 0.0, 0.0,
                 -1.5, -1.0,  0.0, 1.0, 0.0,
                 -1.5,  3.0,  0.0, 1.0, 1.0,
                 -1.5,  3.0,  0.5, 0.0, 1.0,

                  1.5, -1.0,  0.5, 0.0, 0.0,
                  1.5, -1.0,  0.0, 1.0, 0.0,
                 -1.5, -1.0,  0.0, 1.0, 1.0,
                 -1.5, -1.0,  0.5, 0.0, 1.0,

                  1.5,  3.0,  0.5, 0.0, 0.0,
                  1.5,  3.0,  0.0, 1.0, 0.0,
                 -1.5,  3.0,  0.0, 1.0, 1.0,
                 -1.5,  3.0,  0.5, 0.0, 1.0]
            
            
vertices_floor = [-10.0, -1.0,  10.0, 0.0, 0.0,
                   10.0, -1.0,  10.0, 1.0, 0.0,
                   10.0, -0.7,  10.0, 1.0, 1.0,
                  -10.0, -0.7,  10.0, 0.0, 1.0,

                  -10.0, -1.0, -10.0, 0.0, 0.0,
                   10.0, -1.0, -10.0, 1.0, 0.0,
                   10.0, -0.7, -10.0, 1.0, 1.0,
                  -10.0, -0.7, -10.0, 0.0, 1.0,

                   10.0, -1.0,  10.0, 0.0, 0.0,
                   10.0, -1.0, -10.0, 1.0, 0.0,
                   10.0, -0.7, -10.0, 1.0, 1.0,
                   10.0, -0.7,  10.0, 0.0, 1.0,

                  -10.0, -1.0,  10.0, 0.0, 0.0,
                  -10.0, -1.0, -10.0, 1.0, 0.0,
                  -10.0, -0.7, -10.0, 1.0, 1.0,
                  -10.0, -0.7,  10.0, 0.0, 1.0,

                  10.0, -1.0,  10.0, 0.0, 0.0,
                  10.0, -1.0, -10.0, 1.0, 0.0,
                 -10.0, -1.0, -10.0, 1.0, 1.0,
                 -10.0, -1.0,  10.0, 0.0, 1.0,

                  10.0, -0.7,  10.0, 0.0, 0.0,
                  10.0, -0.7, -10.0, 1.0, 0.0,
                 -10.0, -0.7, -10.0, 1.0, 1.0,
                 -10.0, -0.7,  10.0, 0.0, 1.0]

from obj_hook import vertices_hook, indices_hook
from obj_saw import vertices_saw, indices_saw, vertices_sawo, indices_sawo
from obj_eng_key import vertices_key, indices_key
from obj_hammer import vertices_hammer, indices_hammer, vertices_gagang, indices_gagang
from obj_bor import vertices_bor, indices_bor, vertices_tombol, indices_tombol, vertices_matabor, indices_matabor
from obj_obeng import vertices_obeng, indices_obeng, vertices_besiobeng, indices_besiobeng
from obj_sledge import vertices_sledge, indices_sledge, vertices_kayu, indices_kayu


# For connecting da dots!! 
# for each vertices is connected to where!


indices_wall = [ 0,  1,  2,  2,  3,  0,
                 4,  5,  6,  6,  7,  4,
                 8,  9, 10, 10, 11,  8,
                12, 13, 14, 14, 15, 12,
                16, 17, 18, 18, 19, 16,
                20, 21, 22, 22, 23, 20]

indices_floor = [ 0,  1,  2,  2,  3,  0,
                 4,  5,  6,  6,  7,  4,
                 8,  9, 10, 10, 11,  8,
                12, 13, 14, 14, 15, 12,
                16, 17, 18, 18, 19, 16,
                20, 21, 22, 22, 23, 20]





               # vertices = np.array(vertices, dtype=np.float32)
               # indicies = np.array(indicies, dtype=np.uint32)

vertices_wall = np.array(vertices_wall, dtype=np.float32)
indices_wall = np.array(indices_wall, dtype=np.uint32)

vertices_floor = np.array(vertices_floor, dtype=np.float32)
indices_floor = np.array(indices_floor, dtype=np.uint32)

vertices_hook = np.array(vertices_hook, dtype=np.float32)
indices_hook = np.array(indices_hook, dtype=np.uint32)
## -- Triangle ends here

vertices_saw = np.array(vertices_saw, dtype=np.float32)
indices_saw = np.array(indices_saw, dtype=np.uint32)

vertices_sawo = np.array(vertices_sawo, dtype=np.float32)
indices_sawo = np.array(indices_sawo, dtype=np.uint32)

vertices_key = np.array(vertices_key, dtype=np.float32)
indices_key = np.array(indices_key, dtype=np.uint32)

vertices_hammer = np.array(vertices_hammer, dtype=np.float32)
indices_hammer = np.array(indices_hammer, dtype=np.uint32)

vertices_gagang = np.array(vertices_gagang, dtype=np.float32)
indices_gagang = np.array(indices_gagang, dtype=np.uint32)

vertices_bor = np.array(vertices_bor, dtype=np.float32)
indices_bor = np.array(indices_bor, dtype=np.uint32)

vertices_tombol = np.array(vertices_tombol, dtype=np.float32)
indices_tombol = np.array(indices_tombol, dtype=np.uint32)

vertices_matabor = np.array(vertices_matabor, dtype=np.float32)
indices_matabor = np.array(indices_matabor, dtype=np.uint32)

vertices_obeng = np.array(vertices_obeng, dtype=np.float32)
indices_obeng = np.array(indices_obeng, dtype=np.uint32)

vertices_besiobeng = np.array(vertices_besiobeng, dtype=np.float32)
indices_besiobeng = np.array(indices_besiobeng, dtype=np.uint32)

vertices_sledge = np.array(vertices_sledge, dtype=np.float32)
indices_sledge = np.array(indices_sledge, dtype=np.uint32)

vertices_kayu = np.array(vertices_kayu, dtype=np.float32)
indices_kayu = np.array(indices_kayu, dtype=np.uint32)



shader = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER), compileShader(fragmen_src, GL_FRAGMENT_SHADER))

# Cube VAO
               # cube_VAO = glGenVertexArrays(1)
               # glBindVertexArray(cube_VAO)

               # #vertex shader
               # # vertex buffer object
               # VBO = glGenBuffers(1)
               # glBindBuffer(GL_ARRAY_BUFFER, VBO)
               # glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

               # #element buffer object
               # # FUTURE NOTE, THIS APPLIES TOO LIKE glGenTextures
               # EBO = glGenBuffers(1)
               # glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
               # glBufferData(GL_ELEMENT_ARRAY_BUFFER, indicies.nbytes, indicies, GL_STATIC_DRAW)

               # #for vertex POSITION coordinate
               # glEnableVertexAttribArray(0)
               # glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, vertices.itemsize * 5, ctypes.c_void_p(0))

               # #for color / TEXTURE coordinate, depending on the value, check pipeline!!
               # glEnableVertexAttribArray(1)
               # glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, vertices.itemsize * 5, ctypes.c_void_p(12))

# ~~ NEW ONE HERE ~~ 

# Wall

wall_VAO = glGenVertexArrays(1)
glBindVertexArray(wall_VAO)

# vertex buffer object
VBO = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, VBO)
glBufferData(GL_ARRAY_BUFFER, vertices_wall.nbytes, vertices_wall, GL_STATIC_DRAW)

#element buffer object
EBO = glGenBuffers(1)
glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices_wall.nbytes, indices_wall, GL_STATIC_DRAW)

#for vertex POSITION coordinate
glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, vertices_wall.itemsize * 5, ctypes.c_void_p(0))

#for color / TEXTURE coordinate, depending on the value, check pipeline!!
glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, vertices_wall.itemsize * 5, ctypes.c_void_p(12))

# Floor

floor_VAO = glGenVertexArrays(1)
glBindVertexArray(floor_VAO)

# vertex buffer object
VBO = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, VBO)
glBufferData(GL_ARRAY_BUFFER, vertices_floor.nbytes, vertices_floor, GL_STATIC_DRAW)

#element buffer object
EBO = glGenBuffers(1)
glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices_floor.nbytes, indices_floor, GL_STATIC_DRAW)

#for vertex POSITION coordinate
glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, vertices_floor.itemsize * 5, ctypes.c_void_p(0))

#for color / TEXTURE coordinate, depending on the value, check pipeline!!
glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, vertices_floor.itemsize * 5, ctypes.c_void_p(12))

# Hook

hook_VAO = glGenVertexArrays(1)
glBindVertexArray(hook_VAO)

# vertex buffer object
VBO = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, VBO)
glBufferData(GL_ARRAY_BUFFER, vertices_hook.nbytes, vertices_hook, GL_STATIC_DRAW)

#element buffer object
EBO = glGenBuffers(1)
glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices_hook.nbytes, indices_hook, GL_STATIC_DRAW)

#for vertex POSITION coordinate
glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, vertices_hook.itemsize * 5, ctypes.c_void_p(0))

#for color / TEXTURE coordinate, depending on the value, check pipeline!!
glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, vertices_hook.itemsize * 5, ctypes.c_void_p(102))

# Saw

saw_VAO = glGenVertexArrays(1)
glBindVertexArray(saw_VAO)

# vertex buffer object
VBO = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, VBO)
glBufferData(GL_ARRAY_BUFFER, vertices_saw.nbytes, vertices_saw, GL_STATIC_DRAW)

#element buffer object
EBO = glGenBuffers(1)
glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices_saw.nbytes, indices_saw, GL_STATIC_DRAW)

#for vertex POSITION coordinate
glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, vertices_saw.itemsize * 5, ctypes.c_void_p(0))

#for color / TEXTURE coordinate, depending on the value, check pipeline!!
glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, vertices_saw.itemsize * 5, ctypes.c_void_p(12))

sawo_VAO = glGenVertexArrays(1)
glBindVertexArray(sawo_VAO)

# vertex buffer object
VBO = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, VBO)
glBufferData(GL_ARRAY_BUFFER, vertices_sawo.nbytes, vertices_sawo, GL_STATIC_DRAW)

#element buffer object
EBO = glGenBuffers(1)
glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices_sawo.nbytes, indices_sawo, GL_STATIC_DRAW)

#for vertex POSITION coordinate
glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, vertices_sawo.itemsize * 5, ctypes.c_void_p(0))

#for color / TEXTURE coordinate, depending on the value, check pipeline!!
glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, vertices_sawo.itemsize * 5, ctypes.c_void_p(24))


# Key 
key_VAO = glGenVertexArrays(1)
glBindVertexArray(key_VAO)

VBO = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, VBO)
glBufferData(GL_ARRAY_BUFFER, vertices_key.nbytes, vertices_key, GL_STATIC_DRAW)

#element buffer object
EBO = glGenBuffers(1)
glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices_key.nbytes, indices_key, GL_STATIC_DRAW)

#for vertex POSITION coordinate
glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, vertices_key.itemsize * 5, ctypes.c_void_p(0))

#for color / TEXTURE coordinate, depending on the value, check pipeline!!
glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, vertices_key.itemsize * 5, ctypes.c_void_p(24))

# Hammer 
hammer_VAO = glGenVertexArrays(1)
glBindVertexArray(hammer_VAO)

VBO = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, VBO)
glBufferData(GL_ARRAY_BUFFER, vertices_hammer.nbytes, vertices_hammer, GL_STATIC_DRAW)

#element buffer object
EBO = glGenBuffers(1)
glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices_hammer.nbytes, indices_hammer, GL_STATIC_DRAW)

#for vertex POSITION coordinate
glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, vertices_hammer.itemsize * 5, ctypes.c_void_p(0))

#for color / TEXTURE coordinate, depending on the value, check pipeline!!
glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, vertices_hammer.itemsize * 5, ctypes.c_void_p(36))

gagang_VAO = glGenVertexArrays(1)
glBindVertexArray(gagang_VAO)

VBO = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, VBO)
glBufferData(GL_ARRAY_BUFFER, vertices_gagang.nbytes, vertices_gagang, GL_STATIC_DRAW)

#element buffer object
EBO = glGenBuffers(1)
glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices_gagang.nbytes, indices_gagang, GL_STATIC_DRAW)

#for vertex POSITION coordinate
glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, vertices_gagang.itemsize * 5, ctypes.c_void_p(0))

#for color / TEXTURE coordinate, depending on the value, check pipeline!!
glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, vertices_gagang.itemsize * 5, ctypes.c_void_p(12))

# Bor 

bor_VAO = glGenVertexArrays(1)
glBindVertexArray(bor_VAO)

VBO = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, VBO)
glBufferData(GL_ARRAY_BUFFER, vertices_bor.nbytes, vertices_bor, GL_STATIC_DRAW)

#element buffer object
EBO = glGenBuffers(1)
glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices_bor.nbytes, indices_bor, GL_STATIC_DRAW)

#for vertex POSITION coordinate
glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, vertices_bor.itemsize * 5, ctypes.c_void_p(0))

#for color / TEXTURE coordinate, depending on the value, check pipeline!!
glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, vertices_bor.itemsize * 5, ctypes.c_void_p(24))

tombol_VAO = glGenVertexArrays(1)
glBindVertexArray(tombol_VAO)

VBO = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, VBO)
glBufferData(GL_ARRAY_BUFFER, vertices_tombol.nbytes, vertices_tombol, GL_STATIC_DRAW)

#element buffer object
EBO = glGenBuffers(1)
glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices_tombol.nbytes, indices_tombol, GL_STATIC_DRAW)

#for vertex POSITION coordinate
glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, vertices_tombol.itemsize * 5, ctypes.c_void_p(0))

#for color / TEXTURE coordinate, depending on the value, check pipeline!!
glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, vertices_tombol.itemsize * 5, ctypes.c_void_p(24))

matabor_VAO = glGenVertexArrays(1)
glBindVertexArray(matabor_VAO)

VBO = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, VBO)
glBufferData(GL_ARRAY_BUFFER, vertices_matabor.nbytes, vertices_matabor, GL_STATIC_DRAW)

#element buffer object
EBO = glGenBuffers(1)
glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices_matabor.nbytes, indices_matabor, GL_STATIC_DRAW)

#for vertex POSITION coordinate
glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, vertices_matabor.itemsize * 5, ctypes.c_void_p(0))

#for color / TEXTURE coordinate, depending on the value, check pipeline!!
glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, vertices_matabor.itemsize * 5, ctypes.c_void_p(24))


# Obeng

obeng_VAO = glGenVertexArrays(1)
glBindVertexArray(obeng_VAO)

VBO = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, VBO)
glBufferData(GL_ARRAY_BUFFER, vertices_obeng.nbytes, vertices_obeng, GL_STATIC_DRAW)

#element buffer object
EBO = glGenBuffers(1)
glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices_obeng.nbytes, indices_obeng, GL_STATIC_DRAW)

#for vertex POSITION coordinate
glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, vertices_obeng.itemsize * 5, ctypes.c_void_p(0))

#for color / TEXTURE coordinate, depending on the value, check pipeline!!
glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, vertices_obeng.itemsize * 5, ctypes.c_void_p(24))

besiobeng_VAO = glGenVertexArrays(1)
glBindVertexArray(besiobeng_VAO)

VBO = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, VBO)
glBufferData(GL_ARRAY_BUFFER, vertices_besiobeng.nbytes, vertices_besiobeng, GL_STATIC_DRAW)

#element buffer object
EBO = glGenBuffers(1)
glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices_besiobeng.nbytes, indices_besiobeng, GL_STATIC_DRAW)

#for vertex POSITION coordinate
glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, vertices_besiobeng.itemsize * 5, ctypes.c_void_p(0))

#for color / TEXTURE coordinate, depending on the value, check pipeline!!
glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, vertices_besiobeng.itemsize * 5, ctypes.c_void_p(24))

# sledge

sledge_VAO = glGenVertexArrays(1)
glBindVertexArray(sledge_VAO)

VBO = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, VBO)
glBufferData(GL_ARRAY_BUFFER, vertices_sledge.nbytes, vertices_sledge, GL_STATIC_DRAW)

#element buffer object
EBO = glGenBuffers(1)
glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices_sledge.nbytes, indices_sledge, GL_STATIC_DRAW)

#for vertex POSITION coordinate
glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, vertices_sledge.itemsize * 5, ctypes.c_void_p(0))

#for color / TEXTURE coordinate, depending on the value, check pipeline!!
glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, vertices_sledge.itemsize * 5, ctypes.c_void_p(24))

#kayu

kayu_VAO = glGenVertexArrays(1)
glBindVertexArray(kayu_VAO)

VBO = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, VBO)
glBufferData(GL_ARRAY_BUFFER, vertices_kayu.nbytes, vertices_kayu, GL_STATIC_DRAW)

#element buffer object
EBO = glGenBuffers(1)
glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices_kayu.nbytes, indices_kayu, GL_STATIC_DRAW)

#for vertex POSITION coordinate
glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, vertices_kayu.itemsize * 5, ctypes.c_void_p(0))

#for color / TEXTURE coordinate, depending on the value, check pipeline!!
glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, vertices_kayu.itemsize * 5, ctypes.c_void_p(24))


# ~~ END HERE ~~

# The value here define how many texture we want to create
texture = glGenTextures(15)

# LOADING HTE IMAGES USING TEXTURELOADER
# array here related to glGenTextures above!
               # cube1_texture = load_texture("TEXTURE/cardboard1.jpg", texture[0])
               # cube2_texture = load_texture("TEXTURE/cardboard2.jpg", texture[1])
wall_texture = load_texture("TEXTURE/wall.jpg", texture[3]) 
floor_texture = load_texture("TEXTURE/floor.jpg", texture[2])
hook_texture = load_texture("TEXTURE/hook.jpg", texture[1])
saw_texture = load_texture("TEXTURE/saw_gagang.jpg", texture[0])
sawo_texture = load_texture("TEXTURE/floor.jpg", texture[4])
key_texture = load_texture("TEXTURE/metal.jpg", texture[5])
hammer_texture = load_texture("TEXTURE/metal.jpg", texture[6])
gagang_texture = load_texture("TEXTURE/kayu.jpg", texture[7])
bor = load_texture("TEXTURE/metal.jpg", texture[8])
tombol = load_texture("TEXTURE/metal.jpg", texture[9])
matabor = load_texture("TEXTURE/floor.jpg", texture[10])
obeng = load_texture("TEXTURE/metal.jpg", texture[11])
besiobeng = load_texture("TEXTURE/metal.jpg", texture[12])
kayu = load_texture("TEXTURE/kayu.jpg", texture[13])

#using the shader
glUseProgram(shader)

#window color
glClearColor(0, 0.1, 0.1, 1)

#for free rotation
glEnable(GL_DEPTH_TEST)

#this is for transparancy
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

#for projection matrix ~~~~ starts here ~~~~~

#4 argument( FOV, Aspect ratio window, Near Clipping pane, far clipping pane)
#copied for eazier window management
# ALSO UPDATED FOR SUPPORTING DA CAMERA?
projection = pyrr.matrix44.create_perspective_projection_matrix(45, WIDTH/HEIGHT, 0.1, 100)

# HERE Is for translation matrix
# We're creating three translation matrix, because 3 box
               # cube1 = pyrr.matrix44.create_from_translation(pyrr.Vector3([1, 2, 0]))
               # cube2 = pyrr.matrix44.create_from_translation(pyrr.Vector3([-1, 2, 0]))
wall = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 3, -2]))
floor = pyrr.matrix44.create_from_translation(pyrr.Vector3([-5, 3, -2]))
hook = pyrr.matrix44.create_from_translation(pyrr.Vector3([-0.8, 5, -1.5]))
saw = pyrr.matrix44.create_from_translation(pyrr.Vector3([-0.78, 4.8, -1.5]))
sawo = pyrr.matrix44.create_from_translation(pyrr.Vector3([3, 0, -1.5]))
key = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 5, -1.5]))
hammer = pyrr.matrix44.create_from_translation(pyrr.Vector3([0.8, 4.6, -1.5]))
gagang = pyrr.matrix44.create_from_translation(pyrr.Vector3([0.8, 4.6, -1.5]))
bor = pyrr.matrix44.create_from_translation(pyrr.Vector3([1, 5.4, -1.64]))
tombol = pyrr.matrix44.create_from_translation(pyrr.Vector3([0.98, 5.4, -1.64]))
matabor = pyrr.matrix44.create_from_translation(pyrr.Vector3([1.2, 5.375, -1.71]))
obeng = pyrr.matrix44.create_from_translation(pyrr.Vector3([-0.4, 5.5, -1.47]))
besiobeng = pyrr.matrix44.create_from_translation(pyrr.Vector3([-0.4, 5.5, -1.47]))
sledge = pyrr.matrix44.create_from_translation(pyrr.Vector3([-1.1, 2.7, -1.47]))
kayu = pyrr.matrix44.create_from_translation(pyrr.Vector3([-1.1, 2.7, -1.47]))


# Misalnya, untuk scaling objek "wall" menjadi dua kali lebih besar pada semua sumbu:
scale_factor = 0.03
scaling_matrix = pyrr.matrix44.create_from_scale(pyrr.Vector3([scale_factor, scale_factor, scale_factor]))
scaled_wall = scaling_matrix @ hook  # Terapkan scaling pada matriks transformasi model objek "wall"
hook = scaled_wall

# For Saw (addition)
rotation_matrix = pyrr.matrix44.create_from_x_rotation(np.radians(180))
new_sawo = pyrr.matrix44.multiply(sawo, rotation_matrix)
sawoo = pyrr.matrix44.create_from_translation(pyrr.Vector3([-3.78, 4.62, -2.9]))
old_sawo = pyrr.matrix44.multiply(new_sawo, sawoo)
ultimate_saw = pyrr.matrix44.multiply(old_sawo, saw)
scale_factor = 0.2
scaling = pyrr.matrix44.create_from_scale(pyrr.Vector3([scale_factor, scale_factor, scale_factor]))
scaling_saw = scaling @ old_sawo
old_sawo = scaling_saw
scaling_saw = scaling @ saw
saw = scaling_saw
scaling_key = scaling @ key
key = scaling_key

scaling_hammer = pyrr.matrix44.create_from_scale(pyrr.Vector3([0.3, 0.3, 0.3])) @ hammer
scaling_gagang = pyrr.matrix44.create_from_scale(pyrr.Vector3([0.3, 0.3, 0.3])) @ gagang
hammer = scaling_hammer
gagang = scaling_gagang

scale_factory = 0.8
scaling = pyrr.matrix44.create_from_scale(pyrr.Vector3([scale_factory, scale_factory, scale_factory]))
scaling_bor = scaling @ bor
scaling_tombol = scaling @ tombol
bor = scaling_bor
tombol = scaling_tombol

scale_factory = 0.3
scaling = pyrr.matrix44.create_from_scale(pyrr.Vector3([scale_factory, scale_factory, scale_factory]))
scaling_obeng = scaling @ obeng
obeng = scaling_obeng
scaling_besiobeng = scaling @ besiobeng
besiobeng = scaling_besiobeng

scaling_sledge = scaling @ sledge
sledge = scaling_sledge

scaling_kayu = scaling @ kayu
kayu = scaling_kayu

# scaling_hammer = pyrr.matrix44.create_from_scale(pyrr.Vector3([0.6, 0.6, 0.6]))
# scaling_gagang = pyrr.matrix44.create_from_scale(pyrr.Vector3([0.6, 0.6, 0.6]))
# hammer = scaling_hammer
# gagang = scaling_gagang

scaling = pyrr.matrix44.create_from_scale(pyrr.Vector3([0.6, 0.6, 0.6]))
scaling_ley = scaling @ key
key = scaling_ley
#~~~~ end here ~~~~~

#rotation for the cube // switched to model because the shader file said
model_loc = glGetUniformLocation(shader, "model")

proj_loc= glGetUniformLocation(shader, "projection")

#adding shader for view matrix
view_loc= glGetUniformLocation(shader, "view")

#for switcher inside the fragment
switcher_loc = glGetUniformLocation(shader, "switcher")

#this one too moved into resize for better window management
glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)

# The main application loop
while not glfw.window_should_close(window):
      glfw.poll_events()
      do_movement()

      view = cam.get_view_matrix()
      glUniformMatrix4fv(view_loc, 1, GL_FALSE, view)

      glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

      glUniform1i(switcher_loc, 0)

                    #If previously we just declaring right away, we can add the vao
                    #  glBindVertexArray(cube_VAO)
                    #  #Declaring the cube array
                    #  glBindTexture(GL_TEXTURE_2D, texture[0])
                    #  glUniformMatrix4fv(model_loc, 1, GL_FALSE, cube1)
                    #  #Drawing the array
                    #  glDrawElements(GL_TRIANGLES, len(indicies), GL_UNSIGNED_INT, None)

                    #  #Declaring the cube array
                    #  glBindVertexArray(cube_VAO)
                    #  glBindTexture(GL_TEXTURE_2D, texture[1])
                    #  glUniformMatrix4fv(model_loc, 1, GL_FALSE, cube2)
                    #  #Drawing the array
                    #  glDrawElements(GL_TRIANGLES, len(indicies), GL_UNSIGNED_INT, None)

      #Declaring the wall
      glBindVertexArray(wall_VAO)
      glBindTexture(GL_TEXTURE_2D, texture[3])
      glUniformMatrix4fv(model_loc, 1, GL_FALSE, wall)
      glDrawElements(GL_TRIANGLES, len(indices_wall), GL_UNSIGNED_INT, None)
    
      #Declaring the floor
      glBindVertexArray(floor_VAO)
      glBindTexture(GL_TEXTURE_2D, texture[2])
      glUniformMatrix4fv(model_loc, 1, GL_FALSE, floor)
      glDrawElements(GL_TRIANGLES, len(indices_floor), GL_UNSIGNED_INT, None)

      #Declaring the hook
      glBindVertexArray(hook_VAO)
      glBindTexture(GL_TEXTURE_2D, texture[1])
      glUniformMatrix4fv(model_loc, 1, GL_FALSE, hook)
      glDrawElements(GL_TRIANGLES, len(indices_hook), GL_UNSIGNED_INT, None)

      #Declaring the saw
      glBindVertexArray(saw_VAO)
      glBindTexture(GL_TEXTURE_2D, texture[0])
      glUniformMatrix4fv(model_loc, 1, GL_FALSE, saw)
      glDrawElements(GL_TRIANGLES, len(indices_saw), GL_UNSIGNED_INT, None)

      glBindVertexArray(sawo_VAO)
      glBindTexture(GL_TEXTURE_2D, texture[4])
      glUniformMatrix4fv(model_loc, 1, GL_FALSE, old_sawo)
      glDrawElements(GL_TRIANGLES, len(indices_sawo), GL_UNSIGNED_INT, None)

      #Declaring the key
      glBindVertexArray(key_VAO)
      glBindTexture(GL_TEXTURE_2D, texture[5])
      glUniformMatrix4fv(model_loc, 1, GL_FALSE, key)
      glDrawElements(GL_TRIANGLES, len(indices_key), GL_UNSIGNED_INT, None)
      
      #Declaring the hammer
      glBindVertexArray(hammer_VAO)
      glBindTexture(GL_TEXTURE_2D, texture[6])
      glUniformMatrix4fv(model_loc, 1, GL_FALSE, hammer)
      glDrawElements(GL_TRIANGLES, len(indices_hammer), GL_UNSIGNED_INT, None)

      glBindVertexArray(gagang_VAO)
      glBindTexture(GL_TEXTURE_2D, texture[7])
      glUniformMatrix4fv(model_loc, 1, GL_FALSE, gagang)
      glDrawElements(GL_TRIANGLES, len(indices_gagang), GL_UNSIGNED_INT, None)

      #Declaring the bor
      glBindVertexArray(bor_VAO)
      glBindTexture(GL_TEXTURE_2D, texture[8])
      glUniformMatrix4fv(model_loc, 1, GL_FALSE, bor)
      glDrawElements(GL_TRIANGLES, len(indices_bor), GL_UNSIGNED_INT, None)

      glBindVertexArray(tombol_VAO)
      glBindTexture(GL_TEXTURE_2D, texture[8])
      glUniformMatrix4fv(model_loc, 1, GL_FALSE, tombol)
      glDrawElements(GL_TRIANGLES, len(indices_tombol), GL_UNSIGNED_INT, None)

      glBindVertexArray(matabor_VAO)
      glBindTexture(GL_TEXTURE_2D, texture[9])
      glUniformMatrix4fv(model_loc, 1, GL_FALSE, matabor)
      glDrawElements(GL_TRIANGLES, len(indices_matabor), GL_UNSIGNED_INT, None)

      #Declaring the obeng
      glBindVertexArray(obeng_VAO)
      glBindTexture(GL_TEXTURE_2D, texture[11])
      glUniformMatrix4fv(model_loc, 1, GL_FALSE, obeng)
      glDrawElements(GL_TRIANGLES, len(indices_obeng), GL_UNSIGNED_INT, None)

      glBindVertexArray(besiobeng_VAO)
      glBindTexture(GL_TEXTURE_2D, texture[11])
      glUniformMatrix4fv(model_loc, 1, GL_FALSE, besiobeng)
      glDrawElements(GL_TRIANGLES, len(indices_besiobeng), GL_UNSIGNED_INT, None)

      #Declaring the sledge
      glBindVertexArray(sledge_VAO)
      glBindTexture(GL_TEXTURE_2D, texture[11])
      glUniformMatrix4fv(model_loc, 1, GL_FALSE, sledge)
      glDrawElements(GL_TRIANGLES, len(indices_sledge), GL_UNSIGNED_INT, None)

      glBindVertexArray(kayu_VAO)
      glBindTexture(GL_TEXTURE_2D, texture[13])
      glUniformMatrix4fv(model_loc, 1, GL_FALSE, kayu)
      glDrawElements(GL_TRIANGLES, len(indices_kayu), GL_UNSIGNED_INT, None)


      
      glfw.swap_buffers(window)

# For terminating glfw
glfw.terminate()