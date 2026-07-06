# LISA CONTARDO SM3201635
class RenderError(Exception):
    pass 

class PaletteError(RenderError):
    pass

class VRAMError(RenderError):
    """Errore relativo al caricamento o alla decodifica dei file binari.

    Esempi:
    - file .bin non trovato;
    - file .bin con dimensione diversa da 32768 byte.
    """
    pass

class SceneError(RenderError):
    """Errore relativo al caricamento o alla validazione della scena.

    Esempi:
    - file scene.json non trovato;
    - tile_map con dimensioni errate;
    - sprite con rotation non valida (es. 45°).
    """
    pass

class BlitterError(RenderError):
    pass

