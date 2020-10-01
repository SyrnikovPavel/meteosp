import network


def connect_network():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect('WiFi-HOME', 'Nastya26042015')
        while not sta_if.isconnected():
            pass
    return True
