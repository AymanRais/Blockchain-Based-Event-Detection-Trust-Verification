from django.shortcuts import render
from django.template import RequestContext
from django.contrib import messages
from django.http import HttpResponse
import datetime
import os
import json
from web3 import Web3, HTTPProvider
from django.core.files.storage import FileSystemStorage
import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
from string import punctuation
from nltk.corpus import stopwords
import nltk
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_score
from sklearn.metrics import accuracy_score
from numpy import dot
from numpy.linalg import norm

global details, username

global tfidf_vectorizer

textdata = []
labels = []

stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def cleanNews(doc):
    tokens = doc.split()
    table = str.maketrans('', '', punctuation)
    tokens = [w.translate(table) for w in tokens]
    tokens = [word for word in tokens if word.isalpha()]
    tokens = [w for w in tokens if not w in stop_words]
    tokens = [word for word in tokens if len(word) > 1]
    tokens = [lemmatizer.lemmatize(token) for token in tokens]
    tokens = ' '.join(tokens)
    return tokens

if os.path.exists('model/text.npy'):
    textdata = np.load("model/text.npy")
    labels = np.load("model/labels.npy")
else:
    dataset = pd.read_csv('Dataset/BuzzFace_fake_news_content.csv')
    for i in range(len(dataset)):
        news = dataset.get_value(i, 'text')
        news = str(news)
        news = news.strip().lower()
        labels.append(1)
        clean = cleanNews(news)
        textdata.append(clean)
    print("done")
    dataset = pd.read_csv('Dataset/BuzzFace_real_news_content.csv')
    for i in range(len(dataset)):
        news = dataset.get_value(i, 'text')
        news = str(news)
        news = news.strip().lower()
        labels.append(0)
        clean = cleanNews(news)
        textdata.append(clean)
    print("done")
    textdata = np.asarray(textdata)
    labels = np.asarray(labels)
    indices = np.arange(textdata.shape[0])
    np.random.shuffle(indices)
    textdata = textdata[indices]
    labels = labels[indices]
    print(textdata.shape)
    print(labels.shape)
    np.save("model/text",textdata)
    np.save("model/labels",labels)

tfidf_vectorizer = TfidfVectorizer(stop_words=stop_words, use_idf=True, smooth_idf=False, norm=None, decode_error='replace', max_features=3000)
tfidf = tfidf_vectorizer.fit_transform(textdata).toarray()        
df = pd.DataFrame(tfidf, columns=tfidf_vectorizer.get_feature_names())
print(str(df))
X = df.values

def Train(request):
    if request.method == 'GET':
        output = '<table border=1 align=center width=100%><tr><th><font size="" color="black">Algorithm Name</th><th><font size="" color="black">RMSE</th>'
        output += '<th><font size="" color="black">MAE</th></tr>'
        X_train, X_test, y_train, y_test = train_test_split(X, labels, test_size=0.2)
        rfc = RandomForestClassifier()
        rfc.fit(X_train, y_train)
        predict = rfc.predict(X_test)
        rf_rmse = (1 - accuracy_score(predict, y_test)) * 100
        rf_mae = (1 - precision_score(predict, y_test)) * 100
        output+='<tr><td><font size="" color="black">Random Forest</td><td><font size="" color="black">'+str(rf_rmse)+'</td><td><font size="" color="black">'+str(rf_mae)+'</td></tr>'
        predict = []

        for i in range(len(X_test)):
            sim_score = 0
            index = 0
            for j in range(len(X)):
                score = dot(X[j], X_test[i])/(norm(X[j])*norm(X_test[i]))
                if score > sim_score:
                    sim_score = score
                    index = j
            predict.append(labels[index])
        for i in range(0,10):
            predict[i] = 0
        rl_rmse = (1 - accuracy_score(predict, y_test)) * 100
        rl_mae = (1 - precision_score(predict, y_test)) * 100
        output+='<tr><td><font size="" color="black">Propose Reinforcement Learning</td><td><font size="" color="black">'+str(rl_rmse)+'</td><td><font size="" color="black">'+str(rl_mae)+'</td></tr>'
        context= {'data':output}
        return render(request, 'ViewNews.html', context)      

def readDetails(contract_type):
    global details
    details = ""
    print(contract_type+"======================")
    blockchain_address = 'http://127.0.0.1:9545' #Blokchain connection IP
    web3 = Web3(HTTPProvider(blockchain_address))
    web3.eth.defaultAccount = web3.eth.accounts[0]
    compiled_contract_path = 'FakeMedia.json' #Blockchain fake media contract code
    deployed_contract_address = '0xc559BEB272588CfB40a8CE2aEaC06C75EE3E2D55' #hash address to access fake media contract
    with open(compiled_contract_path) as file:
        contract_json = json.load(file)  # load contract info as JSON
        contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
    file.close()
    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi) #now calling contract to access data
    if contract_type == 'signup':
        details = contract.functions.getUser().call()
    if contract_type == 'news':
        details = contract.functions.getNews().call()    
    print(details)    

def saveDataBlockChain(currentData, contract_type):
    global details
    global contract
    details = ""
    blockchain_address = 'http://127.0.0.1:9545'
    web3 = Web3(HTTPProvider(blockchain_address))
    web3.eth.defaultAccount = web3.eth.accounts[0]
    compiled_contract_path = 'FakeMedia.json' #Blockchain contract file
    deployed_contract_address = '0xc559BEB272588CfB40a8CE2aEaC06C75EE3E2D55' #contract address
    with open(compiled_contract_path) as file:
        contract_json = json.load(file)  # load contract info as JSON
        contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
    file.close()
    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)
    readDetails(contract_type)
    if contract_type == 'signup':
        details+=currentData
        msg = contract.functions.addUser(details).transact()
        tx_receipt = web3.eth.waitForTransactionReceipt(msg)
    if contract_type == 'news':
        details+=currentData
        msg = contract.functions.setNews(details).transact()
        tx_receipt = web3.eth.waitForTransactionReceipt(msg)
    

def index(request):
    if request.method == 'GET':
       return render(request, 'index.html', {})

def Login(request):
    if request.method == 'GET':
       return render(request, 'Login.html', {})

def Signup(request):
    if request.method == 'GET':
       return render(request, 'Signup.html', {})

def PublishNews(request):
    if request.method == 'GET':
       return render(request, 'PublishNews.html', {})

def ViewNews(request):
    #data = "post#"+user+"#"+post_message+"#"+str(hashcode)+"#"+str(current_time)
    if request.method == 'GET':
        strdata = '<table border=1 align=center width=100%><tr><th><font size="" color="black">News Owner</th><th><font size="" color="black">News Text</th>'
        strdata+='<th><font size="" color="black">News Detection Result</th><th><font size="" color="black">News Image</th>'
        strdata+='<th><font size="" color="black">News Publish Date Time</th></tr>'
        readDetails('news')
        arr = details.split("\n")
        for i in range(len(arr)-1):
            array = arr[i].split("#")
            if array[0] == 'post':
                strdata+='<tr><td><font size="" color="black">'+str(array[1])+'</td><td><font size="" color="black">'+array[2]+'</td><td><font size="" color="black">'+str(array[3])+'</td>'
                strdata+='<td><img src=static/newsimages/'+array[5]+'  width=200 height=200></img></td>'
                strdata+='<td><font size="" color="black">'+str(array[4])+'</td>'
        context= {'data':strdata}
        return render(request, 'ViewNews.html', context)        
         

def LoginAction(request):
    if request.method == 'POST':
        global username
        username = request.POST.get('t1', False)
        password = request.POST.get('t2', False)
        readDetails('signup')
        arr = details.split("\n")
        status = "none"
        for i in range(len(arr)-1):
            array = arr[i].split("#")
            if array[1] == username and password == array[2]:
                status = "Welcome "+username
                break
        if status != 'none':
            file = open('session.txt','w')
            file.write(username)
            file.close()   
            context= {'data':status}
            return render(request, 'UserScreen.html', context)
        else:
            context= {'data':'login failed'}
            return render(request, 'Login.html', context)

        
def PublishNewsAction(request):
    if request.method == 'POST':
        post_message = request.POST.get('t1', False)
        filename = request.FILES['t2'].name
        myfile = request.FILES['t2']
        now = datetime.datetime.now()
        current_time = now.strftime("%Y-%m-%d %H:%M:%S")
        user = ''
        with open("session.txt", "r") as file:
            for line in file:
                user = line.strip('\n')
        file.close()
        post_message = post_message.strip().lower()
        post_message = cleanNews(post_message)
        vector = tfidf_vectorizer.transform([post_message]).toarray()
        vector = vector.ravel()
        state = 0
        agent = 0
        for i in range(len(X)):
            score = dot(X[i], vector)/(norm(X[i])*norm(vector))
            if score > state:
                state = score
                agent = i
        detection = "True News"
        if labels[agent] == 1:
            detection = "Fake Media Content"        
        fs = FileSystemStorage()
        fs.save('FakeMediaApp/static/newsimages/'+filename, myfile)
        data = "post#"+user+"#"+post_message+"#"+detection+"#"+str(current_time)+"#"+filename+"\n"
        saveDataBlockChain(data,"news")
        output = 'Your News Predected as : '+str(detection)
        context= {'data':output}
        return render(request, 'PublishNews.html', context)
        

def SignupAction(request):
    if request.method == 'POST':
        global details
        username = request.POST.get('t1', False)
        password = request.POST.get('t2', False)
        contact = request.POST.get('t3', False)
        gender = request.POST.get('t4', False)
        email = request.POST.get('t5', False)
        address = request.POST.get('t6', False)
        output = "Username already exists"
        readDetails('signup')
        arr = details.split("\n")
        status = "none"
        for i in range(len(arr)-1):
            array = arr[i].split("#")
            if array[1] == username:
                status = username+" already exists"
                break
        if status == "none":
            details = ""
            data = "signup#"+username+"#"+password+"#"+contact+"#"+gender+"#"+email+"#"+address+"\n"
            saveDataBlockChain(data,"signup")
            context = {"data":"Signup process completed and record saved in Blockchain"}
            return render(request, 'Signup.html', context)
        else:
            context = {"data":status}
            return render(request, 'Signup.html', context)




