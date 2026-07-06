#LISA CONTARDO SM3201635
"""
classe che legge file binari e li trasforma in matrici utilizzabili
"""

import numpy as np
from exceptions import VRAMError

class VirtualVRAM():

    def __init__ (self, tiles_path: str, sprites_path: str):
        #ottengo 2 matrici 256x256 
        self.tiles = self._load(tiles_path) #contiene i 64 tile
        self.sprites = self._load(sprites_path) #contiene i 16 sprite

    #legge file binario packed a 4 bit e lo spacchetta in matrice 256x256
    #input: percorso del file .bin
    #output: np.ndarray di forma (256, 256), dtype uint8, valori 0-15
    def _load(self, path:str):
        EXPECTED_BYTES = 32768
        #leggo byte grezzi dal file
        try:
            with open(path, "rb") as f:
                bytes = f.read()
        except FileNotFoundError:
            raise VRAMError(f"File binario non trovato: {path}")

        if len(bytes) != self.EXPECTED_BYTES:
            raise VRAMError(f"Dimensione errata: attesi {EXPECTED_BYTES} byte, trovati {len(bytes)}")
        
        #converto in array numpy di 32768 numeri(uno per byte) - cambia solo il tipo di oggetto
        bytes_array = np.frombuffer(bytes, dtype=np.uint8)

        #per ogni byte sposta i primi 4 bit a destra --> ottieni primo pixel
        array_alti = bytes_array >> 4     #array da 32768 elementi 
        #applica operazione a ogni elemento: azzera i 4 bit alti e tiene i 4 bassi 
        array_bassi = bytes_array & 0x0F      #array da 32768 elementi

        #array vuoto da 65536 elementi (totale pixel)
        pixels = np.empty(65536, dtype=np.uint8)
        #riempio array
        pixels[0::2] = array_alti #metto primi pixel dei bytes
        pixels[1::2] = array_bassi 
        
        #ottengo 1 numero per pixel
        #ridimensiona in griglia 256x256
        return pixels.reshape(256, 256)

