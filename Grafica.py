from graphviz import Digraph
from Matrices import *
from Lista_simple import *

def mostrar_datos_estudiante():
    print('''
> Keneth Willard Lopez Ovalle
> 202100106
> Introduccion a la Programación y computación 2 
> Ingenieria en Ciencias y Sistemas
> 6to Semestre
    ''')


def generar_grafica(matriz, matriz_reducida):
        print('\nGenerar gráfica')
        print('\nSeñales guardadas:\n')

        # Mostrar todas las señales guardadas
        for i in range(len(matriz.señales)):
            numeracion = str(i + 1) + "."
            print(numeracion, "Señal ", i + 1)

        seleccion = int(input('Ingrese el número de señal a graficar: '))

        # Verificar si la selección es válida
        if 1 <= seleccion <= len(matriz.señales):
            seleccion -= 1

            # Obtener la señal original y reducida seleccionada
            señal_original = matriz.señales.index(seleccion).value
            señal_reducida = matriz_reducida.matrices_reducidas.index(seleccion).value

            t = len(señal_original)
            A = len(señal_original.index(0).value)
            g = len(señal_reducida)

            # Generar gráfico para la señal original
            dot_original = Digraph("Señal Original", format="png")
            dot_original.graph_attr["rankdir"] = "LR"
            dot_original.node('Senal', 'Señal')
            dot_original.node('nombre', f'Nombre: Señal {seleccion + 1}')
            dot_original.node('t', f't = {t}', _attributes={"shape": "doublecircle", "color": "blue"})
            dot_original.node('A', f'A = {A}', _attributes={"shape": "doublecircle", "color": "blue"})
            dot_original.edge('Senal', 'nombre')
            dot_original.edge('nombre', 't')
            dot_original.edge('nombre', 'A')
            for j in range(t):
                fila = señal_original.index(j).value
                for k in range(A):
                    dato = fila.index(k).value
                    dot_original.node(f'x={k}y={j}', str(dato))
                    if k > 0:
                        dot_original.edge(f'x={k-1}y={j}', f'x={k}y={j}')
            dot_original.render(f"Reporte_Senal_{seleccion + 1}_Original", view=True)

            # Generar gráfico para la señal reducida
            dot_reducida = Digraph("Señal Reducida", format="png")
            dot_reducida.graph_attr["rankdir"] = "LR"
            dot_reducida.node('Senal', 'Señal')
            dot_reducida.node('nombre', f'Nombre: Señal {seleccion + 1}')
            dot_reducida.node('g', f'g = {g}', _attributes={"shape": "doublecircle", "color": "blue"})
            dot_reducida.node('A', f'A = {A}', _attributes={"shape": "doublecircle", "color": "blue"})
            dot_reducida.edge('Senal', 'nombre')
            dot_reducida.edge('nombre', 'g')
            dot_reducida.edge('nombre', 'A')
            for j in range(g):
                fila = señal_reducida.index(j).value
                for k in range(A):
                    dato = fila.index(k).value
                    dot_reducida.node(f'gx={k}gy={j}', str(dato))
                    if k > 0:
                        dot_reducida.edge(f'gx={k-1}gy={j}', f'gx={k}gy={j}')
            dot_reducida.render(f"Reporte_Senal_{seleccion + 1}_Reducida", view=True)

            print(f'Las gráficas de la señal {seleccion + 1} y su señal reducida se han generado y guardado.')

        else:
            print('Número de señal inválido')
