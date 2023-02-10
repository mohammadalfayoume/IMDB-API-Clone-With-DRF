# from django.shortcuts import render
# from watchlist_app.models import Movie
# from django.http import JsonResponse # to return a json response formatted
# # Create your views here.

# # create a request to get all movies from database
# def movie_list(request):
#     movies= Movie.objects.all() # all objects in the Movie model avaliable as query set but we can't return them directly, we have to return them in the JSON format
#     # movies.values() to make the objects in a dictionary format
#     data= {
#         'movies': list(movies.values())
#     }
#     return JsonResponse(data)

# # create a request to specific movie from database
# def movie_details(request,pk):
#     movie= Movie.objects.get(pk=pk)
#     data={
#         'name': movie.name,
#         'description': movie.description,
#         'active': movie.active
#     }
    
#     return JsonResponse(data)