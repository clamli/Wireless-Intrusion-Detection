## \# Wireless Intrusion Detection

- [Presentation](https://drive.google.com/open?id=1hKKZ6D4MEjD4X8Rq7K0lVZ0X7AJSj_fk)
- [Report](https://drive.google.com/open?id=1yoKY1VRToHlowS8Q9HHzT8jNtaOv4Fo4)
- [Video](https://drive.google.com/open?id=1Ojg1BVjl9dJArBXsy6_SuLDwXcMqTXlM)

### \# Device

 - MATRIX Labs MATRIX Creator
- Raspberry Pi 3 Model B
### \# Pre-Installation

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
### \# Commands

- Raspberry end

  ```
  cmake --build . && ./bin/Mic       // run in /cpp/build, data record and transmission
  ```

- PC end

  ```
  python display.py                  // data analysis and display
  ```

## \# References

 - [Direction of Arrival for MATRIX Voice/Creator Using ODAS](https://www.hackster.io/matrix-labs/direction-of-arrival-for-matrix-voice-creator-using-odas-b7a15b)
- [Use Pyaudio Package to Record Acoustic Data](https://github.com/matrix-io/matrixio-kernel-modules/blob/master/misc/pyaudio_test.py)
- [Microphone Array on MATRIX Creator](https://matrix-io.github.io/matrix-documentation/matrix-creator/resources/microphone/#usage)
- [Plot Microphone Signal(s) in Real-Time](https://python-sounddevice.readthedocs.io/en/0.3.12/examples.html#plot-microphone-signal-s-in-real-time)
- [FRI-based DOA Estimation for Arbitrary Array Layout](https://github.com/LCAV/FRIDA)
