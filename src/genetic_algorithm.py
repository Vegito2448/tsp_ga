# genetic_algorithm.py
# Implementación de un Algoritmo Genético para el TSP
#
# CONCEPTOS CLAVE:
# - Individuo / Cromosoma: una ruta completa, representada como lista de ciudades
#   Ejemplo para 5 ciudades: [2, 0, 4, 1, 3] significa "visitar en ese orden"
# - Población: un conjunto de individuos (muchas rutas candidatas)
# - Fitness: qué tan bueno es un individuo (usamos 1/costo, más alto = mejor)
# - Selección: elegir los mejores individuos para reproducirse
# - Cruce (Crossover): combinar dos rutas para crear una nueva
# - Mutación: hacer un pequeño cambio aleatorio en una ruta

import random
import time
import copy
from src.nearest_neighbor import route_cost  # Reutilizamos la función de costo


# ─────────────────────────────────────────────
# INICIALIZACIÓN DE LA POBLACIÓN
# ─────────────────────────────────────────────

def create_individual(n):
    """
    Crea un individuo aleatorio: una permutación aleatoria de 0 a n-1.
    Ejemplo para n=5: podría devolver [3, 0, 4, 1, 2]
    """
    individual = list(range(n))   # Crea [0, 1, 2, ..., n-1]
    random.shuffle(individual)    # Mezcla aleatoriamente: ej. [3, 0, 4, 1, 2]
    return individual


def create_population(pop_size, n):
    """
    Crea una población de `pop_size` individuos aleatorios.

    Parámetros:
    - pop_size: cuántos individuos tendrá la población
    - n: número de ciudades

    Retorna: lista de individuos (lista de listas)
    """
    return [create_individual(n) for _ in range(pop_size)]
    # Esta es una "list comprehension": equivale a:
    # population = []
    # for _ in range(pop_size):
    #     population.append(create_individual(n))
    # return population


# ─────────────────────────────────────────────
# FITNESS (APTITUD)
# ─────────────────────────────────────────────

def fitness(individual, dist_matrix):
    """
    Calcula el fitness de un individuo.
    Como queremos MINIMIZAR el costo, el fitness es el recíproco del costo.
    Un costo bajo → fitness alto → mejor individuo.
    """
    cost = route_cost(individual, dist_matrix)
    return 1.0 / cost  # Evitamos división por cero porque ninguna ruta tiene costo 0


def evaluate_population(population, dist_matrix):
    """
    Evalúa todos los individuos de la población.
    Retorna lista de tuplas (fitness, individuo) ordenada de mayor a menor fitness.
    """
    evaluated = []
    for ind in population:
        fit = fitness(ind, dist_matrix)      # Calculamos el fitness
        evaluated.append((fit, ind))          # Guardamos como tupla (fitness, individuo)

    # sorted() ordena la lista; reverse=True = de mayor a menor
    # key=lambda x: x[0] significa "ordenar por el primer elemento de la tupla (el fitness)"
    evaluated.sort(key=lambda x: x[0], reverse=True)
    return evaluated


# ─────────────────────────────────────────────
# SELECCIÓN: TORNEO
# ─────────────────────────────────────────────

def tournament_selection(evaluated_pop, tournament_size=3):
    """
    Selección por torneo: elegimos `tournament_size` individuos al azar
    y devolvemos el mejor de ese grupo.

    Es una forma de selección que favorece a los mejores pero con cierta
    presión selectiva ajustable (más grande el torneo → más presión).
    """
    # Elegimos `tournament_size` índices aleatorios sin repetición
    participants = random.sample(evaluated_pop, tournament_size)
    # El ganador es el de mayor fitness (primer elemento de la tupla)
    winner = max(participants, key=lambda x: x[0])
    return winner[1]  # Devolvemos solo el individuo (la ruta), no el fitness


# ─────────────────────────────────────────────
# CRUCE: ORDER CROSSOVER (OX1)
# ─────────────────────────────────────────────

def order_crossover(parent1, parent2):
    """
    Cruce OX1 (Order Crossover): uno de los más usados para TSP.

    Por qué no usamos el cruce simple de bits:
    Si tenemos [0,1,2,3,4] y [4,3,2,1,0] y cortamos al medio:
    [0,1] + [2,1,0] → [0,1,2,1,0] ← ciudad 1 aparece DOS veces! Inválido para TSP.
    OX1 garantiza que no se repitan ciudades.

    Cómo funciona OX1:
    1. Elegimos dos puntos de corte aleatorios en el padre 1
    2. Copiamos el segmento entre esos puntos al hijo
    3. Llenamos el resto con las ciudades del padre 2, en orden,
       saltando las que ya están en el hijo

    Ejemplo:
    Parent1: [1, 2, 3 | 4, 5, 6 | 7, 8]   (segmento central: 4,5,6)
    Parent2: [3, 7, 5, 1, 6, 8, 2, 4]

    Hijo: [?, ?, ?, 4, 5, 6, ?, ?]
    Llenamos con P2 (empezando después del segundo corte, en orden circular):
    P2 sin {4,5,6}: [3, 7, 1, 8, 2]  → [3, 7, ?, 4, 5, 6, 1, 8]... etc.
    """
    n = len(parent1)

    # Elegimos dos puntos de corte distintos
    # random.sample([0..n-1], 2) elige 2 números sin repetición
    cut1, cut2 = sorted(random.sample(range(n), 2))
    # sorted() garantiza que cut1 <= cut2

    # Creamos el hijo con None en todas las posiciones
    child = [None] * n

    # Copiamos el segmento del padre 1 al hijo
    child[cut1:cut2+1] = parent1[cut1:cut2+1]
    # parent1[cut1:cut2+1] es el "slice" de cut1 hasta cut2 (inclusive)

    # Conjunto de ciudades ya colocadas en el hijo (para verificar rápidamente)
    placed = set(child[cut1:cut2+1])

    # Llenamos el resto con ciudades del padre 2 en orden
    # Empezamos desde la posición cut2+1 del padre 2 (de forma circular)
    p2_idx = (cut2 + 1) % n  # Índice en parent2, circular
    c_idx = (cut2 + 1) % n   # Índice en child donde colocaremos, circular

    while None in child:
        city = parent2[p2_idx]
        if city not in placed:
            child[c_idx] = city       # Colocamos la ciudad en el hijo
            placed.add(city)           # La marcamos como colocada
            c_idx = (c_idx + 1) % n   # Avanzamos al siguiente slot del hijo
        p2_idx = (p2_idx + 1) % n     # Siempre avanzamos en parent2

    return child


# ─────────────────────────────────────────────
# MUTACIÓN: SWAP (INTERCAMBIO)
# ─────────────────────────────────────────────

def swap_mutation(individual, mutation_rate):
    """
    Mutación por intercambio: con probabilidad mutation_rate,
    intercambiamos dos ciudades aleatoriamente en la ruta.

    Ejemplo: [0, 3, 7, 2, 5] → intercambiamos posiciones 1 y 3:
             [0, 2, 7, 3, 5]

    Esto mantiene la validez de la ruta (no se duplican ciudades).
    """
    ind = individual[:]  # Hacemos una COPIA de la lista (importante!)
                          # Si no copiamos, modificaríamos el original

    if random.random() < mutation_rate:
        # random.random() devuelve un float entre 0.0 y 1.0
        # Si es menor que mutation_rate, aplicamos la mutación

        # Elegimos 2 posiciones distintas al azar
        i, j = random.sample(range(len(ind)), 2)

        # Intercambiamos las ciudades en esas posiciones (swap)
        ind[i], ind[j] = ind[j], ind[i]  # Python permite este swap en una sola línea!

    return ind


# ─────────────────────────────────────────────
# ALGORITMO GENÉTICO PRINCIPAL
# ─────────────────────────────────────────────

def genetic_algorithm(
    dist_matrix,
    pop_size=100,        # Tamaño de la población
    generations=500,     # Número de generaciones
    mutation_rate=0.1,   # Probabilidad de mutación (10%)
    elite_size=10,       # Cuántos mejores individuos pasan sin cambios (elitismo)
    tournament_size=5,   # Tamaño del torneo para selección
    seed=42              # Semilla para reproducibilidad
):
    """
    Ejecuta el Algoritmo Genético completo para el TSP.

    Parámetros explicados:
    - pop_size: más grande → más diversidad, pero más lento
    - generations: más generaciones → más tiempo para converger
    - mutation_rate: muy bajo → convergencia prematura; muy alto → búsqueda aleatoria
    - elite_size: elitismo asegura que las mejores soluciones no se pierdan
    - tournament_size: controla la presión selectiva
    - seed: fijar la semilla permite reproducir exactamente los mismos resultados

    Retorna:
    - best_route: la mejor ruta encontrada
    - best_cost: su costo total
    - history: lista con el mejor costo por generación (para graficar convergencia)
    - elapsed: tiempo total de ejecución
    """

    random.seed(seed)  # Fijamos la semilla aleatoria para reproducibilidad

    start_time = time.time()
    n = len(dist_matrix)  # Número de ciudades

    # ── Paso 1: Crear población inicial ──
    population = create_population(pop_size, n)

    best_route = None      # La mejor ruta encontrada hasta ahora
    best_cost = float('inf')  # El mejor costo (inicialmente infinito)
    history = []           # Guardamos el mejor costo de cada generación

    # ── Paso 2: Iterar por generaciones ──
    for gen in range(generations):

        # Evaluamos toda la población: calculamos fitness y ordenamos de mejor a peor
        evaluated = evaluate_population(population, dist_matrix)

        # ── Elitismo: los mejores `elite_size` individuos pasan directamente ──
        # [1] en la tupla es el individuo (la ruta); [0] sería el fitness
        new_population = [copy.deepcopy(ind) for _, ind in evaluated[:elite_size]]
        # copy.deepcopy() hace una copia profunda para evitar referencias compartidas

        # ── Verificamos si el mejor de esta generación es el mejor global ──
        best_of_gen_cost = route_cost(evaluated[0][1], dist_matrix)  # evaluated[0] = mejor
        if best_of_gen_cost < best_cost:
            best_cost = best_of_gen_cost
            best_route = evaluated[0][1][:]  # Guardamos una copia del mejor individuo

        history.append(best_cost)  # Registramos el mejor costo de esta generación

        # ── Paso 3: Crear el resto de la nueva población por cruce y mutación ──
        while len(new_population) < pop_size:
            # Seleccionamos dos padres por torneo
            parent1 = tournament_selection(evaluated, tournament_size)
            parent2 = tournament_selection(evaluated, tournament_size)

            # Cruzamos para crear un hijo
            child = order_crossover(parent1, parent2)

            # Aplicamos mutación
            child = swap_mutation(child, mutation_rate)

            new_population.append(child)  # Añadimos el hijo a la nueva población

        # La nueva población reemplaza a la anterior
        population = new_population

        # Imprimimos progreso cada 100 generaciones
        if (gen + 1) % 100 == 0:
            print(f"  Generacion {gen+1}/{generations} | Mejor costo: {best_cost}")

    elapsed = time.time() - start_time

    return best_route, best_cost, history, elapsed
