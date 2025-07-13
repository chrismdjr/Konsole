import rgbmatrix
from PIL import Image, ImageDraw, ImageFont, ImageEnhance

class Renderer:
    def __init__(self, rows, cols):
        options = rgbmatrix.RGBMatrixOptions()
        options.rows = rows
        options.cols = cols
        options.drop_privileges = False
        options.hardware_mapping = "adafruit-hat"

        self.brightness_multiplier = 0.25

        self._rows = rows
        self._cols = cols
        self._matrix = rgbmatrix.RGBMatrix(options=options)
        self._frame = None
        self._frame_draw = None
        self.clear() # inits self._frame and self._frame_draw

    def present(self):
        self._frame = self._frame.transpose(Image.FLIP_LEFT_RIGHT)
        self._frame = self._frame.transpose(Image.FLIP_TOP_BOTTOM)
        self._matrix.SetImage(self._frame)

    def clear(self, clear_matrix=False):
        if clear_matrix == True:
            self._matrix.Clear()
            
        self._frame = Image.new("RGB", (self._rows, self._cols))
        self._frame_draw = ImageDraw.Draw(self._frame)

    def draw_rect(self, x, y, width, height, color):
        self._frame_draw.rectangle((x, y, x + width, y + height), fill=self._process_color(color))

    def draw_ellipse(self, x, y, width, height, color):
        self._frame_draw.ellipse((x, y, x + width, y + height), fill=self._process_color(color))

    def draw_text(self, x, y, text, color):
        font = ImageFont.truetype("tiny.ttf", 6)
        self._frame_draw.text(
            (x, y),
            text,
            fill=self._process_color(color),
            font=font,
            spacing=0
        )

    def draw_polygon(self, points, color):
        self._frame_draw.polygon(points, fill=self._process_color(color))

    def draw_image(self, x, y, image):
        image_enhancer = ImageEnhance.Brightness(image)
        image = image_enhancer.enhance(self.brightness_multiplier)
        self._frame.paste(image, (x, y))

    def _process_color(self, color):
        return (
            int(color[0] * self.brightness_multiplier),
            int(color[1] * self.brightness_multiplier),
            int(color[2] * self.brightness_multiplier)
        )