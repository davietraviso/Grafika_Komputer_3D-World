import glfw
from OpenGL.GL import *
import numpy as np

# Deklarasi vertices yang sudah ada
existing_vertices = np.array([
    [-0.8, -0.8],
    [-0.6, -0.6],
    [-0.4, -0.4],
    [-0.2, -0.2],
    [0.0, 0.0],
    [0.2, 0.2],
    [0.4, 0.4],
    [0.6, 0.6],
    [0.8, 0.8]
])

# Titik kontrol untuk kurva bezier
control_points = np.array([
    [-0.5, -0.5],
    [-0.2, 0.5],
    [0.2, 0.5],
    [0.5, -0.5]
])

# Fungsi untuk menghitung posisi titik pada kurva bezier
def bezier_curve(t):
    return (1-t)**3 * control_points[0] + 3*(1-t)**2 * t * control_points[1] + 3*(1-t) * t**2 * control_points[2] + t**3 * control_points[3]

# Fungsi untuk menggabungkan kurva bezier dengan vertices yang sudah ada
def combine_curve_with_vertices(vertices):
    curve_points = []
    for t in np.linspace(0, 1, 100):
        point = bezier_curve(t)
        curve_points.append(point)
    combined_vertices = np.concatenate((vertices, np.array(curve_points)))
    return combined_vertices

# Fungsi untuk merender objek gabungan
def render_combined_object(combined_vertices):
    glColor3f(1.0, 1.0, 1.0)  # warna objek
    glBegin(GL_POINTS)
    for vertex in combined_vertices:
        glVertex2f(vertex[0], vertex[1])
    glEnd()

# Fungsi utama untuk menjalankan aplikasi
def main():
    if not glfw.init():
        return

    window = glfw.create_window(800, 600, "Combined Object", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)

    while not glfw.window_should_close(window):
        glfw.poll_events()

        glClear(GL_COLOR_BUFFER_BIT)

        # Gabungkan kurva bezier dengan vertices yang sudah ada
        combined_vertices = combine_curve_with_vertices(existing_vertices)
    
        # Panggil fungsi untuk merender objek gabungan
        render_combined_object(combined_vertices)

        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()
