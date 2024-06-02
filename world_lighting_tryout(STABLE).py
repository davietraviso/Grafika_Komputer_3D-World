import glfw
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import numpy as np
from ImageTexture import upload_texture_utama
import pyrr
from PIL import Image
from File_Kamera import Kamera_utama
from lightSource import light_function
from lampSource import lamp_function

# Main declaration for the camera

kamera_utama = Kamera_utama()
LEBAR_LAYAR, TINGGI_LAYAR = 1280, 720
endofX, endofY = LEBAR_LAYAR / 2, TINGGI_LAYAR / 2
default_one = True


# For defining the files from the light and lamp shader

light_vertex_src, light_fragmen_src = light_function()
lamp_vertex_src, lamp_fragmen_src = lamp_function()


# For resizing the main windows

def resizing_window_utama(jendela_utama, lebar_layar, tinggi_layar):
    glViewport(0, 0, lebar_layar, tinggi_layar)

    proyeksi_utama= pyrr.matrix44.create_perspective_projection_matrix(45, lebar_layar / tinggi_layar, 0.1, 100)

    glUniformMatrix4fv(projLoc, 1, GL_FALSE, proyeksi_utama)

# For glfw lib initialization

if not glfw.init():
    raise Exception("glfw can not be initialized!")

# This for creating the main window

jendela_utama = glfw.create_window(LEBAR_LAYAR, TINGGI_LAYAR, "Media Pelunas MK Grakom, bismillah lulus", None, None)



# This is for keyboard callback


kiri, kanan, depan, mundur, keatas, kebawah = False, False, False, False, False, False
def inputan_keyboard(jendela_utama, tombol, kode_scan, tindakan_keyboard, mode_render):
     global kiri, kanan, depan, mundur, keatas, kebawah
     if tombol == glfw.KEY_ESCAPE and tindakan_keyboard == glfw.PRESS:
          glfw.set_window_should_close(jendela_utama, True)

     elif tombol == glfw.KEY_W and tindakan_keyboard == glfw.PRESS:
          depan = True

     elif tombol == glfw.KEY_S and tindakan_keyboard == glfw.PRESS:
          mundur = True

     elif tombol == glfw.KEY_A and tindakan_keyboard == glfw.PRESS:
          kiri = True
          
     elif tombol == glfw.KEY_D and tindakan_keyboard == glfw.PRESS:
          kanan = True

     elif tombol == glfw.KEY_Z and tindakan_keyboard == glfw.PRESS:
          keatas = True

     elif tombol == glfw.KEY_X and tindakan_keyboard == glfw.PRESS:
          kebawah = True
          
     elif tombol in [glfw.KEY_W, glfw.KEY_S, glfw.KEY_D, glfw.KEY_A, glfw.KEY_Z, glfw.KEY_X] and tindakan_keyboard == glfw.RELEASE:
          kiri, kanan, depan, mundur, keatas, kebawah = False, False, False, False, False, False


# This is for confirmation of main window creation

if not jendela_utama:
        glfw.terminate()
        raise Exception("glfw cannot be created!")


# This is for mouse callback

def pergerakan_mouse(jendela_utama, posisi_x, posisi_y):
    global default_one, endofX, endofY

    if default_one:
        
        endofX = posisi_x
        endofY = posisi_y
        default_one = False

    sisi_akhir_x = posisi_x - endofX
    sisi_akhir_y = endofY - posisi_y

    endofX = posisi_x
    endofY = posisi_y
    
    kamera_utama.proses_pergerakan_mouse(sisi_akhir_x, sisi_akhir_y)


# This is for setting the position of main window
glfw.set_window_pos(jendela_utama, 150, 100)

# This is for calling the function of resizing the main window
glfw.set_window_size_callback(jendela_utama, resizing_window_utama)

# This is for calling the function of mouse callback
glfw.set_cursor_pos_callback(jendela_utama, pergerakan_mouse)

# This is for calling the cursor function, so that the cursor is supported inside the program
glfw.set_input_mode(jendela_utama, glfw.CURSOR, glfw.CURSOR_DISABLED)

# This is for calling the keyboard callback function from above
glfw.set_key_callback(jendela_utama, inputan_keyboard)

# This is for setting the main windows context current
glfw.make_context_current(jendela_utama)

# This part is the keyboard movement
def pergerakan_keyboard():
     if kiri:
          kamera_utama.konfigurasi_pergerakan_keyboard("KIRI", 0.01)

     elif kanan:
          kamera_utama.konfigurasi_pergerakan_keyboard("KANAN", 0.01)

     elif depan:
          kamera_utama.konfigurasi_pergerakan_keyboard("MAJU", 0.01)

     elif mundur:
          kamera_utama.konfigurasi_pergerakan_keyboard("MUNDUR", 0.01)

     elif keatas:
          kamera_utama.konfigurasi_pergerakan_keyboard("KEATAS", 0.01)

     elif kebawah:
          kamera_utama.konfigurasi_pergerakan_keyboard("KEBAWAH", 0.01)

# This part is for calling the indices and vertices of objects in other files

from obj_hook import vertices_hook, indices_hook
from obj_saw import vertices_saw, indices_saw, vertices_sawo, indices_sawo
from obj_eng_key import vertices_key, indices_key
from obj_hammer import vertices_hammer, indices_hammer, vertices_gagang, indices_gagang
from obj_bor import vertices_bor, indices_bor, vertices_tombol, indices_tombol, vertices_matabor, indices_matabor
from obj_obeng import vertices_obeng, indices_obeng, vertices_besiobeng, indices_besiobeng
from obj_sledge import vertices_sledge, indices_sledge, vertices_kayu, indices_kayu
from obj_wall import vertices_wall, indices_wall
from obj_floor import vertices_floor, indices_floor
from obj_wall1 import vertices_wall1 ,indices_wall1
from obj_wall2 import vertices_wall2 ,indices_wall2
from obj_wallEX import vertices_wallEX, indices_wallEX
from obj_light import vertices_light
from obj_box1 import vertices_box1, indices_box1
from obj_box4 import vertices_box4, indices_box4
from obj_kayu1 import vertices_kayu1, indices_kayu1
from obj_kayu2 import vertices_kayu2, indices_kayu2

# This here for defining only the light cube vertices and indices

vertices_light = np.array(vertices_light, dtype=np.float32)

# This part is for defining the object name in this main file

objects = {
    "wallEX": (vertices_wallEX, indices_wallEX),
    "wall": (vertices_wall, indices_wall),
    "floor": (vertices_floor, indices_floor),
    "hook": (vertices_hook, indices_hook),
    "saw": (vertices_saw, indices_saw),
    "sawo": (vertices_sawo, indices_sawo),
    "key": (vertices_key, indices_key),
    "hammer": (vertices_hammer, indices_hammer),
    "gagang": (vertices_gagang, indices_gagang),
    "bor": (vertices_bor, indices_bor),
    "tombol": (vertices_tombol, indices_tombol),
    "matabor": (vertices_matabor, indices_matabor),
    "obeng": (vertices_obeng, indices_obeng),
    "besiobeng": (vertices_besiobeng, indices_besiobeng),
    "sledge": (vertices_sledge, indices_sledge),
    "kayu": (vertices_kayu, indices_kayu),
    "wall1": (vertices_wall1, indices_wall1),
    "wall2": (vertices_wall2, indices_wall2),
    "box1" : (vertices_box1, indices_box1),
    "box2" : (vertices_box1, indices_box1),
    "box4" : (vertices_box4, indices_box4),
    "kayu1" : (vertices_kayu1, indices_kayu1),
    "kayu2" : (vertices_kayu2, indices_kayu2)
}

# This part is for using the objects name for assiging them data type accordingly

for name, (vertices, indices) in objects.items():
    globals()["vertices_" + name] = np.array(vertices, dtype=np.float32)
    globals()["indices_" + name] = np.array(indices, dtype=np.uint32)

# This part is for compiling the shader for both lighting and lamp shader

lightingShader = compileProgram(compileShader(light_vertex_src, GL_VERTEX_SHADER), compileShader(light_fragmen_src, GL_FRAGMENT_SHADER))
lampShader = compileProgram(compileShader(lamp_vertex_src, GL_VERTEX_SHADER), compileShader(lamp_fragmen_src, GL_FRAGMENT_SHADER))


# This part is for the light cube VAO

lightVAO = glGenVertexArrays(1)
glBindVertexArray(lightVAO)

     #for binding the vbo and vao
VBO = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, VBO)
glBufferData(GL_ARRAY_BUFFER, vertices_light.nbytes, vertices_light, GL_STATIC_DRAW)

glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, vertices_light.itemsize * 6, ctypes.c_void_p(0))

glBindVertexArray(0)

# This part is for lighting setup

diffuseMap = glGenTextures(1)
specularMap = glGenTextures(1)

textureLebar_layar = 0  # Initialize textureLebar_layar
textureTinggi_layar = 0  # Initialize textureTinggi_layar
image = None  # Initialize image as None?

# This part is for setting how much texture array is needed

texture = glGenTextures(50)

# This part is a function for calling VAO creation, usage is below

def create_object_VAO(vertices, indices, stride, position_offset, normal_offset, texture_offset): #MODIFY THIS LATER FOR LIGHTING MATERIAL
    VAO = glGenVertexArrays(1)
    glBindVertexArray(VAO)

    # Vertex buffer object data setup
    VBO = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

    # Element buffer object data setup
    EBO = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

    # This part is for vertex POSITION coordinate
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(position_offset))

    # This part is for Normal coordinate
    glEnableVertexAttribArray(1)
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(normal_offset))
 
    # This part is for texture coordinate
    glEnableVertexAttribArray(2)
    glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(texture_offset))

    glBindVertexArray(0)

    return VAO


# This part is for using the VAO creation function, and setting it's name for each objects

floor_VAO = create_object_VAO(vertices_floor, indices_floor, vertices_floor.itemsize * 8, 0, 20, 12)
wall_VAO = create_object_VAO(vertices_wallEX, indices_wallEX, vertices_wallEX.itemsize * 8, 0, 20, 12)
saw_VAO = create_object_VAO(vertices_saw, indices_saw, vertices_saw.itemsize * 8, 0, 20, 12)
sawo_VAO = create_object_VAO(vertices_sawo, indices_sawo, vertices_sawo.itemsize * 8, 0, 20, 12)
key_VAO = create_object_VAO(vertices_key, indices_key, vertices_key.itemsize * 8, 0, 20, 12)
hammer_VAO = create_object_VAO(vertices_hammer, indices_hammer, vertices_hammer.itemsize * 8, 0, 20, 12)
gagang_VAO = create_object_VAO(vertices_gagang, indices_gagang, vertices_gagang.itemsize * 8, 0, 20, 12)
bor_VAO = create_object_VAO(vertices_bor, indices_bor, vertices_bor.itemsize * 8, 0, 20, 12)
tombol_VAO = create_object_VAO(vertices_tombol, indices_tombol, vertices_tombol.itemsize * 8, 0, 20, 12)
matabor_VAO = create_object_VAO(vertices_matabor, indices_matabor, vertices_matabor.itemsize * 8, 0, 20, 12)
obeng_VAO = create_object_VAO(vertices_obeng, indices_obeng, vertices_obeng.itemsize * 8, 0, 20, 12)
besiobeng_VAO = create_object_VAO(vertices_besiobeng, indices_besiobeng, vertices_besiobeng.itemsize * 8, 0, 20, 12)
sledge_VAO = create_object_VAO(vertices_sledge, indices_sledge, vertices_sledge.itemsize * 8, 0, 20, 12)
kayu_VAO = create_object_VAO(vertices_kayu, indices_kayu, vertices_kayu.itemsize * 8, 0, 20, 12)
wall1_VAO = create_object_VAO(vertices_wall1, indices_wall1, vertices_wall1.itemsize * 8, 0, 20, 12)
wall2_VAO = create_object_VAO(vertices_wall2, indices_wall2, vertices_wall2.itemsize * 8, 0, 20, 12)
box1_VAO = create_object_VAO(vertices_box1, indices_box1, vertices_box1.itemsize * 8, 0, 20, 12)
box2_VAO = create_object_VAO(vertices_box1, indices_box1, vertices_box1.itemsize * 8, 0, 20, 12)
box4_VAO = create_object_VAO(vertices_box4, indices_box4, vertices_box4.itemsize * 8, 0, 20, 12)
kayu1_VAO = create_object_VAO(vertices_kayu1, indices_kayu1, vertices_kayu1.itemsize * 8, 0, 20, 12)
kayu2_VAO = create_object_VAO(vertices_kayu2, indices_kayu2, vertices_kayu2.itemsize * 8, 0, 20, 12)


# This part is for giving the window its color

glClearColor(0, 0.1, 0.1, 1)

# This part is for using the depth of texture

glEnable(GL_DEPTH_TEST)

# This part is for the main projection of the screen

proyeksi_utama= pyrr.matrix44.create_perspective_projection_matrix(45, LEBAR_LAYAR/TINGGI_LAYAR, 0.1, 100)

# This part is a bunch of translation matrix

light = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 0, -1]))
wall = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 3, -2]))
floor = pyrr.matrix44.create_from_translation(pyrr.Vector3([-0.2, 2.2, -1.5]))
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
wall1 = pyrr.matrix44.create_from_translation(pyrr.Vector3([-0.2, 2.2, -1.5]))
wall2 = pyrr.matrix44.create_from_translation(pyrr.Vector3([-2.0, 4.2, -1.5]))
box1 = pyrr.matrix44.create_from_translation(pyrr.Vector3([-3.7, 3.35, 0]))
box2 = pyrr.matrix44.create_from_translation(pyrr.Vector3([-3.7, 3.35, -2]))
box3 = pyrr.matrix44.create_from_translation(pyrr.Vector3([1.7, 3.85, -2]))
box4 = pyrr.matrix44.create_from_translation(pyrr.Vector3([1.7, 3.85, -3.0]))
box5 = pyrr.matrix44.create_from_translation(pyrr.Vector3([1.7, 5.7, -4.0]))
kayu1 = pyrr.matrix44.create_from_translation(pyrr.Vector3([-8.7, 5.8, 6.5]))
kayu2 = pyrr.matrix44.create_from_translation(pyrr.Vector3([-8.7, 5.8, 6.0]))
kayu3 = pyrr.matrix44.create_from_translation(pyrr.Vector3([-8.7, 5.9, 6.25]))
kayu4 = pyrr.matrix44.create_from_translation(pyrr.Vector3([-8.7, 5.85, 5.25]))
kayu5 = pyrr.matrix44.create_from_translation(pyrr.Vector3([-18.0, -3.0, 0.25]))
kayu6 = pyrr.matrix44.create_from_translation(pyrr.Vector3([-18.0, -2.975, 2.25]))
kayu7 = pyrr.matrix44.create_from_translation(pyrr.Vector3([1.5, 6.0, -8.0]))
kayu8 = pyrr.matrix44.create_from_translation(pyrr.Vector3([1.9, 4.2, -6.5]))

# THIS IS A BUNCH OF TRANSLATION, A WHOLE OF I MYSELF DON'T REMEMBER HOW TO USE, PLEASE JUST AVOID IT

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

scaling_floor = scaling @ floor
floor = scaling_floor

scaling_wall1 = scaling @ wall1
wall1 = scaling_wall1

scaling_wall2 = scaling @ wall2
wall2 = scaling_wall2
rotation_matrix2 = pyrr.matrix44.create_from_y_rotation(np.radians(90))
new_wall2 = pyrr.matrix44.multiply(wall2, rotation_matrix2)

wall2_t = pyrr.matrix44.create_from_translation(pyrr.Vector3([-1.7, -2.0, 0.5]))
wall_t_multi = pyrr.matrix44.multiply(new_wall2, wall2_t)
wall2 = wall_t_multi

scaling_sledge = scaling @ sledge
sledge = scaling_sledge

scaling_kayu = scaling @ kayu
kayu = scaling_kayu

scaling = pyrr.matrix44.create_from_scale(pyrr.Vector3([0.6, 0.6, 0.6]))
scaling_ley = scaling @ key
key = scaling_ley

scale2 = 0.7
scaling2 = pyrr.matrix44.create_from_scale(pyrr.Vector3([scale2, scale2, scale2]))

scale3 = 0.6
scaling3 = pyrr.matrix44.create_from_scale(pyrr.Vector3([scale3, scale3, scale3]))
box1 = box1 @ scaling2
box2 = box2 @ scaling2
box3 = box3 @ scaling3
box4 = box4 @ scaling3

scale3 = 0.5
scaling3 = pyrr.matrix44.create_from_scale(pyrr.Vector3([scale3, scale3, scale3]))
box5 = box5 @ scaling3

rotation_box4 = pyrr.matrix44.create_from_y_rotation(np.radians(30))
rotation_box5 = pyrr.matrix44.create_from_y_rotation(np.radians(40))
box4 = box4 @ rotation_box4
box5 = box5 @ rotation_box5

scale3 = 0.4
scaling3 = pyrr.matrix44.create_from_scale(pyrr.Vector3([scale3, scale3, scale3]))
# box5 = box5 @ scaling3

rotation_kayu = pyrr.matrix44.create_from_y_rotation(np.radians(90))
kayu1 = kayu1 @ rotation_kayu
kayu1 = kayu1 @ scaling3

kayu2 = kayu2 @ rotation_kayu
kayu2 = kayu2 @ scaling3

kayu3 = kayu3 @ rotation_kayu
kayu3 = kayu3 @ scaling3

kayu4 = kayu4 @ rotation_kayu
kayu4 = kayu4 @ scaling3

rotation_kayu4 = pyrr.matrix44.create_from_y_rotation(np.radians(10))
kayu4 = kayu4 @ rotation_kayu4

rotation_kayu4 = pyrr.matrix44.create_from_x_rotation(np.radians(10))
kayu4 = kayu4 @ rotation_kayu4

rotation_kayu5 = pyrr.matrix44.create_from_z_rotation(np.radians(70))
kayu5 = kayu5 @ rotation_kayu5
kayu5 = kayu5 @ scaling3

kayu6 = kayu6 @ rotation_kayu5
kayu6 = kayu6 @ scaling3

rotation_kayu6 = pyrr.matrix44.create_from_x_rotation(np.radians(15))
rotation_kayu7 = pyrr.matrix44.create_from_x_rotation(np.radians(21))

kayu7 = kayu7 @ scaling3
kayu7 = kayu7 @ rotation_kayu6

kayu8 = kayu8 @ scaling3
kayu8 = kayu8 @ rotation_kayu7

rotation_kayu6 = pyrr.matrix44.create_from_y_rotation(np.radians(15))
kayu6 = kayu6 @ rotation_kayu6

#~~~~ end here of the translation ~~~~~

# These here is for updating the position of the light

viewPosCam = kamera_utama.update_posisi_baru()
lightPos = np.array([8.2, 35.0, 8.0], dtype=np.float32) #AARDVAK

# This here is a function that calling the VAO data from previous VAO creation function for each objects

def draw_object(vao, texture_index, model_matrix, indices):
    glBindVertexArray(vao)
    glBindTexture(GL_TEXTURE_2D, texture[texture_index])
    glUniformMatrix4fv(modelLoc, 1, GL_FALSE, model_matrix)
    glDrawElements(GL_TRIANGLES, len(indices), GL_UNSIGNED_INT, None)
    glBindVertexArray(0)

# This part is for store information about each objects

objects = [
    (wall_VAO, 3, wall, indices_wallEX),
    (floor_VAO, 2, floor, indices_floor),
    (saw_VAO, 0, saw, indices_saw),
    (sawo_VAO, 4, old_sawo, indices_sawo),
    (key_VAO, 5, key, indices_key),
    (hammer_VAO, 6, hammer, indices_hammer),
    (gagang_VAO, 7, gagang, indices_gagang),
    (bor_VAO, 8, bor, indices_bor),
    (tombol_VAO, 8, tombol, indices_tombol),
    (matabor_VAO, 9, matabor, indices_matabor),
    (obeng_VAO, 11, obeng, indices_obeng),
    (besiobeng_VAO, 12, besiobeng, indices_besiobeng),
    (sledge_VAO, 15, sledge, indices_sledge),
    (kayu_VAO, 13, kayu, indices_kayu),
    (wall1_VAO, 14, wall1, indices_wall1),
    (wall2_VAO, 14, wall2, indices_wall2),
    (box1_VAO, 16, box1, indices_box1),
    (box2_VAO, 17, box2, indices_box1),
    (box2_VAO, 19, box3, indices_box1),
    (box4_VAO, 19, box4, indices_box1),
    (box4_VAO, 19, box5, indices_box1),
    (kayu1_VAO, 18, kayu1, indices_kayu1),
    (kayu1_VAO, 18, kayu2, indices_kayu1),
    (kayu1_VAO, 18, kayu3, indices_kayu1),
    (kayu1_VAO, 18, kayu4, indices_kayu1),
    (kayu1_VAO, 18, kayu5, indices_kayu1),
    (kayu1_VAO, 18, kayu6, indices_kayu1),
    (kayu2_VAO, 20, kayu7, indices_kayu1),
    (kayu2_VAO, 20, kayu8, indices_kayu1)
]

# This part is for using the texture uploader

def load_and_configure_texture(sumber_gambar, texture_unit):
    image = upload_texture_utama(sumber_gambar, texture_unit)
    glBindTexture(GL_TEXTURE_2D, diffuseMap)
    glGenerateMipmap(GL_TEXTURE_2D)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glBindTexture(GL_TEXTURE_2D, 0)
    return image

# This is for the usage of using the texture uploader

image = load_and_configure_texture("TEXTURE/wall.jpg", texture[3])
image = load_and_configure_texture("TEXTURE/floor.jpg", texture[2])
image = load_and_configure_texture("TEXTURE/wood.jpg", texture[0])
image = load_and_configure_texture("TEXTURE/metal.jpg", texture[4])
image = load_and_configure_texture("TEXTURE/steelhammer3.jpg", texture[5])
image = load_and_configure_texture("TEXTURE/metal.jpg", texture[6])
image = load_and_configure_texture("TEXTURE/kayu.jpg", texture[7])
image = load_and_configure_texture("TEXTURE/plastic2.jpg", texture[8])
image = load_and_configure_texture("TEXTURE/metal.jpg", texture[9])
image = load_and_configure_texture("TEXTURE/floor.jpg", texture[10])
image = load_and_configure_texture("TEXTURE/rubber3.jpg", texture[11])
image = load_and_configure_texture("TEXTURE/metal.jpg", texture[12])
image = load_and_configure_texture("TEXTURE/kayu.jpg", texture[13])
image = load_and_configure_texture("TEXTURE/wal3.jpg", texture[14])
image = load_and_configure_texture("TEXTURE/sledge2.jpg", texture[15])
image = load_and_configure_texture("TEXTURE/cardboard1.jpg", texture[16])
image = load_and_configure_texture("TEXTURE/cardboard3.jpg", texture[17])
image = load_and_configure_texture("TEXTURE/kayu1.jpg", texture[18])
image = load_and_configure_texture("TEXTURE/cardboard4.jpg", texture[19])
image = load_and_configure_texture("TEXTURE/kayu2.jpg", texture[20])


# Specular Part (doubt will use it? but imma include it nontheless)?

# image = upload_texture_utama("TEXTURE/wall.jpg", texture[3]) 
# # img_data = image.convert("RGBA").tobytes()
# glBindTexture( GL_TEXTURE_2D, specularMap)
# # glTexImage2D( GL_TEXTURE_2D, 0, GL_RGB, textureLebar_layar, textureTinggi_layar, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)
# glGenerateMipmap( GL_TEXTURE_2D )
# # SOIL_free_image_data( image )
# glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT )
# glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT )
# glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR )
# glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

# glUseProgram(lightingShader)

# glUniform1i( glGetUniformLocation( lightingShader, "material.diffuse"), 0)
# glUniform1i( glGetUniformLocation( lightingShader, "material.specular"), 1)



# This part is the main loop, the core of the program

while not glfw.window_should_close(jendela_utama):
      
      glfw.poll_events()
      pergerakan_keyboard()

      glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)


      # This part is the usage of lighting shader, to render everything using the lighting shader
      # Lighting
      glUseProgram(lightingShader) #Harus diupdate juga untuk lighting

      view = kamera_utama.call_matrix_view_camera()

      lightPosLoc = glGetUniformLocation( lightingShader, "light.position" )
      viewPosLoc = glGetUniformLocation( lightingShader, "viewPos" )
      glUniform3f(lightPosLoc, lightPos[0], lightPos[1], lightPos[2])
      glUniform3f( viewPosLoc, viewPosCam[0], viewPosCam[1], viewPosCam[2])

      glUniform3f( glGetUniformLocation( lightingShader, "light.ambient"), 0.1, 0.1, 0.1)
      glUniform3f( glGetUniformLocation( lightingShader, "light.diffuse"), 1.0, 1.0, 1.0)
      glUniform3f( glGetUniformLocation( lightingShader, "light.specular"), 1.0, 1.0, 1.0)

      glUniform1f( glGetUniformLocation( lightingShader, "material.shininess"), 32.0)

      modelLoc = glGetUniformLocation(lightingShader, "model")
      viewLoc = glGetUniformLocation(lightingShader, "view")
      projLoc = glGetUniformLocation(lightingShader, "projection")


      #this one too moved into resize for better jendela_utama management
      glUniformMatrix4fv(projLoc, 1, GL_FALSE, proyeksi_utama) # Harus diupdate untuk lighing
      glUniformMatrix4fv(viewLoc, 1, GL_FALSE, view) #Harus diupdate untuk lighting

      
      glActiveTexture( GL_TEXTURE0 ) 
      glBindTexture( GL_TEXTURE_2D, diffuseMap )
      glBindTexture( GL_TEXTURE_2D, 0)

      
      
      for vao, texture_index, model_matrix, indices in objects:
           draw_object(vao, texture_index, model_matrix, indices)


      # This one then is for rendering the lamp model, so that the objects can get light
      # Lamp

      glUseProgram(lampShader)
      
      modelLocLamp = glGetUniformLocation(lampShader, "model")
      viewLocLamp = glGetUniformLocation(lampShader, "view")
      projLocLamp = glGetUniformLocation(lampShader, "projection")

      glUniformMatrix4fv(viewLocLamp, 1, GL_FALSE, view)
      glUniformMatrix4fv(projLocLamp, 1, GL_FALSE, proyeksi_utama)

      model = pyrr.Matrix44.identity()  # Create an identity matrix
      translation = pyrr.matrix44.create_from_translation(lightPos)  # Create a translation matrix
      scale = pyrr.matrix44.create_from_scale(np.array([0.2, 0.2, 0.2]))  # Create a scale matrix
      
      model = np.dot(model, translation)  # Combine translation with model matrix
      model = np.dot(model, scale)
          
      glUniformMatrix4fv(modelLocLamp, 1, GL_FALSE, model)
      glBindVertexArray(lightVAO)
      glDrawArrays( GL_TRIANGLES, 0, 36 )
      glBindVertexArray(0)

      glfw.swap_buffers(jendela_utama)

# This part is for terminating glfw, cleaning it's garbage
glfw.terminate()