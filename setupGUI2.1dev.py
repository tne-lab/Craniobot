import pygame
from RESOURCES.GUI_elements_by_flav import *
from RESOURCES.Calculate_Plane_and_plot import *
from RobotCommands import *
import thorlabs_apt as apt
import thorlabs_apt.core as core
import threading
from drill_craniotomy2 import *
from drill_holes2 import *
import queue

red         = (255,0,0)
green       = (0,255,0)
blue        = (0,0,255)
gray        = (150,150,150)
darkgray    = (50,50,50)
lightgray   = (200,200,200)
black       = (0,0,0)
white       = (255,255,255)
yellow      = (255,255,0)
pink        = (255, 192, 203)
pink1= (255, 181, 197, 255),
pink2= (238, 169, 184, 255),
pink3= (205, 145, 158, 255),
pink4= (139, 99, 108, 255),


lightpurple  = (160,12,75)
darkpurple  = (51,5,25)

roboXs = []
roboYs = []
roboZs = []

ScrXYZ = (0,0,0) # in pixels

BREGMAscrn = [213,466,580] # in pixels (BREGMA)
BREGMArobo = [10.0, 10.0, 15.0] # in ROBOT Coordinates (BREGMA) mm
BREGMArat = [0.0, 0.0, 0.0] # in ROBOT Coordinates (BREGMA) mm
graphic_scaleXY = 7.3333   #66 pix for 9mm dist from bregma to lambda = 7.333 pix/mm
graphic_scaleZ = 5.0
Robo000scrn = [0,0,0]

Robo000scrn[0] = BREGMAscrn[0]  + BREGMArobo[0] * graphic_scaleXY
Robo000scrn[1] = BREGMAscrn[1]  - BREGMArobo[1] * graphic_scaleXY
Robo000scrn[2] = BREGMAscrn[2]  - BREGMArobo[2] * graphic_scaleZ  

###########################################################################################################
# screw holes
hole_idx = 0
screw_holes_rat = [(-2.67, -5.625), (2.67,-5.625), (5, 7.68), (2.65, 9), (-2.65, 9), (-5, 7.68), (-1,11) ]
#screw_holes_rat = [(-5.625,-2.67), (-5.625,2.67), (7.68,5), (9,2.65), (9,-2.65), (7.68,-5), (11,-1) ]
## In rat coordinates.  NOTE:!!!! x and y are reversed from CAD drawings ???? changed???
##screw_holes_rat = [(-2.67, -5.625),
##                    (2.67,-5.625),
##                    (5, 7.68),
##                    (2.65, 9),
##                    (-2.65, 9),
##                    (-5, 7.68),
##                    (-1,11) ]
###########################################################################################################




drill_vel = 2.0
#######################################
def CranioBot_GUI_ELEMENTS(myscreen):
    global drill_vel, screw_holes_rat, hole_idx
    # BOXES
    boxes = []
    #def __init__(self, surface, x, y, w, h, fill_color, line_color=black):

    # BUTTONS
    buttons = []
    #(self, surface, index, x, y, w, h,
    #                text,fsize = 18,
    #                face_color = (150,150,150),
    #                text_color = (0,0,0)):
    buttons.append(MyButton(myscreen,0, 470,20, 100,35,"HOME ROBOT",14))
    buttons.append(MyButton(myscreen,0, 470,60, 100,35,"TO BREGMA",14))
    buttons.append(MyButton(myscreen,1, 350,160, 100,35,"SELECT POINT",14))
    buttons.append(MyButton(myscreen,11, 350,200, 100,35,"CLR POINT",14))
    buttons.append(MyButton(myscreen,30, 350,240, 100,35,"BEST FIT PLANE",14))
    
    buttons.append(MyButton(myscreen,2, 480,520, 20,18,"0.1",12))          # Y - Up
    buttons.append(MyButton(myscreen,12, 480,500, 20,18,"1",12))          # Y - Up
    buttons.append(MyButton(myscreen,22, 480,480, 20,18,"5",12))          # Y - Up
    
    buttons.append(MyButton(myscreen,3, 480,580, 20,18,"0.1",12))         # Y - DN
    buttons.append(MyButton(myscreen,13, 480,600, 20,18,"1",12))
    buttons.append(MyButton(myscreen,23, 480,620, 20,18,"5",12))

    buttons.append(MyButton(myscreen,4, 450,550, 20,20,"0.1",12))         # X - L
    buttons.append(MyButton(myscreen,14, 430,550, 20,20,"1",12))         # X - L
    buttons.append(MyButton(myscreen,24, 410,550, 20,20,"5",12))         # X - L
    
    buttons.append(MyButton(myscreen,5, 510,550, 20,20,"0.1",12))         # X - R
    buttons.append(MyButton(myscreen,15, 530,550, 20,20,"1",12))         # X - L
    buttons.append(MyButton(myscreen,25, 550,550, 20,20,"5",12))         # X - L

    buttons.append(MyButton(myscreen,6, 600,520, 20,18,"0.1",12))         # Z - up
    buttons.append(MyButton(myscreen,16, 600,500, 20,18,"1",12))         # Z - up
    buttons.append(MyButton(myscreen,26, 600,480, 20,18,"5",12))         # Z - up
    
    buttons.append(MyButton(myscreen,7, 600,580, 20,18,"0.1",12))         # Z - Dn
    buttons.append(MyButton(myscreen,17, 600,600, 20,18,"1",12))         # Z - Dn
    buttons.append(MyButton(myscreen,27, 600,620, 20,18,"5",12))         # Z - Dn
    buttons.append(MyButton(myscreen,8, 100,640, 100,60,"Next Hole",22))
    buttons.append(MyButton(myscreen,9, 230,640, 100,60,"Craniotomy",22))
    #buttons.append(MyButton(myscreen,10,280,720, 100,100,"DRILL",16))
    
    buttons.append(MyButton(myscreen,11, 540,660, 140,60,"PAUSE",22))
    buttons.append(MyButton(myscreen,11, 20,730, 660,60,"STOP NOW!!",26,(255,0,0)))

    buttons.append(MyButton(myscreen,11, 485,670, 20,20,"+",22))
    buttons.append(MyButton(myscreen,11, 485,690, 20,20,"-",26))    
    # CIRCLES (IF ANY)
    circles = []
    
    # LEDS (LIGHTS AND NOSE POKES)
    LEDs = []
    #LEDs.append(MyLED(myscreen,0, 15,15,  30,"OFF", red, darkgray)) # L LIGHTS

    # LABELS
    labels = []
    # def __init__(surface,x, y, label_name,label_pos, text ,fsize = 12):
    labels.append(MyLabel(myscreen,20,20,   "1.) Align Robot to Stereotaxic equipment. Then press 'HOME ROBOT'",16))
    labels.append(MyLabel(myscreen,20,40,   "2.) Use + | buttons below to move ",16))
    labels.append(MyLabel(myscreen,20,60,   "      Robot to BREGMA.  Then press 'SELECT POINT'",16))
    labels.append(MyLabel(myscreen,20,80,   "3.) Now use GUI to move Robot to set at least 4 more",16))
    labels.append(MyLabel(myscreen,20,100,  "     points on skull. Press 'SELECT POINT'",16))
    labels.append(MyLabel(myscreen,20,280,  "4.) Select best-fit plane through 5 points.",16))
    labels.append(MyLabel(myscreen,100,140, "           Robo                      Rat",16))
    labels.append(MyLabel(myscreen,370,645, "    Craniotomy",16))
    labels.append(MyLabel(myscreen,80,710, "Modify using UP \ DN keys                        Button or Space Bar",14))

    # INFO BOXES
    info_boxes = []
    #def __init__(self, surface,x, y, w, h, label,label_pos, text ,fsize = 14,surface_color = (255,255,255),BLINKING = False):

    # ROBO COORDS
    # Point 1
    info_boxes.append(InfoBox( myscreen,100,160,120,20,"Bregma",'LEFT','0, 0, 0'))
    # Point 2
    info_boxes.append(InfoBox( myscreen,100,180,120,20,"Other",'LEFT','0, 0, 0'))
    # Point 3
    info_boxes.append(InfoBox( myscreen,100,200,120,20,"Other",'LEFT','0, 0, 0'))
    # Point 4
    info_boxes.append(InfoBox( myscreen,100,220,120,20,"Other",'LEFT','0, 0, 0'))
    # Point 5
    info_boxes.append(InfoBox( myscreen,100,240,120,20,"Other",'LEFT','0, 0, 0'))

    #RAT COORD
    # Point 1
    info_boxes.append(InfoBox( myscreen,220,160,120,20,"",'LEFT','0, 0, 0'))
    # Point 2
    info_boxes.append(InfoBox( myscreen,220,180,120,20,"",'LEFT','0, 0, 0'))
    # Point 3
    info_boxes.append(InfoBox( myscreen,220,200,120,20,"",'LEFT','0, 0, 0'))
    # Point 4
    info_boxes.append(InfoBox( myscreen,220,220,120,20,"",'LEFT','0, 0, 0'))
    # Point 5
    info_boxes.append(InfoBox( myscreen,220,240,120,20,"",'LEFT','0, 0, 0'))

    # USER INPUT BOXES
    user_inputs = []
    #def __init__(self, surface,x, y, w, h, label_name,label_pos, text ,fsize = 12):
    

    user_inputs.append(get_user_input( myscreen,373,300,50,17,"5.) Enter crainiotomy center X offset from Bregma (mm) ",'LEFT','0'))
    user_inputs.append(get_user_input( myscreen,373,320,50,17,"6.) Enter crainiotomy center Y offset from Bregma (mm) ",'LEFT','-1.7'))
    user_inputs.append(get_user_input( myscreen,373,340,50,17,"7.) Enter radius(remember to subtract drill diam)(mm) ",'LEFT','5.0'))

    user_inputs.append(get_user_input(myscreen,450,370,50,17,"Scrn X",'TOP','435'))
    user_inputs.append(get_user_input(myscreen,530,370,50,17,"Scrn Y",'TOP','360'))
    user_inputs.append(get_user_input(myscreen,610,370,50,17,"Scrn Z",'TOP','360'))
    
    user_inputs.append(get_user_input(myscreen,450,410,50,17,"Drill X",'TOP','10'))
    user_inputs.append(get_user_input(myscreen,530,410,50,17,"Drill Y",'TOP','10'))
    user_inputs.append(get_user_input(myscreen,610,410,50,17,"Drill Z",'TOP','10'))

    user_inputs.append(get_user_input(myscreen,450,450,50,17,"Rat X",'TOP','10'))
    user_inputs.append(get_user_input(myscreen,530,450,50,17,"Rat Y",'TOP','10'))
    user_inputs.append(get_user_input(myscreen,610,450,50,17,"Rat Z",'TOP','10'))

    user_inputs.append(get_user_input(myscreen,360,680,50,17,"Depth (mm)",'TOP','0.0'))
    user_inputs.append(get_user_input(myscreen,430,680,50,17,"Vel",'TOP',str(drill_vel)))

    user_inputs.append(get_user_input(myscreen,20,640,50,17,"Hole #",'TOP',str(hole_idx)))
    user_inputs.append(get_user_input(myscreen,20,680,50,17," of ",'TOP',str(len(screw_holes_rat))))
    # NOTE:  Spaces are required otherwise this will also be put into info box labeled "offset.."
    
    # TOGGLES
    toggles = []


    return buttons, boxes, LEDs, toggles, info_boxes, user_inputs, labels


class MyDrill:
    """
    MyDrill class
    button_state = "UP" or "DN"
    """
    global BREGMAscrn
    def __init__(self, surface, x, y):
        self.myscreen = surface
        self.rect = pygame.Rect(x-10,y-10,20,20)
        self.x = x
        self.y = y
        self.z = 10
        self.color = (255,0,0)
        
    def draw_drillXY(self, x, y):
        myscreen = self.myscreen
        col = self.color
        pygame.draw.circle(myscreen,col,(x, y),10,2)# Circle
        pygame.draw.circle(myscreen,col,(x, y),3,0) # Filled Circle
        pygame.draw.line(myscreen,col,(x-20, y),(x+20, y) ,2)
        pygame.draw.line(myscreen,col,(x, y-20),(x, y+20) ,2)
        self.rect = pygame.Rect(x-10,y-10,20,20)
        
    def draw_drillZ(self, x, y):
        #line(surface, color, start_pos, end_pos, width) -> Rect
        myscreen = self.myscreen
        col = self.color
        #black = (0,0,0)
        pygame.draw.line(myscreen,col,(x-20, y),(x+20, y) ,2) # ____
        pygame.draw.line(myscreen,col,(x-5, y-10),(x, y) ,2)  #  \
        pygame.draw.line(myscreen,col,(x+5, y-10),(x, y) ,2)  #   /

        # SKULL SURFACE
        pygame.draw.line(myscreen,black,(630, BREGMAscrn[2]+2),(690, BREGMAscrn[2]+2) ,5) # SKULL TOP

def draw_craniotomy(myscreen,user_inputs): # User inputs are offset from bregma and Raduis in mm
    global graphic_scaleXY,BREGMAscrn

    x = BREGMAscrn[0]
    z = BREGMAscrn[2]

    for usr_input in user_inputs:
        if "X offset" in usr_input.label:
            #x = int(BregmaScrn[0] - float(usr_input.text)*graphic_scaleXY )
            x = int(x - float(usr_input.text)*graphic_scaleXY )
        if "Y offset" in usr_input.label:
            y = int(BREGMAscrn[1] - float(usr_input.text)*graphic_scaleXY )
        if "radius" in usr_input.label:
            r = float(usr_input.text)*graphic_scaleXY #pix/mm
    radius = int(r)
    pygame.draw.circle(myscreen,(0,0,255),(x, y),radius,1)

def draw_screw_holes(myscreen):
    global screw_holes_rat, BREGMArobo, BREGMAscrn,graphic_scaleXY
    for hole in screw_holes_rat:
        location_robo = (int(hole[0]+ BREGMArobo[0]),
                         int(hole[1] + BREGMArobo[1]))# in Robot coords
        location_scrn = (int(hole[0]*graphic_scaleXY + BREGMAscrn[0]),
                         int(hole[1] *graphic_scaleXY + BREGMAscrn[1]))
        pygame.draw.circle(myscreen,(0,255,0),location_scrn,2,0)

def draw_screw_hole(myscreen, hole, color):
    global BREGMArobo, BREGMAscrn,graphic_scaleXY

##    location_robo = (int(hole[0]+ BREGMArobo[0]),
##                     int(hole[1] + BREGMArobo[1]))# in Robot coords
    location_scrn = (int(BREGMAscrn[0] - hole[0]*graphic_scaleXY ),
                     int(BREGMAscrn[1] + hole[1] *graphic_scaleXY))
    pygame.draw.circle(myscreen,color,location_scrn,2,0)
   
#################################
#  MAIN PROGRAM
     
def setupGUI():
    # FLAGS
    BOX_SELECTED = False
    LEFT_MOUSE_DOWN = False
    RIGHT_MOUSE_DOWN = False
    BUTTON_SELECTED = False
    MOVING_DRILL =  False
    ROBOT_HOMED = False
    ROBOT_CONNECTED = False
    BREGMA_SELECTED = False
    DRILLING_HOLE = False
    SETTING_UP = True
    UP_KEY = False
    DN_KEY = False
    MOVED_UP = False
    MOVED_DN = False
    MOVED_XY = False
    MOVING_UP = None
    MOVING_XY = None
    MOVING_DN = None
    MOVING = None
    circle = None
    queStep = queue.Queue()
    step_msg = None
    queHoles = queue.Queue()
    queCran = queue.Queue()
    depth = 0.0
    moveThreadX = None
    moveThreadY = None
    moveThreadZ = None
    # GLOBALS
    global BREGMAscrn, BREGMArobo, graphic_scaleXY, graphic_scaleZ,screw_holes_rat, drill_vel
    global Robo000scrn, skull_Zsurface_scrn,hole_idx

    
    pygame.init()
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (10,30) # Place window on computer screen
    UMNlogo = pygame.image.load(r'.\RESOURCES\UMNlogo.PNG')
    pygame.display.set_icon(UMNlogo)
    TNElogo = pygame.image.load(r'.\RESOURCES\TNE logo.jpg')
    TNElogo = pygame.transform.scale(TNElogo, (70, 50))
    skull_graphic = pygame.image.load(r'.\RESOURCES\skull_graphicB.png')

    pygame.display.set_caption('Craniotomy Robot 2.1 under dev by F. da Silva & Mark Schatza Nov. 20, 2019') # Enter your window caption here

    screw_holes_robo = []

    # At BREGMA IF NO ROBOT IS CONNECTED
    DRILLscrn = [213, 486, 549]  # BREGMA
    DRILLrat =  [0.0, 0.0, 0.0]  #
    DRILLrobo =  [10.0, 10.0, 15.0] # ROBOT 000
    
    ########################
    # Prepare Screen
    #########################
    myscreen = pygame.display.set_mode((700,900),pygame.RESIZABLE,32)
    myscreen.fill(pink1)

    
    #########################
    #  Create GUI elements
    #########################
    buttons,boxes,LEDs,toggles,info_boxes,user_inputs,labels = CranioBot_GUI_ELEMENTS( myscreen )
    drill = MyDrill(myscreen,215, 473)
    drill_static_graphic = MyDrill(myscreen,510, 540)
    # WARNING MSGS
    warning = WARNINGBox( myscreen,480,150,160,160,"",'LEFT','WARNING!!',22)
    clk_time_start = time.perf_counter()
    START_TIME = time.perf_counter()
    cur_time =  time.perf_counter()

    START_EXPT = False
    PAUSE_STARTED = False

    # FLAGS
    SETTING_UP = True
    RUNNING = False

    SKULL_SURFACE = False
    BRAIN_SURFACE = False
    ###############################
    # Connect to motors
    Mx,My,Mz = connect_to_3motors()
    print("Mx,My,Mz: ",Mx,My,Mz)
    if Mx is not None and My is not None and Mz is not None:
            Mx.disable()
            My.disable()
            Mz.disable()
            time.sleep (0.1) #in sec
            Mx.enable()
            My.enable()
            Mz.enable()
            time.sleep (0.1) #in sec
            DRILLrobo = [Mx.position, My.position, Mz.position]
            ROBOT_CONNECTED = True ## REMOVE ME IF USING OTHER COMP
    #############################
    #  MAIN LOOP
    #############################

    while SETTING_UP:
        '''
         SYSTEM EVENTS
        '''

        for button in buttons: # Check for collision with EXISTING buttons
            if ( button.index == 2 or button.index == 12 or
                button.index == 22 or button.index == 3 or
                button.index == 13 or button.index == 23 ):
                if moveThreadY is not None and moveThreadY.is_alive():
                    button.face_color = lightgray
                else:
                    button.face_color = gray
            elif ( button.index == 4 or button.index == 14 or
                 button.index == 24 or button.index == 5 or
                 button.index == 15 or button.index == 25 ):
                 if moveThreadX is not None and moveThreadX.is_alive():
                     button.face_color = lightgray
                 else:
                     button.face_color = gray
            elif ( button.index == 6 or button.index == 16 or
                 button.index == 26 or button.index == 7 or
                 button.index == 17 or button.index == 27 ):
                     if moveThreadZ is not None and moveThreadZ.is_alive():
                         button.face_color = lightgray
                     else:
                         button.face_color = gray            
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game()

            ################################
            ############################################################################
            #  HANDLE GUI EVENTS
            ###########################################################################################################

            # STOP ON SPACE PRESS
            elif (event.type == pygame.KEYDOWN):
                if event.key == pygame.K_SPACE:
                    for button in buttons:
                        if button.text == "STOP":
                            button.UP_DN = "DN"
                            if Mx is not None and My is not None and Mz is not None:
                                Mx.disable()
                                My.disable()
                                Mz.disable()
                                queHoles.put('STOP')
                                queCran.put('STOP')
                            button.text = 'GO'
                            button.face_color = (0,255,0)
                        elif button.text == 'GO':
                            button.UP_DN = "DN"
                            if Mx is not None and My is not None and Mz is not None:
                                Mx.enable()
                                My.enable()
                                Mz.enable()
                                queHoles.put('GO')
                                queCran.put('GO')
                            button.text = 'STOP'
                            button.face_color = (255,0,0)
                            
                # ARROW KEYS TO GO UP/DN WHEN DRILLING HOLES
                elif event.key == pygame.K_DOWN:
                   if moveThreadZ is None or not moveThreadZ.is_alive():
                      if DRILLING_HOLE: # CHANGE ME for new coord system
                          moveThreadZ = threading.Thread(target =  move_step, args =(0.1,Mz))
                          moveThreadZ.start()
               
                elif event.key == pygame.K_UP:
                   if moveThreadZ is None or not moveThreadZ.is_alive():
                      if DRILLING_HOLE: # CHANGE ME for new coord system
                          moveThreadZ = threading.Thread(target =  move_step, args =(-0.1,Mz))
                          moveThreadZ.start()       
            #-----------------------------------------
            # MOUSE MOVE
            elif (event.type == pygame.MOUSEMOTION):#
                cur_x,cur_y = pygame.mouse.get_pos()

                if MOVING_DRILL:
                    
                    DRILLscrn[0] = cur_x #
                    DRILLscrn[1] = cur_y #
                    #print("DRILLscrn",DRILLscrn[0],DRILLscrn[1],"BREGMAscrn: ",BREGMAscrn[0],BREGMAscrn[1])
                    DRILLrobo[0] = -(DRILLscrn[0] - Robo000scrn[0])/graphic_scaleXY
                    DRILLrobo[1] = (DRILLscrn[1] - Robo000scrn[1])/graphic_scaleXY
                    DRILLrobo[2] = (DRILLscrn[2] - Robo000scrn[2])/graphic_scaleZ
                    if DRILLrobo[0] < 0.0 or DRILLrobo[0] > 25.0:
                        print("1.ROBO X OUT OF BOUNDS!!!!!")
                    if DRILLrobo[1] < 0.0 or DRILLrobo[1] > 25.0:
                        print("1.ROBO Y OUT OF BOUNDS!!!!!")
                    if DRILLrobo[2] < 0.0 or DRILLrobo[2] > 25.0:
                        print("1.ROBO Z OUT OF BOUNDS!!!!!")
                    DRILLrat[0] = DRILLrobo[0] - BREGMArobo[0]
                    DRILLrat[1] = DRILLrobo[1] - BREGMArobo[1]
                    DRILLrat[2] = DRILLrobo[2] - BREGMArobo[2]



                        
            # MOUSE DOWN
            elif (event.type == pygame.MOUSEBUTTONDOWN ):#Mouse Clicked
                #print("MOUSE CLICKED")
                LEFT_MOUSE_DOWN = False
                RIGHT_MOUSE_DOWN = False
                
                cur_x,cur_y = pygame.mouse.get_pos()
                print("cur_x: ",cur_x,"cur_y: ",cur_y)
                if event.button == 1:
                    LEFT_MOUSE_DOWN = True
                elif event.button == 3:
                    RIGHT_MOUSE_DOWN = True

                elif event.button == 4:  #Wheel roll UP
                    MOUSE_WHEEL_SCROLL_UP = True
                    
                elif event.button == 5: #Wheel roll Down
                    MOUSE_WHEEL_SCROLL_DN = True

                stepSize = 1 # Change with buttons
                # BUTTONS
                if LEFT_MOUSE_DOWN:

                    # BUTTONS
                    for button in buttons: # Check for collision with EXISTING buttons
                        if button.rect.collidepoint(cur_x,cur_y):
                               #########
                               # DRILL Y
                               if button.index == 2 or button.index == 12 or button.index == 22: # y"^" Move drill to UP (+y)
                                   if button.index == 2: stepSize = 0.1
                                   elif button.index == 12: stepSize = 1
                                   elif button.index == 22: stepSize = 5
                                   

                                   if moveThreadY is None or not moveThreadY.is_alive():
                                      button.UP_DN = "DN" 
                                      if DRILLrobo[1] - stepSize < 0.0:
                                            DRILLrobo[1] = 0.0
                                            print("1.ROBO Y OUT OF BOUNDS IF MOVED!!!!!")
                                      else: DRILLrobo[1] -= stepSize # mm
                                      if BREGMA_SELECTED: # CHANGE ME for new coord system
                                            DRILLscrn[1] = DRILLrobo[1]*graphic_scaleXY + Robo000scrn[1]# pixels
                                            DRILLrat[1] = DRILLrobo[1] - BREGMArobo[1]# mm

                                      moveThreadY = threading.Thread(target =  move_step, args =(-1.0 * stepSize,My))
                                      moveThreadY.start()
                                    
                                    
                               if button.index == 3 or button.index == 13 or button.index == 23: # y"v" Move drill to UP (-y)
                                   if button.index == 3: stepSize = 0.1
                                   elif button.index == 13: stepSize = 1
                                   elif button.index == 23: stepSize = 5
                                                                      
                                   if moveThreadY is None or not moveThreadY.is_alive():
                                      button.UP_DN = "DN" 
                                      if DRILLrobo[1] + stepSize > 25.0:
                                            DRILLrobo[1] = 25.0
                                            print("2.ROBO Y OUT OF BOUNDS IF MOVED!!!!!")

                                      else: DRILLrobo[1] += stepSize # mm
                                      if BREGMA_SELECTED: # CHANGE ME for new coord system
                                            DRILLscrn[1] = DRILLrobo[1]*graphic_scaleXY + Robo000scrn[1]# pixels
                                            DRILLrat[1] = DRILLrobo[1] - BREGMArobo[1]# mm

                                      moveThreadY = threading.Thread(target =  move_step, args =(stepSize,My))
                                      moveThreadY.start()

                               #########     
                               # DRILL X     
                               elif button.index == 4 or button.index == 14 or button.index == 24: #x"<" Move drill to left (+x in robo, -x in scrn)
                                   if button.index == 4: stepSize = 0.1
                                   elif button.index == 14: stepSize = 1
                                   elif button.index == 24: stepSize = 5
                                   
                                   
                                   if moveThreadX is None or not moveThreadX.is_alive():
                                      button.UP_DN = "DN"
                                      if DRILLrobo[0] + stepSize > 25.0:
                                            DRILLrobo[0] = 25.0
                                            print("3.ROBO X OUT OF BOUNDS IF MOVED!!!!!")

                                      else: DRILLrobo[0] += stepSize # mm

                                      if BREGMA_SELECTED: # CHANGE ME for new coord system
                                            DRILLscrn[0] = -DRILLrobo[0]*graphic_scaleXY + Robo000scrn[0]# pixels
                                            DRILLrat[0] = DRILLrobo[0] - BREGMArobo[0]# mm

                                      moveThreadX = threading.Thread(target =  move_step, args =(stepSize,Mx))
                                      moveThreadX.start()
                                   
                                        
                               elif button.index == 5 or button.index == 15 or button.index == 25: #x">" Move drill to right (-x in robo)
                                   if button.index == 5: stepSize = 0.1
                                   elif button.index == 15: stepSize = 1
                                   elif button.index == 25: stepSize = 5
                                                                     
                                   if moveThreadX is None or not moveThreadX.is_alive():
                                      button.UP_DN = "DN" 
                                      if DRILLrobo[0] - stepSize < 0.0:
                                            DRILLrobo[0] = 0.0
                                            print("4.ROBO X OUT OF BOUNDS IF MOVED!!!!!")
                                      else: DRILLrobo[0] -= stepSize # mm
                                      if BREGMA_SELECTED: # CHANGE ME for new coord system
                                            DRILLscrn[0] = -DRILLrobo[0]*graphic_scaleXY + Robo000scrn[0]# pixels
                                            DRILLrat[0] = DRILLrobo[0] - BREGMArobo[0]# mm


                                      moveThreadX = threading.Thread(target =  move_step, args =(-1.0 * stepSize,Mx))
                                      moveThreadX.start()
                                   
                               #########       
                               # DRILL Z
                               elif button.index == 6 or button.index == 16 or button.index == 26: #z"^" Move drill to UP -z robo -y screen)
                                   if button.index == 6: stepSize = 0.1
                                   elif button.index == 16: stepSize = 1
                                   elif button.index == 26: stepSize = 5

                                   if moveThreadZ is None or not moveThreadZ.is_alive():
                                      button.UP_DN = "DN"
                                      if DRILLrobo[2] - stepSize < 0.0:
                                            DRILLrobo[2] = 0.0
                                            print("5.ROBO Z OUT OF BOUNDS IF MOVED!!!!!")
                                      else: DRILLrobo[2] -= stepSize # mm
                                      if BREGMA_SELECTED: # CHANGE ME for new coord system
                                            DRILLscrn[2] = DRILLrobo[2]*graphic_scaleZ + Robo000scrn[2]# pixels
                                            DRILLrat[2] = DRILLrobo[2] - BREGMArobo[2]# mm

                                      moveThreadZ = threading.Thread(target =  move_step, args =(-1.0 * stepSize,Mz))
                                      moveThreadZ.start()
                                                                        
                               elif button.index == 7 or button.index == 17 or button.index == 27: #z"v" Move drill to DN (+z robo, +y screen)
                                   if button.index == 7: stepSize = 0.1
                                   elif button.index == 17: stepSize = 1
                                   elif button.index == 27: stepSize = 5
                                   
                                   if moveThreadZ is None or not moveThreadZ.is_alive():
                                      button.UP_DN = "DN"

                                      if BREGMA_SELECTED: # CHANGE ME for new coord system
                                            if DRILLrobo[2] + stepSize > 25.0:
                                                DRILLrobo[2] = 25.0
                                                print("2.ROBO Z OUT OF BOUNDS IF MOVED!!!!!")
                                            else: DRILLrobo[2] += stepSize # mm
                                            # Only allow small steps if at brain surface
                                            if DRILLrobo[2] - BREGMArobo[2] >=1.2 and not (BRAIN_SURFACE == True and stepSize == 0.1):
                                                BRAIN_SURFACE = True
                                                DRILLrobo[2] -= stepSize
                                            else:
                                                BRAIN_SURFACE = False
                                                DRILLscrn[2] = DRILLrobo[2]*graphic_scaleZ + Robo000scrn[2]# pixels
                                                DRILLrat[2] = DRILLrobo[2] - BREGMArobo[2]# mm
                                                if DRILLrat[2] >=0:
                                                    SKULL_SURFACE = True
                                                else: SKULL_SURFACE = False
                                                moveThreadZ = threading.Thread(target =  move_step, args =(stepSize,Mz))
                                                moveThreadZ.start()


                                      else:
                                          moveThreadZ = threading.Thread(target =  move_step, args =(stepSize,Mz))
                                          moveThreadZ.start()
                                          if DRILLrobo[2] + stepSize > 25.0:
                                              DRILLrobo[2] = 25.0
                                              print("2.ROBO Z OUT OF BOUNDS IF MOVED!!!!!")
                                          else: DRILLrobo[2] += stepSize # mm

                               ##################
                               # HOME ROBOT HERE
                               elif "HOME ROBOT" in button.text :  # This is Robot 000 in screen coordinates
                                    button.UP_DN = "DN"
                                    
##                                    BREGMAscrn = [213,486,600] # in pixels (BREGMA)
##                                    BREGMArobo = [10.0, 10.0, 15.0] # in ROBOT Coordinates (BREGMA) mm
##                                    BREGMArat = [0.0, 0.0, 0.0] # in ROBOT Coordinates (BREGMA) mm
##                                    Robo000scrn = [0,0,0]
                                    
                                    for box in info_boxes: # Clear info boxes
                                        box.text = "0, 0, 0"
                                        
                                    

                                    if Mx is not None and My is not None and Mz is not None:
                                        ROBOT_CONNECTED = True
                                        home_all(Mx,My,Mz)
                                        x = Mx.position
                                        y = My.position
                                        z = Mz.position
                                        print("Cur Motor positions: ",x,y,z)
                                        print("ROBOT HOMED")
                                        DRILLrobo = [x, y, z]
                                    else:
                                        ROBOT_CONNECTED = False
                                        print("3.ROBOT NOT CONNECTED")

                                    if ROBOT_CONNECTED:    
                                        DRILLrobo[0] = 0.0# IN ROBOT COORDINATES    
                                        DRILLrobo[1] = 0.0# IN ROBOT COORDINATES    
                                        DRILLrobo[2] = 0.0# IN ROBOT COORDINATES
                                    
                                        DRILLrat[0] = -10# IN RAT COORDINATES    
                                        DRILLrat[1] = 10# IN RAT COORDINATES    
                                        DRILLrat[2] = 15.0# IN RAT COORDINATES                                        
                                    else:
                                        DRILLrobo[0] = 0.0#BREGMAscrn[0]+12.5*graphic_scaleXY# IN ROBOT COORDINATES    
                                        DRILLrobo[1] = 0.0#BREGMAscrn[1]-12.5*graphic_scaleXY# IN ROBOT COORDINATES    
                                        DRILLrobo[2] = 0.0#BREGMAscrn[2]-25.0*graphic_scaleZ # IN ROBOT COORDINATES
                                        
                                        
                                    #DRILLscrn = [215, 473, 549]
                                    DRILLscrn = [Robo000scrn[0],Robo000scrn[1],Robo000scrn[2]]

                                    ROBOT_HOMED = True

                               ####################################    
                               # BACK TO BREGMA
                               elif "TO BREGMA" in button.text :  #
                                    if BREGMA_SELECTED: 
                                        button.UP_DN = "DN"

                                        try:
                                            if MOVING is None or not MOVING.is_alive(): #is_alive is a Tread function
                                                print("MOVING TO BREGMA: ", BREGMArobo[0],BREGMArobo[1],BREGMArobo[2])
                                                MOVING = threading.Thread(target=move_to_XYZ, args = (BREGMArobo[0],
                                                                                                      BREGMArobo[1],
                                                                                                      BREGMArobo[2]-5,
                                                                                                      Mx,My,Mz,""))
                                                MOVING.start()
                                        except:
                                            print('cleanup')
                                            print('movement error')

                                        MOVING = None
                                    else: print("BREGMA NOT SELECTED YET")


                               ####################################     
                               # SELECT BEST-FIT PLANE POINTS
                               elif "SELECT POINT" in button.text:
                                    button.UP_DN = "DN"
                                    n = len(roboXs)+1

                                    ##########################
                                    # POINT 1: BREGMA
                                    if n == 1: # Bregma in screen coord
                                        DRILLrat = [0.0, 0.0, 0.0] # in RAT COORDINATES 

                                        # LOCATION OF ROBOT 000 on SCREEN
                                        if ROBOT_CONNECTED: #
                                            BREGMArobo[0] = Mx.position
                                            BREGMArobo[1] = My.position
                                            BREGMArobo[2] = Mz.position
                                            BREGMArobo = DRILLrobo.copy()
                                            Robo000scrn[0] = BREGMAscrn[0]+BREGMArobo[0]*graphic_scaleXY # ROBOT x00 on screen    
                                            Robo000scrn[1] = BREGMAscrn[1]-BREGMArobo[1]*graphic_scaleXY # ROBOT 0y0 on screen   
                                            Robo000scrn[2] = BREGMAscrn[2]-BREGMArobo[2]*graphic_scaleZ  # ROBOT 00z on screen   

                                        else:
                                            print("ROBOT NOT CONNECTED")
                                            #BREGMArobo = [213,486,10]
                                            BREGMArobo[0] = -(BREGMAscrn[0] - Robo000scrn[0])/graphic_scaleXY
                                            BREGMArobo[1] = (BREGMAscrn[1] - Robo000scrn[1])/graphic_scaleXY
                                            BREGMArobo[2] = (BREGMAscrn[2] - Robo000scrn[2])/graphic_scaleZ
                                            if BREGMArobo[0] <= 0.0 or BREGMArobo[0] >= 25.0:
                                                print("5.ROBO X OUT OF BOUNDS!!!!!")
                                            if BREGMArobo[1] <= 0.0 or BREGMArobo[1] >= 25.0:
                                                print("5.ROBO Y OUT OF BOUNDS!!!!!")
                                            if BREGMArobo[2] <= 0.0 or BREGMArobo[2] >= 25.0:
                                                print("5.ROBO Z OUT OF BOUNDS!!!!!")
                                                
                                        #DRILLscrn = BREGMAscrn !!!!! Why doesn't this work????
                                        DRILLscrn = BREGMAscrn.copy()

                                        print("BREGMA: DRILLscrn",DRILLscrn[0],DRILLscrn[1],\
                                              "BREGMAscrn: ",BREGMAscrn[0],BREGMAscrn[1])
                                        info_boxes[0].text = str(round(BREGMArobo[0],2))+', ' + \
                                                             str(round(BREGMArobo[1],2)) +', '+ \
                                                             str(round(BREGMArobo[2],2))
                                             
                                        info_boxes[5].text = str(BREGMArat[0]) +', '+ \
                                                             str(BREGMArat[1]) +', '+ \
                                                             str(BREGMArat[2]) 
                                        BREGMA_SELECTED = True
                                    
                                    # ROBOT COORDINATES  
                                    if ROBOT_CONNECTED:
                                        DRILLrobo = [Mx.position, My.position, Mz.position]

                                    else: # For screen graphis when ROBOT is NOT connected
                                        DRILLrobo[0] = -(DRILLscrn[0] - Robo000scrn[0])/graphic_scaleXY #in mm (graphic_scaleXY in pix/mm)
                                        DRILLrobo[1] = (DRILLscrn[1] - Robo000scrn[1])/graphic_scaleXY
                                        DRILLrobo[2] = (DRILLscrn[2] - Robo000scrn[2])/graphic_scaleZ
                                        if DRILLrobo[0] <= 0.0 or DRILLrobo[0] >= 25.0:
                                            print("4.ROBO X OUT OF BOUNDS!!!!!")
                                        if DRILLrobo[1] <= 0.0 or DRILLrobo[1] >= 25.0:
                                            print("4.ROBO Y OUT OF BOUNDS!!!!!")
                                        if DRILLrobo[2] <= 0.0 or DRILLrobo[2] >= 25.0:
                                            print("4.ROBO Z OUT OF BOUNDS!!!!!")

                                    print("DrillRobo: ",DRILLrobo, "\nRobo000scrn: ",Robo000scrn)

                                    # RAT COORDINATES
                                    DRILLrat[0] = DRILLrobo[0] - BREGMArobo[0]
                                    DRILLrat[1] = DRILLrobo[1] - BREGMArobo[1]
                                    DRILLrat[2] = DRILLrobo[2] - BREGMArobo[2]                                                          

                                    # SCREEN COORDINATES
                                    DRILLscrn[0] = Robo000scrn[0] - DRILLrobo[0] * graphic_scaleXY
                                    #DRILLscrn[0] = (DRILLrobo[0] - BREGMArobo[0])*graphic_scaleXY + BREGMAscrn[0]  # IN SCREEN COORDINATES   
                                    DRILLscrn[1] = (DRILLrobo[1] - BREGMArobo[1])*graphic_scaleXY + BREGMAscrn[1]
                                    DRILLscrn[2] = (DRILLrobo[2] - BREGMArobo[2])*graphic_scaleZ  + BREGMAscrn[2]                                                       

                                    # POINT LOCATIONS    
                                    roboXs.append(DRILLrobo[0]) # For calculating best fit plane
                                    roboYs.append(DRILLrobo[1])
                                    roboZs.append(DRILLrobo[2])
                                    print("Point Xs: ",roboXs)
                                    print("Point Ys: ",roboYs)
                                    print("Point Zs: ",roboZs)

                                    
                                    # POINT 2
                                    if n == 2: # in screen coord
                                                 
                                        info_boxes[1].text = str(round(DRILLrobo[0],2)) +', ' + \
                                                             str(round(DRILLrobo[1],2)) +', ' + \
                                                             str(round(DRILLrobo[2],2))

                                        info_boxes[6].text = str(round(DRILLrat[0],2))  + ', '+\
                                                             str(round(DRILLrat[1],2))  + ', '+\
                                                             str(round(DRILLrat[2],2))                                        # POINT 3
                                    # POINT 3               
                                    if n == 3:
                                        info_boxes[2].text = str(round(DRILLrobo[0],2)) +', ' + \
                                                             str(round(DRILLrobo[1],2)) +', ' + \
                                                             str(round(DRILLrobo[2],2))
                                        info_boxes[7].text = str(round(DRILLrat[0],2))  + ', '+\
                                                             str(round(DRILLrat[1],2))  + ', '+\
                                                             str(round(DRILLrat[2],2)) 
                                    # POINT 4
                                    if n == 4:
                                        info_boxes[3].text = str(round(DRILLrobo[0],2)) +', ' + \
                                                             str(round(DRILLrobo[1],2)) +', ' + \
                                                             str(round(DRILLrobo[2],2))
                                        info_boxes[8].text = str(round(DRILLrat[0],2))  + ', '+\
                                                             str(round(DRILLrat[1],2))  + ', '+\
                                                             str(round(DRILLrat[2],2)) 
                                    # POINT 5
                                    if n == 5:
                                        info_boxes[4].text = str(round(DRILLrobo[0],2)) +', ' + \
                                                             str(round(DRILLrobo[1],2)) +', ' + \
                                                             str(round(DRILLrobo[2],2))
                                        info_boxes[9].text = str(round(DRILLrat[0],2))  + ', '+\
                                                             str(round(DRILLrat[1],2))  + ', '+\
                                                             str(round(DRILLrat[2],2))

                               ############################################ 
                               elif "CLR" in button.text:
                                    button.UP_DN = "DN"
                                    if len(roboXs) >0:
                                        roboXs.pop()
                                        roboYs.pop()
                                        roboZs.pop()
                                        n = len(roboXs)
                                        info_boxes[n].text = '(0, 0, 0)'
                                        info_boxes[n+5].text = '(0, 0, 0)'
                               ##########################################
                               ############################################
                               elif button.text == "Craniotomy":
                                    button.UP_DN = "DN"
                                    if circle is not None: # Thisis the projected circle onto the best fit plabe
                                        if ROBOT_CONNECTED:
                                            cranThread = threading.Thread(target = drill_carniotomy,
                                                                      args = (BREGMArobo,Mx,My,Mz,roboXs,roboYs,roboZs,
                                                                              circle, depth, queCran ))
                                            cranThread.start()
                                        else: 
                                            print('ROBOT IS NOT CONNECTED!')
                                        depth = depth+0.1
                                        
                                    else:
                                        print('Define Circle! Hint: press best fit plane')
                               ############################################    
                               elif button.text == "Next Hole":
                                    DRILLING_HOLE = True
                                    button.UP_DN = "DN"
                                    if BREGMA_SELECTED and ROBOT_CONNECTED: #convert to ROBO coordinates
##                                        holeX = round(screw_holes_rat[hole_idx][0] + BREGMArobo[0], 1)
##                                        holeY = round(screw_holes_rat[hole_idx][1] + BREGMArobo[1], 1)
                                        hole = (screw_holes_rat[hole_idx][0],screw_holes_rat[hole_idx][1])
##                                        move_to_hole = threading.Thread(target =  move_step, args =(stepSize,Mz))
##                                        move_to_hole.start()
                                       
                                        holesThread = threading.Thread(target = drill_holes, args = (hole,BREGMArobo,Mx,My,Mz, queHoles))
                                        holesThread.start()
                                        print("Drilling Hole ", hole_idx, " at: ",hole)
                                        hole_idx += 1
                                        queHoles.put('')
                                        if hole_idx >=len(screw_holes_rat):
                                            DRILLING_HOLE = False
                                            print (hole_idx, " holes drilled")
                                    else: print("Bregma MUST be selected first!!!")
                               ############################################         
                               elif button.text == "PAUSE":
                                    button.UP_DN = "DN"
                                    queHoles.put('PAUSE')
                                    queCran.put('PAUSE')
                                    button.text = 'RESUME'
                               elif button.text == 'RESUME':
                                    button.UP_DN = "DN"
                                    queHoles.put('RESUME')
                                    queCran.put('RESUME')
                                    button.text = 'PAUSE'
                               ############################################         
                               elif button.text == "STOP":
                                    button.UP_DN = "DN"
                                    if Mx is not None and My is not None and Mz is not None:
                                        Mx.disable()
                                        My.disable()
                                        Mz.disable()
                                        queHoles.put('STOP')
                                        queCran.put('STOP')
                                    button.text = 'GO'
                                    button.face_color = (0,255,0)
                                    
                               elif button.text == 'GO':
                                    button.UP_DN = "DN"
                                    if Mx is not None and My is not None and Mz is not None:
                                        Mx.enable()
                                        My.enable()
                                        Mz.enable()
                                        queHoles.put('GO')
                                        queCran.put('GO')
                                    button.text = 'STOP'
                                    button.face_color = (255,0,0)

                               ############################################# 
                               elif "BEST FIT" in button.text:
                                    button.UP_DN = "DN"
                                    for usr_input in user_inputs:
                                        if 'X offset' in usr_input.label:
                                            X_Offset = float(usr_input.text)
                                        if 'Y offset' in usr_input.label:
                                            Y_Offset = float(usr_input.text)
                                            
                                        if 'radius' in usr_input.label:
                                            Radius = float(usr_input.text)
                                    ##    # BEST FIT CIRCLE
                                    circle = best_fit_plot(roboXs,roboYs,roboZs,5.5,BREGMArobo,0,-1.7)
                                    ##    points = []

                               ############################################# 

                               elif "+" in button.text:
                                    button.UP_DN = "DN"
                                    queHoles.put('vel_up')
                                    queCran.put('vel_up')
                                    drill_vel += 0.25  # This is for diplay only!
                                                      # Not directly tied to drill vel in craniotomy
                                    if drill_vel >= 2.25: drill_vel = 2.25
                                    
                               elif "-" in button.text:
                                    button.UP_DN = "DN"
                                    queHoles.put('vel_dn')
                                    queCran.put('vel_dn')
                                    drill_vel -= 0.25
                                    if drill_vel <= 0.25: drill_vel = 0.25
                                    # This is for diplay only!
                                                      # Not directly tied to drill vel in craniotomy

                                    
                    ############################################# 

                    if drill.rect.collidepoint(cur_x,cur_y):
                        MOVING_DRILL = True
                        drill.color = (255,255,255)
                        print("moving drill: ",MOVING_DRILL)
                        
            elif (event.type == pygame.MOUSEBUTTONUP ):#Mouse UN-Clicked
                    for button in buttons: # Check for collision with EXISTING buttons
                        if button.rect.collidepoint(cur_x,cur_y):
                               button.UP_DN = "UP"
                    LEFT_MOUSE_DOWN = False
                    RIGHT_MOUSE_DOWN = False
                    MOVING_DRILL = False
                    drill.color = (255,0,0)
        ########################
        # REDRAW GUI ELEMENTS
        ########################
        myscreen.fill(pink4)
        myscreen.blit(TNElogo,(625,5))
        myscreen.blit(skull_graphic,(100,380))
        
        #########################
        #  Create GUI elements
        #########################
        for button in buttons:
            button.draw()

        for LED in LEDs:
            LED.draw()

        for lbl in labels: # Last go on top
            lbl.draw()

        for info in info_boxes: # Last go on top
            info.draw()

        # USER INPUTS
        for user_input in user_inputs:
            user_input.draw()

        # UPDATE DRILL INFO and GRAPHICS
        for user_input in user_inputs:
            if "Scrn X" in user_input.label: user_input.text = str(round(DRILLscrn[0],2))
            if "Scrn Y" in user_input.label: user_input.text = str(round(DRILLscrn[1],2))
             
            if "Drill X" in user_input.label: user_input.text = str(round(DRILLrobo[0],2))
            if "Drill Y" in user_input.label: user_input.text = str(round(DRILLrobo[1],2))
            if "Drill Z" in user_input.label: user_input.text = str(round(DRILLrobo[2],2))
            
            if "Rat X" in user_input.label: user_input.text = str(round(DRILLrat[0],2))
            if "Rat Y" in user_input.label: user_input.text = str(round(DRILLrat[1],2))
            if "Rat Z" in user_input.label: user_input.text = str(round(DRILLrat[2],2))
            if "Depth" in user_input.label: user_input.text = str(round(depth,2))
            if "Vel" in user_input.label: user_input.text = str(round(drill_vel,1))

            if "Hole #" in user_input.label: user_input.text = str(hole_idx)
            if " of " in user_input.label: user_input.text = str(len(screw_holes_rat))
            # NOTE:  Spaces are required otherwise this will also be put into info box labeled "offset.."


        # WARNING MSG
        if BRAIN_SURFACE:
            warning.text = "DANGER!!\nPOTENTIAL BRAIN\nCONTACT!!!\nClick again only if\nyou're 100% sure"
            warning.draw()  
        elif SKULL_SURFACE:
            warning.text = "MAKE SURE\nDRILL IS ON!\n\n     and \n\n     FWD!"
            warning.draw()

        if DRILLrat[2] < 0:
            SKULL_SURFACE = False
            #elif DRILLrat[2] < -4:
            BRAIN_SURFACE = False



        # DRAW ROBOT 000 ON SCREEN IN GREEN   
        pygame.draw.line(myscreen,(0,255,0),(Robo000scrn[0]-20, Robo000scrn[1]),(Robo000scrn[0]+20, Robo000scrn[1]) ,2)
        pygame.draw.line(myscreen,(0,255,0),(Robo000scrn[0], Robo000scrn[1]-20),(Robo000scrn[0], Robo000scrn[1]+20) ,2)
        pygame.draw.line(myscreen,(0,255,0),(630, Robo000scrn[2]),(690, Robo000scrn[2]) ,2)

        
        # DRAW STATIC DRILL Graphic
        drill_static_graphic.draw_drillXY(490, 560)
        #drill.draw_drillZ(660, int(Robo000scrn[2]))
        
        # DRAW DRILL ACTUAL LOCATION
        if BREGMA_SELECTED:
            drill.draw_drillXY(int(DRILLscrn[0]),int(DRILLscrn[1]))
            drill.draw_drillZ(660, int(DRILLscrn[2]))

        
            draw_craniotomy(myscreen,user_inputs)

            h = 0
            for hole in screw_holes_rat:
                if h <= hole_idx -1 : hcolor = (255,0,0)
                else: hcolor = (0,255,0)
                location_robo = (int(hole[0]+ BREGMArobo[0]),
                                 int(hole[1] + BREGMArobo[1]))# in Robot coords
                location_scrn = (int(hole[0]*graphic_scaleXY + BREGMAscrn[0]),
                                 int(hole[1] *graphic_scaleXY + BREGMAscrn[1]))
                
                draw_screw_hole(myscreen, hole, hcolor)
                h += 1

            
            #draw_screw_holes(myscreen)

        pygame.display.flip()                                  

#XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

# send commands to HOME Actual robot
# send commands to Drill Screw Holes
# Plan robot trajectory
# send commands to robot and display on acreen


try:
    setupGUI() 
finally:
    print('cleaned')
    core._cleanup()










