# TVBOX_DISPLAY_I2C_SPI
LED 7 segment i2c spi in userspace installed rk3318 X88 Pro 10 and Bqeel S1, CPU Amlogic S905X4 

# Display LED Control with TM1650 and TM1628 or clone HT1650 AiP1628 

This repository contains code for controlling LED displays using the TM1650 chip on the I2C bus and the TM1628 chip on the SPI bus. Before using these displays, it is necessary to enable the I2C bus with Armbian-Configure. Additionally, you need to determine the GPIO pins used for the SPI bus by running the command `cat /sys/kernel/debug/gpio` on your Android device. In this specific case, the GPIO pins were enabled as follows:

```bash
echo 82 > /sys/class/gpio/export
echo 83 > /sys/class/gpio/export
echo 86 > /sys/class/gpio/export

echo out > /sys/class/gpio/gpio82/direction
echo out > /sys/class/gpio/gpio83/direction
echo out > /sys/class/gpio/gpio86/direction
```

## Overview

The TM1650 and TM1628 are integrated circuits designed to drive 7-segment LED displays. They communicate with the microcontroller using the I2C and SPI protocols, respectively. This repository provides code examples and libraries to control these displays.

## Prerequisites

To use the code in this repository, you'll need the following:

- Raspberry Pi or similar single-board computer
- Armbian OS installed on the board
- Python 3 installed
- I2C and SPI buses enabled on the board

## Getting Started

Follow these steps to get started with controlling TM1650 and TM1628 displays:

1. Connect the TM1650 or TM1628 display to the appropriate GPIO pins on your board.

2. Enable the I2C bus on your board using Armbian-Configure. This will allow communication with the TM1650 display.

3. Determine the GPIO pins used for the SPI bus on your board by running the command `cat /sys/kernel/debug/gpio` on your Android device.

4. install i2c-tools sudo apt install i2c-tools. scan i2c-bus,  sudo i2cdetect -y x 0..?

5. Enable the necessary GPIO pins for the SPI bus using the provided commands. This will allow communication with the TM1628 display.

## Contributing

Contributions to this repository are welcome. If you have any improvements or bug fixes, feel free to submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgements

- [TM1650 datasheet](http://www.datasheetcafe.com/tm1650-datasheet-led-controller/)
- [TM1628 datasheet](https://datasheetspdf.com/datasheet/TM1628.html)

## Contact

For any questions or inquiries, please contact [your-email@example.com](mailto:your-email@example.com).
