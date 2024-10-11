# 03.LAA_ObtencionCoordenadas

# Este Script no es funcional si no se combina con 01.LAA_ObtencionMallado.py y 02.LAA_VisualizacionMallado.py
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