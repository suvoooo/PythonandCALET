#!/usr/bin/python
# program to put image in a horizontal section 
import sys
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
images = map(Image.open, ['Breenu.eps','Brmumunu.eps','Brtautaunu.eps'])
widths, heights = zip(*(i.size for i in images))

total_width = sum(widths)
max_height = max(heights)

new_im = Image.new('RGB', (total_width, max_height))
x_offset = 0
for im in images:
  new_im.paste(im, (x_offset,0))
  x_offset += im.size[0]
#fig.patch.set_facecolor('white')
new_im.save('Branching1d1TDMs1d0Ed10T.eps')#,bbox_inches='tight')

