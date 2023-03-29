
#version 330 core

layout(location = 0) out vec4 color;

uniform int degU;
uniform int degV;
uniform float startU;
uniform float startV;
uniform float endU;
uniform float endV;
uniform vec3 pts[16];

uniform vec4 u_Color;


void main()
{
	color = u_Color;
};