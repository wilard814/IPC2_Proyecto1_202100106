#LecturaXML.py
import xml.etree.ElementTree as ET
from Lista_simple import ListaSimple
from Signal import Signal

class LecturaXML():
    def __init__(self, path):
        self.raiz = ET.parse(path).getroot()

    def getSenales(self):
        listSenales = ListaSimple()
        for senal in self.raiz.findall('senal'):
            nombreSenal = senal.get('nombre')
            tiempoMaximo = senal.get('t')
            amplitudMaxima = senal.get('A')
            tmpSenal = Signal(nombreSenal, tiempoMaximo, amplitudMaxima)
            listSenales.agregarFinal(tmpSenal)  

       
        print("_____Lista de senales_____")
        senalGuardada = listSenales.getInicio()
        while senalGuardada != None:
            print(senalGuardada.getDato().getNombre())
            senalGuardada = senalGuardada.getSiguiente()
        
    def getDatos(self):
        pass
