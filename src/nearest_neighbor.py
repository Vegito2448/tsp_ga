# nearest_neighbor.py
# Implementa la heurística del vecino más cercano (Nearest Neighbor)
# Idea: desde la ciudad actual, siempre ir a la ciudad más cercana NO visitada

import time  # Para medir cuánto tarda

def nearest_neighbor(dist_matrix, start_city=0):
    """
    Construye una ruta usando la heurística del vecino más cercano.

    Parámetros:
    - dist_matrix: matriz de distancias (numpy array 2D)
    - start_city: ciudad desde donde se empieza (por defecto, ciudad 0)

    Retorna:
    - route: lista con el orden de visita de ciudades [0, 3, 7, ...]
    - total_dist: costo total del recorrido
    - elapsed: tiempo en segundos que tardó
    """
    start_time = time.time()  # Guardamos el tiempo de inicio

    n = len(dist_matrix)       # Número de ciudades
    visited = [False] * n      # Lista de booleanos: visited[i]=True si ya visitamos ciudad i
    route = [start_city]       # Empezamos la ruta desde la ciudad inicial
    visited[start_city] = True # Marcamos la ciudad inicial como visitada

    current = start_city       # La ciudad donde estamos parados actualmente

    # Repetimos n-1 veces (porque ya tenemos 1 ciudad en la ruta)
    for _ in range(n - 1):
        best_dist = float('inf')  # Inicializamos con infinito (cualquier distancia será menor)
        best_city = -1             # La mejor ciudad vecina que encontremos

        # Revisamos todas las ciudades posibles
        for j in range(n):
            # Solo consideramos ciudades no visitadas con distancia > 0
            if not visited[j] and dist_matrix[current][j] > 0:
                if dist_matrix[current][j] < best_dist:
                    best_dist = dist_matrix[current][j]  # Actualizamos la mejor distancia
                    best_city = j                         # Y la mejor ciudad

        route.append(best_city)      # Agregamos la ciudad elegida a la ruta
        visited[best_city] = True    # La marcamos como visitada
        current = best_city          # Nos movemos a esa ciudad

    elapsed = time.time() - start_time  # Calculamos el tiempo transcurrido

    # Calculamos el costo total: suma de distancias entre ciudades consecutivas + regreso al inicio
    total_dist = route_cost(route, dist_matrix)

    return route, total_dist, elapsed


def route_cost(route, dist_matrix):
    """
    Calcula el costo total de una ruta (suma de todas las distancias).

    La ruta es un ciclo: después de la última ciudad, regresamos a la primera.
    Ejemplo: [0, 3, 7, 2] → dist(0,3) + dist(3,7) + dist(7,2) + dist(2,0)
    """
    total = 0
    n = len(route)

    for i in range(n):
        # route[i] es la ciudad actual
        # route[(i+1) % n] es la siguiente ciudad
        # El operador % (módulo) hace que después de la última ciudad, volvamos a la primera
        # Ejemplo: i=3, n=4 → (3+1)%4 = 0 → regresamos al inicio
        city_a = route[i]
        city_b = route[(i + 1) % n]
        total += dist_matrix[city_a][city_b]

    return total
