from flask import Flask, jsonify, request, Response, send_from_directory,send_file
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, session
from user import User
from Leader import Leader
from FieldGeologist import fieldGeologist
from Database import Database
import redis
import boto3
import base64
import io 
from io import BytesIO
from PIL import Image
import numpy as np 
from cv2 import cv2
import matplotlib.pyplot as plt
import matplotlib
import os
import s3transfer
from keras.preprocessing.image import img_to_array, load_img
from IPython.core.display import display
from keras.applications.vgg19 import preprocess_input 
import numpy as np
from keras.models import model_from_json
import pickle
from keras.models import load_model
from openpyxl import load_workbook
import tempfile



app = Flask(__name__)

# Check Configuration section for more details
app.secret_key= 'eflkwnfklnewlkfnwekfnewklfnkwenfkjwnflkwenfklweflwnlkewnf'
app.config['SECRER_KEY'] = '_5#y2L"F4Q8z\n\xec]/'
app.config['SESSION_TYPE'] = 'redis'

SESSION_REDIS = redis.from_url('redis://:AsfVoVUeKAWHjryAIC22FxkAbqQqBgVL@redis-14676.c238.us-central1-2.gce.cloud.redislabs.com:14676')


session = redis.Redis(
host='redis-14676.c238.us-central1-2.gce.cloud.redislabs.com',
port=14676,
password='AsfVoVUeKAWHjryAIC22FxkAbqQqBgVL')


db = Database()
mysql = db.initializeDatabase(app) 
s3 = boto3.resource(
    service_name='s3',
    region_name='us-east-2',
    aws_access_key_id='AKIAY4CEWAN7MPD4ABFC',
    aws_secret_access_key='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'
)
bucket = s3.Bucket('bismuth1')

############################ User Section ############################


####### sign up ############
@app.route('/SignUp', methods = ['POST','GET'])
def SignUp():
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        UserData = request.get_json(force=True)
        user = User().signUp(UserData, cur, session)
        if user != None :
            db.save(user, 'User', cur)
            cur.execute('select last_insert_id();')
            lastID = cur.fetchall()  
            session.set('email', user._email)
            session.set('userID' , lastID[0]['last_insert_id()'])
            session.set('jobType', user._jobType)
            session.set( 'logged_in', 'True')
            if user._jobType == 'SingingCharacter.L':
                cur.execute('''INSERT INTO Leader (leaderID) VALUES ({values});'''.format(values = lastID[0]['last_insert_id()']))
                cur.connection.commit()
            else:
                cur.execute('''INSERT INTO FieldGeologist (fieldGeologistID) VALUES ({values});'''.format(values = lastID[0]['last_insert_id()']))
                cur.connection.commit()
        else: 
            session.set( 'logged_in', 'False')
        return Response(status=200)
    else: 
        if session['logged_in'] == b'True':
            userID = str(session.get('userID'))
            jobType = str(session.get('jobType'))
            userr = {'userID': userID[1:].replace("'",("")) , 'jobType' : jobType[1:].replace("'",("")) }
            return jsonify(userr) , 200
        else: 
            login_message = str(session.get('login_message'))
            message = {'message': login_message[1:].replace("'",("")) }
            return jsonify(message) , 400

####### login  ############

@app.route('/Login', methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        Userdata = request.get_json(force=True)
        User().login(Userdata, cur, session)  
        return Response(status=200)    
    else : 
        if session.get('logged_in') == b'True': 
            userID = str(session.get('userID'))
            jobType = str(session.get('jobType'))
            message = {'userID': userID[1:].replace("'",("")) , 'jobType' : jobType[1:].replace("'",("")) }
            return jsonify(message), 200
        else: 
            message = {"message": "The username and password you entered did not match our records. Please double-check and try again."}
            return jsonify(message), 400




####### logout  ############
@app.route('/logout')
def logout():
    session.delete('logged_in')
    session.delete('userID')
    session.delete('jobType')
    return Response(status=200)

 ######################################## Leader #############################################################



 # get fieldgeolgists who is free .    
@app.route('/<leaderID>/getAvailableFieldGeologists',methods = ['GET'])
def getFieldGeologists(leaderID):
    cur = mysql.connection.cursor()
    cur.execute('''SELECT `User`.`name`, `User`.`userID`, `User`.`email`,`User`.`jobType`  FROM `FieldGeologist` INNER JOIN `User` 
        ON `FieldGeologist`.`fieldGeologistID` = `User`.`userID` WHERE 
        `FieldGeologist`.`availability` = 'True' ;''')
    fieldGeologist = cur.fetchall()
    return jsonify(fieldGeologist)



######## add newTask ########
@app.route('/<leaderID>/addTask', methods = ['POST', 'GET'])
def addTask(leaderID):
    if request.method == 'POST':
        taskData = request.get_json(force=True)
        cur = mysql.connection.cursor()
        theLeader = Leader(leaderID)
        taskID = theLeader.createTask(taskData, cur)
        session['newTaskID'] = taskID
        return Response(status=200)
    else: 
        taskID = str(session.get('newTaskID'))
        jsonID = {'taskID':'{s}'.format(s = taskID[1:].replace("'",("")))}
        return jsonify(jsonID)
    

####### GET All Tasks #######
@app.route('/<leaderID>/<taskStatus>/getTasks', methods = ['GET'])
def GetAllLeader(leaderID,taskStatus):
    cur = mysql.connection.cursor()
    ListOfTaskDetails = []
    cur.execute('''SELECT taskID, taskName, objectives, summary, status, internalSupport, externalSupport , deliverables, Task.projectName, programName, departmentName FROM `Task` INNER JOIN `Project_details` 
            ON `Task`.`projectName` = `Project_details`.`projectName` WHERE 
            `Task`.`leaderID` ={leaderID} AND `Task`.`status` ='{status}';'''.format(leaderID= leaderID, status = taskStatus))
    
    tasks = cur.fetchall()
    if (len(tasks)>0):
        for task in tasks:
            # each task object has task information
            # get all field geologists 
            cur.execute('''SELECT `User`.`userID`, `User`.`name`, `User`.`email`, `User`.`jobType`  FROM `FieldGeologist_Task` INNER JOIN `User` 
                        ON `FieldGeologist_Task`.`fieldGeologistID` = `User`.`userID` WHERE 
                        `FieldGeologist_Task`.`taskID` = {taskID} ;'''.format(taskID = task['taskID']))
            fieldGeologists = cur.fetchall()
            if (len(fieldGeologists)>0):
                FG = []
                for fg in fieldGeologists:
                    FG.append(fg)
                task['AssignedFieldGeologist'] = FG
                ListOfTaskDetails.append(task)
    return jsonify(ListOfTaskDetails)

######## add edit task ########
@app.route('/<leaderID>/<taskID>/edit', methods = ['POST'])
def editTask(leaderID, taskID):
    theData = request.get_json(force=True)
    cur = mysql.connection.cursor()
    theleader = Leader(leaderID)
    theleader.editTask(cur, theData,taskID)
    return Response(status=200)


######## add remove task ########
@app.route('/<leaderID>/<taskID>/removeTask', methods = ['POST'])
def removeTask(leaderID, taskID):
    cur = mysql.connection.cursor()
    theleader = Leader(leaderID)
    theleader.removeTask(cur, taskID)
    return Response(status=200)

######## add get report ########
@app.route('/<fieldGeologistID>/<taskID>/getReport', methods = ['POST','GET'])
def getReport(fieldGeologistID, taskID ):
    cur = mysql.connection.cursor()
    cur.execute('''SELECT report_path FROM Task where taskID = {taskID};'''.format(taskID = taskID))
    path = cur.fetchall() 
    obj = bucket.Object(path[0]['report_path']).get()
    data = obj['Body'].read()
    wb = load_workbook(BytesIO(data))
    temp_dir = tempfile.TemporaryDirectory()
    wb.save(temp_dir.name+'/{taskID}.xlsx'.format(taskID = taskID))
    return send_file(temp_dir.name+'/{taskID}.xlsx'.format(taskID = taskID), as_attachment=True)






 ######################################## Field Geologists #############################################################

####### add record #######
@app.route('/<fieldGeologistID>/<taskID>/submitRecord',methods = ['POST', 'GET'])
def addRecord(fieldGeologistID, taskID):
    if request.method == 'POST':
        data= request.get_json(force=True)
        cur = mysql.connection.cursor()
        fieldGeologist(fieldGeologistID).addRecord(data,cur, taskID)
        ######################################## add images #############################################################
        ## get record ID .......... data["Images"]
        cur = mysql.connection.cursor()
        cur.execute('''SELECT MAX(recordID) FROM Record where fieldGeologistID = {fieldGeologistID};'''.format(fieldGeologistID = fieldGeologistID))
        lastID = cur.fetchall()
       
        ## save each image .....................
        for i in range(0,len(data["Images"])):
            cur.execute('''SELECT MAX(recordID) FROM Record where fieldGeologistID = {fieldGeologistID};'''.format(fieldGeologistID = fieldGeologistID))
            lastID = cur.fetchall() 
            recordID = lastID[0]['MAX(recordID)']
            cur.execute('''INSERT INTO Image (imageType, recordID) VALUES ('{imageType}', {recordID});'''.format(imageType = data["Images"][i]['ImageType'], recordID = recordID))


            ###################################################
            cur.execute('''SELECT MAX(imageID) FROM Image where recordID = {recordID};'''.format(recordID = recordID))
            lastID = cur.fetchall() 
            imageID = lastID[0]['MAX(imageID)']
            imagePath = saveImage(data["Images"][i]['ImageType'], data["Images"][i]['image'], '{i}-{recordID}-{fieldGeologistID}.jpg'.format(i = imageID, recordID = recordID, fieldGeologistID = fieldGeologistID))
            cur.execute('''UPDATE Image SET imagePath= '{imagePath}' WHERE imageID= {imageID};'''.format(imagePath= imagePath, imageID= imageID))



        cur.execute('''UPDATE FieldGeologist SET availability= 'True' WHERE fieldGeologistID = {fieldGeologistID}'''.format(fieldGeologistID= fieldGeologistID))
        cur.connection.commit()

         ############################### Check number of field geologist equal to records #########################################
        countFieldGeologist = cur.execute('''SELECT fieldGeologistID FROM FieldGeologist_Task where taskID = {taskID};'''.format(taskID = taskID))
        countRecords = cur.execute('''SELECT recordID FROM Record where taskID = {taskID};'''.format(taskID = taskID))
        if countRecords == countFieldGeologist : 
        ######################################## Generate the Report #############################################################
            path = Leader(-1).generateReport(taskID, cur)
            cur.execute('''UPDATE Task SET status= '{status}', report_path = '{path}' WHERE taskID= {taskID};'''.format(status= 'Completed', taskID= taskID, path = path))
            cur.connection.commit()

        #GgenerateReport(taskID, cur)

        return Response(status=200)
    else: 
        cur = mysql.connection.cursor()
        cur.execute('''SELECT MAX(recordID) FROM Record where fieldGeologistID = {fieldGeologistID};'''.format(fieldGeologistID = fieldGeologistID))
        lastID = cur.fetchall()
        return jsonify({'recordID':lastID[0]['MAX(recordID)'] })




####### GET Completed task #######
@app.route('/<fieldgeolgistID>/getCompleted', methods = ['GET'])
def getAllTAnnjsksF(fieldgeolgistID):
    cur = mysql.connection.cursor()
    ListOfTaskDetails = []
    cur.execute('''SELECT taskID from FieldGeologist_Task where FieldGeologist_Task.fieldGeologistID= {userID}'''.format(userID = fieldgeolgistID))
    tasks = cur.fetchall()
    # check if the task has one or more/// record from fieldgeologist
    if (len(tasks)>0):
        for task in tasks:
            cur.execute('''SELECT taskID, taskName, objectives, summary, status, internalSupport, externalSupport , deliverables, Task.projectName, programName, departmentName FROM `Task` INNER JOIN `Project_details` 
            ON `Task`.`projectName` = `Project_details`.`projectName` WHERE `Task`.`taskID` ={taskID} ;'''.format(taskID= task['taskID']))
            taskDetails = cur.fetchall()

            test = cur.execute('''SELECT * from Record where fieldGeologistID= {fieldGeologistID} AND taskID= {taskID}'''.format(fieldGeologistID =fieldgeolgistID, taskID = task['taskID']))
         
            if test > 0:
           
                # get Leader Information
                cur.execute('''SELECT leaderID FROM `Task` INNER JOIN `Project_details` 
                    ON `Task`.`projectName` = `Project_details`.`projectName` WHERE 
                    `Task`.`taskID` ={taskID};'''.format(taskID= task['taskID']))
                temp = cur.fetchall()

                cur.execute('''SELECT userID, name, email, jobType  from User where userID= {userID}'''.format(userID = temp[0]['leaderID']))
                leaderDetails = cur.fetchall()
                
                taskDetails[0]['leader'] = leaderDetails[0]

                    # get all field geologists 
                cur.execute('''SELECT `User`.`userID`, `User`.`name`, `User`.`email`, `User`.`jobType`  FROM `FieldGeologist_Task` INNER JOIN `User` 
                        ON `FieldGeologist_Task`.`fieldGeologistID` = `User`.`userID` WHERE 
                        `FieldGeologist_Task`.`taskID` = {taskID} ;'''.format(taskID = task['taskID']))
                fieldGeologists = cur.fetchall()
                if (len(fieldGeologists)>0):
                    FG = []
                    for fg in fieldGeologists:
                        FG.append(fg)
                    taskDetails[0]['AssignedFieldGeologist'] = FG
                        # get record and its images. 
                    cur.execute('''SELECT recordID, siteName, stream, city, date, remark, EC, temp, pH, EH, latitude, longitude from Record where fieldGeologistID= {fieldGeologistID} AND taskID= {taskID}'''.format(fieldGeologistID =fieldgeolgistID, taskID = task['taskID']))
                    record = cur.fetchall()
                    if (len(record)>0):
                        cur.execute('''SELECT imageID, imagePath, imageType FROM Image where recordID = {recordID};'''.format(recordID = record[0]['recordID']))
                        images = cur.fetchall() 
                        listOfImages = []
                        for image in images:
                                    ## get Images of the records.
                            img = bucket.Object(image['imagePath']).get().get('Body').read()
                            rawBytes = io.BytesIO(img)
                            rawBytes.seek(0)
                            b64PNG = base64.b64encode(rawBytes.read()).decode("utf-8") 
                            image['image'] = str(b64PNG)
                            listOfImages.append(image)
                        taskDetails[0]['record'] = record[0]
                        taskDetails[0]['record']['images'] = listOfImages
                    ListOfTaskDetails.append(taskDetails[0])
    return jsonify(ListOfTaskDetails)




######### GET Upcoming Tasks #######
@app.route('/<fieldgeolgistID>/<taskStatus>/getUpcoming', methods = ['GET'])
def getAllTAsksF(fieldgeolgistID,taskStatus):
    cur = mysql.connection.cursor()
    ListOfTaskDetails = []
    cur.execute('''SELECT taskID from FieldGeologist_Task where FieldGeologist_Task.fieldGeologistID= {userID}'''.format(userID = fieldgeolgistID))
    tasks = cur.fetchall()
    if (len(tasks)>0):
        for task in tasks:
            # get Task information...
            cur.execute('''SELECT taskID, taskName, objectives, summary, status, internalSupport, externalSupport , deliverables, Task.projectName, programName, departmentName FROM `Task` INNER JOIN `Project_details` 
            ON `Task`.`projectName` = `Project_details`.`projectName` WHERE 
            `Task`.`taskID` ={taskID} AND `Task`.`status` ='{status}';'''.format(taskID= task['taskID'], status = taskStatus))
            taskDetails = cur.fetchall()
            

            test = cur.execute('''SELECT * from Record where fieldGeologistID= {fieldGeologistID} AND taskID= {taskID}'''.format(fieldGeologistID =fieldgeolgistID, taskID = task['taskID']))
            if test == 0:
                    #get Leader Information
                cur.execute('''SELECT leaderID FROM `Task` INNER JOIN `Project_details` 
                        ON `Task`.`projectName` = `Project_details`.`projectName` WHERE 
                        `Task`.`taskID` ={taskID};'''.format(taskID= task['taskID']))
                temp = cur.fetchall()

                cur.execute('''SELECT userID, name, email, jobType  from User where userID= {userID}'''.format(userID = temp[0]['leaderID']))
                leaderDetails = cur.fetchall()
                    
                taskDetails[0]['leader'] = leaderDetails[0]

                        # get all field geologists 
                cur.execute('''SELECT `User`.`userID`, `User`.`name`, `User`.`email`, `User`.`jobType`  FROM `FieldGeologist_Task` INNER JOIN `User` 
                            ON `FieldGeologist_Task`.`fieldGeologistID` = `User`.`userID` WHERE 
                            `FieldGeologist_Task`.`taskID` = {taskID} ;'''.format(taskID = task['taskID']))
                fieldGeologists = cur.fetchall()
                if (len(fieldGeologists)>0):
                    FG = []
                    for fg in fieldGeologists:
                        FG.append(fg)
                    taskDetails[0]['AssignedFieldGeologist'] = FG
                    ListOfTaskDetails.append(taskDetails[0])
    if len(ListOfTaskDetails) == 0:
        return jsonify({"message": "No tasks yet!"}), 400
    else: 
        return jsonify(ListOfTaskDetails[0])



####### Classify image #######
@app.route('/classifyImage', methods = ['POST','GET'])
def classifyImage():
    if request.method == 'POST':
        byteImage = request.files.get('image')
        image_stream = io.BytesIO()
        image_stream.write(byteImage.read())
        image_stream.seek(0)
        file_bytes = np.asarray(bytearray(image_stream.read()), dtype=np.uint8)
        img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        session.set(name='label', value= predict(img))
        return Response(status=200)
    else:
        return jsonify({'label':str(session.get('label')).replace("'","").replace("b","",1)})


from tensorflow import keras



def predict(byteImage): 
    full_model = load_model('model_final.h5')
    full_model.load_weights("/Users/ESRAAZUHAIR/Desktop/new_backend/model_final.h5")
    pic3 = cv2.resize(byteImage,(224,224))
    pic_array1 = img_to_array(pic3)
    expanded1 = np.expand_dims(pic_array1, axis=0)
    preprocessed1 = preprocess_input(expanded1)

    vgg19_prediction1 = full_model.predict_generator(preprocessed1)
    #here 
    print(vgg19_prediction1)
    y_p = np.where(vgg19_prediction1  > 0.5, 1,0)


    y_pp = np.where(vgg19_prediction1 < 0.99999999999, 0,1)
    #0.0000000000000000000000000000000000000001
    print(y_pp)
    print(y_pp.tolist())
    y_pp.tolist()
    #y_pp.shape


    classes=np.argmax(vgg19_prediction1,axis=1)
    pre=classes[0]

    reverse_mapping = ['baslat','dacite','granite','calcite']
    prediction_name = reverse_mapping[pre]
    def check_availability(element, collection: iter):
        return element in collection
    w=check_availability(1, y_pp)
    if w==False:
        prediction_name = "unidentified"
        print("the image is unidentified")

    else:
        print("the rock type is " ,prediction_name)
    #program body ends

    return prediction_name





def saveImage(label, image, fileName):
    image = base64.b64decode(image)  
    im = io.BytesIO(image)
    bucket.Object("RockImages/"+label+"/"+fileName).put(Body=im.read())
    return 'RockImages/{d}/'.format(d = label) + fileName





if __name__ == '__main__':
    app.secret_key = 'sfdsfsdfsfsdfsdfsfsdfsfsfsmnflk'
    app.run(debug=True)
    
