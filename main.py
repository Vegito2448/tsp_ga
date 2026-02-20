# main.py
# Punto de entrada principal del programa
# Ejecuta el TSP para las tres instancias y muestra los resultados

import os  # Para trabajar con rutas de archivos

# Importamos nuestros módulos
from src.parser import parse_tsp
from src.nearest_neighbor import nearest_neighbor
from src.genetic_algorithm import genetic_algorithm
from src.utils import plot_convergence, print_results_table

# ─────────────────────────────────────────────
# CONOCIDOS DE TSPLIB (para calcular eficiencia)
# Fuente: http://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/
# ─────────────────────────────────────────────
KNOWN_OPTIMA = {
    'gr17': 2085,
    'gr21': 2707,
    'gr24': 1272
}

# ─────────────────────────────────────────────
# PARÁMETROS DEL ALGORITMO GENÉTICO
# Ajustados según el tamaño de cada instancia
# ─────────────────────────────────────────────
GA_PARAMS = {
    'gr17': {'pop_size': 200, 'generations': 1000, 'mutation_rate': 0.15, 'elite_size': 20},
    'gr21': {'pop_size': 200, 'generations': 1500, 'mutation_rate': 0.15, 'elite_size': 20},
    'gr24': {'pop_size': 300, 'generations': 2000, 'mutation_rate': 0.20, 'elite_size': 30},
}


def run_instance(name, filepath):
    """
    Ejecuta el análisis completo para una instancia TSP.

    Parámetros:
    - name: nombre de la instancia ('gr17', 'gr21', 'gr24')
    - filepath: ruta al archivo .tsp
    """
    print(f"\n{'='*60}")
    print(f"  INSTANCIA: {name}")
    print(f"{'='*60}")

    # ── 1. Parsear el archivo ──
    print(f"\n[1] Leyendo archivo: {filepath}")
    dimension, dist_matrix = parse_tsp(filepath)
    print(f"    Ciudades: {dimension}")
    print(f"    Matriz: {dist_matrix.shape[0]}x{dist_matrix.shape[1]}")

    # ── 2. Heurística del vecino más cercano ──
    print(f"\n[2] Ejecutando Nearest Neighbor...")
    nn_route, nn_cost, nn_time = nearest_neighbor(dist_matrix, start_city=0)
    print(f"    Costo: {nn_cost} | Tiempo: {nn_time:.4f}s")
    print(f"    Ruta: {nn_route}")

    # ── 3. Algoritmo Genético ──
    print(f"\n[3] Ejecutando Algoritmo Genético...")
    params = GA_PARAMS[name]
    print(f"    Parámetros: {params}")

    ga_route, ga_cost, history, ga_time = genetic_algorithm(dist_matrix, **params)
    # **params "desempaqueta" el diccionario como argumentos nombrados
    # Equivale a: genetic_algorithm(dist_matrix, pop_size=200, generations=1000, ...)

    print(f"\n    Costo final AG: {ga_cost} | Tiempo: {ga_time:.3f}s")
    print(f"    Ruta: {ga_route}")

    # ── 4. Calcular eficiencia ──
    optimal = KNOWN_OPTIMA.get(name, None)
    efficiency = None
    if optimal:
        # Fórmula de la paper: e = 1 - (Z - Z_T) / Z_T
        efficiency = 1 - (ga_cost - optimal) / optimal
        print(f"\n    Optimo conocido: {optimal}")
        print(f"    Eficiencia: {efficiency:.4f}")

    # ── 5. Graficar convergencia ──
    os.makedirs('output', exist_ok=True)  # Crea carpeta 'output' si no existe
    plot_convergence(
        history,
        title=f"Convergencia AG - {name} ({dimension} ciudades)",
        save_path=f"output/convergence_{name}.png"
    )

    # Retornamos un diccionario con todos los resultados
    return {
        'instance': name,
        'dimension': dimension,
        'optimal': optimal or 'N/A',
        'nn_cost': nn_cost,
        'ga_cost': ga_cost,
        'ga_time': ga_time,
        'efficiency': efficiency
    }


def main():
    """
    Función principal: ejecuta las tres instancias y muestra tabla comparativa.
    """
    print("\n" + "="*60)
    print("  TSP con Algoritmo Genetico - UNET Evaluacion #2")
    print("="*60)

    # Definimos las instancias a procesar
    # os.path.join crea rutas compatibles con Windows, Mac y Linux
    instances = [
        ('gr17', os.path.join('data', 'gr17.tsp')),
        ('gr21', os.path.join('data', 'gr21.tsp')),
        ('gr24', os.path.join('data', 'gr24.tsp')),
    ]

    all_results = []

    for name, filepath in instances:
        if not os.path.exists(filepath):
            print(f"\n[ADVERTENCIA] No se encontró: {filepath}")
            continue

        result = run_instance(name, filepath)
        all_results.append(result)

    # ── Tabla comparativa final ──
    print("\n\n>>> RESUMEN COMPARATIVO")
    print_results_table(all_results)

    print("\n[OK] Proceso completado. Graficas guardadas en carpeta 'output/'")


# Este bloque garantiza que main() solo se ejecute cuando corremos este archivo directamente
# Si alguien hace "import main" desde otro módulo, main() NO se ejecutará automáticamente
if __name__ == '__main__':
    main()
