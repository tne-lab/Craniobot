''' PRESS CONTROL_C BEFORE RESTARTING
'''


import thorlabs_apt as apt
import thorlabs_apt.core as core
import threading
import time

def move_step(step,M): # M is motor X, Y or Z
    try:
        Vmin, Acc, Vmax_X = M.get_velocity_parameters() # Get motor defaults
        M.set_velocity_parameters(Vmin, Acc, 2.29) # Max speed
        M.identify()
        cur_pos = M.position
        # Move motor at max speed by step_size (mm?)
        new_pos = round(cur_pos + step,1)
        if new_pos >= 0.0 and new_pos <=25.0:
            M.move_by(step)

            while True:
                if not M.is_in_motion:
                #if round(M.position,1) == new_pos:
                    time.sleep(0.1) # in sec
                    break
            print("motor pos: ", M.position)
        else: print("MOTOR REACHED LIMIT")
    except:
        print("failed to move")
##        print('cleanup')
##        core._cleanup()
        

##def move_to_XY(x,y,Mx,My, RELATIVE = False):
##    Vmax = 2.29 # mm/s
##    curx = Mx.position
##    cury = My.position
##    #cyrz = Mz.position
##    if RELATIVE: # Move by x,y amount from whereever you are
##        dx = x 
##        dy = y 
##
##    else:        # Move to absolute location x,y in robot coordinates
##        dx = x - curx
##        dy = y - cury
##        dz = z - curz
##
##    maxD = max(abs(dx),abs(dy))
##    t = maxD/Vmax
##    Vx = abs(dx)/t
##    Vy = abs(dy)/t
##
##    print("Vx: ",Vx, "Vy: ",Vy)
##    Vmin, Acc, Vmax_X = Mx.get_velocity_parameters() # Get motor defaults   
##    Mx.set_velocity_parameters(Vmin, Acc, Vx)
##    My.set_velocity_parameters(Vmin, Acc, Vy)
##
##    # Move motors at differnt speeds so they all arrive at the same time
##    Mx.move_by(dx)
##    My.move_by(dy)
##    #Mz.move_to(dz)
##    while True:
##        if round(Mx.position,4) == x and round(My.position,4) == y:
##            print("motorX pos: ", Mx.position, "  Motor Y pos: ",My.position)
##            time.sleep(0.1) # in sec
##            break
##    print('reached ',x,y)
##def move_to_XY(x,y,Mx,My,RELATIVE = False):
##    Vmax = 2.29 # mm/s
##    curx = Mx.position
##    cury = My.position
##
##    if RELATIVE: # Move by x,z, amount from whereever you are
##        dx = x 
##        dy = y 
##
##    else:        # Move to absolute location x,y,z in robot coordinates
##        dx = x - curx
##        dy = y - cury
##        
##    maxD = max(abs(dx),abs(dy))
##    t = maxD/Vmax
##    Vx = abs(dx)/t
##    Vy = abs(dy)/t
##    #print("Vx: ",Vx, "Vy: ",Vy)
##
##    Vmin, Acc, Vmax_X = Mx.get_velocity_parameters() # Get motor defaults
##    #print("Motor data: Vmin = ",Vmin,'Vmax_X = ',Vmax_X,'Acc = ',Acc)
##    if Vx > Vmax or Vy > Vmax:
##        print("Error calculating Vs")
##        return False
##    else: #Vs OK
##        if Vx > 0.0 : Mx.set_velocity_parameters(Vmin, Acc, Vx)
##        if Vy > 0.0 : My.set_velocity_parameters(Vmin, Acc, Vy)
##
##    abs_x = curx + dx
##    abs_y = curx + dy
##
##    if abs_x >= 0.0 and abs_x <= 25.0:  Mx.move_by(dx)
##    if abs_y >= 0.0 and abs_y <= 25.0:  My.move_by(dy)
##
##    # Move motors at differnt speeds so they all arrive at the same time
##    while True:
##        if round(Mx.position,1) == abs_x and round(My.position,1) == abs_y:
##            #print("motorX pos: ", Mx.position, "  Motor Y pos: ",My.position)
##            time.sleep(0.1) # in sec
##            break
##    print('reached ',x,y)
##    return True
##
####def move_to_XYZ(x,y,z,Mx,My,Mz,RELATIVE = False):
##    Vmax = 2.29 # mm/s
##    curx = Mx.position
##    cury = My.position
##    curz = Mz.position
##    if RELATIVE: # Move by x,z, amount from whereever you are
##        dx = x 
##        dy = y 
##        dz = z 
##    else:        # Move to absolute location x,y,z in robot coordinates
##        dx = x - curx
##        dy = y - cury
##        dz = z - curz
##        
##    maxD = max(abs(dx),abs(dy),abs(dz))
##    t = maxD/Vmax
##    Vx = abs(dx)/t
##    Vy = abs(dy)/t
##    Vz = abs(dz)/t
####    print("Vx: ",Vx, "Vy: ",Vy, "Vz: ",Vz)
####    if Vx < 0.25: Vx = 0.25
####    if Vy < 0.25: Vy = 0.25
####    if Vz < 0.25: Vz = 0.25
####        
####    print("Vx: ",Vx, "Vy: ",Vy, "Vz: ",Vz)
##    Vmin, Acc, Vmax_X = Mx.get_velocity_parameters() # Get motor defaults
####    print("Motor data: Vmin = ",Vmin,'Vmax_X = ',Vmax_X,'Acc = ',Acc)
##    if Vx > Vmax or Vy > Vmax or Vz > Vmax:
##        print("Error calculating Vs")
##        return False
##    else: #Vs OK
##        if Vx > 0.0 : Mx.set_velocity_parameters(Vmin, Acc, Vx)
##        if Vy > 0.0 : My.set_velocity_parameters(Vmin, Acc, Vy)
##        if Vz > 0.0 : Mz.set_velocity_parameters(Vmin, Acc, Vz)
##    abs_x = curx + dx
##    abs_y = curx + dy
##    abs_z = curx + dz
##    if abs_x >= 0.0 and abs_x <= 25.0:  Mx.move_by(dx)
##    if abs_y >= 0.0 and abs_y <= 25.0:  My.move_by(dy)
##    if abs_z >= 0.0 and abs_z <= 25.0:  Mz.move_by(dz)
##    # Move motors at differnt speeds so they all arrive at the same time
##    while True:
##        if round(Mx.position,1) == abs_x and round(My.position,1) == abs_y and round(Mz.position,1) == abs_z:
##            print("motorX pos: ", Mx.position, "  Motor Y pos: ",My.position, "  Motor Z pos: ",Mz.position)
##            time.sleep(0.1) # in sec
##            break
##    print('reached ',x,y,z, '\n')
##    return True

def connect_to_2motors():
    try:
        print("Available Motors: ",apt.list_available_devices())
        Mx = apt.Motor(27003942)
        My = apt.Motor(27003941)

    except:
        print("Unable to connect")
        return False, False
    return Mx, My

def connect_to_3motors():
    try:

        print("Available Motors: ",apt.list_available_devices())
        Mx = apt.Motor(27003941)
        My = apt.Motor(27003942)
        Mz = apt.Motor(27003952)
    except:
        print("Unable to connect")
        return None, None, None
    return Mx, My, Mz

def home_robot(M):
    try:
        print("HOMING...")
        M.move_home()

        while True:
            if M.has_homing_been_completed:
                M.disable()
                time.sleep (0.1) #in sec
                M.enable()
                time.sleep (0.1) #in sec
                break
        print("Motors homed")
    except:
        print("Unable to home motors")
        print('cleaning up')
        core._cleanup()
        return False
    return True

def home_all(Mx, My, Mz):
    try:
        print("HOMING...")
        Mx.move_home()
        My.move_home()
        Mz.move_home()
        while True:
            if Mx.has_homing_been_completed and \
               (My.has_homing_been_completed) and \
               (Mz.has_homing_been_completed):
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
    except:
        print("Unable to home motors")
        print('cleaning up')
        core._cleanup()
        return False
    return True


##def move_sequence(coordinates,RELATIVE):
##    # moves to coordinates = [(x1,y1,z1),...,(xn,yn,zn)] 0r
##    #          coordinates = [(x1,y1),...,(xn,yn,)] 0r
##    MOVING = None
##    num_coords = len(coordinates)
##    try:
##        i = 0
##        while True:
##            if MOVING is None or not MOVING.is_alive(): #is_alive is a Tread function
##                if i >= len(coordinates):
##                    break
##                if num_coords == 2:
##                    MOVING = threading.Thread(target=move_to_XY, args = (coordinates[i][0],
##                                                                      coordinates[i][1],
##                                                                      Mx,My,
##                                                                      RELATIVE))
##                if num_coords == 3:
##                    MOVING = threading.Thread(target=move_to_XYZ, args = (coordinates[i][0],
##                                                                      coordinates[i][1],
##                                                                      coordinates[i][2],
##                                                                      Mx,My,Mz,
##                                                                      RELATIVE))
##                MOVING.start()
##                
##                i+=1
##                print('started thread ', i)
##
##    except:
##        print("Unable to move")
##        return False
##    return True

##def move_steps(coordinates,RELATIVE):
##    # moves to coordinates = (x1,y1,z1) 0r
##    #          coordinates = (x1,y1) 0r
##    MOVING = None
##    num_coords = len(coordinates)
##    try:
##        #Move
##        #  coordinates = [(10,0,1),(5,5,10),(10,10,10),(5,5,5),(10,5,1)]
##        i = 0
##        while True:
##            if MOVING is None or not MOVING.is_alive(): #is_alive is a Tread function
##                if i >= len(coordinates): break
##                if num_coords == 2:
##                    MOVING = threading.Thread(target=move_to_XY, args = (coordinates[i][0],
##                                                                      coordinates[i][1],
##                                                                      Mx,My,
##                                                                      RELATIVE))
##                if num_coords == 3:
##                    MOVING = threading.Thread(target=move_to_XYZ, args = (coordinates[i][0],
##                                                                      coordinates[i][1],
##                                                                      coordinates[i][2],    
##                                                                      Mx,My,Mz,
##                                                                      RELATIVE))
##
##                MOVING.start()
##                
##                i+=1
##                print('started thread ', i)
##
##    except:
##        print("Unable to move")
##        return False
##    return True



