import serial.tools.list_ports
import numpy as np
import time
ports = serial.tools.list_ports.comports()   #This is going to define all the ports in use rn
serialInst = serial.Serial() 


#Read each port line by line and print out the ports in use
portList = []
for onePort in ports: 
    portList.append(str(onePort))
    print(str(onePort)) #Command checks if the arduino is plugged in



val = input("Select the port: COM")
print(val)

for i in range(0, len(portList)): #This for loop is going to loop through all of the ports plugged in.
    if(portList[i].startswith("COM" + str(val))):
        portVar = "COM" + str(val)
        print(portList[i])


serialInst.baudrate = 9600 #Double check this baudrate
serialInst.port = portVar #this is the arduino and we're setting the port to the portVar we found
serialInst.open() 

print("----------------------------------------------------------") 

#How many ever times we want to read in the data
counter = 0
#Two different lists/arrays are created
s_list = []
c_list = []
read_s = False

data_array = np.zeros((100, 1))
data_index = 0
while True:
    if (serialInst.in_waiting): #If there is data on the arduino.
        packet = serialInst.readline() #Reads the incoming byte from the serial device
        check_packet = packet.decode("utf")
        #print(check_packet)


        #Command will replace s and c with all the data
        s_packet = check_packet.replace('s', '') 
        final_packet = s_packet.replace('c', '')
        final_packet = float(final_packet)
        data_array[data_index] = final_packet
        data_index += 1

        t = time.localtime()
        current_time = time.strftime("%H%M%S", t)
        print(current_time)
        if (data_array[99] != 0):
            np.save(str(current_time), data_array)
            
            data_array = np.zeros((100, 1))
            data_index = 0

        # if(read_s == True):
        #     s_list.append(check_packet)
        #     read_s = False
        # elif(check_packet == 's'):
        #     read_s = True
            
            
        

        # if(check_packet == 's'):
        #     check_packet = packet.decode("utf-32")
        #     print(check_packet)
        #     s_list.append(check_packet)
            
        # if(check_packet == 'c'):
        #     c_list.append(check_packet)
        #     print(c_list)
    
    counter = counter + 1

