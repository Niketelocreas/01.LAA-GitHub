# 01.LAA-GitHub
Proyecto: Cálculo de Base y Punto más Cercano en Mallados
Este proyecto realiza el cálculo de propiedades de mallados (área, volumen, centro de masas) y determina los puntos más cercanos entre dos mallados a partir de sus centros de masas. Utiliza PyVista para la visualización y manipulación de archivos VTK.

Descripción
El objetivo del proyecto es comparar dos mallados (uno generado manualmente y otro automáticamente) representados en formato VTK, y calcular sus propiedades fundamentales. Además, se determina el punto más cercano entre los mallados tomando como referencia sus centros de masas. La visualización de ambos mallados permite una fácil interpretación de los resultados.

Funcionalidades
Carga y visualización de mallados VTK: Se leen los archivos VTK desde un directorio y se almacenan en un diccionario para su posterior uso.
Cálculo de propiedades:
Volumen
Área
Centro de masas
Determinación de puntos más cercanos: Se identifican los puntos más cercanos en cada mallado respecto al centro de masas del otro mallado.
Visualización 3D de los mallados: Se utilizan gráficos interactivos para mostrar los mallados superpuestos o de forma separada.

