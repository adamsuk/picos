## picoGames

This repo contains the resources and code needed to play games on the [Raspberry Pi Pico](https://www.raspberrypi.org/products/raspberry-pi-pico/) with the [Pico Unicorn](https://shop.pimoroni.com/products/pico-unicorn-pack?variant=32369501306963&currency=GBP&utm_source=google&utm_medium=cpc&utm_campaign=google+shopping&gclid=Cj0KCQjw--GFBhDeARIsACH_kdYmVDDEvoPM0kjAxO8ePYvCVOlKwaxowtD1fmzEWObHQV6HNIgCadYaAs9sEALw_wcB) accessory.

These games are written in Python and have been developed for MicroPython with the picounicorn package.

### Getting Started

Assuming you have all the hardware setup (Pico, header pins and Unicorn display) you need to do the following as prerequisites to getting any Pico Unicorn code to run:
- If you haven't used the Pico before download either [Thonny](https://thonny.org/) or VSCode with the [Pico extension](https://marketplace.visualstudio.com/items?itemName=ChrisWood.pico-go).
- If already loaded with a UF2 then the Pico needs resetting with the [flash nuke](boot/flash_nuke.uf2).
- Load the Pico Unicorn version of [MicroPython](boot/pimoroni-pico-v0.2.0-micropython-v1.15.uf2) updates can be found [here](https://github.com/pimoroni/pimoroni-pico/tags). This allows you to use the picounicorn package on the Pico.

I personally use Thonny on a Raspberry Pi 4 because it completely simplifies the setup so all I have to worry about is code.

### Running Code!

The Pico works in a really simplistic way. Anything uploaded to the root called `main.py` will be ran automatically.