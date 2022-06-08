# PicOS

This repo contains the resources and code needed to play games on the [Raspberry Pi Pico](https://www.raspberrypi.org/products/raspberry-pi-pico/) with the [Pico Unicorn](https://shop.pimoroni.com/products/pico-unicorn-pack?variant=32369501306963&currency=GBP&utm_source=google&utm_medium=cpc&utm_campaign=google+shopping&gclid=Cj0KCQjw--GFBhDeARIsACH_kdYmVDDEvoPM0kjAxO8ePYvCVOlKwaxowtD1fmzEWObHQV6HNIgCadYaAs9sEALw_wcB) accessory.

These games are written in Python and have been developed for MicroPython with the picounicorn package.

## GAMES!

Pong - a nice little competitive game between friends

Snake - a decent distraction when trying to think through problems!

https://user-images.githubusercontent.com/25231418/120858925-67ea7500-c57b-11eb-80c5-475175914e09.mp4

## Getting Started

Assuming you have all the hardware setup (Pico, header pins and Unicorn display) you need to do the following as prerequisites to getting any Pico Unicorn code to run:
- If you haven't used the Pico before download either [Thonny](https://thonny.org/) or VSCode with the [Pico extension](https://marketplace.visualstudio.com/items?itemName=ChrisWood.pico-go).
- If already loaded with a UF2 then the Pico needs resetting with the [flash nuke](boot/flash_nuke.uf2).
- Load the Pico Unicorn version of [MicroPython](boot/pimoroni-pico-v1.18.7-micropython.uf2) updates can be found [here](https://github.com/pimoroni/pimoroni-pico/tags). This allows you to use the picounicorn package on the Pico.

I personally use Thonny on a Raspberry Pi 4 because it completely simplifies the setup so all I have to worry about is code.

## Running Code on your Pico!

The Pico works in a really simplistic way. Anything uploaded to the root called `main.py` will be ran automatically.

This is the start of an extremely simplified OS for the Pico so for the time being it'll give you a list of importable games from the games subdirectory. To run this as a whole copy all `.py` files across to your Pico and both `pong.py` and `snake.py` will be options available to you. To exit out of these games press A + X together.

## TODO:

- PicoGame abstraction - both pong and snake contain code that can be abstracted out, ideal for an Abstract Base Class!
- Text scrolling - I bashed this together using existing code for displaying the game scores but it would be best if it scrolled the other way for the menu.
- Customisation  - I'd LOVE to build in options so game booleans (like walls in snake or infinite looping paddles in pong) can be toggled on/off. Also custom colours. Store these in a JSON on the Pico and they'll persist too!
- More games and other things!! Like a tiny calculator or game high scores ... the possibilities are endless.

## Thanks

Firstly I need to give a shout out to pippayy and her [PONG.py](https://github.com/pippayyy/PONG) code. Without stumbling on her [LinkedIn video](https://www.linkedin.com/posts/pip-austin-222615173_raspberrypi-python-ugcPost-6797972161341530112-oWUq/?src=aff-lilpar&veh=aff_src.aff-lilpar_c.partners_pkw.10078_plc.Skimbit%20Ltd._pcrid.449670_learning&trk=aff_src.aff-lilpar_c.partners_pkw.10078_plc.Skimbit%20Ltd._pcrid.449670_learning&clickid=QtjQA5QlNxyLTxPwUx0Mo3EoUkBw2kyph37dRs0&irgwc=1) I wouldn't have started this project and the Picos I preordered would've gathered dust for a little while longer. I used her project as a starter for 10, did a little refactoring, fixed a couple of bugs then got to work on my own take on a classic :)
