from django.contrib import admin
from django.urls import path
from Remote_User import views as remoteuser
from Service_Provider import views as serviceprovider
from ad_click_fraud_detection import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', remoteuser.login, name="login"),
    path('Register1/', remoteuser.Register1, name="Register1"),
    path('Detection_Of_Ad_Click_Fraud_Type/', remoteuser.Detection_Of_Ad_Click_Fraud_Type, name="Detection_Of_Ad_Click_Fraud_Type"),
    path('ViewYourProfile/', remoteuser.ViewYourProfile, name="ViewYourProfile"),
    path('serviceproviderlogin/', serviceprovider.serviceproviderlogin, name="serviceproviderlogin"),
    path('View_Remote_Users/', serviceprovider.View_Remote_Users, name="View_Remote_Users"),
    
    path('charts/<str:chart_type>/', serviceprovider.charts, name="charts"),
    path('charts1/<str:chart_type>/', serviceprovider.charts1, name="charts1"),
    path('likeschart/<str:like_chart>/', serviceprovider.likeschart, name="likeschart"),
    
    path('Upload_Datasets/', serviceprovider.Upload_Datasets, name="Upload_Datasets"),
    path('Download_Uploaded_Datasets/', remoteuser.Download_Uploaded_Datasets, name="Download_Uploaded_Datasets"),
    path('View_Detected_Ad_Click_Fraud_Type_Ratio/', serviceprovider.View_Detected_Ad_Click_Fraud_Type_Ratio, name="View_Detected_Ad_Click_Fraud_Type_Ratio"),
    path('Train_Test_DataSets/', serviceprovider.Train_Test_DataSets, name="Train_Test_DataSets"),
    path('View_Detected_Ad_Click_Fraud_Type/', serviceprovider.View_Detected_Ad_Click_Fraud_Type, name="View_Detected_Ad_Click_Fraud_Type"),
    path('Download_Trained_DataSets/', serviceprovider.Download_Trained_DataSets, name="Download_Trained_DataSets"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)