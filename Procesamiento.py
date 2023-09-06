import xml.etree.ElementTree as ET
from Matrices import *
from Lista_simple import *
import time

def cargar_archivo():
    print('\nOpcion Cargar Archivo:')
    archivo = input('Ingrese la ruta del archivo: ')

    matriz = Matriz()  # Inicialización de la estructura para guardar las señales

    try:
        archivo_xml = ET.parse(archivo)
        raiz = archivo_xml.getroot()

        for senal in raiz:
            # Verificar si el atributo 'nombre' está presente
            if 'nombre' not in senal.attrib:
                print("Error: Falta el atributo 'nombre' en la etiqueta 'senal'.")
                continue
            nombre = senal.attrib['nombre']

            # Verificar si los atributos 't' y 'A' están presentes
            if 't' not in senal.attrib or 'A' not in senal.attrib:
                print(f"Error: Faltan los atributos 't' y/o 'A' en la señal '{nombre}'.")
                continue

            # Convertir los atributos a enteros
            t = int(senal.attrib['t'])
            A = int(senal.attrib['A'])

            # Verificar los valores de 't' y 'A'
            if t <= 0 or t > 3600:
                print(f"Error: El valor de 't' en la señal '{nombre}' no es válido.")
                continue
            if A <= 0 or A > 130:
                print(f"Error: El valor de 'A' en la señal '{nombre}' no es válido.")
                continue

            datos_validos = True
            matriz_operar = ListaSimple()
            for dato in senal:
                t_dato = int(dato.attrib.get('t', -1))
                A_dato = int(dato.attrib.get('A', -1))

                # Verificar que los datos estén dentro de los límites de 't' y 'A'
                if t_dato > t or A_dato > A or t_dato <= 0 or A_dato <= 0:
                    datos_validos = False
                    print(f"Error: Datos en la señal '{nombre}' exceden las dimensiones declaradas o son inválidos.")
                    break

                # Guardar el dato en la matriz temporal
                fila_matriz = matriz_operar.index(t_dato - 1)
                if fila_matriz:
                    fila_matriz.value.index(A_dato - 1).value = int(dato.text)
                else:
                    fila = ListaSimple()
                    for _ in range(A):
                        fila.add(0)
                    fila.index(A_dato - 1).value = int(dato.text)
                    matriz_operar.add(fila)

            # Guardar la señal si los datos son válidos
            if datos_validos:
                matriz.guardarSeñal(matriz_operar)

    except Exception as e:
        print('Ocurrio un error:', str(e))
    return matriz

def procesar_archivo(matriz):
    # Verificación si la matriz no está cargada
        if matriz is None or len(matriz.señales) == 0:
            print("Error: No se ha cargado ninguna matriz.")
            return 
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
        return matriz_reducida


def escribir_archivo_salida(matriz_reducida):
        if matriz_reducida is None or len(matriz_reducida.matrices_reducidas) == 0:
            print("Error: No se ha cargado ninguna matriz.")
            return 
        print("\nArchivos de Salida")
        print("Escribiendo archivo...")
        try:
            xml_str = '<?xml version="1.0"?>\n'
            xml_str += '<senalesReducidas>\n'

            # Iterar sobre todas las matrices reducidas
            matriz_reducida_index = 0
            matriz_reducida_current = matriz_reducida.matrices_reducidas.first
            while matriz_reducida_current:
                matriz_reducida_actual = matriz_reducida_current.value

                # Añadir etiqueta de señal al XML
                xml_str += '\t<senal nombre="Señal {}" A="{}">\n'.format(matriz_reducida_index + 1, len(matriz_reducida_actual.index(0).value))

                fila_index = 0
                fila_current = matriz_reducida_actual.first
                while fila_current:
                    fila = fila_current.value

                    # Obtener tiempos para el grupo actual
                    grupo_str = str(fila)
                    tiempos = matriz_reducida.encontrarTiemposPorGrupo(grupo_str)
                    tiempos_str = ",".join(str(tiempo) for tiempo in tiempos) if tiempos else ""

                    # Añadir etiqueta de grupo al XML
                    xml_str += '\t\t<grupo g="{}">\n'.format(fila_index + 1)
                    xml_str += '\t\t\t<tiempos>{}</tiempos>\n'.format(tiempos_str)
                    xml_str += '\t\t\t<datosGrupo>\n'

                    # Iterar sobre los datos de la fila y añadirlos al XML
                    dato_index = 0
                    dato_current = fila.first
                    while dato_current:
                        dato = dato_current.value
                        xml_str += '\t\t\t\t<dato A="{}">{}</dato>\n'.format(dato_index + 1, dato)
                        dato_index += 1
                        dato_current = dato_current.next

                    xml_str += '\t\t\t</datosGrupo>\n'
                    xml_str += '\t\t</grupo>\n'

                    fila_index += 1
                    fila_current = fila_current.next
                
                xml_str += '\t</senal>\n'
                matriz_reducida_index += 1
                matriz_reducida_current = matriz_reducida_current.next

            xml_str += '</senalesReducidas>\n'

            # Escribir el XML a un archivo de salida
            with open("salida.xml", "w", encoding="utf-8") as f:
                f.write(xml_str)

            print("Archivo de salida escrito correctamente.")
                
        except Exception as e:
            print(f"Ocurrió un error al escribir el archivo de salida: {str(e)}")