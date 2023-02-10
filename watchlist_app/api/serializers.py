from rest_framework import serializers
from watchlist_app import models

class ReviewSerializer(serializers.ModelSerializer):
    review_user= serializers.StringRelatedField(read_only=True)
    class Meta:
        model=models.Review
        # fields='__all__'
        exclude=('watchlist',)


class WatchListSerializer(serializers.ModelSerializer):
    # len_name= serializers.SerializerMethodField()
    # reviews= ReviewSerializer(many=True,read_only=True)
    platform= serializers.CharField(source='platform.name')
    class Meta:
        model= models.WatchList
        fields= '__all__'
        # fields= ['id','name', 'description']
        # exclude= ['active']
        
class StreamPlatformSerializer(serializers.ModelSerializer):
    
    watchlist= WatchListSerializer(many=True,read_only=True)
    # watchlist = serializers.StringRelatedField(many=True)
    # watchlist = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    # watchlist = serializers.HyperlinkedIdentityField(view_name='movie-detail')
    class Meta:
        model=models.StreamPlatform
        fields='__all__'


        
    # def get_len_name(self,object):
    #     return len(object.name)
    
    # ## 1- Field level validation ##
    # def validate_name(self,value):
    #     if len(value)<2:
    #         raise serializers.ValidationError("Name is too short!")
    #     else:
    #         return value
    # ## 2- object level validation ##
    # def validate(self,data):
    #     if data['name']==data['description']:
    #         raise serializers.ValidationError("Name and Description should be different!")
    #     else:
    #         return data


# def name_length(value):
#     if len(value)<2:
#             raise serializers.ValidationError("Name is too short!")

########### Class Serializer ###########
# class MovieSerializer(serializers.Serializer):
#     id= serializers.IntegerField(read_only=True)
#     name= serializers.CharField(validators=[name_length])
#     description= serializers.CharField()
#     active= serializers.BooleanField()
    
#     def create(self, validated_data):
#         return Movie.objects.create(**validated_data)
    
#     # instance: carries the old values
#     # validated_data: carries the new values
#     def update(self,instance, validated_data):
#         instance.name= validated_data.get('name',instance.name)
#         instance.description= validated_data.get('description', instance.description)
#         instance.active= validated_data.get('active', instance.active)
#         instance.save()
#         return instance # because it has all the values
########### End Class Serializer ###########

    ###### Validation ######
    ## 1- Field level validation ##
    # def validate_name(self,value):
    #     if len(value)<2:
    #         raise serializers.ValidationError("Name is too short!")
    #     else:
    #         return value
    ## 2- object level validation ##
    # def validate(self,data):
    #     if data['name']==data['description']:
    #         raise serializers.ValidationError("Name and Description should be different!")
    #     else:
    #         return data
    ## 3- validators ##
    # see the serializer field above