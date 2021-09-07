import sys
import time

sys.path.append(".")
from coldplate_serialcom import ColdPlate_serialcom

class COLDPLATE:
    def __init__(self, port):
        try:
            self.coldplate = ColdPlate_serialcom(port)
            print('Coldplate device created')
        except:
            print('Failed to create coldplate device')

    def __del__(self):
        self.coldplate.ask("toff")
        del self.coldplate

    def get_version(self):
        response = self.coldplate.ask("version")
        return response

    def set_buzzer(self, millis):
        command = "setBuzzer" + str(millis)
        self.coldplate.ask(command)

    def set_tempOn(self):
        command = "ton"
        self.coldplate.ask(command)

    def set_tempOff(self):
        command = "toff"
        self.coldplate.ask(command)

    def get_tempActual(self):
        response = self.coldplate.ask("gta")
        return round(float(response), 2)

    def set_tempTarget(self, temp):
        temp = int(round(float(temp), 1)*10)
        command = "stt" + str(temp)
        self.coldplate.ask(command)

    def get_tempTarget(self, temp):
        response = self.coldplate.ask("gtt")
        return round(float(response), 1)

    def set_tempLimiterMin(self, temp):
        temp = int(round(float(temp), 1)*10)
        command = "stlmin" + str(temp)
        self.coldplate.ask(command)

    def get_tempLimiterMin(self):
        response = self.coldplate.ask("gtlmin")
        return round(float(response), 1)

    def set_tempLimiterMax(self, temp):
        temp = int(round(float(temp), 1)*10)
        command = "stlmax" + str(temp)
        self.coldplate.ask(command)

    def get_tempLimiterMax(self):
        response = self.coldplate.ask("gtlmax")
        return round(float(response), 1)

    def get_tempState(self):
        response = self.coldplate.ask("gts")
        return ("inactive", "active")[int(response)]


    def receive(self):
        data = self.coldplate.receive()
        return data


    def bring_to_start_temp(self, temperature_reading = None, starting_temp = 25, max_setpoint = 99, min_setpoint = -10, margin = 0.5):
        # Determine if it should start heating or cooling
        if temperature_reading is None:
            temperature_reading = COLDPLATE.get_tempActual(self) # Measure current temperature of the sample

        if temperature_reading < starting_temp:
            initTemp = max_setpoint
        elif temperature_reading > starting_temp:
            initTemp = min_setpoint
        # Set and start initial temperature target
        COLDPLATE.set_tempTarget(self, initTemp)
        COLDPLATE.set_tempOn(self)
        print("Target: {} deg   Current: {} deg Set point: {} deg".format(starting_temp, temperature_reading, initTemp))

        # Bring thermocycler samples to the starting cold temperature
        n = 0
        while True:
            if temperature_reading is None:
                temperature_reading = COLDPLATE.get_tempActual(self) # Measure current temperature of the sample
            if n == 100:
                print("Current temp {} deg".format(temperature_reading))
                n = 0
            if (starting_temp - margin) >= temperature_reading or temperature_reading >= (starting_temp + margin):
                n = n+1
            else:
                print("Target reached: {} - {} = {} deg".format(temperature_reading, starting_temp, temperature_reading-starting_temp))
                break





