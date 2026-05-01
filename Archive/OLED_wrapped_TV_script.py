#local interpreter
import subprocess
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
import signal

i2c = board.I2C()
oled = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)

oled.fill(0)
oled.show()

image = Image.new("1", (oled.width, oled.height))
draw = ImageDraw.Draw(image)

font=ImageFont.load_default()

process = subprocess.Popen(
    ["python3", "/home/merieloc/Documents/projects/Combined_TV_Scripts/combined_tv_controller.py"],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
    bufsize=1
)

lines_buffer=[]
MAX_LINES=3

for line in process.stdout:
    line = line.strip()
    if not line:
        continue
    print(line)
    
    lines_buffer.append(line)
    if len(lines_buffer)>MAX_LINES:
        lines_buffer.pop(0)
        
    draw.rectangle((0,0, oled.width, oled.height), outline=0, fill=0)
    
    y=0
    for l in lines_buffer:
        draw.text((0,y), l, font=font,fill=255)
        y += 10

    oled.image(image)
    oled.show()

def handle_sigint(sigma, frame):
    print('Stopping child...')
    process.terminate()
    process.wait(timeout=5)
    sys.exit(0)
    
signal.signal(signal.SIGINT, handle_sigint)

