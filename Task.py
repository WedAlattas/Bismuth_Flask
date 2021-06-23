
class Task: 
    def __init__(self):
        self._leaderID = None
        self._taskName = None
        self._projectName = None
        self._programName = None
        self._departmentName = None
        self._objectives = None
        self._summary = None
        self._internalSupport = None
        self._externalSupport = None
        self._deliverables = None
        self._status = 'Ongoing'



    @property
    def taskName(self):
        return self.taskName

    # define setter function for taskName property
    @taskName.setter 
    def taskName(self, taskName):
        self._taskName = taskName

    @property
    def projectName(self):
        return self._projectName

    # define setter function for projectName property
    @projectName.setter 
    def projectName(self, projectName):
        self._projectName = projectName


    @property
    def programName(self):
        return self._programName

    # define setter function for programName property
    @programName.setter 
    def programName(self, programName):
        self._programName = programName

    @property
    def departmentName(self):
        return self._departmentName

    # define setter function for departmentName property
    @departmentName.setter 
    def departmentName(self, departmentName):
        self._departmentName = departmentName


    @property
    def objectives(self):
        return self._objectives

    # define setter function for objectives property
    @objectives.setter 
    def objectives(self, objectives):
        self._objectives = objectives

    @property
    def summary(self):
        return self._summary

    # define setter function for summary property
    @summary.setter 
    def summary(self, summary):
        self._summary = summary

    @property
    def internalSupport(self):
        return self._internalSupport

    # define setter function for internalSupport property
    @internalSupport.setter 
    def internalSupport(self, internalSupport):
        self._internalSupport = internalSupport

    @property
    def externalSupport(self):
        return self._externalSupport

    # define setter function for externalSupport property
    @externalSupport.setter 
    def externalSupport(self, externalSupport):
        self._externalSupport = externalSupport

    @property
    def deliverables(self):
        return self._deliverables

    # define setter function for deliverables property
    @deliverables.setter 
    def deliverables(self, deliverables):
        self._deliverables = deliverables

    @property
    def status(self):
        return self._status

    # define setter function for status property
    @status.setter 
    def status(self, status):
        self._status = status

    @property
    def reportPath(self):
        return self._reportPath

    # define setter function for reportPath property
    @reportPath.setter 
    def reportPath(self, reportPath):
        self._reportPath = reportPath

    
