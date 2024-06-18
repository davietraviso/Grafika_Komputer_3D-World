def shadowmap_function():
    shadowmap_vertex_src = """ 
    #version 330 core

    layout(location = 0) in vec3 aPos;

    uniform mat4 lightProjection;
    uniform mat4 lightView;
    uniform mat4 model;

    void main()
    {
        gl_Position = lightProjection * lightView * model * vec4(aPos, 1.0);
    }

    """

    shadowmap_fragmen_src = """
    #version 330 core

    void main()
    {
    }
    """

    return shadowmap_vertex_src, shadowmap_fragmen_src

import glm

print("glm version:", glm.__version__)
print("glm file location:", glm.__file__)
print("glm attributes:", dir(glm))