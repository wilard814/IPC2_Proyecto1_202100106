from Grafica import *
from Procesamiento import *

matriz = None
matriz_reducida = None

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

    if not opcion:
        print('Opcion no valida')
        continue

    if opcion == '1':
        matriz =cargar_archivo()
        continue

    if opcion == '2':
        matriz_reducida = procesar_archivo(matriz)
        continue

    if opcion == '3':
        escribir_archivo_salida(matriz_reducida)
        continue

    if opcion == '4':
        mostrar_datos_estudiante()
        continue

    if opcion == '5':
        generar_grafica(matriz, matriz_reducida)
        continue

    if opcion == '6':
        print('Inicializando sistema...')
        time.sleep(0.3)
        matriz = Matriz()
        matriz_reducida = MatrizReducida()
        print('El sistema ha sido Inicializado')
        continue

    if opcion == '7':
        break


