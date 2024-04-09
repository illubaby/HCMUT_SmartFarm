import time                                                                                                                                                                   
import serial.tools.list_ports   
from adafruit import *                                                             

def crc16_modbus_recheck(data):
    """
    Recheck the CRC-16 calculation for a given string of bytes using the Modbus protocol.
    
    Args:
    - data: A bytes object containing the message for which the CRC should be recalculated.
    
    Returns:
    - A tuple containing the CRC-16 as two separate bytes (low byte, high byte).
    """
    crc = 0xFFFF
    for pos in data:
        crc ^= pos
        for i in range(8):
            if (crc & 1) != 0:
                crc >>= 1
                crc ^= 0xA001
            else:
                crc >>= 1
    return crc & 0xFF, (crc >> 8) & 0xFF

# Example usage with the message before CRC calculation
                                                                                              
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

def readData(dataAray):
    decValue = 0
    for i in range (2, len(dataAray) - 2):
        decValue = decValue + dataAray[i] * (256 ** (len(dataAray) - i - 3))
    return decValue

relay1_ON = [2, 6, 0, 0, 0, 255, 201, 185]                                                                                                                                       
relay1_OFF = [2, 6, 0, 0, 0, 0, 137, 249]                                                     
                                                                                              
message_on = bytes(relay1_ON[0:5])
message_off = bytes(relay1_OFF[0:5])


# Splitting the result into two bytes
relay1_ON[6] ,relay1_ON[7] = crc16_modbus_recheck(bytes(relay1_ON[0:6]))
relay1_OFF[6] ,relay1_OFF[7] = crc16_modbus_recheck(bytes(relay1_OFF[0:6]))

print(relay1_ON)                                 
                                                                                              
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
            value = readData(data_array)                                                                                     
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

soil_moisture[len(soil_moisture)-2], soil_moisture[len(soil_moisture)-1]=crc16_modbus_recheck(bytes(soil_moisture[0:len(soil_moisture)-2]))

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
                                                                                  
    print("Moisture: ")                                                                       
    moisture= readMoisture()                                                                          
    print(moisture)
    client.publish("sonar", moisture)
    client.publish("pump-in", moisture)                                                                                                                                                           
    client.publish("pump-out", moisture)                                                                                                                                                           
    time.sleep(1)                                                                                                                                                                    
    # print("Temperature: ")                                                                                                                                                           
    # print(readTemperature())                                                                                                                                                    
    # time.sleep(1)