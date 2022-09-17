import PIL.ImageGrab
imagem = PIL.ImageGrab.grab(bbox=None, include_layered_windows=False, all_screens=False, xdisplay=None)
imagem.save("screenshot.png")
