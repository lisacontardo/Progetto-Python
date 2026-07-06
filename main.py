# LISA CONTARDO SM3201635

import sys
from exceptions import RenderError
from palette import Palette
from vram import VirtualVRAM
from scene_parser import SceneParser
from pipeline import RenderingPipeline
NUM_ARGS = 5

"""
valida e interpreta gli argomenti da riga di comando
input: argv (list[str]): argomenti passati al programma senza il nome script
output: tupla (palette_path, scene_path, tiles_path, sprites_path, output_path).
"""
def func_args(argv):
    
    if len(argv) != NUM_ARGS:
        raise RenderError(
            "Utilizzo: python main.py <palette.json> <scene.json> "
            "<tiles.bin> <sprites.bin> <output.png>"
        )
    return tuple(argv)

#esegue il programma: legge gli argomenti e avvia il funzione per il rendering
def main():
    try:
        palette_path, scene_path, tiles_path, sprites_path, output_path = func_args(sys.argv[1:])
        
        #istanzio oggetti delle classi
        palette = Palette(palette_path)
        vram    = VirtualVRAM(tiles_path, sprites_path)
        scena   = SceneParser(scene_path)
        
        pipeline = RenderingPipeline(palette, vram, scena)
        #invoca metodo speciale che genera immagine png
        pipeline.esegui(output_path)

        print(f"Immagine salvata in '{output_path}'.")

    except RenderError as e:
        print(f"Errore: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()