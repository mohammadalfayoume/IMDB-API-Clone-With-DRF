from django.urls import include, path
from rest_framework.routers import DefaultRouter

# from watchlist_app.api.views import movie_list,movie_details
from watchlist_app.api import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register('stream',views.StreamPlatformVS ,basename='streamplatform')


urlpatterns = [
    path('', views.WatchListAV.as_view(), name='movie-list'),
    path('<int:pk>/', views.WatchListDetailAV.as_view(), name='movie-detail'),

    path('list2/', views.WatchListGV.as_view(), name='watch-list'),
    
    
    path('',include(router.urls)),
    # path('stream/',views.StreamPlatformAV.as_view(), name='stream'),
    # path('stream/<int:pk>',views.StreamPlatformDetailAV.as_view(),name='stream-detail'),
    
    # create a review for a particular movie
    path('<int:pk>/reviews/create/',views.ReviewCreate.as_view(),name='review-create'),
    # this mean it's going to return all the reviews for specific movie
    path('<int:pk>/reviews/',views.ReviewList.as_view(),name='review-list'),
    # this will return individual review
    path('reviews/<int:pk>/',views.ReviewDetail.as_view(),name='review-detail'),
    
    # Filtering against the current user
    # path('reviews/<str:username>/',views.UserReview.as_view(),name='user-review-detail'),
    
    # Filtering against query parameters
    path('user-reviews/',views.UserReview.as_view(),name='user-review-detail'),
    
    # path('review/',views.ReviewList.as_view(),name='review-list'),
    # path('review/<int:pk>',views.ReviewDetail.as_view(),name='review-detail'),
]
