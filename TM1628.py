import time
import threading


class TM1628Display:
    def __init__(self, spi_cs_gpio, spi_clk_gpio, spi_data_gpio):
        self.spi_cs_gpio = spi_cs_gpio
        self.spi_clk_gpio = spi_clk_gpio
        self.spi_data_gpio = spi_data_gpio
        self.led_info = 0

    def set_reset_bit(self, value, position, set_bit):
        mask = 1 << position

        if set_bit:
            new_value = value | mask
        else:
            new_value = value & ~mask

        self.led_info = new_value
        return new_value

    def set_gpio_value(self, gpio_path, value):
        with open(gpio_path, 'w') as f:
            f.write(str(value))

    def spi_send_bit(self, bit):
        self.set_gpio_value(self.spi_clk_gpio, 0)
        self.set_gpio_value(self.spi_data_gpio, bit)
        self.set_gpio_value(self.spi_clk_gpio, 1)

    def spi_send_byte(self, byte):
        for _ in range(8):
            self.spi_send_bit(byte & 0x01)
            byte >>= 1

    def tm1628_send_command(self, cmd):
        self.set_gpio_value(self.spi_cs_gpio, 0)
        self.spi_send_byte(cmd)
        self.set_gpio_value(self.spi_cs_gpio, 1)

    def tm1628_init(self):
        self.tm1628_send_command(0x8a)
        self.tm1628_display_clear()
        self.tm1628_set_led_power(1)

    def tm1628_display_digit(self, digit, value):
        self.tm1628_send_command(0x44)

        self.set_gpio_value(self.spi_cs_gpio, 0)
        self.spi_send_byte(0xc0 | digit)
        self.spi_send_byte(value)
        self.set_gpio_value(self.spi_cs_gpio, 1)

    def tm1628_display_clear(self):
        for i in range(16):
            self.tm1628_display_digit(i, 0)

    def tm1628_set_led_dot(self, a_state):
        self.set_reset_bit(self.led_info, LED_DOT, a_state)
        self.tm1628_display_digit(LCD_POS[4], self.led_info)

    def tm1628_set_led_power(self, a_state):
        self.set_reset_bit(self.led_info, LED_POWER, a_state)
        self.tm1628_display_digit(LCD_POS[4], self.led_info)

    def tm1628_set_led_wifi(self, a_state):
        self.set_reset_bit(self.led_info, LED_WIFI_LOW, a_state)
        self.set_reset_bit(self.led_info, LED_WIFI_HI, a_state)
        self.tm1628_display_digit(LCD_POS[4], self.led_info)

    def tm1628_set_led_lan(self, a_state):
        self.set_reset_bit(self.led_info, LED_LAN, a_state)
        self.tm1628_display_digit(LCD_POS[4], self.led_info)

    def tm1628_set_time(self):
        hour_now = time.strftime("%H:%M")
        hour = int(hour_now[:2])
        minutes = int(hour_now[3:5])

        hour_0 = hour // 10
        hour_1 = hour % 10
        minutes_0 = minutes // 10
        minutes_1 = minutes % 10

        self.tm1628_display_digit(LCD_POS[0], array_cifre[hour_0])
        self.tm1628_display_digit(LCD_POS[1], array_cifre[hour_1])
        self.tm1628_display_digit(LCD_POS[2], array_cifre[minutes_0])
        self.tm1628_display_digit(LCD_POS[3], array_cifre[minutes_1])
        self.tm1628_display_digit(LCD_POS[4], self.led_info)
        self.tm1628_set_led_dot(1)
        time.sleep(1)
        self.tm1628_set_led_dot(0)
        time.sleep(1)



def write_to_displays(display):
    while True:
        display.tm1628_set_time()
        time.sleep(1)



if __name__ == '__main__':
    SPI_CS_GPIO = '/sys/class/gpio/gpio82/value'
    SPI_CLK_GPIO = '/sys/class/gpio/gpio83/value'
    SPI_DATA_GPIO = '/sys/class/gpio/gpio86/value'

    array_cifre = [
        191,        # 0
        6,          # 1
        91,         # 2
        79,         # 3
        102,        # 4
        109,        # 5
        1,          # 6
        7,          # 7
        127,        # 8
        111         # 9
    ]

    LCD_POS = [
        0,
        2,
        4,
        6,
        8
    ]

    LED_POWER = 2
    LED_LAN = 3
    LED_DOT = 4
    LED_WIFI_HI = 5
    LED_WIFI_LOW = 6

    tm1628_displays = []
    for _ in range(5):
        display = TM1628Display(SPI_CS_GPIO, SPI_CLK_GPIO, SPI_DATA_GPIO)
        display.tm1628_init()
        display.tm1628_set_led_power(1)
        display.tm1628_set_led_wifi(1)
        display.tm1628_set_led_lan(1)
        tm1628_displays.append(display)

    update_thread = threading.Thread(target=write_to_displays, args=(tm1628_displays[0],))
    update_thread.start()
