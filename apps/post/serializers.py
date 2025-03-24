from rest_framework import serializers
from .models import *

from django.contrib.auth import get_user_model

User = get_user_model()

def get_user_id(request):
    if(not request.user.is_authenticated):
        return 0
    token = f'{request.user}'.strip(' ')[-1]
    user_id = int(token)
    return user_id

# TODO : do this
# class CommentCreateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Comment
    


class CommentListSerializer(serializers.ModelSerializer):
    
    author = author = serializers.SerializerMethodField()
    
    class Meta:
        model = Comment
        fields = ['id', 'post', 'date_posted', 'content', 'author']
        
    def get_author(self, obj:Post):
        return f'{obj.author.first_name} {obj.author.last_name}'
    

class Authorserializer(serializers.ModelSerializer):
    
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['image', 'full_name']
        
    def get_full_name(self, obj : User):
        return f'{obj.first_name} {obj.last_name}'
        
        

class PostViewSerializer(serializers.ModelSerializer):
    
    likes = serializers.SerializerMethodField()
    comment = serializers.SerializerMethodField()
    
    author = Authorserializer()
    
    flag = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = ['id', 'description', 'date_posted', 'image', 'likes','author', 'comment', 'flag']
        
    # def get_author(self, obj:Post):
    #     return f'{obj.author.first_name} {obj.author.last_name}'

    def get_likes(self, obj : Post):
        return obj.likers.count()
    
    def get_flag(self, obj: Post):
        user_id = get_user_id(self.context['request'])
        user = User.objects.filter(id=user_id).first()
        if(user in list(obj.likers.all())):
            return 1
        return 0
    
    def get_comment(self, obj : Comment):
        return CommentListSerializer(obj.comment_set, many=True).data


class PostCreateSerializer(serializers.ModelSerializer):
        
    class Meta:
        model = Post
        fields = ['description', 'image']
        
    def create(self, validated_data):
        
        user_id = get_user_id(self.context['request'])
        
        user = User.objects.get(id=user_id)
        
        return Post.objects.create(
            author = user,
            **validated_data
        )
        
class LikeSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    
    def validate_id(self, val):
        
        if Post.objects.filter(id = val).exists():
            return val
        else:
            raise serializers.ValidationError("This Post does not exists.")
        