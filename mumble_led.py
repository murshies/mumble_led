#!/usr/bin/env python

import logging
import psutil
import sys
import time

from RPi import GPIO

logger = logging.getLogger(__name__)

def get_mumble_clients(port):
    return [sconn.raddr for sconn in psutil.net_connections()
            if sconn.laddr[1] == port and sconn.status == 'ESTABLISHED']

def tick(led_is_on, prev_connect_count, mumble_port, gpio_pin):
    clients = get_mumble_clients(mumble_port)
    num_clients = len(clients)
    clients_connected = num_clients > 0

    if clients_connected:
        led_is_on = not led_is_on
        led_gpio_state = GPIO.HIGH if led_is_on else GPIO.LOW
        GPIO.output(gpio_pin, led_gpio_state)
    else:
        led_is_on = False
        GPIO.output(gpio_pin, GPIO.LOW)

    if num_clients != prev_connect_count:
        clients_join = ','.join('%s:%s' % client for client in clients)
        clients_str = '' if num_clients == 0 else ': %s' % clients_join
        plural_str = '' if num_clients == 1 else 's'
        logger.info('%s client%s connected%s', num_clients, plural_str,
                    clients_str)

    return num_clients, led_is_on

def main():
    logging.basicConfig(
        format='[%(asctime)-15s] %(message)s', level=logging.INFO)

    gpio_pin = 18
    mumble_port = 64738

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(gpio_pin, GPIO.OUT)

    led_is_on = False
    num_clients = -1

    try:
        while True:
            num_clients, led_is_on = tick(led_is_on, num_clients, mumble_port, gpio_pin)
            time.sleep(1)
    except:
        GPIO.output(gpio_pin, GPIO.LOW)

if __name__ == '__main__':
    sys.exit(main())
