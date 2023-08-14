
opcion = 0

while opcion != 7:
    print("1. Cargar archivo")
    print("2. Procesar archivo")
    print("3. Escribir archivo de salida")
    print("4. Mostrar datos del estudiante")
    print("5. Generar gráfica")
    print("6. Incializar sistema")
    print("7. Salir")
    opcion = int(input("Ingrese una opción: "))

    if opcion == 1:
        print("Cargar archivo")
        print ("Ingrese la ruta del archivo:")
    elif opcion == 2:
        print("Procesar archivo")
        print("Calculando la matriz binaria...")
        print("Realizando suma de tuplas...")
    elif opcion == 3:
        print("Escribir archivo de salida")
    elif opcion == 4:
        print("Mostrar datos del estudiante")
        print("> Keneth Willard López Ovalle")
        print(">202100106")
        print("Ingeniería en Ciencias y Sistemas")
        print("6to. Semestre")
    elif opcion == 5:
        print("Generar gráfica")
    elif opcion == 6:
        print("Incializar sistema")
    elif opcion == 7:
        print("Salir")
        break                    
    
