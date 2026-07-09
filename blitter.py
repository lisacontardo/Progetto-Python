#LISA CONTARDO SM3201635
"""
classe che si occupa di estrarre tile/sprite dai rispettivi sheet in VRAM, 
applica trasformazioni e li copia nel frame buffer 
"""
import numpy as np
from exceptions import BlitterError

class Blitter:
    #attributi di classe
    FB_RIGHE   = 480
    FB_COLONNE   = 640

    TILE_SIZE   = 32
    TILE_COL   = 8

    SPRITE_SIZE = 64
    SPRITE_COL = 4

    """
    input: vram (oggetto con matrici tiles e sprites)
    + frame_buffer (matrice np.ndarray 480x640 vuota creata in pipeline.py) 
    output: no, effettuo modifiche sulla matrice 480x640
    """
    def __init__(self, vram, frame_buffer):
        #creo riferimento alle matrici in input per la classe blitter per effettuare modifiche
        self.vram = vram 
        self.frame_buffer = frame_buffer 

    """
    funzione che disegna un tile del fondale (estrae tile da sheet e copia  in frame buffer)
    input: id del tile, colonna(x) e riga(y) di destinazione
    output: no, modifica self.frame_buffer
    """
    def disegna_tile(self, tile_id, x, y):
        
        if not isinstance(tile_id, int) or not (0 <= tile_id <= 63):
            raise BlitterError(f"tile_id non valido")
        
        #estrae tile di 32x32pixel (self.vram.tiles)
        tile = self._estrai_da_sheet(
            self.vram.tiles, #matrice 256x256 di tile
            tile_id,
            self.TILE_SIZE,
            self.TILE_COL
        ) 
        #funzione che copia il tile(32x32) di numeri (0-15)
        self._copia_buffer(tile, x, y, trasparenza=None)

    """
    funzione che disegna uno sprite (estrae sprite da sheet, lo trasforma e lo copia)
    input: dettagli degli sprite presi da scene.json
    output: no, modifica self.frame_buffer
    """
    def disegna_sprite(self, sprite_id, x, y, flip_h, flip_v, rotation, transparent_index):
         
        if not isinstance(sprite_id, int) or not (0 <= sprite_id <= 15):
            raise BlitterError(f"sprite_id non valido")
        if rotation not in {0, 90, 180, 270}:
            raise BlitterError(f"rotation non valida: {rotation}")
        
        #estrae sprite 64x64 pixel (self.vram.sprites)
        sprite = self._estrai_da_sheet(
            self.vram.sprites, #matrice 256x256 di sprites
            sprite_id,
            self.SPRITE_SIZE,
            self.SPRITE_COL
        ) 
        sprite = self._trasformazioni(sprite, flip_h, flip_v, rotation)
        #copia lo sprite64x64 di numeri (0-15)
        self._copia_buffer(sprite, x, y, trasparenza=transparent_index)

    """ 
    GLI INDICI PER TILE /SPRITE VENGONO USATI SOLO PER MAPPARE/ESTRARRE CORRETTAMENTE 
    IL TILE/SPRITE dal tile/sprite sheet --> al frame buffer
    l'ordinamento viene fornito dal file scene.json che contiene una matrice 15x20 di INDICI (0-15)
    """

    """
    funzione che seleziona un quadrato della matrice originale 256x256 
    sulla base dell'indice passato in input 
    input: self.vram.tiles/sprites (256x256), ID desiderato, 32/64 pixels, 8/4 elementi
    output: ritaglia blocco 32x32 o 64x64 pixel (matrice numpy)
    """
    def _estrai_da_sheet(self, sheet, element_id, size, elementi_per_riga):
        #divisione intera (ID // elementi per riga)
        riga = element_id // elementi_per_riga 
        #quanto avanza (resto divisione)
        colonna = element_id % elementi_per_riga

        #trovo posizione iniziale in pixel
        r_inizio = riga * size
        c_inizio = colonna * size

        #estrae tile o sprite corrispondente da tile/sprite sheet in base all'ID
        return sheet[r_inizio:r_inizio + size,  c_inizio:c_inizio + size] #matrice numpy 

    """
    applica flip e rotazione a uno sprite(matrice di forma 64x64 pixel)
    input: matrice numpy di pixel da trasformare usando dettagli da scene_parser
    output: nuovo sprite trasformato
    """
    def _trasformazioni(self, sprite, flip_h, flip_v, rotation):
        if flip_h:
            sprite = np.fliplr(sprite)   # specchia orizzontalmente
        if flip_v:
            sprite = np.flipud(sprite)   # specchia verticalmente
        if rotation == 90:
            sprite = np.rot90(sprite, k=3)
        elif rotation == 180:
            sprite = np.rot90(sprite, k=2)
        elif rotation == 270:
            sprite = np.rot90(sprite, k=1)

        return sprite 

    """
    funzione che copia tile/sprite nel frame buffer anche se è parzialmente fuori schermo
    x, y = posizioni di destinazione - suffisso 1=inizio intervallo e suffisso 2 = fine intervallo
    input: tile/sprite, pixel di destinazione, trasparenza
    output: matrice frame_buffer modificata contenente indici di palette per ogni pixel
    """
    def _copia_buffer(self, img, x, y, trasparenza=None):
        # altezza, larghezza dell'immagine(tile/sprite)
        h, w = img.shape   

        #regole per disegnare in frame buffer

        #inizio e fine intervallo colonne
        dst_x1 = max(0, x)                        #non prima della colonna 0
        dst_x2 = min(self.FB_COLONNE,  x + w)       #non oltre l'ultima colonna

        #inizio e fine intervallo righe
        dst_y1 = max(0, y)                        #non prima della riga 0
        dst_y2 = min(self.FB_RIGHE, y + h)       #non oltre l'ultima riga

        #sprite/tile interamente fuori dallo schermo
        if dst_x1 >= dst_x2 or dst_y1 >= dst_y2:
            return
        #ignoro e passo sprite/tile successivo

        #regole per l'immagine sorgente (tile/sprite)
        #inizio dell'intervallo sorgente: saltare pixel che stanno fuori
        #se x o y sono negativi, -x/-y dice quante caselle saltare (punto di partenza)
        src_x1 = max(0, -x)
        src_y1 = max(0, -y)
        #fine dell'intervallo sorgente 
        src_x2 = src_x1 + (dst_x2 - dst_x1)
        src_y2 = src_y1 + (dst_y2 - dst_y1)

        #ritaglio pixel da copiare 
        sorgente = img[src_y1:src_y2, src_x1:src_x2]
        #destinazione è il pezzo del frame buffer dove copiare il tile/sprite
        destinazione = self.frame_buffer[dst_y1:dst_y2, dst_x1:dst_x2]

        #si tratta di un tile
        if trasparenza is None:
            destinazione[:] = sorgente
        #si tratta di uno sprite
        else:
            # dove è trasparente NON copio
            maschera = sorgente != trasparenza #contiene true solo
            destinazione[maschera] = sorgente[maschera]