from django.urls import path
from .views import *

urlpatterns = [
    path('partners', PartnerListView.as_view(), name='partner-list'),
    path('suggestions', SuggestionListView.as_view(), name='suggestion-list'),
    path('user_exists', CheckUserView.as_view(), name='check-user-exists'),
    path('registration-request', RegisterRequestView.as_view(), name='registration-request'),
    path('registration-confirm', RegisterView.as_view(), name='registration-request'),
    path('login', LoginView.as_view(), name='login'),
    path('user', UserView.as_view(), name='get-user-info'),
    path('documents', UserDocuments.as_view(), name='get-user-documents'),
    path('documents/<id>', UserDocumentsById.as_view(), name='get-application-by-id'),
    path('upload_document', UploadDocumentView.as_view(), name='upload-document'),
    path('application', ApplicationView.as_view(), name='get-application'),
    path('applications', ApplicationAdminView.as_view(), name='get-all-applications'),
    path('application/<id>', ApplicationByIdView.as_view(), name='getapplication-by-id'),
    path('approve', ApproveApplicationView.as_view(), name='approve-application'),
    path('universities/<search>', UniversitiesView.as_view(), name='get-universities'),
    path('university/<slug>', UniversityBySlugView.as_view(), name='university-by-slug'),
    path('user/update/<str:field>/', update_user, name='update_user'),
    path('document/update/<str:id>', EditDocumentStatusView.as_view(), name='edit-document-status'),
    path('submit-suggestion', SubmitSuggestionView.as_view(), name='submit-suggestion'),
    path('request-for-partnership', SubmitPartnerView.as_view(), name='submit-suggestion'),

]
