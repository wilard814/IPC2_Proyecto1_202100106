import xml.etree.ElementTree as ET
from graphviz import Digraph
from Matrices import *
from Lista_simple import *
import time

Menu_principal = {'1', '2', '3', '4', '5', '6'}

matriz = Matriz() # Guarda la matriz y sus datos generales como el nombre, la cantidad de filas y la cantidad de columnas
matriz_obtenida = Matriz_Reducida()

while True:
    print('''   
Menú principal:
    1. Cargar archivo
    2. Procesar archivo
    3. Escribir archivo salida
    4. Mostrar datos del estudiante
    5. Generar gráfica
    6. Salida
''')

    opcion = input('Seleccione una opcion: ')

    if not (opcion in Menu_principal):
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

            for senales in raiz.findall('senales'):
                for senal in senales.findall('senal'):
                    nombre = senal.get('nombre')
                    t = int(senal.get('t'))
                    A = int(senal.get('A'))

                    mayor_t = 0
                    mayor_A = 0

                    lista_t = []
                    lista_A = []

                    lista_dato = ListaSimple()

                    for dato in senal.findall('dato'):
                        t_actual = int(dato.get('t'))
                        if t_actual > mayor_t:
                            mayor_t = t_actual

                        A_actual = int(dato.get('A'))
                        if A_actual > mayor_A:
                            mayor_A = A_actual

                        lista_t.append(t_actual)
                        lista_A.append(A_actual)

                        lista_dato.add(int(dato.text))

                    contador = 0

                    matriz_operar = ListaSimple()

                    for no_fila in range(0, t):
                        fila_matriz = ListaSimple()
                        for no_columna in range(0, A):
                            fila_matriz.add(lista_dato.index(contador))
                            contador += 1
                        matriz_operar.add(fila_matriz)

                    if t <= 3600 and A <= 130 and int(t) == int(mayor_t) and int(A) == int(mayor_A) and len(lista_t) == len(lista_A):
                        matriz.guardar(nombre, t, A, matriz_operar)
                    else:
                        print(f'Las dimensiones no cumplen las reglas para la señal {nombre}')

        except Exception as e:
            print('Ocurrio un error:', str(e))
        continue


    if opcion == '2':
        time.sleep(0.1)
        print('\nProcesar archivo')

        print('> Calculando la matriz binaria...')
        time.sleep(3)

        grupos_matriz = ListaSimple()

        matrizBinaria = matriz.crearMatrizPatrones()

        for i in range(len(matrizBinaria)):
            matriz.grupos_Matriz(i)  
            grupos_matriz.add(matriz.grupos_Matriz(i))

        print('> Realizando suma de tuplas...')
        time.sleep(3)
        
        matriz_reducida_lista = ListaSimple()  # Lista para guardar las instancias de Matriz_Reducida
        
        for lista_index in range(len(grupos_matriz)):
            lista = matriz.dato.index(lista_index).value
            index_lista = grupos_matriz.index(lista_index).value

            reducida = ListaSimple()
            frecuencia = ListaSimple()
            no_frecuencia = ListaSimple()

            m = 0
            for index in range(len(index_lista)):
                no_frecuencia.add(len(index_lista.index(index).value))
                posicion = index_lista.index(index).value
                if len(posicion) > 1:
                    auxiliar = lista.index(posicion.index(0).value).value 
                    frecuencia.add(posicion.index(0).value + 1)
                    for x in range(1, len(posicion)):
                        fila_actual = lista.index(posicion.index(x).value).value
                        auxiliar = [a + b for a, b in zip(auxiliar, fila_actual)]
                    reducida.add(auxiliar)
                else:
                    posicion = index_lista.index(index).value
                    frecuencia.add(posicion.index(0).value + 1)
                    reducida.add(lista.index(posicion.index(0).value).value)

            nombre = matriz.nombre.index(lista_index).value  
            n = len(reducida)
            m = len(reducida.index(0).value)  
            
            # Crear la instancia de Matriz_Reducida y guardarla en matriz_reducida_lista
            matriz_reducida = Matriz_Reducida()
            matriz_reducida.guardar(nombre, n, m, len(grupos_matriz.index(lista_index).value), frecuencia, no_frecuencia, reducida)
            matriz_reducida_lista.add(matriz_reducida)
        
        # Guardar la lista de instancias de Matriz_Reducida en matriz_obtenida
        matriz_obtenida.matriz = matriz_reducida_lista
        
        continue



    if opcion == '3':
        time.sleep(0.1)
        print('\nArchivos de Salida')
        ruta_especifica = input('Escribir una ruta específica: ')
        
        try:
            print('Se escribió el archivo satisfactorio')

            root = ET.Element("senalesReducidas")
            for i in range(len(matriz_obtenida.nombre)):
                nombre = matriz_obtenida.nombre.index(i).value
                A = matriz_obtenida.columna.index(i).value

                senal = ET.SubElement(root, "senal", nombre=nombre, A=str(A))

                grupos = matriz_obtenida.grupos.index(i).value
                frecuencia = matriz_obtenida.frecuencia.index(i).value
                no_frecuencia = matriz_obtenida.no_frecuencia.index(i).value
                matriz_Salida = matriz_obtenida.matriz.index(i).value

                for j in range(len(grupos)):
                    grupo = ET.SubElement(senal, "grupo", g=str(j+1))

                    tiempos = grupos.index(j).value
                    tiempos_str = ','.join(map(str, tiempos))
                    tiempos_tag = ET.SubElement(grupo, "tiempos")
                    tiempos_tag.text = tiempos_str

                    datos_grupo = matriz_Salida.index(j).value
                    datos_grupo_tag = ET.SubElement(grupo, "datosGrupo")

                    for k in range(len(datos_grupo)):
                        dato = datos_grupo.index(k).value
                        dato_tag = ET.SubElement(datos_grupo_tag, "dato", A=str(k+1))
                        dato_tag.text = str(dato)

            arbol = ET.ElementTree(root)
            arbol.write(ruta_especifica, xml_declaration=True, encoding="UTF-8", method="xml")
            
            print(f'Se ha generado el archivo de salida en formato XML en la ruta: {ruta_especifica}')

        except:
            print('Ocurrió un error al generar el archivo de salida')
            
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
        print('\nMatrices guardadas:\n')

        for i in range(len(matriz.nombre)):
            numeracion = str(i + 1) + "."
            print(numeracion, matriz.nombre.index(i))
            for j in range(len(matriz.dato.index(i).value)):
                print('\t', matriz.dato.index(i).value.index(j))
            print('')

        seleccion = int(input('Ingrese el número de matriz a graficar: '))

        if 1 <= seleccion <= len(matriz.nombre):
            seleccion -= 1
            nombre = matriz.nombre.index(seleccion).value
            t = matriz.fila.index(seleccion).value
            A = matriz.columna.index(seleccion).value
            matriz_Graficar = matriz.dato.index(seleccion).value

            matriz_patron = matriz.crearMatrizPatrones()
            grupos = matriz.grupos_Matriz(seleccion)

            # Generar el gráfico de la matriz original
            dot_original = Digraph("Matriz Original", format="png")
            dot_original.graph_attr["rankdir"] = "LR"
            dot_original.node('Senal', 'Señal')
            dot_original.node('nombre', f'Nombre: {nombre}')
            dot_original.node('t', f't = {t}', _attributes={"shape": "doublecircle", "color": "blue"})
            dot_original.node('A', f'A = {A}', _attributes={"shape": "doublecircle", "color": "blue"})
            dot_original.edge('Senal', 'nombre')
            dot_original.edge('nombre', 't')
            dot_original.edge('nombre', 'A')

            for j in range(len(matriz_Graficar)):
                nuevaMatriz = matriz_Graficar.index(j).value

                for k in range(len(nuevaMatriz)):
                    dato = nuevaMatriz.index(k).value
                    if k == 0:
                        dot_original.node('x=' + str(k) + 'y=' + str(j), str(dato))
                        dot_original.edge('nombre', 'x=' + str(k) + 'y=' + str(j))
                    else:
                        dot_original.node('x=' + str(k) + 'y=' + str(j), str(dato))
                        dot_original.edge('x=' + str(k-1) + 'y=' + str(j), 'x=' + str(k) + 'y=' + str(j))
            dot_original.render(f"Reporte_Matriz_{nombre}_Original", view=True)

            # Generar el gráfico de la matriz reducida
            dot_reducida = Digraph("Matriz Reducida", format="png")
            dot_reducida.graph_attr["rankdir"] = "LR"
            dot_reducida.node('Senal', 'Señal')
            dot_reducida.node('nombre', f'Nombre: {nombre}')
            dot_reducida.node('g', f'g = {len(grupos)}', _attributes={"shape": "doublecircle", "color": "blue"})
            dot_reducida.node('A', f'A = {A}', _attributes={"shape": "doublecircle", "color": "blue"})
            dot_reducida.edge('Senal', 'nombre')
            dot_reducida.edge('nombre', 'g')
            dot_reducida.edge('nombre', 'A')

            for j in range(len(matriz_patron)):
                fila_reducida = matriz_patron.index(j).value

                for k in range(len(fila_reducida)):
                    dato_reducido = fila_reducida.index(k).value
                    if k == 0:
                        dot_reducida.node('gx=' + str(k) + 'y=' + str(j), str(dato_reducido))
                        dot_reducida.edge('nombre', 'gx=' + str(k) + 'y=' + str(j))
                    else:
                        dot_reducida.node('gx=' + str(k) + 'y=' + str(j), str(dato_reducido))
                        dot_reducida.edge('gx=' + str(k-1) + 'y=' + str(j), 'gx=' + str(k) + 'y=' + str(j))
            dot_reducida.render(f"Reporte_Matriz_{nombre}_Reducida", view=True)

            print(f'Las gráficas de la señal {nombre} y su matriz reducida se han generado y guardado como Reporte_Matriz_{nombre}_Original.png y Reporte_Matriz_{nombre}_Reducida.png')

        else:
            print('Número de matriz inválido')
            continue


    if opcion == '6':
        break