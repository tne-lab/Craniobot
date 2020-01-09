from struct import pack,unpack
import serial
import time

#Basic Python APT/Kinesis Command Protocol Example using KDC001 and MTS50-Z8
#Tested in Anaconda dsitrbution of Python 2.7 and virtual environment of Python 3.6
#Command Protol PDF can be found https://www.thorlabs.com/Software/Motion%20Control/APT_Communications_Protocol.pdf
#Pyserial is a not a native module installed within python and may need to be installed if not already


def get_HW_info(KDC001):
        KDC001.write(pack('<HBBBB', 0x0005, 0x00, 0x00, 0x50, 0x01))
        KDC001.flushInput()
        KDC001.flushOutput()        

def enable_stage(KDC001):
        KDC001.write(pack('<HBBBB',0x0210,Channel,0x01,destination,source))
        print('Stage Enabled')
        time.sleep(0.1)

def home_stage(KDC001):
        KDC001.write(pack('<HBBBB',0x0443,Channel,0x00,destination,source))
        print('Homing stage...')

        #Confirm stage homed before advancing; MGMSG_MOT_MOVE_HOMED 
        Rx = ''
        Homed = pack('<H',0x0444)
        while Rx != Homed:
                Rx = KDC001.read(2)
        print('Stage Homed')
        KDC001.flushInput()
        KDC001.flushOutput()
        return True

def move_absolute(): # mm
        #Move to absolute position 5.0 mm; MGMSG_MOT_MOVE_ABSOLUTE (long version)
        pos = 5.0 # mm
        dUnitpos = int(Device_Unit_SF*pos)
        KDC001.write(pack('<HBBBBHI',0x0453,0x06,0x00,destination|0x80,source,Channel,dUnitpos))
        print('Moving stage')

        #Confirm stage completed move before advancing; MGMSG_MOT_MOVE_COMPLETED 
        Rx = ''
        Moved = pack('<H',0x0464)
        while Rx != Moved:
                Rx = KDC001.read(2)

def flush_all(X,Y,Z):
        X.flushInput()
        X.flushOutput()
        Y.flushInput()
        Y.flushOutput()
        Z.flushInput()
        Z.flushOutput()

def claose_all(X,Y,Z):
        X.close()
        Y.close()
        Z.close()
        del X
        del Y
        del Z


        
#Port Settings
baud_rate = 115200
data_bits = 8
stop_bits = 1
Parity = serial.PARITY_NONE

#Controller's Port and Channel
COM_PortY = 'COM11'
COM_PortZ = 'COM10' #Change to preferred
COM_PortX = 'COM9'
Channel = 1 #Channel is always 1 for a K Cube/T Cube

Device_Unit_SF = 34304. #pg 34 of protocal PDF (as of Issue 23)
destination = 0x50 #Destination byte; 0x50 for T Cube/K Cube, USB controllers
source = 0x01 #Source Byte

#Create Serial Object
KDC001X = serial.Serial(port = COM_PortX, baudrate = baud_rate, bytesize=data_bits, parity=Parity, stopbits=stop_bits,timeout=0.1)
KDC001Y = serial.Serial(port = COM_PortY, baudrate = baud_rate, bytesize=data_bits, parity=Parity, stopbits=stop_bits,timeout=0.1)
KDC001Z = serial.Serial(port = COM_PortZ, baudrate = baud_rate, bytesize=data_bits, parity=Parity, stopbits=stop_bits,timeout=0.1)

#Get HW info; MGMSG_HW_REQ_INFO; may be require by a K Cube to allow confirmation Rx messages
get_HW_info(KDC001X)
get_HW_info(KDC001Y)
get_HW_info(KDC001Z)

#Enable Stage; MGMSG_MOD_SET_CHANENABLESTATE 
enable_stage(KDC001X)
enable_stage(KDC001Y)
enable_stage(KDC001Z)

#Home Stage; MGMSG_MOT_MOVE_HOME
home_stage(KDC001X)
home_stage(KDC001Y)
home_stage(KDC001Z)

# When done, flushInput and output of all stages
flush_all(KDC001X,KDC001Y,KDC001Z)


#Request Position; MGMSG_MOT_REQ_POSCOUNTER 
KDC001X.write(pack('<HBBBB',0x0411,Channel,0x00,destination,source))
KDC001Y.write(pack('<HBBBB',0x0411,Channel,0x00,destination,source))
KDC001Z.write(pack('<HBBBB',0x0411,Channel,0x00,destination,source))

#Read back position returns by the cube; Rx message MGMSG_MOT_GET_POSCOUNTER 
header, chan_dent, position_dUnits = unpack('<6sHI',KDC001X.read(12))
getpos = position_dUnits/float(Device_Unit_SF)
print('Position: %.4f mm' % (getpos))


#Enable Stage; MGMSG_MOD_SET_CHANENABLESTATE
KDC001X.write(pack('<HBBBB',0x0210,Channel,0x02,destination,source))
print('Stage Disabled')
time.sleep(0.1)


KDC001.close()
del KDC001
