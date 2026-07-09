#LISA CONTARDO SM3201635
"""
classe che coordina tutte le classi per produrre l'immagine finale e salvarla come PNG:
prima disegna il fondale tile per tile, poi gli sprite nell'ordine della
lista, poi converte il frame buffer indicizzato in RGB e salva il PNG.
"""
import numpy as np
from PIL import Image
from exceptions import RenderError
from blitter import Blitter 

class RenderingPipeline:
    FB_RIGHE = 480
    FB_COLONNE  = 640

    """
    inizializza la pipeline con i dati gia' caricati
    input: 3 oggetti
    output: /
    """
    def __init__(self, palette, vram, scena):
        #creo riferimenti per la classe RenderingPipeline
        self.palette = palette
        self.vram    = vram
        self.scena   = scena

    """
    funzione chiamata nel main che avvia la pipeline: crea il frame buffer, disegna il fondale, 
    disegna gli sprite, converte in RGB e salva il file PNG.
    input: percorso del file PNG da salvare.
    output: salva PNG nel percorso indicato
    """
    def esegui(self, output_path: str):
        # crea matrice 480x640 di zeri
        frame_buffer = np.zeros((self.FB_RIGHE, self.FB_COLONNE), dtype=np.uint8)

        # crea il Blitter passandogli vram e frame buffer
        blitter = Blitter(self.vram, frame_buffer)
        #a sua volta modifica frame_buffer riempiendolo di indici

        self._disegna_fondale(blitter)
        self._disegna_oggetti(blitter)

        # converti il frame buffer da indici a RGB e salva
        self._salva_png(frame_buffer, output_path)

    """
    disegna tutti i tile del fondale nel frame buffer
    input: blitter (Blitter): oggetto che sa disegnare i tile
    output: no, modifica il frame buffer tramite il blitter
    """
    def _disegna_fondale(self, blitter):

        #per ogni elemento della lista di liste(griglia 15x20) 
        for riga in range(len(self.scena.tile_map)):
            for colonna in range(len(self.scena.tile_map[riga])):
                
                #scorro la matrice 256x256 e lavoro con 1 singolo tile(32x32) 
                tile_id = self.scena.tile_map[riga][colonna]
                
                x  = colonna * 32  
                y  = riga    * 32 
                
                #funzione che estrae il tile ID dal tile sheet e lo copia nel frame buffer
                blitter.disegna_tile(tile_id, x, y)

    """
    disegna tutti gli sprite nel frame buffer
    input: blitter (Blitter): oggetto che sa disegnare gli sprite
    output: no, modifica il frame buffer tramite il blitter
    """
    def _disegna_oggetti(self, blitter):
        #per ogni dizionario della lista
        for sprite in self.scena.sprites:
            blitter.disegna_sprite(
                sprite["id"],
                sprite["x"],
                sprite["y"],
                sprite["flip_h"],
                sprite["flip_v"],
                sprite["rotation"],
                self.scena.transparent_index
            )

    """
    Converte il frame buffer da indici di palette a RGB e salva il PNG
    Per ogni pixel del frame buffer (un indice da 0 a 15), recupera
    il colore RGB corrispondente dalla palette e lo scrive nell'immagine
    finale. Usa Pillow solo per il salvataggio finale.
    input: frame_buffer, matrice (480, 640) di indici di palette 
            + output_path, percorso del file PNG da salvare.
    output:no, salva il file PNG nel percorso indicato
    """
    def _salva_png(self, frame_buffer, output_path):

        # self.palette.colors e' la tabella (16, 3)
        # uso come "dizionario" numpy: palette.colors[frame_buffer] sostituisce
        # ogni indice con la sua terna RGB in una sola operazione
        immagine_rgb = self.palette.colors[frame_buffer]

        # usa Pillow per salvare il PNG
        try:
            immagine = Image.fromarray(immagine_rgb, mode="RGB")
            immagine.save(output_path)
        except Exception as e:
            raise RenderError(f"Impossibile salvare il file PNG: {output_path} ({e})")