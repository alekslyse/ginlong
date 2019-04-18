import ginlong

ginlong = ginlong.Ginlong()

ginlong.authenticate("username", "password")

pp = ginlong.get_powerplants()

p = ginlong.get_powerplant(245519)

p = ginlong.get_powerplant_devices(245519)

d = ginlong.get_powerplant_inverter(245519, 101099035)

l = ginlong.get_powerplant_logger(245519, 704867519)

c = ginlong.get_powerplant_condition(245519)

print(c)