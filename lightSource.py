from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader

def light_function():
    light_vertex_src = """
    # version 330 core

    layout(location = 0) in vec3 a_position;
    layout(location = 1) in vec3 a_normal;
    layout(location = 2) in vec2 a_texture;

    out vec3 Normal;
    out vec3 FragPos;
    out vec2 v_texture;

    uniform mat4 model;
    uniform mat4 view;
    uniform mat4 projection;

    void main()
    {
        gl_Position = projection * view *  model * vec4(a_position, 1.0);
        FragPos = vec3(model * vec4(a_position, 1.0));
        Normal = mat3(transpose(inverse(model))) * a_normal;
        v_texture = a_texture;
    }
    """

    light_fragmen_src = """
    #version 330 core

    struct Material 
    {
        sampler2D diffuse;
        sampler2D specular;
        float shininess;
    };

    struct Light
    {
        vec3 position;
        
        vec3 ambient;
        vec3 diffuse;
        vec3 specular;
    };

    in vec3 FragPos;
    in vec3 Normal;
    in vec2 v_texture;
    
    uniform vec3 viewPos;
    uniform Material material;
    uniform Light light;

    out vec4 FragColor;

    void main()
    {
        // ambient
        vec3 ambient = light.ambient * vec3(texture(material.diffuse, v_texture));

        // diffuse
        vec3 norm = normalize(Normal);
        vec3 lightDir = normalize(light.position - FragPos); // Corrected assignment
        float diff = max(dot(norm, lightDir), 0.0);
        vec3 diffuse = light.diffuse * diff * vec3(texture(material.diffuse, v_texture));

        // specular
        vec3 viewDir = normalize(viewPos - FragPos);
        vec3 reflectDir = reflect(-lightDir, norm);
        float spec = pow(max(dot(viewDir, reflectDir), 0.0), material.shininess);
        vec3 specular = light.specular * spec * vec3(texture(material.specular, v_texture));

        FragColor = vec4(ambient + diffuse + specular, 1.0); // Corrected variable name
    }

    """
    return light_vertex_src, light_fragmen_src