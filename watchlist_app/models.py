from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

class StreamPlatform(models.Model):
    name= models.CharField(max_length=30)
    about= models.CharField(max_length=150)
    website= models.URLField(max_length=100)
    
    def __str__(self):
        return self.name
    
class WatchList(models.Model):
    title= models.CharField(max_length=50)
    storyline= models.CharField(max_length=200)
    platform= models.ForeignKey(StreamPlatform, on_delete=models.CASCADE, related_name='watchlist') # one movie, one watch show, one web series can has one plateform
    # on_delete means if I delete this YouTube, all the videos from this watchlist should deleted
    active= models.BooleanField(default=True)
    avg_rating= models.FloatField(default=0)
    number_rating=models.IntegerField(default=0)
    created=models.DateField(auto_now_add=True) # once you send a post request with some content so this is going to have 'auto_now_add=True'
    
    def __str__(self):
        return self.title

class Review(models.Model):
    review_user= models.ForeignKey(User,on_delete=models.CASCADE)
    rating= models.PositiveIntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    description= models.CharField(max_length=200,null=True)
    watchlist= models.ForeignKey(WatchList,on_delete=models.CASCADE,related_name='reviews')
    active=models.BooleanField(default=True) # if active was true so it's a valid review otherwise its fake review
    created= models.DateTimeField(auto_now_add=True)
    updated= models.DateTimeField(auto_now=True) # every time we update, our time will be updated
    
    def __str__(self):
        return str(self.rating) + ' | ' + self.watchlist.title + ' | ' + str(self.review_user)