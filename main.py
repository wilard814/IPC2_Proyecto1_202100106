#main.py
from LecturaXML import LecturaXML

def main():
    lectura = None
    while True:
        print("Menú principal:")
        print("1. Cargar archivo")
        print("2. Procesar archivo")
        print("3. Escribir archivo salida")
        print("4. Mostrar datos del estudiante")
        print("5. Generar gráfica")
        print("6. Inicializar sistema")
        print("7. Salida")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            archivo = input("Ingrese la ruta del archivo XML: ")
            lectura = LecturaXML(archivo)
            print("Archivo cargado exitosamente.")

        elif opcion == "2":
            if lectura is not None:
                procesar_archivo(lectura)
            else:
                print("Debe cargar un archivo primero.")

        elif opcion == "3":
           
            pass

        elif opcion == "4":
            print("Datos del estudiante:")
            print("Nombre: Keneth Willard Lopez Ovalle")
            print("Carné: 202100106")
            print("Curso: Introducción a la Programación y Computación 2")
            print("Carrera: Ingeniería en Ciencias y Sistemas")
            print("Semestre: 6to")

        elif opcion == "5":
            
            pass

        elif opcion == "6":
            
            pass

        elif opcion == "7":
            print("¡Hasta luego!")
            break

        else:
            print("Opción no válida. Por favor, seleccione una opción válida.")

def procesar_archivo(lectura):
    senales = lectura.getSenales().getInicio()

    while senales is not None:
        senal = senales.getDato()
        print(f"Procesando señal: {senal.getNombre()}")

        matriz_frecuencia = senal.calcular_matriz_frecuencia()
        matriz_binaria = calcular_matriz_binaria(matriz_frecuencia)  

        print("Matriz de frecuencia:")
        for fila in matriz_frecuencia:
            print(" ".join(map(str, fila)))

        print("Matriz binaria:")
        for fila in matriz_binaria:  
            print(" ".join(map(str, fila)))

        matriz_reducida = calcular_matriz_reducida(matriz_frecuencia, matriz_binaria)

        print("Matriz reducida:")
        for fila in matriz_reducida:
            print(" ".join(map(str, fila)))

        senales = senales.getSiguiente()

def calcular_matriz_binaria(matriz_frecuencia):
    matriz_binaria = []

    for fila in matriz_frecuencia:
        fila_binaria = []
        for valor in fila:
            if valor > 0:
                fila_binaria.append(1)
            else:
                fila_binaria.append(0)
        matriz_binaria.append(fila_binaria)

    return matriz_binaria

def calcular_matriz_reducida(matriz_frecuencia, matriz_binaria):
    matriz_reducida = [[0] * len(matriz_frecuencia[0]) for _ in range(len(matriz_frecuencia))]
    
    for i in range(len(matriz_frecuencia)):
        for j in range(len(matriz_frecuencia[0])):
            if matriz_binaria[i][j] == 1:
                for k in range(len(matriz_frecuencia)):
                    matriz_reducida[k][j] += matriz_frecuencia[k][j]
    
    return matriz_reducida
if __name__ == "__main__":
    main()

