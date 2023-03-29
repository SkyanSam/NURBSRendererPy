#version 330 core
in vec3 position;
in vec2 vertex_uv;
out vec2 fragCoord;
void main() {
    gl_Position = vec4(position.x, position.y, 0.0, 1.0);
    fragCoord = vertex_uv;
}