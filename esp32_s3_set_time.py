import network
import time
import ntptime


SSID = 'WIFI_NAME'
PASSWORD = 'WIFI_PASSWD'

def connect_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('Connecting to network...')
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            time.sleep(1)
    print('Network connected:', wlan.ifconfig())

def get_network_time():
    try:
        print('Getting network time...')
        ntptime.host = "time.windows.com"
        ntptime.settime()
        tm = time.localtime(time.time() + 8 * 3600) # 时差补偿
        current_time = "{:04}-{:02}-{:02} {:02}:{:02}:{:02}".format(tm[0], tm[1], tm[2], tm[3], tm[4], tm[5])
        print('Current network time:', current_time)
    except Exception as e:
        print('Failed to get network time:', e)


connect_wifi(SSID, PASSWORD)
get_network_time()

while True:
    time.sleep(1)
    tm = time.localtime(time.time() + 8 * 3600) # 时差补偿
    current_time = "{:04}-{:02}-{:02} {:02}:{:02}:{:02}".format(tm[0], tm[1], tm[2], tm[3], tm[4], tm[5])
    print('Current network time:', current_time)
