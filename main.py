import time

from robot import Robot

############## Настройки программы ##############
baud = 115200
arduino_port = 4
################# Конец настроек #################

robot = Robot(f'COM{arduino_port}', baud)
robot.connect()
robot.start_threads()
time.sleep(1)
robot.startConsole()