# LISA CONTARDO SM3201635
class RenderError(Exception):
    pass 

class PaletteError(RenderError):
    pass

class VRAMError(RenderError):
    pass

class SceneError(RenderError):
    pass

class BlitterError(RenderError):
    pass

