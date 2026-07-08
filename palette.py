# LISA CONTARDO SM3201635
"""
questa classe è responsabile di caricare e validare la palette di 16 colori
usata dal renderer e di risolvere un indice di palette (0-15) 
nel corrispondente colore RGB  
"""
import json
import numpy as np

from exceptions import Paletteerror

class Palette:
    NUM_COLORS = 16 
    #costruttore riceve percorso del file
    def __init__(self, json_path: str): #dovrebbe essere una stringa
        data = self._load(json_path) 
        self.colors = self._validate_converte(data)

    #legge percorso e restituisce il contenuto come lista python
    def _load(self, path):
        try:
        #prova ad aprire il file palette.json
            with open(path, "r") as f:
                return json.load(f) #lista grezza
        except FileNotFoundError:
        #se il file non esiste
            raise PaletteError("File non trovato.")
        #file esiste ma il JSON è malformato
        except json.JSONDecodeError:
            raise SceneError(f"File della scena non è un JSON valido: {path}")
        


    #controlla la lista e converte in array numpy
    #creo corrispondenza tra indici (che trovo nel disegno) e colori RGB nella lista
    def _validate_converte(self, data):
        #controllo il tipo esterno 
        if not isinstance(data, list):
            raise PaletteError("La palette deve essere una lista")
        
        #controllo dimensione
        if len(data) != self.NUM_COLORS:
            raise PaletteError(f"La palette deve avere esattamente {self.NUM_COLORS} colori")

        for i, color in enumerate(data):
            #controllo il tipo di ogni elemento interno della lista
            if not isinstance(color, list) or len(color) != 3:
                raise PaletteError(f"Il colore {i} non è una terna RGB: {color}")
            #controllo ogni colore
            for element in color:
                if not isinstance(element, int) or not (0 <= element <= 255):
                    raise PaletteError(f"Valore non valido nel colore {i}")
        #converte e ritorna array numpy 16x3 
        return np.array(data, dtype=np.uint8) 


    #Restituisce il colore RGB corrispondente a un indice di palette
    def get_rgb(self, index: int):
    
        if not isinstance (index, (int, np.integer)) or not (0 <= index < self.NUM_COLORS):
            raise PaletteError(f"Indice non valido: {index}")
        
        #ritorna riga 'index' della tabella 
        return self.colors[index]
    
    

