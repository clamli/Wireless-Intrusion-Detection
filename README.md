## \# Device
 - MATRIX Labs MATRIX Creator
- Raspberry Pi 3 Model B
## \# Pre-Installation
 - [balenaEtcher](https://www.balena.io/etcher/): Flash OS images to SD cards.

- [RASPBIAN STRETCH WITH DESKTOP](https://www.raspberrypi.org/downloads/raspbian/): Image with desktop based on Debian Stretch.

- [Driver installation for Microphone Array](https://matrix-io.github.io/matrix-documentation/matrix-creator/resources/microphone/#usage)

  ```
  > curl https://apt.matrix.one/doc/apt-key.gpg | sudo apt-key add -
  > echo "deb https://apt.matrix.one/raspbian $(lsb_release -sc) main" | sudo tee     /etc/apt/sources.list.d/matrixlabs.list
  > sudo apt-get update
  > sudo apt-get upgrade
  > sudo reboot
  > sudo apt install matrixio-kernel-modules
  > sudo reboot
  ```
## \# References
 - [Direction of Arrival for MATRIX Voice/Creator Using ODAS](https://www.hackster.io/matrix-labs/direction-of-arrival-for-matrix-voice-creator-using-odas-b7a15b)
- [Realtime Audio Visualization In Python](https://www.swharden.com/wp/2016-07-19-realtime-audio-visualization-in-python/)
- [Use Pyaudio Package to Record Acoustic Data](https://github.com/matrix-io/matrixio-kernel-modules/blob/master/misc/pyaudio_test.py)
- [Microphone Array on MATRIX Creator](https://matrix-io.github.io/matrix-documentation/matrix-creator/resources/microphone/#usage)
