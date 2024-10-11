#01.LAA-Scripting - Obtención del Mallado

# Obtención de los puntos sobre el mallado
# Importación de librerías
import os
import pyvista as pv
import numpy as np

# Desactivar el backend de Jupyter y forzar el uso estándar si se trabaja con Jupyter Lab o Jupyter Notebook
# pv.global_theme.notebook = False

# Directorio que contiene los archivos VTK
vtk_dir = r"C:\Users\Usuario\Desktop\NotebookCollection\Gadicor_PracticasExtracurriculares\01.LAA\01.LAA-GitHub\Espacio-Pruebas\Patient2"

# Lista de archivos VTK en el directorio
vtk_files = [os.path.join(vtk_dir, file) for file in os.listdir(vtk_dir) if file.endswith('.vtk')]

# Lectura de archivos VTK y almacenamiento en mallas
meshes = {}
for vtk_file in vtk_files:
    mesh = pv.read(vtk_file)
    meshes[os.path.basename(vtk_file)] = mesh

# Identificar el archivo manual y el automático
manual_mesh = None
auto_mesh = None

for vtk_file in vtk_files:
    if "manual" in os.path.basename(vtk_file).lower():
        manual_mesh = pv.read(vtk_file)
    else:
        auto_mesh = pv.read(vtk_file)

# Comprobación de que ambos archivos han sido identificados correctamente
if manual_mesh is None or auto_mesh is None:
    raise ValueError("No se pudo encontrar los archivos")

# Función de calculo de propiedades: volumen, area y centro de masas

def calculate_properties(mesh):
    volume = mesh.volume
    area = mesh.area
    center_of_mass = mesh.center_of_mass()
    return volume, area, center_of_mass

# Calculo de las propiedades del archivo manual
manual_volume, manual_area, manual_center_of_mass = calculate_properties(manual_mesh)

# Calculo de las propiedades del archivo automático
auto_volume, auto_area, auto_center_of_mass = calculate_properties(auto_mesh)

# Encuentra los puntos más cercanos entre las mallas desde los centros de masa
def find_closest_points_from_centers(mesh1, mesh2, center1, center2):
    points1 = mesh1.points
    points2 = mesh2.points

    # Se inicializa la distancia mínima y los puntos más cercanos para el primer bucle
    min_distance1 = float("inf")
    closest_point1 = None

    # Encontrar el punto más cercano en mesh1 al centro de masas de mesh2
    for point1 in points1:
        distance1 = np.linalg.norm(point1 - center2)
        if distance1 < min_distance1:
            min_distance1 = distance1
            closest_point1 = point1

    # Se inicializa la distancia mínima y los puntos más cercanos para el segundo bucle
    min_distance2 = float("inf")
    closest_point2 = None

    # Encontrar el punto más cercano en mesh2 al centro de masas de mesh1
    for point2 in points2:
        distance2 = np.linalg.norm(point2 - center1)
        if distance2 < min_distance2:
            min_distance2 = distance2
            closest_point2 = point2

    return closest_point1, closest_point2, min_distance1, min_distance2

# Calcular los puntos más cercanos
closest_point_manual, closest_point_auto, closest_distance_manual, closest_distance_auto = find_closest_points_from_centers(
    manual_mesh, auto_mesh, manual_center_of_mass, auto_center_of_mass
)