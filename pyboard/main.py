
from machine import I2C
import mpu6050
import time
import ujson

usb = pyb.USB_VCP()

def send_data(data):
    global usb
    print(data)
    toto = ujson.dumps(data)
    usb.write(toto + "\n")

a = 1
while a:
    try:
        # Set pin: scl on Y9 and sda on Y10
        i2c = I2C(scl='Y9', sda='Y10', freq=400000)
        mpu_6050 = mpu6050.MPU6050(i2c)
        a = 0
    except:
        print("init bad")

if mpu_6050.detect():
    data = None
    while True:
        try:
            # get sensors values
            mpu_6050.lecture_capteurs()

            # Details
            gX = mpu_6050.gyroX
            gY = mpu_6050.gyroY
            gZ = mpu_6050.gyroZ

            gX_c = mpu_6050.gyroX_calibre
            gY_c = mpu_6050.gyroY_calibre
            gZ_c = mpu_6050.gyroZ_calibre

            aX = mpu_6050.accX
            aY = mpu_6050.accY
            aZ = mpu_6050.accZ

            aX_c = mpu_6050.accX_calibre
            aY_c = mpu_6050.accY_calibre
            aZ_c = mpu_6050.accZ_calibre

            angleX = mpu_6050.AngleX
            angleY = mpu_6050.AngleY
            angleZ = mpu_6050.AngleZ

            #  all data
            data = {"gX": gX,
                    "gY": gY,
                    "gZ": gZ,
                    "gX_c": gX_c,
                    "gY_c": gY_c,
                    "gZ_c": gZ_c,
                    "aX": aX,
                    "aY": aY,
                    "aZ": aZ,
                    "aX_c": aX_c,
                    "aY_c": aY_c,
                    "aZ_c": aZ_c,
                    "angleX": angleX,
                    "angleY": angleY,
                    "angleZ": angleZ}
        except:
            data = "bad\n"

        print(data)

        # Send with I2C
        send_data(data)
        pyb.delay(20)
