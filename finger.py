import base64
from pyfingerprint.pyfingerprint import PyFingerprint
FINGERPRINT_CHARBUFFER1 = 0x01
FINGERPRINT_CHARBUFFER2 = 0x02

def get_finger(finger_original):
    accuracy = 0 
    try:
        f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)

        if ( f.verifyPassword() == False ):
            raise ValueError('The given fingerprint sensor password is wrong!')

        print('Waiting for finger...')

        ## Wait that finger is read
        while ( f.readImage() == False ):
            pass

        ## Converts read image to characteristics and stores it in charbuffer 1
        f.convertImage(FINGERPRINT_CHARBUFFER1)

        if (f.uploadCharacteristics(FINGERPRINT_CHARBUFFER2,finger_original)==False):
            raise ValueError("Could not upload characteristics")

        accuracy = f.compareCharacteristics()
    except Exception as e:
        print('The fingerprint sensor could not be initialized!')
        print('Exception message: ' + str(e))
    finally:
        return accuracy
