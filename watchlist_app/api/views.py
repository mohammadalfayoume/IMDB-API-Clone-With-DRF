from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
# from rest_framework import mixins
from rest_framework import filters, generics, status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.throttling import (AnonRateThrottle, ScopedRateThrottle,
                                       UserRateThrottle)
# from rest_framework.decorators import api_view
from rest_framework.views import APIView

from watchlist_app.api import pagination, permissions, serializers, throttling
from watchlist_app.models import Review, StreamPlatform, WatchList


########## Class Based View using generic class-based views  ##########
class UserReview(generics.ListAPIView):
    # queryset= Review.objects.all()
    serializer_class=serializers.ReviewSerializer
    # permission_classes = [IsAuthenticated]
    # throttle_classes = [throttling.ReviewListThrottle,AnonRateThrottle]
    
    # Filtering against the current user
    # def get_queryset(self):
    #     username= self.kwargs['username']
    #     return Review.objects.filter(review_user__username=username)   
    
    # Filtering against query parameters
    def get_queryset(self):
        username = self.request.query_params.get('username')
        return Review.objects.filter(review_user__username=username)   


class ReviewCreate(generics.CreateAPIView):
    serializer_class= serializers.ReviewSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [throttling.ReviewCreateThrottle]
    
    def get_queryset(self):
        return Review.objects.all()
    
    def perform_create(self, serializer):
        pk=self.kwargs.get('pk')
        movie=WatchList.objects.get(pk=pk)

        review_user= self.request.user # now I have access on user who create a review
        review_queryset= Review.objects.filter(watchlist=movie, review_user=review_user) # here I want to filter objects based on watchlist and review_user
        if review_queryset.exists():
            raise ValidationError("You have already reviewed this movie!")
        
        if movie.number_rating==0:
            movie.avg_rating=serializer.validated_data['rating']
        else:
            movie.avg_rating= (movie.avg_rating+ serializer.validated_data['rating'])/2
        
        movie.number_rating= movie.number_rating+1
        movie.save()
        
        serializer.save(watchlist=movie, review_user=review_user)

class ReviewList(generics.ListAPIView):
    # queryset= Review.objects.all()
    serializer_class=serializers.ReviewSerializer
    # permission_classes = [IsAuthenticated]
    throttle_classes = [throttling.ReviewListThrottle,AnonRateThrottle]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['review_user__username', 'active']
    
    def get_queryset(self):
        pk= self.kwargs['pk']
        return Review.objects.filter(watchlist=pk)    

class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset= Review.objects.all()
    serializer_class=serializers.ReviewSerializer
    # permission_classes = [AdminOrReadOnly]
    permission_classes = [permissions.IsReviewUserOrReadOnly]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope= 'review-detail'

class WatchListGV(generics.ListAPIView):
    queryset= WatchList.objects.all()
    serializer_class=serializers.WatchListSerializer
    # pagination_class= pagination.WatchListPagination
    # pagination_class= pagination.WatchListLOPagination
    pagination_class= pagination.WatchListCPagination
    # permission_classes = [IsAuthenticated]
    throttle_classes = [throttling.ReviewListThrottle,AnonRateThrottle]
    
    # Filter
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['title', 'platform__name']
    # Search
    # filter_backends = [filters.SearchFilter]
    # search_fields = ['title', 'platform__name']
    # Order
    # filter_backends = [filters.OrderingFilter]
    # ordering_fields = ['avg_rating']

########## End Class Based View using generic class-based views  ##########


########## Class Based View using Mixins ##########
# class ReviewDetail(mixins.RetrieveModelMixin, generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = serializers.ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)

# mixins.ListModelMixin: it means I need to perform a get request for list
# mixins.CreateModelMixin: it means I need to perform a post request which is going to be create
# class ReviewList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
#     # queryset, serializer_class => attribute names we can't change them
#     queryset = Review.objects.all()
#     serializer_class = serializers.ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)
########## End Class Based View using Mixins ##########

########## Model ViewSet ###########
# class StreamPlatformVS(viewsets.ReadOnlyModelViewSet):
#     queryset = StreamPlatform.objects.all()
#     serializer_class = serializers.StreamPlatformSerializer
class StreamPlatformVS(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAdminOrReadOnly]
    queryset = StreamPlatform.objects.all()
    serializer_class = serializers.StreamPlatformSerializer
########## End Model ViewSet ###########

########## ViewSet ###########
# class StreamPlatformVS(viewsets.ViewSet):
#     """
#     A simple ViewSet for listing or retrieving users.
#     """
#     def list(self, request):
#         queryset = StreamPlatform.objects.all()
#         serializer = serializers.StreamPlatformSerializer(queryset, many=True)
#         return Response(serializer.data)

#     def retrieve(self, request, pk=None):
#         queryset = StreamPlatform.objects.all()
#         watchlist = get_object_or_404(queryset, pk=pk)
#         serializer = serializers.StreamPlatformSerializer(watchlist)
#         return Response(serializer.data)
    
#     def create(self,request):
#         serializer=serializers.StreamPlatformSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)
    
#     def destroy(self,request,pk):
#         stream= StreamPlatform.objects.get(pk=pk)
#         stream.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
########## End ViewSet ###########
########### Class Based View ###########
class StreamPlatformAV(APIView):
    permission_classes = [permissions.IsAdminOrReadOnly]
    def get(self,request):
        platform=StreamPlatform.objects.all()
        serializer=serializers.StreamPlatformSerializer(platform,many=True)
        # serializer=serializers.StreamPlatformSerializer(platform,many=True,context={'request': request})
        return Response(serializer.data)
    def post(self,request):
        serializer=serializers.StreamPlatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

class StreamPlatformDetailAV(APIView):
    permission_classes = [permissions.IsAdminOrReadOnly]
    def get(self,request,pk):
        try:
            stream=StreamPlatform.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response({'Error': 'not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer=serializers.StreamPlatformSerializer(stream)
        return Response(serializer.data)
    
    def put(self,request,pk):
        stream= StreamPlatform.objects.get(pk=pk)
        serializer= serializers.StreamPlatformSerializer(stream,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk):
        stream= StreamPlatform.objects.get(pk=pk)
        stream.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
class WatchListAV(APIView):
    permission_classes = [permissions.IsAdminOrReadOnly]
    def get(self,request):
        movies= WatchList.objects.all()
        serializer= serializers.WatchListSerializer(movies,many=True)
        return Response(serializer.data)


    def post(self,request):
        serializer= serializers.WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

class WatchListDetailAV(APIView):
    permission_classes = [permissions.IsAdminOrReadOnly]
    def get(self,request,pk):
        try:
            movie=WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response({'Error': 'not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer=serializers.WatchListSerializer(movie)
        return Response(serializer.data)
    
    def put(self,request,pk):
        movie= WatchList.objects.get(pk=pk)
        serializer= serializers.WatchListSerializer(movie,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk):
        movie= WatchList.objects.get(pk=pk)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
########### End Class Based View ###########
    
########## Function Based View ##########

# @api_view(['GET', 'POST']) # default method is GET
# def movie_list(request):
#     if request.method=='GET': # here I want to send the data to user so I want to return response of data
#         movies= Movie.objects.all()
#         serializer= MovieSerializer(movies,many=True)
#         return Response(serializer.data)
#     if request.method=='POST': # here I want to recive data from user and save it in database so I will not return anything
#         serializer= MovieSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)

# @api_view(['GET', 'PUT','DELETE'])
# def movie_details(request, pk):
#     if request.method=='GET':
#         try:
#             movie=Movie.objects.get(pk=pk)
#         except Movie.DoesNotExist:
#             return Response({'Error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)
        
#         serializer=MovieSerializer(movie)
#         return Response(serializer.data)
    
#     if request.method=='PUT':
#         movie= Movie.objects.get(pk=pk)
#         serializer= MovieSerializer(movie,data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
#     if request.method=='DELETE':
#         movie= Movie.objects.get(pk=pk)
#         movie.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

########## End Function Based View ##########