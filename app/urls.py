from django.urls import path
from .views import SignUpAPIView,SignInAPIView,PaperCreateAPIView,AuthorCreateAPIView,HomeListAPIView,AgendaListAPIView,ConferenseSectionListAPIView,SponsorListAPIView,DirectionListAPIView



urlpatterns=[

    path('sign-up/', SignUpAPIView.as_view()),
    path('sign-in/',SignInAPIView.as_view()),
    path('author/',AuthorCreateAPIView.as_view()),
    path('paper/',PaperCreateAPIView.as_view()),
    path('home/',HomeListAPIView.as_view()),
    path('agenda/',AgendaListAPIView.as_view()),
    path('section/',ConferenseSectionListAPIView.as_view()),
    path('sponsor/',SponsorListAPIView.as_view()),
    path('direction/',DirectionListAPIView.as_view()),


   
  
    
]