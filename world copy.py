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


# INDICES!!
# For connecting da dots!! 
# for each vertices is connected to where!

objects = {
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
    "wall1": (vertices_wall1, indices_wall1)
}

for name, (vertices, indices) in objects.items():
    globals()["vertices_" + name] = np.array(vertices, dtype=np.float32)
    globals()["indices_" + name] = np.array(indices, dtype=np.uint32)




shader = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER), compileShader(fragmen_src, GL_FRAGMENT_SHADER))


def create_object_VAO(vertices, indices, stride, position_offset, texture_offset):
    VAO = glGenVertexArrays(1)
    glBindVertexArray(VAO)

    # Vertex buffer object
    VBO = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

    # Element buffer object
    EBO = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

    # For vertex POSITION coordinate
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(position_offset))

    # For color / TEXTURE coordinate
    glEnableVertexAttribArray(1)
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(texture_offset))

    return VAO

# Usage 
wall_VAO = create_object_VAO(vertices_wall, indices_wall, vertices_wall.itemsize * 5, 0, 12)
floor_VAO = create_object_VAO(vertices_floor, indices_floor, vertices_floor.itemsize * 5, 0, 12)
hook_VAO = create_object_VAO(vertices_hook, indices_hook, vertices_hook.itemsize * 5, 0, 102)
saw_VAO = create_object_VAO(vertices_saw, indices_saw, vertices_saw.itemsize * 5, 0, 12)
sawo_VAO = create_object_VAO(vertices_sawo, indices_sawo, vertices_sawo.itemsize * 5, 0, 24)
key_VAO = create_object_VAO(vertices_key, indices_key, vertices_key.itemsize * 5, 0, 24)
hammer_VAO = create_object_VAO(vertices_hammer, indices_hammer, vertices_hammer.itemsize * 5, 0, 36)
gagang_VAO = create_object_VAO(vertices_gagang, indices_gagang, vertices_gagang.itemsize * 5, 0, 24)
bor_VAO = create_object_VAO(vertices_bor, indices_bor, vertices_bor.itemsize * 5, 0, 24)
tombol_VAO = create_object_VAO(vertices_tombol, indices_tombol, vertices_tombol.itemsize * 5, 0, 24)
matabor_VAO = create_object_VAO(vertices_matabor, indices_matabor, vertices_matabor.itemsize * 5, 0, 24)
obeng_VAO = create_object_VAO(vertices_obeng, indices_obeng, vertices_obeng.itemsize * 5, 0, 24)
besiobeng_VAO = create_object_VAO(vertices_besiobeng, indices_besiobeng, vertices_besiobeng.itemsize * 5, 0, 24)
sledge_VAO = create_object_VAO(vertices_sledge, indices_sledge, vertices_sledge.itemsize * 5, 0, 24)
kayu_VAO = create_object_VAO(vertices_kayu, indices_kayu, vertices_kayu.itemsize * 5, 0, 24)
wall1_VAO = create_object_VAO(vertices_wall1, indices_wall1, vertices_wall1.itemsize * 5, 0, 12)



# ~~ END HERE ~~

# The value here define how many texture we want to create
texture = glGenTextures(20)

# LOADING HTE IMAGES USING TEXTURELOADER
# array here related to glGenTextures above!
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
wall1 = load_texture("TEXTURE/wall2.jpg", texture[14])

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
wall = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 3, -2]))
floor = pyrr.matrix44.create_from_translation(pyrr.Vector3([-0.2, 2.2, -2]))
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
wall1 = pyrr.matrix44.create_from_translation(pyrr.Vector3([-0.2, 2.2, -2]))


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

scaling_floor = scaling @ floor
floor = scaling_floor

scaling_wall1 = scaling @ wall1
wall1 = scaling_wall1

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

# Data originally from the main loop

def draw_object(vao, texture_index, model_matrix, indices):
    glBindVertexArray(vao)
    glBindTexture(GL_TEXTURE_2D, texture[texture_index])
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, model_matrix)
    glDrawElements(GL_TRIANGLES, len(indices), GL_UNSIGNED_INT, None)

# Store information about each object
objects = [
    (wall_VAO, 3, wall, indices_wall),
    (floor_VAO, 2, floor, indices_floor),
    (hook_VAO, 1, hook, indices_hook),
    (saw_VAO, 0, saw, indices_saw),
    (sawo_VAO, 4, old_sawo, indices_sawo),
    (key_VAO, 5, key, indices_key),
    (hammer_VAO, 6, hammer, indices_hammer),
    (gagang_VAO, 7, gagang, indices_gagang),
    (bor_VAO, 8, bor, indices_bor),
    (tombol_VAO, 8, tombol, indices_tombol),
    (matabor_VAO, 9, matabor, indices_matabor),
    (obeng_VAO, 11, obeng, indices_obeng),
    (besiobeng_VAO, 11, besiobeng, indices_besiobeng),
    (sledge_VAO, 11, sledge, indices_sledge),
    (kayu_VAO, 13, kayu, indices_kayu),
    (wall1_VAO, 14, wall1, indices_wall1)
]

# The main application loop
while not glfw.window_should_close(window):
      glfw.poll_events()
      do_movement()

      view = cam.get_view_matrix()
      glUniformMatrix4fv(view_loc, 1, GL_FALSE, view)

      glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

      glUniform1i(switcher_loc, 0)

      for vao, texture_index, model_matrix, indices in objects:
           draw_object(vao, texture_index, model_matrix, indices)
           
      glfw.swap_buffers(window)

# For terminating glfw
glfw.terminate()