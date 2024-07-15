# from divas.models.community_forum import Community_forum
from divas.models.submissions import Submission, CompetitionName,Rating,WishlistPost
from divas.models.community_forum import Community_forum
from rest_framework import serializers
from .models.user import Users


class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model= Submission
        fields=['username','design_image','competition_name']

class LiveCompetitionsSerializer(serializers.ModelSerializer):
    class Meta:
        model= CompetitionName
        exclude=['date_started','date_ended']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users  # Your user model
        fields = ['id', 'username']

class CompetitionViewSerializer(serializers.ModelSerializer):
    username = UserSerializer()
    class Meta:
        model=Submission
        exclude=['created','updated']

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model=Rating
        fields = '__all__'

class AddWishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model=WishlistPost
        fields='__all__'

class LeaderboardSerializer(serializers.ModelSerializer):
   
    username = UserSerializer()
    class Meta:
        model=Submission
        fields=['no_of_votes','design_image','username']


class CommunityForumSerializer(serializers.ModelSerializer):
    commented_by = serializers.StringRelatedField()
    class Meta:
        model=Community_forum
        exclude=['updated',]
class AddCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Community_forum
        exclude=['updated','created']

class PostViewSerializer(serializers.ModelSerializer):

    username = UserSerializer()
    class Meta:
        model=Submission
        fields=['username','design_image','no_of_votes']

class ViewProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=Users
        fields='__all__'

class EditProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=Users
        include=['about','profile','username']

