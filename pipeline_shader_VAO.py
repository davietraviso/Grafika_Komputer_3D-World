import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import numpy as np

def shader_function():
    vertex_src = """
    # version 330 core

    layout(location = 0) in vec3 a_position;
    layout(location = 1) in vec2 a_texture;
    layout(location = 2) in vec3 a_color; //for color shapes
    
    uniform mat4 model; // will be combined translation and rotation
    uniform mat4 projection;
    uniform mat4 view;

    out vec3 v_color;
    out vec2 v_texture;

    void main()
    {
        gl_Position = projection * view * model * vec4(a_position, 1.0);
        v_texture = a_texture;
        v_color = a_color;

        //v_texture = 1 - a_texture; // for flippin the image vertical and horizontal
        //v_texture = vec2(a_texture.s, 1 - a_texture.t); //for flippin the image vertically
    }
    """

    fragmen_src = """
    # version 330 core

    in vec3 v_color;
    in vec2 v_texture;

    out vec4 out_color;
    uniform int switcher;

    uniform sampler2D s_texture;

    void main()
    {
        //now we're using if else function using switcher
        if(switcher == 0){
            out_color = texture(s_texture, v_texture);    //vec4(v_color, 1.0);
        }
        else if(switcher == 1){
            out_color = vec4(v_color, 1.0);
        }
    }
    """
    return vertex_src, fragmen_src