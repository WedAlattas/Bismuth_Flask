import re
from werkzeug.security import generate_password_hash, check_password_hash
import json


# Needed methods: Encrypte the password (after implement flask), check password, check email, isValidName. 

# methods: isValidEmail, isValidPassword, setters and getters.
class User(object):

    def __init__(self):
        self._name = None
        self._password = None 
        self._email = None
        self._jobType = None


    def JSONtostring(self, jsonOb): 
            self._name = jsonOb['name']
            self._password = jsonOb['password']
            self._email = jsonOb["email"] 
            self._jobType = jsonOb["jobType"]
            return self


    def isValidEmail(self, email):
        email = str(email).lower()
        rexes = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        if(re.search(rexes, email)):  
            return True 
        else:  
            return False


    def isValidPassword(self, password): 
        rexes = ('[A-Z]', '[a-z]', '[0-9]')
        if len(password) >= 8 and all(re.search(r, password) for r in rexes):
            return True
        else: 
            return False

    def signUp(self, data , cursor, session):

        # check if the name is valid
        if len(data['name'])<3:
            session['login_message']  = 'the name is short'
            return None 
        else: 
            self._name = data['name']

        count = cursor.execute('''SELECT * FROM User WHERE email='{}';'''.format(str.lower(data['email'])))

        # check if email is used is valid and it not used 
        if self.isValidEmail(str.lower(data['email'])):
            count = cursor.execute('''SELECT * FROM User WHERE email='{}';'''.format(str.lower(data['email'])))
            if count == 0 :
                self._email = str.lower(data['email'])
        else: 
            session['login_message']  = 'invalid email'
            return None


        # check if the password is strong.. 
        if self.isValidPassword(data['password']): 
            self._password = generate_password_hash(data['password'])
        else: 
            session['login_message'] = 'The password should contains capital letters, small letters and digits.'
            return None 

        self._jobType = data['jobType']
        return self


    def login(self, data , cursor, session): 
        cursor.execute('''SELECT email, password, jobType, userID FROM User WHERE email='{}';'''.format(str.lower(data['email'])))
        values = cursor.fetchall()
        if(len(values)>0):
            if(check_password_hash(str(values[0]['password']), data['password'])): 
                session.set('email', values[0]['email'])
                session.set('userID' ,values[0]['userID'])
                session.set('jobType', values[0]['jobType'])
                session.set( 'logged_in', 'True')

       
                

    


    # define setters and getters 

    # define getter function for name property
    @property
    def name(self):
        return self._name

    # define setter function for name property
    @name.setter 
    def name(self, name):
        if len(name)<3:
            raise ValueError('name')
        else: 
            self._name = name
    
    # define getter function for password property
    @property
    def password(self):
        return self._password

    # define setter function for password property
    @password.setter 
    def password(self, password):
        if (self.isValidPassword(password)):
            self._password = generate_password_hash(password)
        else: 
            raise ValueError('password')
        
    
    # define getter function for email property
    @property
    def email(self):
        return self._email

    # define setter function for email property
    @email.setter 
    def email(self, email):
        if(self.isValidEmail(email)): 
            self._email = email
        else: 
            print('try again')

    # define getter function for jobType property
    @property
    def jobType(self):
        return self._jobType

    # define setter function for jobType property
    @jobType.setter 
    def jobType(self, jobType):
        self._jobType = jobType

    # define getter function for userID property
    @property
    def userID(self):
        return self._userID

    # define setter function for userID property
    @userID.setter 
    def userID(self, userID):
        self._userID = userID
    
    










       
