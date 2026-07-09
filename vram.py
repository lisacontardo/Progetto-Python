#LISA CONTARDO SM3201635
"""
classe che legge file binari e li trasforma in matrici utilizzabili
"""

import numpy as np
from exceptions import VRAMError

class VirtualVRAM():

    #prende in input i percorsi dei file binari e delega al metodo privato
    def __init__ (self, tiles_path: str, sprites_path: str):

        self.tiles = self._load(tiles_path) #contiene i 64 tile
        self.sprites = self._load(sprites_path) #contiene i 16 sprite

    #legge file binario e lo spacchetta in matrice 256x256 pixel
    #input: percorso del file .bin da 32768 bytes
    #output: np.ndarray di forma (256, 256), dtype uint8 con valori tra 0-15(indici palette)
    def _load(self, path:str):
        
        EXPECTED_BYTES = 32768

        #leggo byte grezzi dal file
        try:
            with open(path, "rb") as f:
                bytes_grezzi = f.read()
        except FileNotFoundError:
            raise VRAMError(f"File binario non trovato: {path}")

        if len(bytes_grezzi) != EXPECTED_BYTES:
            raise VRAMError(f"Dimensione errata: attesi {EXPECTED_BYTES} byte, trovati {len(bytes_grezzi)}")
        
        #np.frombuffer converte in array numpy 1D di 32768 numeri(uno per byte) 
        bytes_array = np.frombuffer(bytes_grezzi, dtype=np.uint8)

        #operazione di shift a destra
        #per ogni byte sposta i primi 4 bit a destra --> ottieni primo pixel
        pixel1 = bytes_array >> 4     #array da 32768 elementi 
        
        #operazione AND bit a bit 
        #applica operazione a ogni elemento: azzera i 4 bit alti e tiene i 4 bassi 
        pixel2 = bytes_array & 0x0F      #array da 32768 elementi

        #array vuoto da 65536 elementi (totale pixel)
        pixels = np.empty(65536, dtype=np.uint8)
        
        #riempio array
        pixels[0::2] = pixel1 
        pixels[1::2] = pixel2
        
        #ridimensiona in  array numpy 256x256
        return pixels.reshape(256, 256)

