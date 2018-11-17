#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PIL import Image
from PIL import ImageDraw
from pygments.formatters.img import ImageFormatter


class Formatter(ImageFormatter):

    def format(self, tokensource, outfile):
        """
        Format ``tokensource``, an iterable of ``(tokentype, tokenstring)``
        tuples and write it into ``outfile``.

        This implementation calculates where it should draw each token on the
        pixmap, then calculates the required pixmap size and draws the items.
        """
        self._create_drawables(tokensource)
        self.maxcharno = 120
        self.maxlineno = 47
        self._draw_line_numbers()
        im = Image.new(
            'RGB',
            self._get_image_size(self.maxcharno, self.maxlineno),
            self.background_color
        )
        self._paint_line_number_bg(im)
        draw = ImageDraw.Draw(im)
        # Highlight
        if self.hl_lines:
            x = self.image_pad + self.line_number_width - self.line_number_pad + 1
            recth = self._get_line_height()
            rectw = im.size[0] - x
            for linenumber in self.hl_lines:
                y = self._get_line_y(linenumber - 1)
                draw.rectangle([(x, y), (x + rectw, y + recth)],
                               fill=self.hl_color)
        for pos, value, font, kw in self.drawables:
            draw.text(pos, value, font=font, **kw)

        self.image = im
