	#Library credits: RRoy  https://community.dfrobot.com/makelog-310469.html
 
import ubinascii
import time
from machine import UART,I2C,Pin
 
commandHeaderAndAddress = "55AA11"
algorthimsByteID = {
    "ALGORITHM_OBJECT_TRACKING": "0100",
    "ALGORITHM_FACE_RECOGNITION": "0000",
    "ALGORITHM_OBJECT_RECOGNITION": "0200",
    "ALGORITHM_LINE_TRACKING": "0300",
    "ALGORITHM_COLOR_RECOGNITION": "0400",
    "ALGORITHM_TAG_RECOGNITION": "0500",
    "ALGORITHM_OBJECT_CLASSIFICATION": "0600"
}
 
COMMAND_REQUEST_CUSTOMNAMES= 0x2f
COMMAND_REQUEST_TAKE_PHOTO_TO_SD_CARD = 0x30
COMMAND_REQUEST_SAVE_MODEL_TO_SD_CARD = 0x32
COMMAND_REQUEST_LOAD_MODEL_FROM_SD_CARD = 0x33
COMMAND_REQUEST_CUSTOM_TEXT = 0x34
COMMAND_REQUEST_CLEAR_TEXT = 0x35
COMMAND_REQUEST_LEARN_ONECE = 0x36
COMMAND_REQUEST_FORGET = 0x37
COMMAND_REQUEST_SCREENSHOT_TO_SD_CARD = 0x39
COMMAND_REQUEST_FIRMWARE_VERSION = 0x3C
 
class HuskyLensLibrary:
    def __init__(self, proto):
        self.proto=proto
        self.address=0x32
        if(self.proto=="SERIAL"):
            self.huskylensSer = UART(2,baudrate=9600,rx=33,tx=32,timeout=100)
        else :
            self.huskylensSer = I2C(0, scl=Pin(5), sda=Pin(4), freq=100000)
        self.lastCmdSent = ""
 
    def writeToHuskyLens(self, cmd):
        self.lastCmdSent = cmd
        if(self.proto=="SERIAL"):
            self.huskylensSer.write(cmd)
        else :
            self.huskylensSer.writeto(self.address, cmd)
 
    def calculateChecksum(self, hexStr):
        total = 0
        for i in range(0, len(hexStr), 2):
            total += int(hexStr[i:i+2], 16)
        hexStr = hex(total)[-2:]
        return hexStr
 
    def cmdToBytes(self, cmd):
        return ubinascii.unhexlify(cmd)
 
    def splitCommandToParts(self, str):
        headers = str[0:4]
        address = str[4:6]
        data_length = int(str[6:8], 16)
        command = str[8:10]
        if(data_length > 0):
            data = str[10:10+data_length*2]
        else:
            data = []
        checkSum = str[2*(6+data_length-1):2*(6+data_length-1)+2]
        return [headers, address, data_length, command, data, checkSum]
 
    def getBlockOrArrowCommand(self):
        if(self.proto=="SERIAL"):
                    byteString = self.huskylensSer.read(5)
                    byteString += self.huskylensSer.read(int(byteString[3]))
                    byteString += self.huskylensSer.read(1)
        else:
                    byteString  =self.huskylensSer.readfrom(self.address,5)
                    ##print("______")
                    ##print(byteString)
                    ##print(byteString[3])
                    byteString +=self.huskylensSer.readfrom(self.address,byteString[3]+1)
                    ##print("=======")
                    ##print(byteString)
        commandSplit = self.splitCommandToParts(''.join(['%02x' % b for b in byteString]))
        return commandSplit[4]
 
    def processReturnData(self):
        inProduction = True
        if(inProduction):
            try:
                if(self.proto=="SERIAL"):
                    byteString = self.huskylensSer.read(5)
                    byteString += self.huskylensSer.read(int(byteString[3]))
                    byteString += self.huskylensSer.read(1)
                else:
                    byteString  =self.huskylensSer.readfrom(self.address,5)
                    ##print("______")
                    ##print(byteString)
                    ##print(byteString[3])
                    byteString +=self.huskylensSer.readfrom(self.address,byteString[3]+1)
                    ##print("=======")
                    ##print(byteString)
                commandSplit = self.splitCommandToParts(''.join(['%02x' % b for b in byteString]))
                if(commandSplit[3] == "2e"):
                    return "Knock Recieved"
                else:
                    returnData = []
                    numberOfBlocksOrArrow = int(
                        commandSplit[4][2:4]+commandSplit[4][0:2], 16)
                    numberOfIDLearned = int(
                        commandSplit[4][6:8]+commandSplit[4][4:6], 16)
                    frameNumber = int(
                        commandSplit[4][10:12]+commandSplit[4][8:10], 16)
                    for i in range(numberOfBlocksOrArrow):
                        returnData.append(self.getBlockOrArrowCommand())
                    finalData=[]
                    tmp=[]
                    for i in returnData:
                        tmp=[]
                        for q in range(0,len(i),4):
                            tmp.append(int(i[q:q+2],16)+int(i[q+2:q+4],16))
                        finalData.append(tmp)
                        tmp=[]
                    return finalData
            except:
                 print("Read error")
                 return []
                
    def command_request_knock(self):
        cmd = self.cmdToBytes(commandHeaderAndAddress+"002c3c")
        self.writeToHuskyLens(cmd)
        return self.processReturnData()
 
    def command_request(self):
        cmd = self.cmdToBytes(commandHeaderAndAddress+"002030")
        self.writeToHuskyLens(cmd)
        return self.processReturnData()
 
    def command_request_blocks(self):
        cmd = self.cmdToBytes(commandHeaderAndAddress+"002131")
        self.writeToHuskyLens(cmd)
        return self.processReturnData()
 
    def command_request_arrows(self):
        cmd = self.cmdToBytes(commandHeaderAndAddress+"002232")
        self.writeToHuskyLens(cmd)
        return self.processReturnData()
 
    def command_request_learned(self):
        cmd = self.cmdToBytes(commandHeaderAndAddress+"002333")
        self.writeToHuskyLens(cmd)
        return self.processReturnData()
 
    def command_request_blocks_learned(self):
        cmd = self.cmdToBytes(commandHeaderAndAddress+"002434")
        self.writeToHuskyLens(cmd)
        return self.processReturnData()
 
    def command_request_arrows_learned(self):
        cmd = self.cmdToBytes(commandHeaderAndAddress+"002535")
        self.writeToHuskyLens(cmd)
        return self.processReturnData()
 
    def line_tracking_mode(self):
        cmd = self.cmdToBytes(commandHeaderAndAddress+"022d030042")
        self.writeToHuskyLens(cmd)
        return self.processReturnData()
 
    def face_recognition_mode(self):
        cmd = self.cmdToBytes(commandHeaderAndAddress+"022d00003f")
        self.writeToHuskyLens(cmd)
        return self.processReturnData()
 
    def object_tracking_mode(self):
        cmd = self.cmdToBytes(commandHeaderAndAddress+"022d010040")
        self.writeToHuskyLens(cmd)
        return self.processReturnData()
 
    def object_recognition_mode(self):
        cmd = self.cmdToBytes(commandHeaderAndAddress+"022d020041")
        self.writeToHuskyLens(cmd)
        return self.processReturnData()
 
    def color_recognition_mode(self):
        cmd = self.cmdToBytes(commandHeaderAndAddress+"022d040043")
        self.writeToHuskyLens(cmd)
        return self.processReturnData()
 
    def tag_recognition_mode(self):
        cmd = self.cmdToBytes(commandHeaderAndAddress+"022d050044")
        self.writeToHuskyLens(cmd)
        return self.processReturnData()
 
    def command_request_by_id(self, idVal):
        idVal = "{:04x}".format(idVal)
        idVal = idVal[2:]+idVal[0:2]
        cmd = commandHeaderAndAddress+"0226"+idVal
        cmd += self.calculateChecksum(cmd)
        cmd = self.cmdToBytes(cmd)
        self.writeToHuskyLens(cmd)
        return self.processReturnData()
 
    def command_request_blocks_by_id(self, idVal):
        idVal = "{:04x}".format(idVal)
        idVal = idVal[2:]+idVal[0:2]
        cmd = commandHeaderAndAddress+"0227"+idVal
        cmd += self.calculateChecksum(cmd)
        cmd = self.cmdToBytes(cmd)
        self.writeToHuskyLens(cmd)
        return self.processReturnData()
 
    def command_request_arrows_by_id(self, idVal):
        idVal = "{:04x}".format(idVal)
        idVal = idVal[2:]+idVal[0:2]
        cmd = commandHeaderAndAddress+"0228"+idVal
        cmd += self.calculateChecksum(cmd)
        cmd = self.cmdToBytes(cmd)
        self.writeToHuskyLens(cmd)
        return self.processReturnData()
 
    def command_request_algorthim(self, alg):
        if alg in algorthimsByteID:
            cmd = commandHeaderAndAddress+"022d"+algorthimsByteID[alg]
            cmd += self.calculateChecksum(cmd)
            cmd = self.cmdToBytes(cmd)
            self.writeToHuskyLens(cmd)
            return self.processReturnData()
        else:
            print("INCORRECT ALGORITHIM NAME")
            
    #---------------------  8.5 update new features           
    #在哈士奇的屏幕上显示文字    
    def command_request_custom_text(self, text,x,y):
 
        textLength = len(text)
        dataLength = textLength+4
        cmd = commandHeaderAndAddress #[0x55,0xAA,0x11] [85, 170, 17]
        cmd += "{:02x}".format(dataLength)   #length of data [4+len(msg)=6]
        #cmd += str(34)#COMMAND_REQUEST_CUSTOM_TEXT = 0x34,[52]
        cmd += "{:02x}".format(COMMAND_REQUEST_CUSTOM_TEXT) 
        #first 4 digits, len,cor_x1,cor_x2,cor_y 
        #len
        cmd += "{:02x}".format(dataLength)  
        #cor_x1,cor_x2    
        if x > 255:
            data_1 = 0xff
            cmd += "{:02x}".format(data_1)      
            data_2 = x % 256        
            cmd += "{:02x}".format(data_2)   
        else:
            cmd += "{:02x}".format(0)
            cmd += "{:02x}".format(x)
        #cor_y 
        cmd += "{:02x}".format(y)
        
        
        for char in text:
            cmd += "{:02x}".format(ord(char))
            
        cmd += self.calculateChecksum(cmd)
        cmd = self.cmdToBytes(cmd)
        self.writeToHuskyLens(cmd)
        #print("cmd:",cmd)
        return self.processReturnData()
        
     #清屏
    def command_request_clear_text(self):
        cmd = commandHeaderAndAddress#[0x55,0xAA,0x11] [85, 170, 17]
        dataLength = 0
        cmd += "{:02x}".format(dataLength)
        cmd += "{:02x}".format(COMMAND_REQUEST_CLEAR_TEXT)
        cmd += self.calculateChecksum(cmd)
        cmd = self.cmdToBytes(cmd)
        self.writeToHuskyLens(cmd)
        return self.processReturnData()
 
    
    #存照片至SD卡    
    def command_request_photo(self):
        cmd = commandHeaderAndAddress
        dataLength = 0
        cmd += "{:02x}".format(dataLength)
        cmd += "{:02x}".format(COMMAND_REQUEST_TAKE_PHOTO_TO_SD_CARD)
        cmd += self.calculateChecksum(cmd)
        cmd = self.cmdToBytes(cmd)
        self.writeToHuskyLens(cmd)
        return self.processReturnData()
        
        
    #忘记算法  
    def command_request_forget(self):
        cmd = commandHeaderAndAddress
        dataLength = 0
        cmd += "{:02x}".format(dataLength)
        cmd += "{:02x}".format(COMMAND_REQUEST_FORGET)       
        cmd += self.calculateChecksum(cmd)
        cmd = self.cmdToBytes(cmd)
        self.writeToHuskyLens(cmd)
        return self.processReturnData()
 
   
    #存截图至SD卡    
    def command_request_screenshot(self):
        cmd = commandHeaderAndAddress
        dataLength = 0
        cmd += "{:02x}".format(dataLength)
        cmd += "{:02x}".format(COMMAND_REQUEST_SCREENSHOT_TO_SD_CARD)      
        cmd += self.calculateChecksum(cmd)
        cmd = self.cmdToBytes(cmd)
        self.writeToHuskyLens(cmd)
        return self.processReturnData()
       
    #学习id一次   
    def command_request_learn_once(self,id):
        cmd = commandHeaderAndAddress        
        dataLength = 2
        cmd += "{:02x}".format(dataLength)
        cmd += "{:02x}".format(COMMAND_REQUEST_LEARN_ONECE)   
        id = [id & 0xff, (id >> 8) & 0xff]   
        cmd += "{:02x}".format(id[0])
        cmd += "{:02x}".format(id[1])        
        cmd += self.calculateChecksum(cmd)
        cmd = self.cmdToBytes(cmd)
        self.writeToHuskyLens(cmd)
        return self.processReturnData()
        
    # 自定名id名
    def command_request_customnames(self, id, name):
        nameLength = len(name)
        dataLength = nameLength+3
        cmd = commandHeaderAndAddress        
        cmd += "{:02x}".format(dataLength)
        cmd += "{:02x}".format(COMMAND_REQUEST_CUSTOMNAMES)   
        
        cmd += "{:02x}".format(id)
        cmd += "{:02x}".format(nameLength+1)
        for char in name:
            cmd += "{:02x}".format(ord(char))           
        cmd += "{:02x}".format(0)
        cmd += self.calculateChecksum(cmd)
        cmd = self.cmdToBytes(cmd)
        self.writeToHuskyLens(cmd)
        return self.processReturnData()
        
   #保存模型到SD卡        
    def command_request_save_model_to_SD_card(self,index):
        cmd = commandHeaderAndAddress        
        dataLength = 2
        cmd += "{:02x}".format(dataLength)
        cmd += "{:02x}".format(COMMAND_REQUEST_SAVE_MODEL_TO_SD_CARD)   
        index = [index & 0xff, (index >> 8) & 0xff]   
        cmd += "{:02x}".format(index[0])
        cmd += "{:02x}".format(index[1])        
        cmd += self.calculateChecksum(cmd)
        cmd = self.cmdToBytes(cmd)
        self.writeToHuskyLens(cmd)
        return self.processReturnData()
     
   #读取模型到SD卡   
    def command_request_load_model_from_SD_card(self, index):
        cmd = commandHeaderAndAddress        
        dataLength = 2
        cmd += "{:02x}".format(dataLength)
        cmd += "{:02x}".format(COMMAND_REQUEST_LOAD_MODEL_FROM_SD_CARD)   
        index = [index & 0xff, (index >> 8) & 0xff]   
        cmd += "{:02x}".format(index[0])
        cmd += "{:02x}".format(index[1])        
        cmd += self.calculateChecksum(cmd)
        cmd = self.cmdToBytes(cmd)
        self.writeToHuskyLens(cmd)
        return self.processReturnData() 