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
    out vec4 FragPosLightSpace;

    uniform mat4 model;
    uniform mat4 view;
    uniform mat4 projection;
    uniform mat4 lightSpaceMatrix;

    uniform mat4 camMatrix;

    uniform float scale;
    uniform vec3 translation;
    uniform mat4 rotation;

    uniform mat4 lightProjection;

    void main()
    {
        FragPos = vec3(vec4(a_position, 1.0));
        
        vec4 pos = vec4(a_position + a_position * scale, 1.0);
        pos = rotation * pos;
        pos = pos + vec4(translation, 0.0);

        FragPosLightSpace = lightProjection * pos;

        gl_Position = camMatrix * pos;


        // gl_Position = projection * view *  model * vec4(a_position, 1.0);
        // FragPos = vec3(model * vec4(a_position, 1.0));
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
        vec3 direction;
        vec3 position;

        vec4 color;
        
        vec3 ambient;
        vec3 diffuse;
        vec3 specular;
    };

    float ShadowCalculation(vec4 FragPosLightSpace, vec3 Normal, vec3 light.direction)
    {
        // Perform perspective divide
        vec3 projCoords = FragPosLightSpace.xyz / FragPosLightSpace.w;
        // Transform to [0,1] range
        projCoords = projCoords * 0.5 + 0.5;
        
        // Check if the projected coordinates are outside the [0, 1] range
        if(projCoords.z > 1.0)
            return 0.0;

        // Get depth of current fragment from light's perspective
        float currentDepth = projCoords.z;

        // Bias to avoid shadow acne
        float bias = max(0.005 * (1.0 - dot(Normal, light.direction)), 0.005);

        // PCF kernel size
        float shadow = 0.0;
        vec2 texelSize = 1.0 / textureSize(shadowMap, 0);
        for(int x = -1; x <= 1; ++x)
        {
            for(int y = -1; y <= 1; ++y)
            {
                float pcfDepth = texture(shadowMap, projCoords.xy + vec2(x, y) * texelSize).r; 
                shadow += currentDepth - bias > pcfDepth ? 1.0 : 0.0;
            }
        }
        shadow /= 9.0; // Averaging the 3x3 kernel results

        // Clamp shadow to [0,1]
        shadow = clamp(shadow, 0.0, 1.0);

        return shadow;
    }

    in vec3 FragPos;
    in vec3 Normal;
    in vec2 v_texture;
    in vec4 FragPosLightSpace;
    
    uniform sampler2D tex0;
    uniform sampler2D shadowMap;

    uniform vec3 viewPos;
    uniform Material material;
    uniform Light light;
    uniform vec3 camPos;

    out vec4 FragColor;

    void main()
    {
        // ambient
        vec3 ambient = 0,4;

        // diffuse
        vec3 norm = normalize(Normal);

        //vec3 lightDir = normalize(light.position - FragPos); // Corrected assignment

        vec3 lightDir = normalize(light.position - FragPos);
        float diff = max(dot(norm, lightDir), 0.0);
        // vec3 diffuse = light.diffuse * diff * vec3(texture(material.diffuse, v_texture));

        if(diff != 0.0 )
        {
            // specular
            float specularLight = 0.5;
            vec3 viewDir = normalize(viewPos - FragPos);
            vec3 reflectDir = reflect(-lightDir, norm);

            vec3 halfLightVec = normalize(viewDir + lightDir);

            float specAmount = pow(max(dot(norm, halfLightVec), 0.0), material.shininess);
            vec3 specular = specAmount * specularLight;

        }
        
        float shadow = ShadowCalculation(FragPosLightSpace, norm, lightDir);

        FragColor = texture(tex0, v_texture) * light.color * (diff * (1.0 - shadow) + ambient + specular);
    }

    """
    return light_vertex_src, light_fragmen_src