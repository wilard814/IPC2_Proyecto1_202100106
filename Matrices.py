from Lista_simple import ListaSimple

class Matriz:

    def __init__(self):
        self.nombre = ListaSimple()
        self.fila = ListaSimple()
        self.columna = ListaSimple()
        self.dato = ListaSimple()

    def guardar(self, nombre, t, A, dato):
        self.nombre.add(nombre)
        self.fila.add(t)
        self.columna.add(A)
        self.dato.add(dato)

    def crearMatrizPatrones(self):
        matriz_patron = ListaSimple()
        lista = ListaSimple()
        listaJ = ListaSimple()
        listaK = ListaSimple()
        for i in range(len(self.dato)):
            lista = self.dato.index(i).value
            fila = ListaSimple()
            for j in range(len(lista)):
                listaJ = lista.index(j).value
                columna = ListaSimple()
                for k in range(len(listaJ)):
                    listaK = listaJ.index(k).value
                    if listaK.value > 0:
                        columna.add(1)
                    else:
                        columna.add(0)
                fila.add(columna)
            matriz_patron.add(fila)
        return matriz_patron

    def grupos_Matriz(self, indice):
        unico = ListaSimple()
        fila_binaria = self.dato.index(indice).value  # Usamos el índice recibido como argumento para acceder al valor

        if unico.buscar(str(fila_binaria)) == False:
            unico.add(str(fila_binaria))

        grupos = ListaSimple()

        for i in range(len(unico)):
            contador = 0
            repetidos = ListaSimple()

            for j in range(len(self.dato)):
                if str(unico.index(i)) == str(self.dato.index(j)):
                    repetidos.add(contador)
                contador += 1

            grupos.add(repetidos)

        return grupos

class Matriz_Reducida:

    def __init__(self):
        self.nombre = ListaSimple()
        self.fila = ListaSimple()
        self.columna = ListaSimple()
        self.grupos = ListaSimple()
        self.frecuencia = ListaSimple()
        self.no_frecuencia = ListaSimple()
        self.matriz = ListaSimple()

    def guardar(self, nombre, t, A, g, f, no_f, matriz):
        self.nombre.add(nombre)
        self.fila.add(t)
        self.columna.add(A)
        self.grupos.add(g)
        self.frecuencia.add(f)
        self.no_frecuencia.add(no_f)
        self.matriz.add(matriz)
