# 🧬 TSP — Algoritmo Genético

> Resolución del Problema del Agente Viajero (TSP) mediante un Algoritmo Genético con cruce OX1, selección por torneo y mutación swap.

**Evaluación #2** — Computación Emergente · Maestría en Informática · UNET

---

## 📋 Descripción

Este proyecto implementa un **Algoritmo Genético (AG)** para resolver instancias del [Problema del Agente Viajero](https://en.wikipedia.org/wiki/Travelling_salesman_problem) (TSP). Las instancias utilizadas (`gr17`, `gr21`, `gr24`) fueron obtenidas del repositorio [mastqe/tsplib](https://github.com/mastqe/tsplib/).

### Características principales

- **Representación por permutación entera** — cada individuo es una ruta válida
- **Cruce OX1** (Order Crossover) — preserva el orden relativo de las ciudades
- **Mutación Swap** — intercambia dos ciudades manteniendo la validez de la ruta
- **Selección por Torneo** — balance ajustable entre presión selectiva y diversidad
- **Elitismo** — los mejores individuos se preservan entre generaciones
- **Parser TSPLIB** — lee archivos `.tsp` en formato `LOWER_DIAG_ROW`
- **Gráficas de convergencia** — visualización automática de la evolución del costo

---

## 📁 Estructura del Proyecto

```
tsp_ga/
├── data/
│   ├── gr17.tsp                 # 17 ciudades (óptimo: 2085)
│   ├── gr21.tsp                 # 21 ciudades (óptimo: 2707)
│   └── gr24.tsp                 # 24 ciudades (óptimo: 1272)
├── src/
│   ├── __init__.py              # Marca src como paquete Python
│   ├── parser.py                # Lectura de archivos .tsp
│   ├── nearest_neighbor.py      # Heurística del vecino más cercano
│   ├── genetic_algorithm.py     # Implementación del AG
│   └── utils.py                 # Gráficas y tablas de resultados
├── output/                      # Gráficas de convergencia (generadas)
├── main.py                      # Punto de entrada
├── informe_IEEE.md              # Informe académico en formato IEEE
├── requirements.txt             # Dependencias
└── pyproject.toml               # Configuración del proyecto
```

---

## 🚀 Instalación y Ejecución

### Requisitos previos

- Python 3.10 o superior

### Instalación

```bash
# Clonar el repositorio
git clone https://github.com/Vegito2448/tsp_ga.git
cd tsp_ga

# (Opcional) Crear entorno virtual
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac / Linux

# Instalar dependencias
pip install -r requirements.txt
```

### Ejecución

```bash
python main.py
```

El programa ejecuta las tres instancias de forma secuencial y genera:
- Resultados detallados en consola
- Gráficas de convergencia en `output/`

---

## 📊 Resultados

| Instancia | N | Óptimo | Vecino Cercano | Alg. Genético | Tiempo | Eficiencia | Mejora vs NN |
|:---------:|:---:|:------:|:--------------:|:-------------:|:------:|:----------:|:------------:|
| **gr17**  | 17  | 2,085  | 2,187          | 2,142         | 4.21s  | 97.27%     | 2.06%        |
| **gr21**  | 21  | 2,707  | 3,333          | **2,707** ✓   | 7.21s  | **100%**   | 18.78%       |
| **gr24**  | 24  | 1,272  | 1,553          | 1,289         | 17.80s | 98.66%     | 17.00%       |

> ✓ El AG encontró la **solución óptima exacta** en la instancia gr21.

### Parámetros utilizados

| Parámetro          | gr17  | gr21  | gr24  |
|:-------------------|:-----:|:-----:|:-----:|
| Población          | 200   | 200   | 300   |
| Generaciones       | 1,000 | 1,500 | 2,000 |
| Tasa de mutación   | 0.15  | 0.15  | 0.20  |
| Élite              | 20    | 20    | 30    |
| Tamaño de torneo   | 5     | 5     | 5     |
| Semilla aleatoria  | 42    | 42    | 42    |

---

## 📈 Gráficas de Convergencia

Las gráficas muestran la evolución del mejor costo encontrado a lo largo de las generaciones. Se generan automáticamente en `output/`:

- `output/convergence_gr17.png`
- `output/convergence_gr21.png`
- `output/convergence_gr24.png`

---

## 🧩 Módulos

### `src/parser.py`
Lee archivos `.tsp` en formato TSPLIB (`LOWER_DIAG_ROW`) y reconstruye la matriz de distancias simétrica completa.

### `src/nearest_neighbor.py`
Implementa la heurística greedy del Vecino Más Cercano: desde una ciudad inicial, siempre visita la ciudad no visitada más cercana. Incluye la función `route_cost()` reutilizada por el AG.

### `src/genetic_algorithm.py`
Implementación completa del AG:
- `create_population()` — Genera población inicial aleatoria
- `evaluate_population()` — Calcula fitness y ordena
- `tournament_selection()` — Selección por torneo
- `order_crossover()` — Cruce OX1
- `swap_mutation()` — Mutación por intercambio
- `genetic_algorithm()` — Ciclo evolutivo principal

### `src/utils.py`
Funciones de visualización: gráficas de convergencia con Matplotlib y tabla de resultados formateada.

---

## 📚 Referencias

1. T. H. Cormen et al., *Introduction to Algorithms*, 3rd ed. MIT Press, 2009.
2. J. H. Holland, *Adaptation in Natural and Artificial Systems*. MIT Press, 1992.
3. G. Reinelt, "TSPLIB — A traveling salesman problem library," *ORSA J. Comput.*, 1991.
4. M. Mitchell, *An Introduction to Genetic Algorithms*. MIT Press, 1998.
5. D. E. Goldberg, *Genetic Algorithms in Search, Optimization, and Machine Learning*. Addison-Wesley, 1989.

---

## 👤 Autor

**Jesús David Peña Jaimes**
Maestría en Informática — Universidad Nacional Experimental del Táchira (UNET)

---

## 📄 Licencia

Este proyecto se distribuye bajo la licencia MIT. Consulta el archivo `LICENSE` para más detalles.
