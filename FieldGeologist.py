
from user import User 


class fieldGeologist(User):

    def __init__ (self, ID):
        self._fieldGeologistID = ID
        self._avaliability = True 

    def addRecord(self, data, cur, taskID):
        cur.execute('''INSERT INTO Record (siteName, stream, city, date, remark, EC, temp, pH, EH, taskID, fieldGeologistID, latitude, longitude) VALUES ('{siteName}', '{stream}', '{city}', '{date}','{remark}',{EC},{temp}, {pH}, {EH}, {taskID}, {fieldGeologistID}, {latitude}, {longitude});'''.format(siteName = data['siteName'],stream= data['stream'], city = data['city'] ,date=data['date'],remark = data['remark'],EC=data['EC'], temp = data['temp'],pH=data['pH'],EH = data['EH'],taskID=taskID, fieldGeologistID = self._fieldGeologistID, latitude = data['latitude'], longitude = data['longitude']))
        cur.connection.commit

            
    def insertImage(self,data,cur,recordID):
        cur.execute('''INSERT INTO Image (imageType, imagePath, recordID) 
            VALUES ('{imageType}', '{imagePath}', '{recordID}');'''.format(imageType = data['imageType'],imagePath= data['imagePath'], recordID = recordID))
        cur.connection.commit()
        
      

    @property
    def fieldGeologistID(self):
        return self._fieldGeologistID

    # define setter function for fieldGeologistID property
    @fieldGeologistID.setter 
    def fieldGeologistID(self, fieldGeologistID):
        self._fieldGeologistID = fieldGeologistID

    @property
    def avaliability(self):
        return self._avaliability

    # define setter function for avaliability property
    @avaliability.setter 
    def avaliability(self, avaliability):
        self._avaliability = avaliability