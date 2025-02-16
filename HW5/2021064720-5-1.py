import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import pdb

camAng = .5
camHeight = 1.
gVertexArrayIndexed = None
gIndexArray = None

def drawFrame():
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex3fv(np.array([0., 0., 0.]))
    glVertex3fv(np.array([1., 0., 0.]))
    glColor3ub(0, 255, 0)
    glVertex3fv(np.array([0., 0., 0.]))
    glVertex3fv(np.array([0., 1., 0.]))
    glColor3ub(0, 0, 255)
    glVertex3fv(np.array([0., 0., 0]))
    glVertex3fv(np.array([0., 0., 1.]))
    glEnd()

def createArray():
    varr = np.array([
        (0, 0, 0),
        (1.5, 0, 0),
        (0, 1.5, 0),
        (0, 0, 1.5),
        ], 'float32')
    iarr = np.array([
        (0, 1, 2),
        (0, 2, 3),
        (0, 1, 3),
        (2, 3, 1)
        ])
    return varr, iarr

def drawPyramid():
    global gVertexArrayIndexed, gIndexArray
    varr = gVertexArrayIndexed
    iarr = gIndexArray
    glEnableClientState(GL_VERTEX_ARRAY)
    glVertexPointer(3, GL_FLOAT, 3*varr.itemsize, varr)
    glDrawElements(GL_TRIANGLES, iarr.size, GL_UNSIGNED_INT, iarr)

def render():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

    glLoadIdentity()
    gluPerspective(45, 1, 1, 10)
    gluLookAt(4*np.sin(camAng), camHeight, 4*np.cos(camAng), 0, 0, 0, 0, 1, 0)

    drawFrame()
    glColor3ub(255, 255, 255)
    drawPyramid()

def key_callback(window, key, scancode, action, mods):
    global camAng, camHeight

    if action == glfw.PRESS or action == glfw.REPEAT:
        if key == glfw.KEY_1:
            camAng += np.radians(-10)
        elif key == glfw.KEY_3:
            camAng += np.radians(10)
        elif key == glfw.KEY_2:
            camHeight += .1
        elif key == glfw.KEY_W:
            camHeight -= .1

def main():
    global M, gVertexArrayIndexed, gIndexArray
    gVertexArrayIndexed, gIndexArray = createArray()
    if not glfw.init():
        return
    window = glfw.create_window(480, 480, "2021064720-5-1", None, None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)
    glfw.swap_interval(1)
    while not glfw.window_should_close(window):
        glfw.poll_events()
        render()
        glfw.swap_buffers(window)
    glfw.terminate()


if __name__ == "__main__":
    main()
