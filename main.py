# LISA CONTARDO SM3201635
import sys
from exceptions import RenderError
from palette import Palette
from vram import VirtualVRAM
from scene_parser import SceneParser
from pipeline import RenderingPipeline

NUM_ARGS = 6

#esegue il programma: legge gli argomenti e avvia il funzione per il rendering
def main():
    try:
        if len(sys.argv) != 6:
            print("Devono essere presenti 6 argomenti: python main.py <palette.json> <scene.json> "
                "<tiles.bin> <sprites.bin> <output.png>" 
            )
            sys.exit(1)  

        palette_path  = sys.argv[1]
        scene_path    = sys.argv[2]
        tiles_path    = sys.argv[3]
        sprites_path  = sys.argv[4]
        output_path   = sys.argv[5]

        #istanzio oggetti delle classi
        palette = Palette(palette_path)
        vram    = VirtualVRAM(tiles_path, sprites_path)
        scena   = SceneParser(scene_path)
    
        #input sono validi e posso costruire pipeline
        pipeline = RenderingPipeline(palette, vram, scena)
        #invoca metodo speciale che genera immagine png
        pipeline.esegui(output_path)

        print(f"Immagine salvata in '{output_path}'.")

    except RenderError as e:
        print(f"Errore: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()