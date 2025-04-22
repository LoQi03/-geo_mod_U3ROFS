from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np
import math
from src import perlin

# Window and terrain parameters
_width, _height = 800, 600
_terrain_size = 50
_scale = 10.0

# Camera parameters
_angle_x = 45
_angle_y = 30
_distance = 100

def _generate_heightmap():
    """
    Generates a heightmap using Perlin noise.
    Returns:
        numpy.ndarray: A 2D array of terrain heights.
    """
    heightmap = np.zeros((_terrain_size, _terrain_size))
    for x in range(_terrain_size):
        for y in range(_terrain_size):
            nx = x / _scale
            ny = y / _scale
            height_val = perlin.noise(nx, ny)
            heightmap[x][y] = int((height_val + 1) * 5)  # Scale to range 0–10
    return heightmap

_heightmap = _generate_heightmap()

def _draw_cube(x, y, z):
    """
    Draws a single cube at the given coordinates.
    """
    size = 1
    glPushMatrix()
    glTranslatef(x, y, z)
    glutSolidCube(size)
    glPopMatrix()

def _draw_terrain():
    """
    Draws the terrain using stacked cubes based on the heightmap.
    """
    max_height = np.max(_heightmap)
    for x in range(_terrain_size):
        for y in range(_terrain_size):
            h = int(_heightmap[x][y])
            for z in range(h):  # Stack cubes up to the height
                brightness = 1.0 - (z / max_height)  # Darker at higher levels
                glColor3f(0.6 * brightness, 0.8 * brightness, 0.3 * brightness)
                _draw_cube(x - _terrain_size // 2, z, y - _terrain_size // 2)

def _display():
    """
    Display callback for rendering the terrain.
    """
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    eye_x = _distance * math.sin(math.radians(_angle_x)) * math.cos(math.radians(_angle_y))
    eye_y = _distance * math.sin(math.radians(_angle_y))
    eye_z = _distance * math.cos(math.radians(_angle_x)) * math.cos(math.radians(_angle_y))
    gluLookAt(eye_x, eye_y, eye_z, 0, 0, 0, 0, 1, 0)

    _draw_terrain()

    glutSwapBuffers()

def _reshape(w, h):
    """
    Reshape callback to handle window resizing.
    """
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, float(w) / float(h), 0.1, 500.0)
    glMatrixMode(GL_MODELVIEW)

def _keyboard(key, x, y):
    """
    Keyboard callback to control the camera angle.
    """
    global _angle_x, _angle_y
    if key == b'a':
        _angle_x -= 5
    elif key == b'd':
        _angle_x += 5
    elif key == b'w':
        _angle_y += 5
    elif key == b's':
        _angle_y -= 5
    glutPostRedisplay()

def _init():
    """
    Initializes OpenGL settings.
    """
    glEnable(GL_DEPTH_TEST)
    glClearColor(0.5, 0.7, 1.0, 1.0)  # Sky blue background

def main():
    """
    Entry point to start the OpenGL application.
    """
    glutInit()
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(_width, _height)
    glutCreateWindow(b"3D Perlin Terrain")

    _init()
    glutDisplayFunc(_display)
    glutReshapeFunc(_reshape)
    glutKeyboardFunc(_keyboard)
    glutMainLoop()

if __name__ == "__main__":
    main()
