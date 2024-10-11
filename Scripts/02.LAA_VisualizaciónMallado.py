# 02.LAA_VisualizaciónMallado 

# Este Script no es funcional si no se combina con 01.LAA_ObtencionMallado.py

# Importación de librerías
import os
import pyvista as pv
import numpy as np

# Visualización de los dos mallados en conjunto
plotter = pv.Plotter(shape=(1, 2))
plotter.subplot(0, 0)
plotter.add_mesh(manual_mesh, color='red', opacity=0.5, show_edges=True)
plotter.add_text("Manual", font_size=12)

plotter.subplot(0, 1)
plotter.add_mesh(auto_mesh, color='blue', opacity=0.5, show_edges=True)
plotter.add_text("Automático", font_size=12)

plotter.show()

# Visualización de los mallados por separado - En caso de necesitarlo
# Mallado Manual
# plotter = pv.Plotter()
# plotter.add_mesh(manual_mesh, color='red', opacity=0.5, show_edges=True)
# plotter.add_text("Manual", font_size=12)

# plotter.show()

# Mallado Automático
# plotter = pv.Plotter()
# plotter.add_mesh(auto_mesh, color='blue', opacity=0.5, show_edges=True)
# plotter.add_text("Automático", font_size=12)

# plotter.show()

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