class Record: 
    def __init__(self):
        self._recordID = ''
        self._siteName = ''
        self._stream = ''
        self._city = ''
        self._coordinates = ''
        self._date = ''
        self._remark = ''
        self._EC = ''
        self._temp = ''
        self._pH = ''
        self._EH = ''
        self._taskID = ''
        self._fieldGeologistID = ''


    @property
    def recordID(self):
        return self._recordID

    # define setter function for recordID property
    @recordID.setter 
    def recordID(self, recordID):
        self._recordID = recordID

    @property
    def siteName(self):
        return self._siteName

    # define setter function for siteName  property
    @siteName.setter 
    def siteName(self, siteName ):
        self._siteName = siteName 


    @property
    def stream(self):
        return self._stream

    # define setter function for stream property
    @stream.setter 
    def stream(self, stream):
        self._stream = stream

    @property
    def city(self):
        return self._city

    # define setter function for city property
    @city.setter 
    def city(self, city):
        self._city = city

    @property
    def coordinates (self):
        return self._coordinates

    # define setter function for coordinates  property
    @coordinates .setter 
    def coordinates (self, coordinates ):
        self._coordinates = coordinates 

    @property
    def date(self):
        return self._date

    # define setter function for date property
    @date.setter 
    def date(self, date):
        self._date = date

    @property
    def remark(self):
        return self._remark

    # define setter function for remark property
    @remark.setter 
    def remark(self, remark):
        self._remark = remark


    @property
    def EC(self):
        return self._EC

    # define setter function for EC property
    @EC.setter 
    def EC(self, EC):
        self._EC = EC

    @property
    def temp (self):
        return self._temp 

    # define setter function for temp  property
    @temp .setter 
    def temp (self, temp ):
        self.temp  = temp 


    @property
    def pH (self):
        return self._pH 

    # define setter function for pH  property
    @pH .setter 
    def pH(self, pH ):
        self._pH = pH 


    @property
    def EH(self):
        return self._EH

    # define setter function for EH property
    @EH.setter 
    def EH(self, EH):
        self._EH = EH

    
    @property
    def taskID(self):
        return self._taskID

    # define setter function for taskID property
    @taskID.setter 
    def taskID(self, taskID):
        self._taskID = taskID


    @property
    def fieldGeologistID(self):
        return self._fieldGeologistID

    # define setter function for fieldGeologistID property
    @fieldGeologistID.setter 
    def fieldGeologistID(self, fieldGeologistID):
        self._fieldGeologistID = fieldGeologistID