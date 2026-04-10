from django.db.models import Count
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
import datetime
import openpyxl
import xlwt
from django.http import HttpResponse


import pandas as pd
import numpy as np
import re
from sklearn.ensemble import VotingClassifier
from sklearn.tree import DecisionTreeClassifier

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score

# Create your views here.
from Remote_User.models import ClientRegister_Model,predict_ad_click_fraud_detection,detection_ratio,detection_accuracy,csvdatasets

def login(request):


    if request.method == "POST" and 'submit1' in request.POST:

        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            enter = ClientRegister_Model.objects.get(username=username,password=password)
            request.session["userid"] = enter.id

            return redirect('ViewYourProfile')
        except:
            pass

    return render(request,'RUser/login.html')

def Register1(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phoneno = request.POST.get('phoneno')
        country = request.POST.get('country')
        state = request.POST.get('state')
        city = request.POST.get('city')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        ClientRegister_Model.objects.create(username=username, email=email, password=password, phoneno=phoneno,
                                            country=country, state=state, city=city, address=address, gender=gender)
        obj = "Registered Successfully"
        return render(request, 'RUser/Register1.html', {'object': obj})
    else:
        return render(request,'RUser/Register1.html')


def Download_Uploaded_Datasets(request):
    response = HttpResponse(content_type='application/ms-excel')
    # decide file name
    response['Content-Disposition'] = 'attachment; filename="Uploaded_Datasets.xls"'
    # creating workbook
    wb = xlwt.Workbook(encoding='utf-8')
    # adding sheet
    ws = wb.add_sheet("sheet1")
    # Sheet header, first row
    row_num = 0
    font_style = xlwt.XFStyle()
    # headers are bold
    font_style.font.bold = True
    # writer = csv.writer(response)
    obj = csvdatasets.objects.all()
    data = obj  # dummy method to fetch data.
    for my_row in data:
        row_num = row_num + 1

        ws.write(row_num, 0, my_row.Fid, font_style)
        ws.write(row_num, 1, my_row.IPAddress, font_style)
        ws.write(row_num, 2, my_row.App_Name, font_style)
        ws.write(row_num, 3, my_row.Device, font_style)
        ws.write(row_num, 4, my_row.OS, font_style)
        ws.write(row_num, 5, my_row.Channel, font_style)
        ws.write(row_num, 6, my_row.Click_time, font_style)
        ws.write(row_num, 7, my_row.Time_to_click, font_style)
        ws.write(row_num, 8, my_row.Session_duration, font_style)
        ws.write(row_num, 9, my_row.Mouse_movement, font_style)
        ws.write(row_num, 10, my_row.IP_frequency, font_style)
        ws.write(row_num, 11, my_row.Referrer_missing, font_style)
        ws.write(row_num, 12, my_row.Scroll_depth, font_style)
        ws.write(row_num, 13, my_row.Time_on_page, font_style)


    wb.save(response)
    return response


def ViewYourProfile(request):
    userid = request.session['userid']
    obj = ClientRegister_Model.objects.get(id= userid)
    return render(request,'RUser/ViewYourProfile.html',{'object':obj})


def Detection_Of_Ad_Click_Fraud_Type(request):

    if request.method == "POST":

        Fid= request.POST.get('Fid')
        IPAddress= request.POST.get('IPAddress')
        App_Name= request.POST.get('App_Name')
        Device= request.POST.get('Device')
        OS= request.POST.get('OS')
        Channel= request.POST.get('Channel')
        Click_time= request.POST.get('Click_time')
        Time_to_click= request.POST.get('Time_to_click')
        Session_duration= request.POST.get('Session_duration')
        Mouse_movement= request.POST.get('Mouse_movement')
        IP_frequency= request.POST.get('IP_frequency')
        Referrer_missing= request.POST.get('Referrer_missing')
        Scroll_depth= request.POST.get('Scroll_depth')
        Time_on_page= request.POST.get('Time_on_page')


        df = pd.read_csv('Datasets.csv', encoding='latin-1')


        df['label'] = df.Label.apply(lambda x: 1 if x == 1 else 0)
        df.head()


        X = df['Fid'].apply(str)
        y = df['label']

        print("Fid")
        print(X)
        print("Label")
        print(y)

        cv = CountVectorizer(lowercase=False, strip_accents='unicode', ngram_range=(1, 1))
        #X = cv.fit_transform(df['ipaddress'].apply(lambda x: np.str_(X)))

        X = cv.fit_transform(X)

        models = []
        from sklearn.model_selection import train_test_split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20)
        X_train.shape, X_test.shape, y_train.shape

        print("Deep Neural Network(DNN)")
        from sklearn.neural_network import MLPClassifier
        mlpc = MLPClassifier().fit(X_train, y_train)
        y_pred = mlpc.predict(X_test)
        testscore_mlpc = accuracy_score(y_test, y_pred)
        accuracy_score(y_test, y_pred)
        print(accuracy_score(y_test, y_pred))
        print(accuracy_score(y_test, y_pred) * 100)
        print("CLASSIFICATION REPORT")
        print(classification_report(y_test, y_pred))
        print("CONFUSION MATRIX")
        print(confusion_matrix(y_test, y_pred))
        models.append(('MLPClassifier', mlpc))

        # SVM Model
        print("SVM")
        from sklearn import svm
        lin_clf = svm.LinearSVC()
        lin_clf.fit(X_train, y_train)
        predict_svm = lin_clf.predict(X_test)
        svm_acc = accuracy_score(y_test, predict_svm) * 100
        print(svm_acc)
        print("CLASSIFICATION REPORT")
        print(classification_report(y_test, predict_svm))
        print("CONFUSION MATRIX")
        print(confusion_matrix(y_test, predict_svm))
        models.append(('svm', lin_clf))
        detection_accuracy.objects.create(names="SVM", ratio=svm_acc)

        print("Logistic Regression")

        from sklearn.linear_model import LogisticRegression
        reg = LogisticRegression(random_state=0, solver='lbfgs').fit(X_train, y_train)
        y_pred = reg.predict(X_test)
        print("ACCURACY")
        print(accuracy_score(y_test, y_pred) * 100)
        print("CLASSIFICATION REPORT")
        print(classification_report(y_test, y_pred))
        print("CONFUSION MATRIX")
        print(confusion_matrix(y_test, y_pred))
        models.append(('logistic', reg))

        detection_accuracy.objects.create(names="Logistic Regression", ratio=accuracy_score(y_test, y_pred) * 100)

        print("Random Forest Classifier")
        from sklearn.ensemble import RandomForestClassifier
        rf_clf = RandomForestClassifier()
        rf_clf.fit(X_train, y_train)
        rfpredict = rf_clf.predict(X_test)
        print("ACCURACY")
        print(accuracy_score(y_test, rfpredict) * 100)
        print("CLASSIFICATION REPORT")
        print(classification_report(y_test, rfpredict))
        print("CONFUSION MATRIX")
        print(confusion_matrix(y_test, rfpredict))
        models.append(('RandomForestClassifier', rf_clf))
        detection_accuracy.objects.create(names="Random Forest Classifier",ratio=accuracy_score(y_test, rfpredict) * 100)

        print("KNeighborsClassifier")

        from sklearn.neighbors import KNeighborsClassifier
        kn = KNeighborsClassifier()
        kn.fit(X_train, y_train)
        knpredict = kn.predict(X_test)
        print("ACCURACY")
        print(accuracy_score(y_test, knpredict) * 100)
        print("CLASSIFICATION REPORT")
        print(classification_report(y_test, knpredict))
        print("CONFUSION MATRIX")
        print(confusion_matrix(y_test, knpredict))
        models.append(('KNeighborsClassifier', kn))
        detection_accuracy.objects.create(names="KNeighborsClassifier", ratio=accuracy_score(y_test, knpredict) * 100)

        print("Gradient Boosting Classifier")

        from sklearn.ensemble import GradientBoostingClassifier
        clf = GradientBoostingClassifier(n_estimators=100, learning_rate=1.0, max_depth=1, random_state=0).fit(X_train,y_train)
        clfpredict = clf.predict(X_test)
        print("ACCURACY")
        print(accuracy_score(y_test, clfpredict) * 100)
        print("CLASSIFICATION REPORT")
        print(classification_report(y_test, clfpredict))
        print("CONFUSION MATRIX")
        print(confusion_matrix(y_test, clfpredict))
        models.append(('GradientBoostingClassifier', clf))
        detection_accuracy.objects.create(names="Gradient Boosting Classifier",ratio=accuracy_score(y_test, clfpredict) * 100)

        classifier = VotingClassifier(models)
        classifier.fit(X_train, y_train)
        y_pred = classifier.predict(X_test)

        Fid1 = [Fid]
        vector1 = cv.transform(Fid1).toarray()
        predict_text = classifier.predict(vector1)

        pred = str(predict_text).replace("[", "")
        pred1 = pred.replace("]", "")

        prediction = int(pred1)

        if prediction == 0:
            val = 'Fraud Not Detected'
        elif prediction == 1:
            val = 'Fraud Detected'

        print(val)
        print(pred1)

        predict_ad_click_fraud_detection.objects.create(
            Fid=Fid,
            IPAddress=IPAddress,
            App_Name=App_Name,
            Device=Device,
            OS=OS,
            Channel=Channel,
            Click_time=Click_time,
            Time_to_click=Time_to_click,
            Session_duration=Session_duration,
            Mouse_movement=Mouse_movement,
            IP_frequency=IP_frequency,
            Referrer_missing=Referrer_missing,
            Scroll_depth=Scroll_depth,
            Time_on_page=Time_on_page,
            Prediction=val)

        return render(request, 'RUser/Detection_Of_Ad_Click_Fraud_Type.html',{'objs': val})
    return render(request, 'RUser/Detection_Of_Ad_Click_Fraud_Type.html')



