# parser.py
# Este módulo se encarga de leer un archivo .tsp y devolver la matriz de distancias

import numpy as np  # Importamos numpy para crear matrices numéricas eficientes

def parse_tsp(filepath):
    """
    Lee un archivo .tsp en formato LOWER_DIAG_ROW y devuelve:
    - dimension: número de ciudades (int)
    - dist_matrix: matriz de distancias completa (numpy array 2D, simétrica)
    """

    # Abrimos el archivo en modo lectura ('r') con codificación UTF-8
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()  # Leemos TODAS las líneas y las guardamos en una lista

    dimension = 0          # Aquí guardaremos el número de ciudades
    in_weights = False     # Bandera: ¿estamos ya en la sección de datos numéricos?
    raw_numbers = []       # Lista donde acumularemos todos los números de distancia

    for line in lines:
        # strip() elimina espacios y saltos de línea al inicio/final de cada línea
        line = line.strip()

        # Si la línea empieza con "DIMENSION", extraemos el número de ciudades
        if line.startswith('DIMENSION'):
            # Ejemplo: "DIMENSION: 17" → split(':') → ['DIMENSION', ' 17'] → [1] → '17' → int
            dimension = int(line.split(':')[1].strip())

        # Si encontramos esta etiqueta, las siguientes líneas son los datos
        elif line == 'EDGE_WEIGHT_SECTION':
            in_weights = True  # Activamos la bandera

        # Si encontramos EOF, dejamos de leer datos
        elif line == 'EOF':
            in_weights = False  # Desactivamos la bandera

        # Si estamos en la sección de pesos, procesamos los números
        elif in_weights:
            # split() sin argumento divide por cualquier espacio en blanco
            # Ejemplo: "0 633 0 257" → ['0', '633', '0', '257']
            numbers = line.split()
            for n in numbers:
                # Convertimos cada string a entero y lo agregamos a nuestra lista
                raw_numbers.append(int(n))

    # Ahora reconstruimos la matriz completa a partir de los números del triángulo inferior
    # Creamos una matriz cuadrada de ceros de tamaño dimension x dimension
    dist_matrix = np.zeros((dimension, dimension), dtype=int)

    idx = 0  # Índice para recorrer raw_numbers secuencialmente

    # Recorremos fila por fila (i = fila actual, de 0 hasta dimension-1)
    for i in range(dimension):
        # En cada fila i, hay i+1 valores (fila 0: 1 valor, fila 1: 2 valores, etc.)
        for j in range(i + 1):
            val = raw_numbers[idx]  # Tomamos el siguiente número de la lista
            idx += 1                 # Avanzamos el índice

            dist_matrix[i][j] = val  # Lo ponemos en la posición (i, j)
            dist_matrix[j][i] = val  # Y también en (j, i) para hacer la matriz simétrica

    return dimension, dist_matrix


def print_matrix(dist_matrix, label="Matriz de distancias"):
    """
    Imprime la matriz de distancias de forma legible en consola.
    Solo para verificación/debugging.
    """
    print(f"\n{label}:")
    print("     ", end="")
    n = len(dist_matrix)
    for j in range(n):
        print(f"{j:5d}", end="")  # Encabezado de columnas
    print()
    for i, row in enumerate(dist_matrix):
        print(f"{i:4d} ", end="")  # Número de fila
        for val in row:
            print(f"{val:5d}", end="")
        print()
