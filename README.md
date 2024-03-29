# hx711 weighing scales

Still in prototype phase. Most up-to-date script is `prototyping/main.py` in which the Pico reads in data (by pulsing the clock pin) across through GIO from the HX711. Each data point is then displayed on the LCD screen, which uses some basic precomputed callibration values. Next steps are to improve the hardware layout a little and create tare functionality.

<img src="images/demo_screen_070823.jpg" width="280">

Drivers for HX711 24-bit Analog-to-Digital Converter for Load Cell weighing scales.

Goal is to built an accurate miniture scale with a display & wifi connection.

Datasheet: https://cdn.sparkfun.com/datasheets/Sensors/ForceFlex/hx711_english.pdf

Components:

- Pi Pico Microprocessor
- HX711 ADC
- Waveshare Pico-LCD [1.14](https://www.amazon.com/dp/B095PF7CQK?ref=ppx_yo2ov_dt_b_product_details&th=1) (Need to daisy-chain ground with HX711)

Later:
- Waveshare Pico-ESP8266 (WiFi)
