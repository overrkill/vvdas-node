

import RPi.GPIO as GPIO

from mfrc522 import SimpleMFRC522



def getrfid():
        
    reader = SimpleMFRC522()
    rf_val = "0"
    try:

            id, text = reader.read()

            print(id)

            rf_val = text

    finally:

            return rf_val