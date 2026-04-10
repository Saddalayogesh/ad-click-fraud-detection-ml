
from django.db.models import  Count, Avg
from django.shortcuts import render, redirect
from django.db.models import Count
from django.db.models import Q
import datetime
import xlwt
import csv
from django.http import HttpResponse
import numpy as np # linear algebra
import pandas as pd

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier

# Create your views here.
from Remote_User.models import ClientRegister_Model,predict_ad_click_fraud_detection,detection_ratio,detection_accuracy,csvdatasets


def serviceproviderlogin(request):
    if request.method  == "POST":
        admin = request.POST.get('username')
        password = request.POST.get('password')
        if admin == "Admin" and password =="Admin":
            return redirect('View_Remote_Users')

    return render(request,'SProvider/serviceproviderlogin.html')

def View_Detected_Ad_Click_Fraud_Type_Ratio(request):
    detection_ratio.objects.all().delete()
    ratio = ""
    kword = 'Fraud Detected'
    print(kword)
    obj = predict_ad_click_fraud_detection.objects.all().filter(Q(Prediction=kword))
    obj1 =predict_ad_click_fraud_detection.objects.all()
    count = obj.count();
    count1 = obj1.count();
    ratio = (count / count1) * 100
    if ratio != 0:
        detection_ratio.objects.create(names=kword, ratio=ratio)

    ratio1 = ""
    kword1 = 'Fraud Not Detected'
    print(kword1)
    obj1 = predict_ad_click_fraud_detection.objects.all().filter(Q(Prediction=kword1))
    obj11 = predict_ad_click_fraud_detection.objects.all()
    count1 = obj1.count();
    count11 = obj11.count();
    ratio1 = (count1 / count11) * 100
    if ratio1 != 0:
        detection_ratio.objects.create(names=kword1, ratio=ratio1)

    obj = detection_ratio.objects.all()
    return render(request, 'SProvider/View_Detected_Ad_Click_Fraud_Type_Ratio.html', {'objs': obj})

def View_Remote_Users(request):
    obj=ClientRegister_Model.objects.all()
    return render(request,'SProvider/View_Remote_Users.html',{'objects':obj})

def ViewTrendings(request):
    topic = predict_ad_click_fraud_detection.objects.values('topics').annotate(dcount=Count('topics')).order_by('-dcount')
    return  render(request,'SProvider/ViewTrendings.html',{'objects':topic})

def charts(request,chart_type):
    chart1 = detection_ratio.objects.values('names').annotate(dcount=Avg('ratio'))
    return render(request,"SProvider/charts.html", {'form':chart1, 'chart_type':chart_type})

def charts1(request,chart_type):
    chart1 = detection_accuracy.objects.values('names').annotate(dcount=Avg('ratio'))
    return render(request,"SProvider/charts1.html", {'form':chart1, 'chart_type':chart_type})

def View_Detected_Ad_Click_Fraud_Type(request):
    obj =predict_ad_click_fraud_detection.objects.all()
    return render(request, 'SProvider/View_Detected_Ad_Click_Fraud_Type.html', {'list_objects': obj})

def likeschart(request,like_chart):
    charts =detection_accuracy.objects.values('names').annotate(dcount=Avg('ratio'))
    return render(request,"SProvider/likeschart.html", {'form':charts, 'like_chart':like_chart})

def Upload_Datasets(request):
    if "GET" == request.method:
        return render(request, 'SProvider/Upload_Datasets.html', {})
    else:

        csvdatasets.objects.all().delete()

        csv_file = request.FILES['csv_file'].read().decode('utf-8').splitlines()
        csv_reader = csv.DictReader(csv_file)

        for row in csv_reader:
            csvdatasets.objects.create(
                Fid=row['Fid'],
                IPAddress=row['IPAddress'],
                App_Name=row['App_Name'],
                Device=row['Device'],
                OS=row['OS'],
                Channel=row['Channel'],
                Click_time=row['Click_time'],
                Time_to_click=row['Time_to_click'],
                Session_duration=row['Session_duration'],
                Mouse_movement=row['Mouse_movement'],
                IP_frequency=row['IP_frequency'],
                Referrer_missing=row['Referrer_missing'],
                Scroll_depth=row['Scroll_depth'],
                Time_on_page=row['Time_on_page'],
            )

    obj = csvdatasets.objects.all()

    return render(request, 'SProvider/Upload_Datasets.html', {'csvdatasets': obj})



def Download_Trained_DataSets(request):

    response = HttpResponse(content_type='application/ms-excel')
    # decide file name
    response['Content-Disposition'] = 'attachment; filename="PredictedData.xls"'
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
    obj = predict_ad_click_fraud_detection.objects.all()
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
        ws.write(row_num, 14, my_row.Prediction, font_style)

    wb.save(response)
    return response

def Train_Test_DataSets(request):
    detection_accuracy.objects.all().delete()

    df = pd.read_csv('Datasets.csv', encoding='latin-1')


    df['label'] = df.Label.apply(lambda x: 1 if x == 1 else 0)
    df.head()


    X = df['Fid']
    y = df['label']

    print("Fid")
    print(X)
    print("Label")
    print(y)

    cv = CountVectorizer()
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
    detection_accuracy.objects.create(names="Deep Neural Network(DNN)", ratio=accuracy_score(y_test, y_pred) * 100)

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
    detection_accuracy.objects.create(names="Random Forest Classifier", ratio=accuracy_score(y_test, rfpredict) * 100)


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
    detection_accuracy.objects.create(names="KNeighborsClassifier", ratio=accuracy_score(y_test, knpredict) * 100)

    print("Gradient Boosting Classifier")

    from sklearn.ensemble import GradientBoostingClassifier
    clf = GradientBoostingClassifier(n_estimators=100, learning_rate=1.0, max_depth=1, random_state=0).fit(
        X_train,
        y_train)
    clfpredict = clf.predict(X_test)
    print("ACCURACY")
    print(accuracy_score(y_test, clfpredict) * 100)
    print("CLASSIFICATION REPORT")
    print(classification_report(y_test, clfpredict))
    print("CONFUSION MATRIX")
    print(confusion_matrix(y_test, clfpredict))
    models.append(('GradientBoostingClassifier', clf))
    detection_accuracy.objects.create(names="Gradient Boosting Classifier",ratio=accuracy_score(y_test, clfpredict) * 100)

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

    predicts = 'LabledData.csv'
    df.to_csv(predicts, index=False)
    df.to_markdown

    obj = detection_accuracy.objects.all()


    return render(request,'SProvider/Train_Test_DataSets.html', {'objs': obj})