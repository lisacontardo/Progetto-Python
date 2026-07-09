#LISA CONTARDO SM3201635
"""
classe che legge e valida il file JSON che descrive la scena
"""
import json
from exceptions import SceneError

class SceneParser:
    #attributi di classe
    TILE_ROWS    = 15
    TILE_COLS    = 20
    MAX_TILE_ID      = 63   # 64 tile in totale
    MAX_SPRITE_ID    = 15   # 16 sprite in totale
    VALID_ROTATIONS  = {0, 90, 180, 270} #set

    def __init__(self, path: str):
        data = self._load(path) #dizionario grezzo
        #attributi di istanza
        self.transparent_index = self._func_transparent_index(data) #int
        self.tile_map          = self._func_tile_map(data) #list[list[int]]
        self.sprites           = self._func_sprites(data) #list[dict]

    """
    funzione che apre file JSON e restituisce il contenuto come dizionario Python
    input: percorso file json
    output: dizionario python con dati grezzi
    """
    def _load(self, path: str):
        try:
            with open(path, "r") as f:
                return json.load(f)
        #caso 1: file non esiste
        except FileNotFoundError:
            raise SceneError(f"File della scena non trovato: {path}")
        #caso 2: file esiste ma il JSON è malformato
        except json.JSONDecodeError:
            raise SceneError(f"File della scena non è un JSON valido: {path}")
        
    """
    controlla il campo transparent_index e lo restituisce
    input: dizionario python con dati grezzi
    output: intero tra 0 e 15
    """
    def _func_transparent_index(self, data: dict):
    
        if "transparent_index" not in data:
            raise SceneError("Campo 'transparent_index' mancante nel JSON")
        #accedo e estraggo
        index = data["transparent_index"]
        
        if not isinstance(index, int) or not (0 <= index <= 15):
            raise SceneError(f"'transparent_index' non valido: {index} ")
        
        return index

    """
    controlla la griglia tile_map e la restituisce 
    input: dizionario python con dati grezzi
    output: lista di 15 liste (ognuna con 20 interi tra 0 e 63): ID del tile
    """
    def _func_tile_map(self, data: dict): 

        if "tile_map" not in data:
            raise SceneError("Campo 'tile_map' mancante nel JSON")

        #accedo e estraggo
        tile_map = data["tile_map"]
        
        if not isinstance(tile_map, list):
            raise SceneError("Non è una lista")

        if (len(tile_map) != self.TILE_ROWS):
            raise SceneError(f"'tile_map' deve avere esattamente {self.TILE_ROWS} righe")
        
        #scendo di 1 livello e controllo ogni riga della lista singolarmente
        for r, row in enumerate(tile_map):
            if not isinstance(row, list):
                raise SceneError("La riga deve essere una lista")
            if (len(row) != self.TILE_COLS):
                raise SceneError(f"La riga {r} della tile_map deve avere {self.TILE_COLS} elementi")
            
            #scendo di 1 livello e controllo ogni numero della riga
            for i, tile_id in enumerate(row):
                if not isinstance(tile_id, int):
                    raise SceneError(f"ID del tile non valido, deve essere un intero")
                if not (0 <= tile_id <= self.MAX_TILE_ID):
                    raise SceneError(f"(deve essere un intero tra 0 e {self.MAX_TILE_ID})")

        return tile_map #lista di liste

    """
    controlla la lista degli sprite e la restituisce
    input: dizionario python con dati grezzi
    output: lista di dizionari(1 dizionario per sprite)
    """
    def _func_sprites(self, data: dict):

        if "sprites" not in data:
            raise SceneError("Campo 'sprites' mancante nel JSON")

        sprites = data["sprites"]

        if not isinstance(sprites, list):
            raise SceneError("'sprites' deve essere una lista")
        
        #controllo di ogni dizionario 
        for i, sprite in enumerate(sprites):
            self._validate_sprite(sprite, i)

        return sprites #lista di dizionari se sono validi
    
    """
    funzione che controlla 1 singolo sprite
    input: sprite(dizionario) + i(indice dello sprite nella lista)
    output: solleva eccezioni se non conforme ai controlli
    """
    def _validate_sprite(self, sprite: dict, i: int):
        # controlla esistenza dei campi
        for campo in ("id", "x", "y", "flip_h", "flip_v", "rotation"):
            if campo not in sprite:
                raise SceneError(f"Campo '{campo}' mancante nello sprite {i}")
        #controlli specifici
        if not isinstance(sprite["id"], int):
            raise SceneError(f"'id' nello sprite {i} non e' un intero: {sprite['id']}")
        if not (0 <= sprite["id"] <= 15):
            raise SceneError(f"'id' nello sprite {i} e' fuori range: {sprite['id']} (deve essere tra 0 e 15)")

        #può essere negativo
        for campo in ("x", "y"):
            if not isinstance(sprite[campo], int):
                raise SceneError(f"'{campo}' non valido nello sprite {i}, deve essere intero")

        for campo in ("flip_h", "flip_v"):
            if not isinstance(sprite[campo], bool):
                raise SceneError(f"'{campo}' non valido nello sprite {i}: deve essere booleano")
            
        if sprite["rotation"] not in self.VALID_ROTATIONS:
            raise SceneError(
                f"'rotation' non valido nello sprite {i}, i valori ammessi sono 0, 90, 180, 270 ")

