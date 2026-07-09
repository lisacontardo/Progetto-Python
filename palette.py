# LISA CONTARDO SM3201635
"""
questa classe è responsabile di caricare e validare la palette di 16 colori
usata dal renderer e di risolvere un indice di palette (0-15) 
nel corrispondente colore RGB  
"""
import json
import numpy as np

from exceptions import PaletteError

class Palette:
    NUM_COLORS = 16 
    #costruttore riceve percorso del file
    def __init__(self, json_path: str): #dovrebbe essere una stringa
        data = self._load(json_path) 
        self.colors = self._validate_converte(data)

    """
    legge percorso e restituisce il contenuto come lista python
    input: path (str), percorso del file palette.json
    output: lista python grezza (non ancora validata)
    """
    def _load(self, path):
        try:
            with open(path, "r") as f:
                return json.load(f) #lista di liste grezza
        except FileNotFoundError:
            raise PaletteError("File non trovato.")

        #file esiste ma il JSON è malformato
        except json.JSONDecodeError:
            raise SceneError(f"File della scena non è un JSON valido: {path}")
    """   
    controlla la lista e converte in array numpy
    creo corrispondenza tra indici (che trovo nel disegno) e colori RGB nella lista
    input:  data, lista python grezza (letta dal JSON)
    output: np.ndarray di forma (16, 3)
    """
    def _validate_converte(self, data):
        #controlli
        if not isinstance(data, list):
            raise PaletteError("La palette deve essere una lista")
        
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

    """
    Restituisce il colore RGB corrispondente a un indice di palette
    input: indice di palette (0-15)
    output: array numpy di 3 elementi (riga corrispondente a un colore RGB)
    """
    def get_rgb(self, index: int):
    
        if not isinstance (index, (int, np.integer)) or not (0 <= index < self.NUM_COLORS):
            raise PaletteError(f"Indice non valido: {index}")
        
        #ritorna riga 'index' della matrice
        return self.colors[index]
    
    

