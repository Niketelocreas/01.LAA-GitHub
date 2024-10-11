# LAA_ScriptCompleto
# Lanzar script usando vtk_env, disponible en la carpeta Environments
#01.LAA-Scripting - Obtención del Mallado

# Obtención de los puntos sobre el mallado
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

# 02.LAA_VisualizaciónMallado
# Visualización de los dos mallados en conjunto
plotter = pv.Plotter(shape=(1, 2))
plotter.subplot(0, 0)
plotter.add_mesh(manual_mesh, color='red', opacity=0.5, show_edges=True)
plotter.add_text("Manual", font_size=12)

plotter.subplot(0, 1)
plotter.add_mesh(auto_mesh, color='blue', opacity=0.5, show_edges=True)
plotter.add_text("Automático", font_size=12)

plotter.show()

# Una vez se cierre esta primera visualización, aparecerá la segunda con los puntos más cercanos marcados

# Visualización de los puntos más cercanos 
plotter = pv.Plotter(shape=(1, 2))

# Subplot para la malla manual
plotter.subplot(0, 0)
plotter.add_mesh(manual_mesh, color='red', opacity=0.5, show_edges=True)
plotter.add_text("Manual", font_size=12)
plotter.add_points(closest_point_manual, color='yellow', point_size=10, render_points_as_spheres=True)

# Subplot para la malla automática
plotter.subplot(0, 1)
plotter.add_mesh(auto_mesh, color='blue', opacity=0.5, show_edges=True)
plotter.add_text("Automático", font_size=12)
plotter.add_points(closest_point_auto, color='yellow', point_size=10, render_points_as_spheres=True)

# Mostrar la visualización
plotter.show()

### Calcular las distancias desde cada punto del modelo manual al punto más cercano del modelo automático
distances = []
for point in manual_mesh.points:
    distances.append(np.min(np.linalg.norm(auto_mesh.points - point, axis=1)))

# Añadir las distancias como un campo escalar en la malla manual
manual_mesh['Distances'] = distances

# Visualizar el mapa de distancias en el modelo manual
plotter = pv.Plotter()
plotter.add_mesh(manual_mesh, scalars='Distances', cmap='viridis', show_edges=True)
plotter.add_scalar_bar(title='Distancia al modelo automático')
plotter.show()


# Mostrar información adicional
print(f"Centro de masas del modelo manual: {manual_mesh.center_of_mass()}")
print(f"Centro de masas del modelo automático: {auto_mesh.center_of_mass()}")

# Prueba Obtención de Coordenadas
## Cálculo del perímetro de la base y del punto central del plano

# Variable global para almacenar las coordenadas del punto de la base seleccionado
last_point_coordinates = None

# Definir la función de devolución de llamada para manejar los clics
def on_click(point):
    global last_point_coordinates
    if point is not None:
        last_point_coordinates = point
        print(f"Coordenadas del punto en la base: {point}")

# Crear el objeto Plotter
plotter = pv.Plotter()

# Agregar la malla manual
plotter.add_mesh(manual_mesh, color='red', opacity=0.5, show_edges=True)
plotter.add_text("Manual", font_size=12)

# Configurar la función de devolución de llamada para el clic
plotter.enable_point_picking(callback=on_click, show_message=True, font_size=12)

# Mostrar la visualización
plotter.show()

base_point_coordinates = last_point_coordinates 


# Después de cerrar la visualización, puedes acceder a las coordenadas del último punto seleccionado
print(f"Coordenadas del punto seleccionado en la base: {base_point_coordinates}")

# Si se seleccionó un punto, calcula el perímetro del plano y el punto central
if base_point_coordinates is not None:
    # Encuentra los puntos más cercanos en la malla manual
    point_id = manual_mesh.find_closest_point(base_point_coordinates)
    neighbors = manual_mesh.extract_surface().extract_feature_edges().point_neighbors(point_id)

    # Obtén las coordenadas de los puntos vecinos
    neighbor_points = manual_mesh.points[neighbors]

    # Calcula el perímetro del polígono formado por los puntos vecinos
    perimeter = 0
    for i in range(len(neighbor_points)):
        p1 = neighbor_points[i]
        p2 = neighbor_points[(i + 1) % len(neighbor_points)]
        perimeter += np.linalg.norm(p1 - p2)

    # Calcula el punto central (centroide) del polígono
    centroid = np.mean(neighbor_points, axis=0)

    print(f"Perímetro de la base: {perimeter}")
    print(f"Punto central de la base: {centroid}")
else:
    print("No se ha seleccionado ningún punto.")

# Espacio para la selección del punto más alejado de la base y su uso para el centre line
# Variable global para almacenar las coordenadas del punto más alejado
last_point_coordinates = None

# Crear el objeto Plotter
plotter = pv.Plotter()

# Agregar la malla manual
plotter.add_mesh(manual_mesh, color='red', opacity=0.5, show_edges=True)
plotter.add_text("Manual", font_size=12)

# Configurar la función de devolución de llamada para el clic
plotter.enable_point_picking(callback=on_click, show_message=True, font_size=12)

# Mostrar la visualización
plotter.show()

farthest_point_coordinates = last_point_coordinates

# Después de cerrar la visualización, puedes acceder a las coordenadas del último punto seleccionado
print(f"Últimas coordenadas del punto seleccionado: {farthest_point_coordinates}")

"""Este script no se ha podido desarrollar en mayor profundidad por falta de tiempo.
Queda explorar la adición de un center line para categorizar las orejuelas segun su conformación"""