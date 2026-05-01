#local interpreter
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

class OLEDDisplay:
    def __init__(self, width=128, height=32, max_lines=3):
        i2c = board.I2C()
        self.oled = adafruit_ssd1306.SSD1306_I2C(width, height, i2c)

        self.oled.fill(0)
        self.oled.show()

        self.image = Image.new("1", (self.oled.width, self.oled.height))
        self.draw = ImageDraw.Draw(self.image)
        self.font = ImageFont.load_default()
        
        self.lines_buffer=[]
        self.max_lines = max_lines
        
    def add_line(self, line):
        line = line.strip()
        if not line:
            return
        
        self.lines_buffer.append(line)
        if len(self.lines_buffer)>self.max_lines:
            self.lines_buffer.pop(0)
            
        self.render()
        
    def render(self):
        self.draw.rectangle((0,0, self.oled.width, self.oled.height), outline=0, fill=0)
    
        y=0
        for l in self.lines_buffer:
            self.draw.text((0,y), l, font=self.font,fill=255)
            y += 10

        self.oled.image(self.image)
        self.oled.show()

    def clear(self):
        self.oled.fill(0)
        self.oled.show()


