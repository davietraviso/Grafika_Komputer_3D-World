from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader

def lamp_function():
    lamp_vertex_src = """
    # version 330 core

    layout(location = 0) in vec3 a_position;

    uniform mat4 model;
    uniform mat4 view;
    uniform mat4 projection;


    void main()
    {
        gl_Position = projection * view * model * vec4(a_position, 1.0);
    }
    """

    lamp_fragmen_src = """
    # version 330 core

    out vec4 FragColor;

    void main()
    {
        FragColor = vec4(1.0);
    }
    """
    return lamp_vertex_src, lamp_fragmen_src