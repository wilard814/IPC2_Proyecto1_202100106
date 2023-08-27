class Node(object):

    def __init__(self, value):
        self.value = value
        self.next = None

    def __str__(self):
        return str(self.value)

    def get(self):
        return self.value


class ListaSimple(object):

    def __init__(self):
        self.first = None
        self.size = 0

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

    def index(self, numero):
        current = self.first
        for _ in range(numero):
            if current is None:
                return None
            current = current.next
        return current

    def buscar(self, dato):
        current = self.first
        while current:
            if current.value == dato:
                return True
            current = current.next
        return False

    def __len__(self):
        return self.size

    def recorrer(self):
        current = self.first
        for _ in range(len(self)):
            print('current =', current)
            current = current.next

    def __str__(self):
        elements = [str(current) for current in self]
        return "[" + ", ".join(elements) + "]"

    def __iter__(self):
        current = self.first
        while current:
            yield current.value
            current = current.next