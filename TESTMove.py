''' PRESS CONTROL_C BEFORE RESTARTING
'''


import thorlabs_apt as apt
import thorlabs_apt.core as core
import threading
import time

def move_to_XY(x,y,Mx,My):
    Vmax = 2.29 # mm/s
    curx = Mx.position
    cury = My.position
    #cyrz = Mz.position
    dx = x - curx
    dy = y - cury
    #dz = z - curz
    maxD = max(abs(dx),abs(dy))
    t = maxD/Vmax
    Vx = abs(dx)/t
    Vy = abs(dy)/t
    #Vz = dz/t
    print("Vx: ",Vx, "Vy: ",Vy)
    Vmin, Acc, Vmax_X = Mx.get_velocity_parameters() # Get motor defaults   
    Mx.set_velocity_parameters(Vmin, Acc, Vx)
    My.set_velocity_parameters(Vmin, Acc, Vy)
    #Mz.set_velocity_parameters(Vmin, Acc, Vz)
    # Move motors at differnt speeds so they all arrive at the same time
    Mx.move_by(dx)
    My.move_by(dy)
    #Mz.move_to(dz)
    while True:
        if round(Mx.position,4) == x and round(My.position,4) == y:
            print("motorX pos: ", Mx.position, "  Motor Y pos: ",My.position)
            time.sleep(0.1) # in sec
            break
    print('reached ',x,y)

def move_to_XYZ(x,y,z,Mx,My,Mz):
    Vmax = 2.29 # mm/s
    curx = Mx.position
    cury = My.position
    curz = Mz.position
    dx = x - curx
    dy = y - cury
    dz = z - curz
    maxD = max(abs(dx),abs(dy),abs(dz))
    t = maxD/Vmax
    Vx = abs(dx)/t
    Vy = abs(dy)/t
    Vz = abs(dz)/t
    print("Vx: ",Vx, "Vy: ",Vy, "Vz: ",Vz)
    if Vx < 0.25: Vx = 0.25
    if Vy < 0.25: Vy = 0.25
    if Vz < 0.25: Vz = 0.25
        
    print("Vx: ",Vx, "Vy: ",Vy, "Vz: ",Vz)
    Vmin, Acc, Vmax_X = Mx.get_velocity_parameters() # Get motor defaults
    print("Motor data: Vmin = ",Vmin,'Vmax_X = ',Vmax_X,'Acc = ',Acc)
    Mx.set_velocity_parameters(Vmin, Acc, Vx)
    My.set_velocity_parameters(Vmin, Acc, Vy)
    Mz.set_velocity_parameters(Vmin, Acc, Vz)
    # Move motors at differnt speeds so they all arrive at the same time
    Mx.move_by(dx)
    My.move_by(dy)
    Mz.move_by(dz)
    while True:
        if round(Mx.position,4) == x and round(My.position,4) == y and round(Mz.position,4) == z:
            print("motorX pos: ", Mx.position, "  Motor Y pos: ",My.position, "  Motor Z pos: ",Mz.position)
            time.sleep(0.1) # in sec
            break
    print('reached ',x,y,z)


###########################################

MOVING = None
try:
    print("Available Motors: ",apt.list_available_devices())
    Mx = apt.Motor(27003942)
    My = apt.Motor(27003941)
    Mz = apt.Motor(27003952)
    print("HOMING...")
    Mx.move_home()
    My.move_home()
    Mz.move_home()
    while True:
        if Mx.has_homing_been_completed and (My.has_homing_been_completed) and (Mz.has_homing_been_completed):
            Mx.disable()
            My.disable()
            Mz.disable()
            time.sleep (0.1) #in sec
            Mx.enable()
            My.enable()
            Mz.enable()
            time.sleep (0.1) #in sec
            break
    print("Motors homed")

    #Move
  coordinates = [(10,0,1),(5,5,10),(10,10,10),(5,5,5),(10,5,1)]
    i = 0
    while True:
    
        if MOVING is None or not MOVING.is_alive(): #is_alive is a Tread function
            if i >= len(coordinates): break
            MOVING = threading.Thread(target=move_to_XYZ, args = (coordinates[i][0],
                                                                  coordinates[i][1],
                                                                  coordinates[i][2],
                                                                  Mx,My,Mz,
                                                                  RELATIVE = False))
            MOVING.start()
            
            i+=1
            print('started thread ', i)



finally:
    print('cleanup')
    core._cleanup()





