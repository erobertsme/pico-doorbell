import urequests as requests
import time
import machine
import network
import config
from buzzer import Buzzer

# Buzzer setup
buzzer_freq = 262 # middle C
buzzer_volume = 10000 # max volume?
buzzer_pin = 15
buzzer = Buzzer(buzzer_pin, buzzer_freq, buzzer_volume)

# Get the WiFi credentials from the environment variables
ssid = config.WIFI_SSID
password = config.WIFI_PASSWORD
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

max_wait = 3
while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    print('Waiting for connection...')
    max_wait -= 1
    time.sleep(1)

if wlan.status() != 3:
    raise RuntimeError('Network connection failed')
else:
    print('Connected to ' + ssid)
    status = wlan.ifconfig()
    print( 'IP: ' + status[0] )

# Get the Gotify URL and token from the environment variables
gotify_url = config.GOTIFY_URL
gotify_token = config.GOTIFY_TOKEN

# Define a function to send a notification to the Gotify server
def send_notification(title, message):
    payload = {
        "title": title,
        "message": message
    }
    headers = {
        "X-Gotify-Key": gotify_token,
        "content-type": 'application/json',
    }

    requests.post(gotify_url, json=payload, headers=headers)

button = machine.Pin(13, machine.Pin.IN, machine.Pin.PULL_UP)

# Main loop
while True:
    # Wait for the button to be pressed
    button_current_state = (not button.value())
    
    if button_current_state == True:
        # Ring the buzzer
        # buzzer.beep(0.2)
        # time.sleep(0.1)
        # buzzer.beep(0.25)
        # time.sleep(0.15)
        # buzzer.beep(0.2)
        # time.sleep(0.01)
        # buzzer.beep(0.3)
        # time.sleep(0.1)
        # buzzer.beep(0.3)
        # time.sleep(0.5)
        # buzzer.beep(0.3)
        # time.sleep(0.1)
        # buzzer.beep(0.3)
        buzzer.beep(0.5)
        
        timestamp = machine.RTC().datetime()

        print('Doorbell Pressed at '+ "%04d-%02d-%02d %02d:%02d:%02d"%(timestamp[0:3] + timestamp[4:7]) )
        
        # Send a notification
        send_notification('Doorbell', 'The doorbell has been pressed at ' + "%04d-%02d-%02d %02d:%02d:%02d"%(timestamp[0:3] + timestamp[4:7]) )
        time.sleep(0.1)