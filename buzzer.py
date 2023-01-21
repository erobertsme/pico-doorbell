import machine
import time

class Buzzer:
  def __init__(self, pin, freq, volume):
    self.buzzer = machine.PWM(machine.Pin(pin))
    self.buzzer.freq(freq)
    self.volume = volume

  def beep(self, n):
    self.buzzer.duty_u16(self.volume)
    time.sleep(n)
    self.mute()

  def mute(self):
    self.buzzer.duty_u16(0)
