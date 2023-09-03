#main.py
import xml.etree.ElementTree as ET
from graphviz import Digraph
from Matrices import *
from Lista_simple import *
import time



while True:
    print('''   
Menú principal:
    1. Cargar archivo
    2. Procesar archivo
    3. Escribir archivo salida
    4. Mostrar datos del estudiante
    5. Generar gráfica
    6. Inicializar sistema      
    7. Salida
''')

    opcion = input('Seleccione una opcion: ')

    if not opcion :
        print('Opcion no valida')
        continue

    if opcion == '1':
        time.sleep(0.1)
        print('\nOpcion Cargar Archivo:')
        archivo = input('Ingrese la ruta del archivo: ')
        try:
            archivo_xml = ET.parse(archivo)
            raiz = archivo_xml.getroot()
            matriz = Matriz()
            for senal in raiz:
                if 'nombre' not in senal.attrib:
                    print("Error: Falta el atributo 'nombre' en la etiqueta 'senal'.")
                    continue

                nombre = senal.attrib['nombre']

                if 't' not in senal.attrib or 'A' not in senal.attrib:
                    print(f"Error: Faltan los atributos 't' y/o 'A' en la señal '{nombre}'.")
                    continue

                t = int(senal.attrib['t'])
                A = int(senal.attrib['A'])

                if t <= 0 or t > 3600:
                    print(f"Error: El valor de 't' en la señal '{nombre}' debe ser mayor a 0 y menor o igual a 3600.")
                    continue

                if A <= 0 or A > 130:
                    print(f"Error: El valor de 'A' en la señal '{nombre}' debe ser mayor a 0 y menor o igual a 130.")
                    continue

                mayor_t = 0
                mayor_A = 0
                lista_dato = ListaSimple()

                for index in senal:
                    if 't' not in index.attrib or 'A' not in index.attrib:
                        print(f"Error: Faltan los atributos 't' y/o 'A' en la etiqueta 'dato' de la señal '{nombre}'.")
                        continue

                    t_actual = int(index.attrib['t'])
                    A_actual = int(index.attrib['A'])

                    if t_actual > mayor_t:
                        mayor_t = t_actual
                    if A_actual > mayor_A:
                        mayor_A = A_actual

                    lista_dato.add(int(index.text))

                matriz_operar = ListaSimple()

                for no_fila in range(0, t):
                    fila_matriz = ListaSimple()
                    for no_columna in range(0, A):
                        fila_matriz.add(lista_dato.index(no_fila * A + no_columna).value)
                    matriz_operar.add(fila_matriz)

                if t == mayor_t and A == mayor_A:
                    matriz.guardarSeñal(matriz_operar)
                    print(f"Guardada la matriz original para la señal {nombre}.")

        except Exception as e:
            print('Ocurrio un error:', str(e))
        continue



    if opcion == '2':
        time.sleep(0.1)
        print('\nProcesar archivo')
        print('> Calculando la matriz binaria...')
        time.sleep(3)
        
        # Obtener la matriz binaria (Matriz de patrones) para cada señal almacenada
        grupos_matriz = ListaSimple()
        matriz_reducida_lista = ListaSimple()
        
        for señal_index in range(len(matriz.señales)):
            señal_actual_node = matriz.señales.index(señal_index)
            if señal_actual_node is None:
                print(f"Error: señal_actual_node es None para el índice {señal_index}")
                continue
            señal_actual = señal_actual_node.value

            matrizBinaria = matriz.crearMatrizPatrones(señal_actual)
            # Mostrar la matriz binaria
            print("Matriz binaria para la señal:", señal_index + 1)
            for fila in matrizBinaria:
                print(fila)

            grupos = matriz.agruparFilas(matrizBinaria)
            grupos_matriz.add(grupos)

        print('> Realizando suma de tuplas...')
        time.sleep(3)
        
        matriz_reducida = MatrizReducida()

        for grupos_index in range(len(grupos_matriz)):
            grupos_actual_node = grupos_matriz.index(grupos_index)
            if grupos_actual_node is None:
                print(f"Error: grupos_actual_node es None para el índice {grupos_index}")
                continue
            grupos_actual = grupos_actual_node.value

            señal_actual_node = matriz.señales.index(grupos_index)
            if señal_actual_node is None:
                print(f"Error: señal_actual_node es None para el índice {grupos_index}")
                continue
            señal_actual = señal_actual_node.value
            
            matriz_reducida.crearMatrizReducida(grupos_actual, señal_actual)
            
            # Mostrar la matriz reducida para cada señal
            print("Matriz reducida para la señal:", grupos_index + 1)
            matriz_reducida_actual_node = matriz_reducida.matrices_reducidas.index(grupos_index)
            if matriz_reducida_actual_node is None:
                print(f"Error: matriz_reducida_actual_node es None para el índice {grupos_index}")
                continue
            matriz_reducida_actual = matriz_reducida_actual_node.value
            for fila in matriz_reducida_actual:
                print(fila)
        
        print("Matrices reducidas y grupos guardados correctamente.")
        continue



    if opcion == '3':
        print("\nArchivos de Salida")
        print("Escribiendo archivo...")
        
        try:
            root = ET.Element("senalesReducidas")
            
            for senal_index in range(len(matriz_reducida.matrices_reducidas)):
                senal_actual_node = matriz_reducida.matrices_reducidas.index(senal_index)
                if senal_actual_node is None:
                    print(f"Error: senal_actual_node es None para el índice {senal_index}")
                    continue
                
                senal_actual = senal_actual_node.value
                grupos_actual_node = grupos_matriz.index(senal_index)
                
                if grupos_actual_node is None:
                    print(f"Error: grupos_actual_node es None para el índice {senal_index}")
                    continue
                
                grupos_actual = grupos_actual_node.value
                senal_element = ET.SubElement(root, "senal", nombre=f"Senal_{senal_index+1}", A=str(len(senal_actual.index(0).value)))

                for grupo_index in range(len(grupos_actual)):
                    grupo_actual_node = grupos_actual.index(grupo_index)
                    if grupo_actual_node is None:
                        print(f"Error: grupo_actual_node es None para el índice {grupo_index}")
                        continue
                    
                    grupo_actual = grupo_actual_node.value
                    grupo_element = ET.SubElement(senal_element, "grupo", g=str(grupo_index + 1))
                    
                    tiempos = ",".join([str(x) for x in grupo_actual])
                    tiempos_element = ET.SubElement(grupo_element, "tiempos")
                    tiempos_element.text = tiempos
                    
                    datosGrupo_element = ET.SubElement(grupo_element, "datosGrupo")
                    
                    for A_index in range(len(senal_actual.index(0).value)):
                        A_value_node = senal_actual.index(grupo_index).value.index(A_index)
                        if A_value_node is None:
                            print(f"Error: A_value_node es None para el índice {A_index}")
                            continue
                        A_value = A_value_node.value
                        dato_element = ET.SubElement(datosGrupo_element, "dato", A=str(A_index + 1))
                        dato_element.text = str(A_value)
            
            # Guardar en el archivo XML
            tree = ET.ElementTree(root)
            tree.write("C:\\Users\\wilar\\OneDrive\\Escritorio\\pruebazzz\\Salidas\\output.xml")
            
            print("Archivo de salida escrito con éxito.")
            
        except Exception as e:
            print(f"Ocurrió un error al generar el archivo de salida: {str(e)}")
        continue

    if opcion == '4':
        time.sleep(0.1)
        print('''
> Keneth Willard Lopez Ovalle
> 202100106
> Introduccion a la Programación y computación 2 
> Ingenieria en Ciencias y Sistemas
> 6to Semestre
        ''')
        continue


    if opcion == '5':
        time.sleep(0.1)
        print('\nGenerar gráfica')
        print('\nSeñales guardadas:\n')

        for i in range(len(matriz.señales)):
            numeracion = str(i + 1) + "."
            print(numeracion, "Señal ", i + 1)

        seleccion = int(input('Ingrese el número de señal a graficar: '))

        if 1 <= seleccion <= len(matriz.señales):
            seleccion -= 1
            señal_original = matriz.señales.index(seleccion).value
            señal_reducida = matriz_reducida.matrices_reducidas.index(seleccion).value

            # Asumimos que 't' y 'A' son las dimensiones de la señal original, que puedes obtener de otra manera si es necesario.
            t = len(señal_original)
            A = len(señal_original.index(0).value)
            g = len(señal_reducida)  # número de grupos en la señal reducida

            # Generar el gráfico de la señal original
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

            # Generar el gráfico de la señal reducida
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
        continue

    if opcion == '6':
        print('Inicializando sistema...')
        time.sleep(0.3)
        matriz = Matriz()  # Reiniciar la instancia de la clase Matriz
        matriz_reducida = MatrizReducida()  # Reiniciar la instancia de la clase MatrizReducida
        print('El sistema ha sido Inicializado')
        continue

    if opcion == '7':
        break