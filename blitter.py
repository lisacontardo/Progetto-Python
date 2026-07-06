#LISA CONTARDO SM3201635

import numpy as np
from exceptions import BlitterError

class Blitter:

    FB_WIDTH    = 640
    FB_HEIGHT   = 480
    TILE_SIZE   = 32
    SPRITE_SIZE = 64
    TILE_COLS   = 8
    SPRITE_COLS = 4

    """
    input: vram (oggetto con matrici tiles e sprites)
    + frame_buffer (matrice np.ndarray 480x640 di indici di palette) 
    output: /
    """
    def __init__(self, vram, frame_buffer):
        self.vram = vram
        self.frame_buffer = frame_buffer

    """
    funzione che estrae un tile dal tile sheet (scene_parser) e lo copia nel frame buffer
    input: id del tile, colonna(x) e riga(y) di destinazione
    output: no, modifica self.frame_buffer
    """
    def disegna_tile(self, tile_id, dest_x, dest_y):
        
        if not isinstance(tile_id, int) or not (0 <= tile_id <= 63):
            raise BlitterError(f"tile_id non valido")
        
        #estrae tile di 32x32pixel da virtualvram(matrice 256x256)
        tile = self._estrai_tile(tile_id) 
        #funzione che copia il tile(32x32) di numeri (0-15)
        self._copia_buffer(tile, dest_x, dest_y, trasparenza=None)

    """
    funzione che estrae uno sprite dallo sprite sheet(scene_parser), lo trasforma e lo copia nel fb
    input: dettagli degli sprite presi da scene.json
    output: no, modifica self.frame_buffer
    """
    def disegna_sprite(self, sprite_id, dest_x, dest_y, flip_h, flip_v, rotation, transparent_index):
         
        if not isinstance(sprite_id, int) or not (0 <= sprite_id <= 15):
            raise BlitterError(f"sprite_id non valido: {sprite_id}")

        if rotation not in {0, 90, 180, 270}:
            raise BlitterError(f"rotation non valida: {rotation}")
        
        #estrae sprite 64x64 pixel da virtualvram(matrice 256x256)
        sprite = self._estrai_sprite(sprite_id)
        sprite = self._trasformazioni(sprite, flip_h, flip_v, rotation)
        #copia lo sprite64x64 di numeri (0-15)
        self._copia_buffer(sprite, dest_x, dest_y, trasparenza=transparent_index)

    """ 
    GLI INDICI PER TILE /SPRITE VENGONO USATI SOLO PER MAPPARE/ESTRARRE CORRETTAMENTE 
    IL TILE/SPRITE dal tile/sprite sheet --> al frame buffer
    l'ordinamento viene fornito dal file scene.json che contiene una matrice 15x20 di INDICI (0-15)
    """

    """
    estrae tile dalla matrice del tile sheet
    input: tile id(0-63)
    output: numpy array di forma 32x32 pixel con indici di palette del tile
    """
    def _estrai_tile(self, tile_id):
        #divisione intera (ID // 8)
        riga_griglia    = tile_id // self.TILE_COLS #ritorna riga di appartenenza(righe complete)
        #quanto avanza nella riga di appartenenza
        colonna_griglia = tile_id - (riga_griglia * self.TILE_COLS) #colonna di appartenenza
        
        #trasformo righe/colonne perchè sto lavorando in una matrice 256x256 (moltiplico x 32pixel)
        r_inizio = riga_griglia    * self.TILE_SIZE
        c_inizio = colonna_griglia * self.TILE_SIZE
        
        #slicing per accedere correttamente al tile della matrice self.tiles di vram
        return self.vram.tiles[r_inizio : r_inizio + self.TILE_SIZE, c_inizio : c_inizio + self.TILE_SIZE]


    """
    estrae uno sprite dalla matrice dello sprite sheet
    input: sprite_id (0-15)
    output: numpy array di forma 64x64 con gli indici di palette dello sprite
    """
    def _estrai_sprite(self, sprite_id):

        #divisione intera (ID // 4)
        riga_griglia    = sprite_id // self.SPRITE_COLS
        colonna_griglia = sprite_id - (riga_griglia * self.SPRITE_COLS)

        #trasformo righe/colonne perchè sto lavorando in una matrice 256x256 (moltiplico x 32pixel)
        r_inizio = riga_griglia    * self.SPRITE_SIZE
        c_inizio = colonna_griglia * self.SPRITE_SIZE

        return self.vram.sprites[r_inizio : r_inizio + self.SPRITE_SIZE, c_inizio : c_inizio + self.SPRITE_SIZE]


    """
    applica flip e rotazione a uno sprite(array di forma 64x64 pixel)
    input: numpy array di pixel da trasformare usando dettagli da scene_parser
    output: sprite / numpy array trasformato
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
    copia una immagine nel frame buffer gestendo trasparenza e clipping.
    input: matrice di pixel da copiare, colonna e riga di destinazione, trasparenza 
    output: no, modifica self.frame_buffer 
    """
    ###NON CAPISCOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO
    def _copia_buffer(self, immagine, dest_x, dest_y, trasparenza):
        
        altezza_img   = immagine.shape[0]
        larghezza_img = immagine.shape[1]

        # calcola i limiti tenendo conto dei bordi dello schermo
        src_c_inizio = max(0, -dest_x)
        dst_c_inizio = max(0,  dest_x)
        src_c_fine   = min(larghezza_img, self.FB_WIDTH  - dest_x)
        dst_c_fine   = min(self.FB_WIDTH,  dest_x + larghezza_img)

        src_r_inizio = max(0, -dest_y)
        dst_r_inizio = max(0,  dest_y)
        src_r_fine   = min(altezza_img, self.FB_HEIGHT - dest_y)
        dst_r_fine   = min(self.FB_HEIGHT, dest_y + altezza_img)

        # se l'immagine e' completamente fuori dallo schermo, non fare nulla
        if src_c_inizio >= src_c_fine or src_r_inizio >= src_r_fine:
            return

        porzione_src = immagine[src_r_inizio:src_r_fine, src_c_inizio:src_c_fine]
        porzione_dst = self.frame_buffer[dst_r_inizio:dst_r_fine, dst_c_inizio:dst_c_fine]
        
        #per i tile
        if trasparenza is None:
            porzione_dst[:] = porzione_src
        #per sprite
        else:
            maschera = porzione_src != trasparenza
            porzione_dst[maschera] = porzione_src[maschera]
