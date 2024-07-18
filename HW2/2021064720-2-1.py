import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

dic = {'1': GL_POINTS, '2': GL_LINES, '3': GL_LINE_STRIP, '4': GL_LINE_LOOP,
       '5': GL_TRIANGLES, '6': GL_TRIANGLE_STRIP, '7': GL_TRIANGLE_FAN,
       '8': GL_QUADS, '9': GL_QUAD_STRIP, '0': GL_POLYGON}
ptype = GL_LINE_LOOP


def render():
    global ptype
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    glBegin(ptype)
    glColor3ub(255, 255, 255)
    for i in range(0, 12):
        th = np.radians(i * 30)
        r = np.array([[np.cos(th), -np.sin(th)],
                      [np.sin(th), np.cos(th)]])
        glVertex2fv(r @ [1., 0.])
    glEnd()


def key_callback(window, key, scancode, action, mods):
    global ptype
    if action == glfw.PRESS:
        # print(key)
        ptype = dic[chr(key)]


def main():

    # Initialize the library
    if not glfw.init():
        return
    # Create a windowed mode window and its OpenGL context
    window = glfw.create_window(480, 480, "2021064720-2-1", None, None)
    if not window:
        glfw.terminate()
        return
        
    # Make the window's context current
    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)

    # Loop until the user closes the window
    while not glfw.window_should_close(window):
        # Poll events
        glfw.poll_events()

        render()

        # Swap front and back buffers
        glfw.swap_buffers(window)

    glfw.terminate()


if __name__ == "__main__":
    main()
