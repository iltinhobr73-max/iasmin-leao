"""Prepara as fotos do site da Iasmim Leão. Saída na raiz, em WebP + JPG.
Casos: só recortes fechados de sorriso e lábios, sem rosto identificável."""
import sys, glob
from PIL import Image, ImageFilter
SRC, OUT = sys.argv[1], sys.argv[2]
def src(n): return Image.open(glob.glob(f"{SRC}/{n}.*")[0]).convert("RGB")
def save(im, name, size):
    im = im.resize(size, Image.LANCZOS).filter(ImageFilter.UnsharpMask(radius=1.2, percent=30, threshold=2))
    im.save(f"{OUT}/{name}.webp", "WEBP", quality=86, method=6); im.save(f"{OUT}/{name}.jpg", "JPEG", quality=88, optimize=True, progressive=True)
# retratos (foto no consultório)
p = src(44)
save(p.crop((78, 96, 366, 480)), "il-retrato", (576, 768))        # 3:4, hero
save(p.crop((0, 4, 432, 544)), "il-consultorio", (432, 540))       # 4:5, sobre
# casos de sorriso: cada metade em 2:1 (empilhadas formam um quadrado)
c = src(46); save(c.crop((0, 0, 618, 309)), "caso1-antes", (600, 300)); save(c.crop((0, 314, 608, 618)), "caso1-depois", (600, 300))
c = src(48); save(c.crop((0, 322, 352, 498)), "caso2-antes", (600, 300)); save(c.crop((44, 0, 352, 154)), "caso2-depois", (600, 300))
# caso lado a lado: cada metade em 1:2
c = src(49); save(c.crop((0, 80, 175, 430)), "caso3-antes", (300, 600)); save(c.crop((175, 80, 350, 430)), "caso3-depois", (300, 600))
# lábios: só a metade de baixo da montagem (sem o rosto), cada lado em 4:5
c = src(45); save(c.crop((0, 310, 246, 618)), "labios-antes", (400, 500)); save(c.crop((250, 310, 496, 618)), "labios-depois", (400, 500))
# capa para compartilhamento
capa = Image.new("RGB", (1200, 630), (22, 17, 16)); r = p.crop((40, 60, 440, 480)).resize((600, 630), Image.LANCZOS); capa.paste(r, (600, 0)); capa.save(f"{OUT}/il-capa.jpg", "JPEG", quality=86)
# miniatura quadrada para a prévia do link no WhatsApp e redes (foto dela, enquadrada no rosto e no tronco)
q = p.crop((70, 92, 370, 392)).resize((600, 600), Image.LANCZOS).filter(ImageFilter.UnsharpMask(radius=1.2, percent=30, threshold=2))
q.save(f"{OUT}/il-link.jpg", "JPEG", quality=88, optimize=True)
print("ok")
