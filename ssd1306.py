# MicroPython SSD1306 OLED driver, I2C and SPI interfaces

from micropython import const
import framebuf
import time

# Registro de comandos SSD1306
SET_CONTRAST = const(0x81)
ENTIRE_DISPLAY_ON = const(0xA4)
NORMAL_DISPLAY = const(0xA6)
DISPLAY_OFF = const(0xAE)
DISPLAY_ON = const(0xAF)
SET_DISPLAY_OFFSET = const(0xD3)
SET_COMPINS = const(0xDA)
SET_VCOM_DETECT = const(0xDB)
SET_DISPLAY_CLOCK_DIV = const(0xD5)
SET_PRECHARGE = const(0xD9)
SET_MULTIPLEX = const(0xA8)
SET_LOW_COLUMN = const(0x00)
SET_HIGH_COLUMN = const(0x10)
SET_START_LINE = const(0x40)
MEMORY_MODE = const(0x20)
COLUMN_ADDR = const(0x21)
PAGE_ADDR = const(0x22)
COM_SCAN_INC = const(0xC0)
COM_SCAN_DEC = const(0xC8)
SEG_REMAP = const(0xA0)
CHARGE_PUMP = const(0x8D)
EXTERNAL_VCC = False
SWITCH_CAP_VCC = True


class SSD1306:
    def __init__(self, width, height, external_vcc):
        self.width = width
        self.height = height
        self.external_vcc = external_vcc
        self.pages = self.height // 8
        self.buffer = bytearray(self.width * self.pages)
        self.framebuf = framebuf.FrameBuffer(self.buffer, self.width, self.height, framebuf.MONO_VLSB)
        self.poweron()
        self.init_display()

    def init_display(self):
        for cmd in (
            DISPLAY_OFF,
            SET_DISPLAY_CLOCK_DIV, 0x80,
            SET_MULTIPLEX, self.height - 1,
            SET_DISPLAY_OFFSET, 0x00,
            SET_START_LINE | 0x00,
            CHARGE_PUMP, 0x14 if not self.external_vcc else 0x10,
            MEMORY_MODE, 0x00,
            SEG_REMAP | 0x01,
            COM_SCAN_DEC,
            SET_COMPINS, 0x12 if self.height == 64 else 0x02,
            SET_CONTRAST, 0xCF,
            SET_PRECHARGE, 0xF1 if not self.external_vcc else 0x22,
            SET_VCOM_DETECT, 0x40,
            DISPLAY_ON,
            NORMAL_DISPLAY,
        ):
            self.write_cmd(cmd)
        self.fill(0)
        self.show()

    def poweroff(self):
        self.write_cmd(DISPLAY_OFF)

    def poweron(self):
        self.write_cmd(DISPLAY_ON)

    def contrast(self, contrast):
        self.write_cmd(SET_CONTRAST)
        self.write_cmd(contrast)

    def invert(self, invert):
        self.write_cmd(0xA7 if invert else 0xA6)

    def show(self):
        for page in range(self.pages):
            self.write_cmd(0xB0 | page)
            self.write_cmd(SET_LOW_COLUMN | 0x00)
            self.write_cmd(SET_HIGH_COLUMN | 0x10)
            start = self.width * page
            end = start + self.width
            self.write_data(self.buffer[start:end])

    def fill(self, color):
        self.framebuf.fill(color)

    def pixel(self, x, y, color):
        self.framebuf.pixel(x, y, color)

    def scroll(self, dx, dy):
        self.framebuf.scroll(dx, dy)

    def text(self, string, x, y, color=1):
        self.framebuf.text(string, x, y, color)

    def hline(self, x, y, w, color):
        self.framebuf.hline(x, y, w, color)

    def vline(self, x, y, h, color):
        self.framebuf.vline(x, y, h, color)

    def rect(self, x, y, w, h, color):
        self.framebuf.rect(x, y, w, h, color)

    def fill_rect(self, x, y, w, h, color):
        self.framebuf.fill_rect(x, y, w, h, color)


class SSD1306_I2C(SSD1306):
    def __init__(self, width, height, i2c, addr=0x3C, external_vcc=False):
        self.i2c = i2c
        self.addr = addr
        self.temp = bytearray(2)
        super().__init__(width, height, external_vcc)

    def write_cmd(self, cmd):
        self.temp[0] = 0x80  # Co=1, D/C#=0
        self.temp[1] = cmd
        self.i2c.writeto(self.addr, self.temp)

    def write_data(self, buf):
        self.i2c.writeto(self.addr, b'\x40' + buf)