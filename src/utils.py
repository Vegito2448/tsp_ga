# utils.py
# Funciones auxiliares: graficar convergencia, formatear resultados

import matplotlib
matplotlib.use('Agg')  # Usar backend no interactivo para evitar problemas con GUI
import matplotlib.pyplot as plt  # Para crear gráficas


def plot_convergence(history, title="Convergencia del Algoritmo Genético", save_path=None):
    """
    Grafica cómo mejora el costo a lo largo de las generaciones.

    Parámetros:
    - history: lista de costos por generación (viene de genetic_algorithm)
    - title: título de la gráfica
    - save_path: si se proporciona, guarda la imagen en esa ruta
    """
    plt.figure(figsize=(10, 5))  # Tamaño de la figura en pulgadas

    # range(len(history)) genera [0, 1, 2, ..., n-1] = número de generación
    plt.plot(range(len(history)), history, 'b-', linewidth=1.5, label='Mejor costo')

    plt.xlabel('Generacion')           # Etiqueta del eje X
    plt.ylabel('Costo de la ruta')     # Etiqueta del eje Y
    plt.title(title)                   # Título de la gráfica
    plt.legend()                       # Muestra la leyenda
    plt.grid(True, alpha=0.3)          # Agrega cuadrícula semi-transparente
    plt.tight_layout()                 # Ajusta márgenes automáticamente

    if save_path:
        plt.savefig(save_path, dpi=150)  # Guarda la imagen con buena resolución
        print(f"  Gráfica guardada en: {save_path}")

    plt.close()  # Cierra la figura para liberar memoria


def print_results_table(results):
    """
    Imprime una tabla comparativa de resultados.

    `results` es una lista de diccionarios, cada uno con:
    {
        'instance': 'gr17',
        'nn_cost': 2163,
        'ga_cost': 2085,
        'optimal': 2085,
        'ga_time': 3.45,
        'efficiency': 1.00
    }
    """
    print("\n" + "="*80)
    print(f"{'Instancia':<12} {'Opt.Lit.':<12} {'NN Costo':<12} {'AG Costo':<12} "
          f"{'Tiempo(s)':<12} {'Eficiencia':<10}")
    print("="*80)

    for r in results:
        eff = r.get('efficiency', 'N/A')
        eff_str = f"{eff:.4f}" if isinstance(eff, float) else eff
        print(f"{r['instance']:<12} {r['optimal']:<12} {r['nn_cost']:<12} "
              f"{r['ga_cost']:<12} {r['ga_time']:<12.3f} {eff_str:<10}")

    print("="*80)
