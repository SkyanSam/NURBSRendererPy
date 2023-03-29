#from glapp.PyOGLApp import *
#from glapp.utils import *
#from glapp.Mesh
import sys
from OpenGL.GL import *
from OpenGL.WGL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np
from shader import Shader, load_shader
from OpenGL.arrays.arraydatatype import ArrayDatatype
#from OpenGLContext.arrays import array,reshape
#from OpenGLContext import context
import objloader
import shader
import datacollection
import tesellator
from raytracetype import RaytraceType
from multiprocessing import Process, freeze_support
#context = wglCreateContext()


def showScreen():
    global last_elapsed_time
    for sindex, s in enumerate(surfaces):
        global last_elapsed_time
        id = program_ids[sindex]
        s = surfaces[sindex]
        glUseProgram(id)
        degU_id = glGetUniformLocation(id, "degU")
        degV_id = glGetUniformLocation(id, "degV")
        startU_id = glGetUniformLocation(id, "startU")
        startV_id = glGetUniformLocation(id, "startV")
        endU_id = glGetUniformLocation(id, "endU")
        endV_id = glGetUniformLocation(id, "endV")
        pts_id = glGetUniformLocation(id, "pts")
        glUniform1i(degU_id, s.degU)
        glUniform1i(degV_id, s.degV)
        glUniform1f(startU_id, s.startU)
        glUniform1f(startV_id, s.startV)
        glUniform1f(endU_id, s.endU)
        glUniform1f(endV_id, s.endV)
        glUniform3fv(pts_id, 16, s.pts)
    datacollection.append_dt((glutGet(GLUT_ELAPSED_TIME) - last_elapsed_time) / 1000)
    datacollection.append_memory()
    last_elapsed_time = glutGet(GLUT_ELAPSED_TIME)

positions, indices = tesellator.evaluate()
def show_screen_tesselated():
    draw_triangles(positions, indices)

def draw_triangles(positions, indices):
    """glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
    GL.glLoadIdentity()
    GL.glTranslate(0.0, 0.0, -50.0)
    GL.glScale(20.0, 20.0, 20.0)
    GL.glRotate(self.yRotDeg, 0.2, 1.0, 0.3)
    GL.glTranslate(-0.5, -0.5, -0.5)"""

    VERTICES = 0
    INDICES = 1
    buffers = any
    glCreateBuffers(2, buffers) # create buffers or gen buffers figure it oiut
    glBindBuffer(GL_ARRAY_BUFFER, buffers[VERTICES])
    glBufferData(GL_ARRAY_BUFFER, len(positions), positions, GL_STATIC_DRAW)
    offset = ctypes.c_void_p(0)
    glVertexPointer(3, GL_FLOAT, 0, offset)
    glEnableClientState(GL_VERTEX_ARRAY)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, buffers[INDICES])
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, len(indices), indices, GL_STATIC_DRAW)
    glDrawElements(GL_QUADS, 24, GL_UNSIGNED_BYTE, offset)
    tes_shader.use()

def on_close():
    print("Sending Sample!")
    datacollection.send_sample()
    total_m = glGetIntegerv(0x9048)
    current_m = glGetIntegerv(0x9049)


def main():
    global last_elapsed_time
    global surfaces
    global program_ids
    global vs_shader_src
    global fs_shader_src
    global tes_fs_shader_src
    global tes_vs_shader_src
    global tes_shader
    global bezier_shader
    datacollection.setGlobals()
    # Intitialize OpenGL
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitContextFlags(GLUT_CORE_PROFILE | GLUT_DEBUG)
    glutInitWindowSize(256, 256)
    glutCreateWindow(b"Research Project")
    print(glGetString(GL_VERSION))


    # Load Freeform Surface
    surfaces = objloader.ObjLoader("bezierpatch3.obj").surfaces
    program_ids = []

    vs_shader_src = open("vertexshader.vs", "r").read()
    fs_shader_src = open("fragshader.vs", "r").read()
    tes_vs_shader_src = open("tes_vertexshader.vs", "r").read()
    tes_fs_shader_src = open("tes_fragshader.vs", "r").read()

    tes_shader = Shader()
    tes_shader.compile(tes_vs_shader_src, tes_fs_shader_src)

    bezier_shader = Shader()
    bezier_shader.compile(vs_shader_src, fs_shader_src)

    last_elapsed_time = 0

    for s in surfaces:
        #program_ids.append(glCreateProgram(open("vertexshader.vs"), open("fragshader.vs")))
        shaderr = shader.Shader()
        shaderr.compile(vs_shader_src, fs_shader_src)
        program_ids.append(shaderr.program)

    

    print("begin glut!")
    glutDisplayFunc(showScreen)
    glutCloseFunc(on_close)
    glutMainLoop()

    input()
    print("application end!")

if __name__ == '__main__':
    freeze_support()
    main()