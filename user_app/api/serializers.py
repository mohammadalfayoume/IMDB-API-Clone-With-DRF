from django.contrib.auth.models import User
from rest_framework import serializers

class RegistrationSerializer(serializers.ModelSerializer):
    password2= serializers.CharField(style={'input_type':'password'}, write_only=True)
    class Meta:
        model= User
        fields=['username','email','password','password2']
        extra_kwargs={
            'password': {'write_only':True}
        }
    # Here we want to varify the user
    def save(self):
        # we want to check I the passwords match or not
        password=self.validated_data['password']
        password2=self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({'error':'P1 and P2 should be same!'})
        # we want to check if the email is exist or not
        if User.objects.filter(email=self.validated_data['email']).exists():
            raise serializers.ValidationError({'error':'Email already exists!'})
        # we want to send new instance carry username and email
        account= User(email=self.validated_data['email'],username=self.validated_data['username'])
        account.set_password(password)
        account.save()
        
        return account