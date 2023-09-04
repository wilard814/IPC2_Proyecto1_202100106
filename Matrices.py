from Lista_simple import ListaSimple 

# Clase para representar y gestionar matrices de señales
class Matriz:
    # Constructor: inicializa una lista de señales vacía
    def __init__(self):
        self.señales = ListaSimple()

    # Método para guardar una matriz como señal
    def guardarSeñal(self, matriz):
        if matriz is not None:
            self.señales.add(matriz)
            print(f"Se ha guardado una nueva señal. Número total de señales: {len(self.señales)}")
        else:
            print("Intento de añadir una matriz None.")

    # Método para convertir una matriz en una matriz de patrones (binaria)
    def crearMatrizPatrones(self, matriz):
        if matriz is None:
            print("Matriz None pasada a crearMatrizPatrones")
            return None
        
        matriz_patrones = ListaSimple()
        for i in range(len(matriz)):
            fila = matriz.index(i)
            if fila is not None:
                fila = fila.value
            else:
                print(f"Nodo None encontrado en el índice {i} en crearMatrizPatrones")
                continue

            fila_patron = ListaSimple()
            for j in range(len(fila)):
                amplitud = fila.index(j)
                if amplitud is not None:
                    amplitud = amplitud.value
                else:
                    print(f"Nodo None encontrado para la amplitud en el índice {j}")
                    continue

                fila_patron.add(1 if amplitud > 0 else 0)
            matriz_patrones.add(fila_patron)
        return matriz_patrones

    # Método para agrupar filas similares en la matriz de patrones
    def agruparFilas(self, matriz_patrones):
        if matriz_patrones is None:
            print("Matriz None pasada a agruparFilas")
            return None

        grupos = ListaSimple()
        for i in range(len(matriz_patrones)):
            fila_i = matriz_patrones.index(i)
            if fila_i is not None:
                fila_i = fila_i.value
            else:
                print(f"Nodo None encontrado en el índice {i} en agruparFilas")
                continue

            grupo = ListaSimple()
            for j in range(len(matriz_patrones)):
                fila_j = matriz_patrones.index(j)
                if fila_j is not None:
                    fila_j = fila_j.value
                else:
                    print(f"Nodo None encontrado en el índice {j} en agruparFilas")
                    continue

                if str(fila_i) == str(fila_j):
                    grupo.add(j)
            if not grupos.buscar(str(grupo)):
                grupos.add(grupo)
        return grupos

# Clase para asociar un grupo de tiempos a una cadena de grupo
class GrupoTiempo:
    def __init__(self, grupo_str, tiempos):
        self.grupo_str = grupo_str
        self.tiempos = tiempos

# Clase para representar y gestionar matrices reducidas
class MatrizReducida:
    def __init__(self):
        self.matrices_reducidas = ListaSimple()
        self.tiempos_por_grupo = ListaSimple()  

    # Método para encontrar tiempos asociados a un grupo específico
    def encontrarTiemposPorGrupo(self, grupo_str):
        current = self.tiempos_por_grupo.first
        while current:
            if current.value.grupo_str == grupo_str:
                return current.value.tiempos
            current = current.next
        return None

    # Método para crear una matriz reducida a partir de grupos y matriz original
    def crearMatrizReducida(self, grupos, matriz_original):
        if grupos is None or matriz_original is None:
            print("Grupos o matriz original None pasados a crearMatrizReducida")
            return

        matriz_reducida = ListaSimple()
        grupos_unicos = ListaSimple()
        for i in range(len(grupos)):
            grupo = grupos.index(i)
            if grupo is not None:
                grupo = grupo.value
            else:
                print(f"Nodo None encontrado en el índice {i} en crearMatrizReducida para grupos")
                continue

            grupo_str = str(grupo)
            tiempos = self.encontrarTiemposPorGrupo(grupo_str)

            if tiempos is None:
                tiempos = ListaSimple()
                nuevo_grupo_tiempo = GrupoTiempo(grupo_str, tiempos)
                self.tiempos_por_grupo.add(nuevo_grupo_tiempo)

            tiempos.add(i + 1)  

            if not grupos_unicos.buscar(grupo_str):
                fila_reducida = ListaSimple()
                for j in range(len(matriz_original.index(0).value)):
                    suma_columna = 0
                    for k in range(len(grupo)):
                        fila_index = grupo.index(k).value
                        fila = matriz_original.index(fila_index).value
                        suma_columna += fila.index(j).value
                    fila_reducida.add(suma_columna)
                matriz_reducida.add(fila_reducida)
                grupos_unicos.add(grupo_str)

        self.matrices_reducidas.add(matriz_reducida)
