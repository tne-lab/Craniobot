import thorlabs_apt as apt
print(apt.list_available_devices())

motorX = apt.Motor(27003942)
motorY = apt.Motor(27003941)
Vmax = 2.29
motorX.move_to(5,True)
motorY.move_to(5,True)
motorX.move_home()
motorY.move_home()
while not (motorX.has_homing_been_completed) and not (motorY.has_homing_been_completed):
    pass
print("X & Y homed")


##print(motor.get_velocity_parameters())
##print("TEST")
##motor.move_home(True)
##print("done")
##print(motor.has_homing_been_completed)
##motor.move_to(5)

'''
def hardware_info(self):

is_in_motion(self):

move_to(self, value, blocking = False)

move_by(self, value, blocking = False)

def get_stage_axis_info(self):

def set_stage_axis_info(self, min_pos, max_pos, units, pitch):

def velocity_upper_limit(self):

def acceleration_upper_limit(self):

def get_velocity_parameter_limits(self):

def set_velocity_parameters(self, min_vel, accn, max_vel):

 def get_velocity_parameters(self):

 def identify(self):

 def is_settled(self):
'''

