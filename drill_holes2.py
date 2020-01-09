''' PRESS CONTROL_C BEFORE RESTARTING
    ASSUMES BREGMA FOUND
'''


import thorlabs_apt as apt
import thorlabs_apt.core as core
import threading
import time
from RobotCommands import home_all


def move_to_XYZ(x,y,z,Mx,My,Mz,chg_V = None):
    Vmax = 2.25 # mm/s
    if chg_V == 'vel_up':
        Vmax += 0.25
        if Vmax >= 2.25:
            Vmax = 2.25
    elif chg_V == 'vel_dn':
        Vmax -= 0.25
        if Vmax <= 0.25:
            Vmax = 0.25

    x= round(x,1)
    y= round(y,1)
    z= round(z,1)
    curx = round(Mx.position,1)
    cury = round(My.position,1)
    curz = round(Mz.position,1)
    dx = x - curx
    dy = y - cury
    dz = z - curz
    maxD = max(abs(dx),abs(dy),abs(dz))
    t = maxD/Vmax
    if t == 0:
        return
    Vx = abs(dx)/t
    Vy = abs(dy)/t
    Vz = abs(dz)/t
    if dx == 0 and dy == 0 and dz >= 0:
        Vz = 0.5
    #print("Vx: ",Vx, "Vy: ",Vy, "Vz: ",Vz)
    if Vx < 0.25: Vx = 0.25
    if Vy < 0.25: Vy = 0.25
    if Vz < 0.25: Vz = 0.25
        
    print("Vx: ",Vx, "Vy: ",Vy, "Vz: ",Vz)
    Vmin, Acc, Vmax_X = Mx.get_velocity_parameters() # Get motor defaults
    #print("Motor data: Vmin = ",Vmin,'Vmax_X = ',Vmax_X,'Acc = ',Acc)
    Mx.set_velocity_parameters(Vmin, Acc, Vx)
    My.set_velocity_parameters(Vmin, Acc, Vy)
    Mz.set_velocity_parameters(Vmin, Acc, Vz)
    # Move motors at differnt speeds so they all arrive at the same time
    print("MOVONG TO: ",x,y,z, "relative: ", dx,dy,dz)
    Mx.move_by(dx)
    My.move_by(dy)
    Mz.move_by(dz)
    while True:
        curx = round(Mx.position,1)
        cury = round(My.position,1)
        curz = round(Mz.position,1)
        #print("MOVONG TO: ",x,y,z,"  At: ",curx,cury,curz)
        if not Mx.is_in_motion and not My.is_in_motion and not Mz.is_in_motion:
        #if curx == x and cury == y and curz == z:
            time.sleep(0.1) # in sec
            break

    print('reached ',x,y,z)

def get_bregma(Mx,My,Mz): #In robo coords
    x = Mx.position
    y = My.position
    z = Mz.position
    return x,y,z    
###########################################

def drill_holes(hole,BREGMArobo,Mx,My,Mz, que):
    ROBO_FOUND = False
    MOVING = None
    ROBOT_OUT_OF_RANGE = False
    PAUSE = False
    STOP = False
    DOWN = False
    UP = False
    DONE = False
    chg_vel = ""
    moves = []
    x0 = BREGMArobo[0]
    y0 = BREGMArobo[1]
    z0 = BREGMArobo[2]
    coords = []
    # CONVERT RAT COORDINATES TO ROBO COORDINATES
    x = hole[0] + x0
    y = hole[1] + y0
    #Lift z off of cur pos
    cur_x = Mx.position
    cur_y = My.position
    z = z0-5
    moves.append((cur_x,cur_y,z)) # MOVE TO 5mm above (cur_x,cur_y), Up  5 mm away from surface
    moves.append((x,y,z)) # MOVE TO 5mm above hole
    z = z0
    moves.append((x,y,z)) # MOVE TO HOLE AT SKULL SURFACE
    z = z0+1 # DN 1 mm
    moves.append((x,y,z)) # drill hole i mm deep
    
##    z = z0-5 # UP
##    moves.append((x,y,z))
##    moves.append((BREGMArobo[0],BREGMArobo[1],BREGMArobo[2]-5)) # Go to just above Bregma
##    print("drill hole PATH: ",holes)
    if (ROBOT_OUT_OF_RANGE):
        print("\n\n\n\ROBOT OUT OF RANGE. RESET BREGMA\n\n\n")
    else:
        print("HOLE: ",x,y,z)
    try:
        i = 0
        while True:
            if not que.empty():
                msg = que.get()
                if msg == 'PAUSE':
                    if not STOP:
                        i-=1
                    PAUSE = True
                elif msg == 'STOP':
                    i-=1
                    STOP = True
                elif msg == 'RESUME':
                    PAUSE = False
                elif msg == 'GO':
                    STOP = False
                elif msg == 'DONE':
                    DONE = True
                if msg == 'vel_up':
                    chg_vel = 'vel_up'
                elif msg == 'vel_dn':
                    chg_vel = 'vel_dn'                    
            #print("msg: ", msg)        
            if MOVING is None or not MOVING.is_alive(): #is_alive is a Tread function
                if i >= len(moves):
                    break
                if PAUSE:  # If PAUSING, stop motion, but lift robot up by 5mm
                    MOVING = threading.Thread(target=move_to_XYZ, args = (moves[i][0],
                                                                          moves[i][1],
                                                                          moves[i][2] - 5,
                                                                          Mx,My,Mz,chg_vel))
                    MOVING.start()
                    
                elif STOP: # If STOPPING, stop all motion.
                    pass

                else: # OTHERWISE, DRILL ON...
                    MOVING = threading.Thread(target=move_to_XYZ, args = (moves[i][0],
                                                                          moves[i][1],
                                                                          moves[i][2],
                                                                          Mx,My,Mz,chg_vel))
                    MOVING.start()
                    i+=1
        MOVING = None
        print("FInished at: ",round(moves[i-1][0],1),round(moves[i-1][0],1),round(moves[i-1][0],1)) 
    except:
        print('cleanup')
        print('movement error')





