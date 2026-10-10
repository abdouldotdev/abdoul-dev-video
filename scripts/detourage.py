"""Épaissit le détourage des poses : retire le fin liseré d'origine, pose une bande blanche épaisse + un trait encre."""
import sys, numpy as np
from PIL import Image
from scipy import ndimage
src, dst = sys.argv[1], sys.argv[2]
WHITE, INK, TRIM, PAD = 16, 5, 4, 24   # px pour une pose de ~900 px
im = Image.open(src).convert("RGBA")
src_a = np.array(im)
cut = src_a[-3:, :, 3].max() > 127                # la pose est coupée par le bas de l'image
bottom = 0 if cut else PAD
arr0 = np.pad(src_a, ((PAD, bottom), (PAD, PAD), (0, 0)))
im = Image.fromarray(arr0)
a = arr0[..., 3] > 127
if cut:  # prolonger le masque vers le bas pour ne pas détourer la coupe
    ext = np.vstack([a, np.repeat(a[-1:], PAD, 0)])
    a_calc = ext
else:
    a_calc = a
d_out = ndimage.distance_transform_edt(~a_calc)[:a.shape[0]]   # distance à l'extérieur
d_in = ndimage.distance_transform_edt(a_calc)[:a.shape[0]]     # distance à l'intérieur
core = d_in > TRIM                               # contenu sans l'ancien liseré
white = d_out <= WHITE                           # tout ce qui est à moins de WHITE px
ink = (d_out > WHITE) & (d_out <= WHITE + INK)
out = np.zeros((*a.shape, 4), np.uint8)
out[white] = (255, 255, 255, 255)
out[ink] = (18, 18, 18, 255)
arr = np.array(im)
out[core] = arr[core]
# anti-crénelage léger du bord extérieur
edge = (d_out > WHITE + INK) & (d_out <= WHITE + INK + 1.5)
out[edge] = (18, 18, 18, 110)
res = Image.fromarray(out)
bbox = res.getbbox(); res = res.crop(bbox)
print('coupée en bas' if cut else 'entière', end=' ')
res.save(dst, "WEBP", quality=88, method=6)
print(dst, res.size)
