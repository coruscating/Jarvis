# checks laser powers

sleeptime=2

freq422orig=self.server.current_states['CH1-0']
power422orig=self.server.current_states['CH1-2']
freq1092orig=self.server.current_states['CH2-0']
power1092orig=self.server.current_states['CH2-2']

devQueue.put("PulseProgrammer;PARAM 0 2 0\n")
devQueue.put("PulseProgrammer;PARAM 2 2 0\n")
devQueue.put("PulseProgrammer;DigOut 0")
devQueue.put("Shutters;Shutter405 OPEN\n")
devQueue.put("Shutters;Shutter461 CLOSE\n")
devQueue.put("PowerMeter;WAVELENGTH 405")
time.sleep(sleeptime)

powers = "405: " + str(round(self.server.current_states['PowerMeterPower'], 1)) + " uW\n"

devQueue.put("Shutters;Shutter405 CLOSE\n")
devQueue.put("Shutters;Shutter461 OPEN\n")
devQueue.put("PowerMeter;WAVELENGTH 461")
time.sleep(sleeptime)

powers += "461: " + str(round(self.server.current_states['PowerMeterPower'], 1)) + " uW\n"

devQueue.put("Shutters;Shutter461 CLOSE\n")
devQueue.put("PulseProgrammer;PARAM 0 0 200\n")
devQueue.put("PulseProgrammer;PARAM 0 2 45000\n")
devQueue.put("PowerMeter;WAVELENGTH 422")
time.sleep(sleeptime)

powers += "422: " + str(round(self.server.current_states['PowerMeterPower'], 1)) + " uW at 200, 45000\n"

devQueue.put("PulseProgrammer;PARAM 0 2 49000\n")
time.sleep(sleeptime/2)

powers += "422: " + str(round(self.server.current_states['PowerMeterPower'], 1)) + " uW at 200, 49000\n"

devQueue.put("PowerMeter;WAVELENGTH 1092")
devQueue.put("PulseProgrammer;PARAM 0 2 0\n")
devQueue.put("PulseProgrammer;PARAM 2 0 200\n")
devQueue.put("PulseProgrammer;PARAM 2 2 65000\n")
time.sleep(sleeptime/2)

powers += "1092: " + str(round(self.server.current_states['PowerMeterPower'], 1)) + " uW at 200, 65000\n"

devQueue.put("PowerMeter;WAVELENGTH 1033\n")
devQueue.put("PulseProgrammer;PARAM 2 2 0\n")
devQueue.put("PulseProgrammer;DigOut 3\n")
time.sleep(sleeptime/2)
powers += "1033: " + str(round(self.server.current_states['PowerMeterPower'], 1)) + " uW"

devQueue.put("PulseProgrammer;DigOut 0\n")

print powers

webQueue.put("SCRIPTOUTPUT;" + self.timeID + ';' + powers + '\n')
