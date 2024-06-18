from OpenGL.GL import *
from OpenGL.GL import glBindTexture, glTexParameteri, GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, \
    GL_TEXTURE_WRAP_T, GL_REPEAT, GL_TEXTURE_MIN_FILTER, GL_TEXTURE_MAG_FILTER, GL_LINEAR,\
    glTexImage2D, GL_RGBA, GL_UNSIGNED_BYTE
import pyrr
from PIL import Image


# GLFW is very usable in here
def upload_texture_utama(sumber_data, detail_gambar):

    glBindTexture(GL_TEXTURE_2D, detail_gambar)

    # Setting the wrapping paramteres for these textures
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)

    # Also setting the filtering parameters for these textures
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    # And here part is for loading texture imageries
    gambar_utama= Image.open(sumber_data)
    
    gambar_utama= gambar_utama.transpose(Image.FLIP_TOP_BOTTOM)

    data_gambar = gambar_utama.convert("RGBA").tobytes()

    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, gambar_utama.width, gambar_utama.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, data_gambar)

    return detail_gambar