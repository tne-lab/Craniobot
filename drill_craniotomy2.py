''' PRESS CONTROL_C BEFORE RESTARTING
    ASSUMES BREGMA FOUND
'''


import thorlabs_apt as apt
import thorlabs_apt.core as core
import threading
import time
from RESOURCES.Calculate_Plane_and_plot import *
from RobotCommands import home_all

def move_to_XYZ(x,y,z,Mx,My,Mz,chg_vel = None): #default Vmax = 2.25 in mm/s
    Vmax = 2.25 #default Vmax = 2.25 in mm/s
    if chg_vel == 'vel_up':
        Vmax += 0.25
        if Vmax >= 2.25:
            Vmax = 2.25
    elif chg_vel == 'vel_dn':
        Vmax -= 0.25
        if Vmax <= 0.25:
            Vmax = 0.25
    print ("Vmax: ", Vmax)    
    x = round(x,1)
    y = round(y,1)
    z = round(z,1)   
    curx = round(Mx.position,1)
    cury = round(My.position,1)
    curz = round(Mz.position,1)
    dx = x - curx
    dy = y - cury
    dz = z - curz
    maxD = max(abs(dx),abs(dy),abs(dz))
    if maxD < 4.0: Vmax = .5
    
    if maxD > 0:
        t = maxD/Vmax
        if t == 0:
            return
        Vx = abs(dx)/t
        Vy = abs(dy)/t
        Vz = abs(dz)/t
        #print("Vx: ",Vx, "Vy: ",Vy, "Vz: ",Vz)
        if Vx < 0.25: Vx = 0.25
        if Vy < 0.25: Vy = 0.25
        if Vz < 0.25: Vz = 0.25
            
        #print("Vx: ",Vx, "Vy: ",Vy, "Vz: ",Vz)
        Vmin, Acc, Vmax_X = Mx.get_velocity_parameters() # Get motor defaults
        #print("Motor data: Vmin = ",Vmin,'Vmax_X = ',Vmax_X,'Acc = ',Acc)
        Mx.set_velocity_parameters(Vmin, Acc, Vx)
        My.set_velocity_parameters(Vmin, Acc, Vy)
        Mz.set_velocity_parameters(Vmin, Acc, Vz)

        # Move motors at differnt speeds so they all arrive at the same time
        #print("MOVING TO: ",x,y,z, "relative: ", dx,dy,dz)
        Mx.move_by(dx)
        My.move_by(dy)
        Mz.move_by(dz)
        while True:
            curx = round( Mx.position,1)
            cury = round( My.position,1)
            curz = round( Mz.position,1)
            #print("MOVONG TO: ",x,y,z,"  At: ",curx,cury,curz)
            
            if not Mx.is_in_motion and not My.is_in_motion and not Mz.is_in_motion:
            #if curx == x and cury == y and curz == z:
                time.sleep(0.1) # in sec
                break
        print('reached ',x,y,z)
    else:
        print("x,y,z,dx,dy,dz: ",x,y,z,dx,dy,dz)
def get_bregma(Mx,My,Mz): #In robo coords
    x = Mx.position
    y = My.position
    z = Mz.position
    return x,y,z    
###########################################

def drill_carniotomy(BREGMArobo,Mx,My,Mz,roboXs,roboYs,roboZs,circle,depth, que ):
    #roboXs,roboYs,roboZs are the selected points for best fit plane
    x0 = BREGMArobo[0]
    y0 = BREGMArobo[1]
    z0 = BREGMArobo[2]

    ROBO_FOUND = False
    MOVING = None
    ROBOT_OUT_OF_RANGE = False
    PAUSE = False
    STOP = False
    chg_vel = None
##    # BEST FIT CIRCLE
##    circle = best_fit_plot(roboXs,roboYs,roboZs,5.5,BREGMArobo,0,-1.7)
    points = []
    z = 0
    x = 0
    y = 0
    idx = 0
    for h in circle:
        print("pt: ",h)
        x = h[0] 
        y = h[1]
        z = h[2]+depth
        # FOR 16 point circle, add depth around edges to accomodate skull shape
        if len(circle) == 16:
            if idx == 0 or idx == 8: z = z + 0.95
            if idx == 1 or idx == 7 or idx == 9 or idx == 15: z = z + 0.5
        print("x,y,z: ",x,y,z)
        if x <0.0 or x >25.0:
            print ("X out of range")
            ROBO_OUT_OF_RANGE = True
        if y <0.0 or y >25.0:
            print ("Y out of range")
            ROBO_OUT_OF_RANGE = True
        if z <0.0 or z >25.0:
            print ("Z out of range")
            ROBO_OUT_OF_RANGE = True
        if len(points) == 0:
            points.append((x,y,z-5))
        points.append((x,y,z)) # MOVE
        idx +=1
    #points.append((x,y,z-5)) # go above BREGMA by 5
    #points.append((1,1,1)) # Go to almost HOME
    #print("drill hole PATH: ",points)
    if (ROBOT_OUT_OF_RANGE):
        print("\n\n\n\ROBOT OUT OF RANGE. RESET BREGMA\n\n\n")
        
    try:
        i = 0
        while True:
            if not que.empty():
                msg = que.get()
                if msg == 'vel_up':
                    chg_vel = 'vel_up'
                elif msg == 'vel_dn':
                    chg_vel = 'vel_dn'
                elif msg == 'PAUSE':
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
            if MOVING is None or not MOVING.is_alive(): #is_alive is a Tread function
                if i >= len(points): break
                if PAUSE:
                    MOVING = threading.Thread(target=move_to_XYZ, args = (points[i][0],
                                                      points[i][1],
                                                      points[i][2] - 5,
                                                      Mx,My,Mz,chg_vel))
                    MOVING.start()
                elif STOP:
                    pass
                else:
                    #print("Going to :", points[i][0],points[i][1],points[i][2])
                    MOVING = threading.Thread(target=move_to_XYZ, args = (points[i][0],
                                                                          points[i][1],
                                                                          points[i][2],
                                                                          Mx,My,Mz,chg_vel))
                    MOVING.start()
                    i+=1
                #print('started thread ', i)

        print("Finished at: ",points[i-1][0],points[i-1][1],points[i-1][2])
    except:
        print('movement error')






