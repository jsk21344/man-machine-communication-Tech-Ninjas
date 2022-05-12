import time
import math
import mraa


class Operations:
    def eingriff():
        s = mraa.Aio(3)
        x = mraa.I2c(0)
        x.address(0x53)

        x.writeReg(0x2D, 8)
        time.sleep(0.01)
        x.writeReg(0x1E, 1)
        time.sleep(0.01)
        x.writeReg(0x1F, 130)
        time.sleep(0.01)
        x.writeReg(0x20, 137)
        time.sleep(0.01)

        sensor_F = 0
        x_out_F = 0
        y_out_F = 0
        z_out_F = 0
        pitch_F = 0
        roll_F = 0

        while True:
            x_out = (x.readReg(0x32) | x.readReg(0x33) << 8)
            x_out = x_out / 25.6
            y_out = (x.readReg(0x34) | x.readReg(0x35) << 8)
            y_out = y_out / 25.6
            z_out = (x.readReg(0x36) | x.readReg(0x37) << 8)
            z_out = z_out / 25.6
            sensor = s.read()

            roll = math.atan(
                y_out/math.sqrt(x_out**2+z_out**2))*180/math.pi
            pitch = math.atan(-1*x_out /
                              math.sqrt(y_out**2+z_out**2))*180/math.pi

            roll_F = 0.5*roll_F+0.5*roll
            pitch_F = 0.5 * pitch_F + 0.5 * pitch
            x_out_F = 0.5 * x_out_F + 0.5 * x_out
            y_out_F = 0.5 * y_out_F + 0.5 * y_out
            z_out_F = 0.5 * z_out_F + 0.5 * z_out
            sensor_F = 0.5 * sensor_F + 0.5 * sensor

            print("Roll:" + str(roll_F) + " pitch: " + str(pitch_F) + " x_out: " + str(x_out_F) +
                  " y_out: " + str(y_out_F) + " z_out: " + str(z_out_F) + "Sensor F: " + str(sensor_F))
            time.sleep(0.1)

    def status():
        global voice_output
        voice_output = "Maschine" + \
            str(maschinenID) + "läuft und hat keinen Fehler"

    def select_machine(id):
        global maschinenID
        maschinenID = id

    def start():
        global voice_output
        voice_output = "Maschine startet"
