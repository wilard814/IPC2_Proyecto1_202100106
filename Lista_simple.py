class Node(object):
    # Constructor: Inicializa el nodo con un valor y el siguiente nodo como None
    def __init__(self, value):
        self.value = value
        self.next = None

    # Método para representar el nodo como una cadena
    def __str__(self):
        return str(self.value)

    # Método para obtener el valor del nodo
    def get(self):
        return self.value
    
class ListaSimple(object):
    # Constructor: Inicializa una lista vacía
    def __init__(self):
        self.first = None
        self.size = 0

    # Método para agregar un nuevo nodo al final de la lista
    def add(self, dato):
        new_node = Node(dato)
        if self.size == 0:
            self.first = new_node
        else:
            current = self.first
            while current.next is not None:
                current = current.next
            current.next = new_node
        self.size += 1
        return new_node

    # Método para obtener el nodo en una posición específica
    def index(self, numero):
        current = self.first
        for _ in range(numero):
            if current is None:
                return None
            current = current.next
        return current

    # Método para buscar un dato en la lista
    def buscar(self, dato):
        current = self.first
        while current:
            if current.value == dato:
                return True
            current = current.next
        return False

    # Método para obtener el tamaño de la lista
    def __len__(self):
        return self.size

    # Método para recorrer y mostrar los nodos de la lista
    def recorrer(self):
        current = self.first
        for _ in range(len(self)):
            print('current =', current)
            current = current.next

    # Método para representar la lista como una cadena
    def __str__(self):
        elements = [str(current) for current in self]
        return "[" + ", ".join(elements) + "]"

    # Método para iterar sobre los nodos de la lista
    def __iter__(self):
        current = self.first
        while current:
            yield current.value
            current = current.next
