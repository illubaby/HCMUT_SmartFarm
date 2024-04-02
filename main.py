import time                                                                                                                                                                   
import serial.tools.list_ports                                                                
                                                                                              
                                                                                              
def getPort():                                                                                                                                                       
    ports = serial.tools.list_ports.comports()                                                                                                                              
    N = len(ports)                                                                                                                                                              
    commPort = "None"                                                                         
                                                                                              
    for i in range(0, N):                                                                     
                                                                                              
        port = ports[i]                                                                       
                                                                                              
        strPort = str(port)                                                                   
                                                                                              
        if "USB" in strPort:                                                                  
                                                                                              
            splitPort = strPort.split(" ")                                                    
                                                                                              
            commPort = (splitPort[0])                                                         
                                                                                              
    return commPort                                                                           
                                                                                              
                                                                                              
portName = getPort()                                                                          
                                                                                              
print(portName)                                                                               
                                                                                              
                                                                                              
try:                                                                                          
                                                                                              
    ser = serial.Serial(port=portName, baudrate=9600)                                         
                                                                                              
    print("Open successfully")                                                                
                                                                                              
except:                                                                                       
                                                                                              
    print("Can not open the port")                                                            
                                                                                              
    exit()  # Exit the script if the port cannot be opened                                    
                                                                                              
                                                                                              
relay1_ON = [2, 6, 0, 0, 0, 255, 201, 185]                                                                                                                                       
relay1_OFF = [2, 6, 0, 0, 0, 0, 137, 249]                                                     
                                                                                              
                                                                                              
def setDevice1(state):                                                                                                                                                   
    if state == True:                                                                                                                                                   
        ser.write(relay1_ON)                                                                                                                                                 
    else:                                                                                                                                                                       
        ser.write(relay1_OFF)                                                                                                                                                  
    time.sleep(1)                                                                                                                                                             
    print(serial_read_data())                                                                 
                                                                                              
                                                                                              
def serial_read_data():                                                                                                                                                       
    bytesToRead = ser.inWaiting()                                                                                                                                              
    if bytesToRead > 0:                                                                                                                                                        
        out = ser.read(bytesToRead)                                                                                                                                           
        data_array = [b for b in out]                                                                                                                                         
        print(data_array)                                                                                                                                                     
        if len(data_array) >= 7:                                                                                                                                            
            array_size = len(data_array)                                                                                                                                   
            value = data_array[array_size - 4] * 256 + data_array[array_size - 3]                                                                                      
            return value                                                                                                                                                       
        else:                                                                                                                                                                 
            return -1                                                                                                                                                          
    return 0                                                                                  
                                                                                              
                                                                                              
soil_temperature = [1, 3, 0, 6, 0, 1, 100, 11]                                                
                                                                                              
def readTemperature():                                                                                                                                                                
    serial_read_data()                                                                                                                                                            
    ser.write(soil_temperature)                                                                                                                                                    
    time.sleep(1)                                                                                                                                                               
    return serial_read_data()                                                                 
                                                                                              
                                                                                              
soil_moisture = [1, 3, 0, 7, 0, 1, 53, 203]                                                   
                                                                                              
def readMoisture():                                                                                                                                                             
    serial_read_data()                                                                        
    ser.write(soil_moisture)                                                                                                                                                          
    time.sleep(1)                                                                                                                                                                       
    return serial_read_data()                                                                 
                                                                                              
                                                                                              
while True:                                                                                   
    print("TEST ACTUATOR")                                                                                                                                                  
    setDevice1(True)                                                                                                                                                            
    time.sleep(2)                                                                                                                                                              
    # setDevice1(False)                                                                                                                                                          
    # time.sleep(2)                                                                             
                                                                                                                                                                                   
    # print("TEST SENSOR")                                                                      
                                                                                  
    # print("Moisture: ")                                                                       
                                                                                              
    # print(readMoisture())                                                                                                                                                           
    # time.sleep(1)                                                                                                                                                                    
    # print("Temperature: ")                                                                                                                                                           
    # print(readTemperature())                                                                                                                                                    
    # time.sleep(1)