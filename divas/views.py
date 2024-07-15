# from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .serializer import SubmissionSerializer,LiveCompetitionsSerializer, CompetitionViewSerializer,RatingSerializer,AddWishlistSerializer,LeaderboardSerializer
from .serializer import CommunityForumSerializer, AddCommentSerializer, ViewProfileSerializer,EditProfileSerializer,PostViewSerializer
from .models.submissions import CompetitionName,Submission,Rating,WishlistPost
from .models.community_forum import Community_forum
from .models.user import Users
from django.utils import timezone

@api_view(['POST',])
def submission(request):
    try:
     if request.method =='POST':
       data={'competition_name':request.data.get("competitionId"),'username':request.data.get("userName"),
             'design_image':request.FILES.get("designImage")}
       
       db_entry = SubmissionSerializer(data=data)
       if db_entry.is_valid():
            db_entry.save()
            return Response({"success":"success"}, status=status.HTTP_201_CREATED)
       print(db_entry.errors)
       return Response({"failure":"Submission Unsuccessfull"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 

@api_view(['GET',])
def live_competition(request):
      live_competitions = CompetitionName.objects.all().filter(date_started__lte=timezone.now(), date_ended__gte=timezone.now())
      if live_competition:
       serializer = LiveCompetitionsSerializer(live_competitions, many=True)
       return Response({"data":serializer.data},status=status.HTTP_200_OK)
      else : 
        return Response({"data":"No competition Live"},status=status.HTTP_404_NOT_FOUND)
        
@api_view(['GET'])
def competition_images(request):
      competition_name = request.GET.get('competition_name', None)
      if(competition_name):
           leaderboard= Submission.objects.all().filter(competition_name=competition_name).order_by('-no_of_votes')
           if leaderboard.exists() :
               serializer=CompetitionViewSerializer(leaderboard,many=True)
               return Response({'data':serializer.data},status=status.HTTP_200_OK)
      return Response({"failure":"No Such Competition Exist"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST',])
def alter_rating_post(request):
    try:
        id=request.data.get('id')
        post=Submission.objects.get(pk=id)
        user=request.data.get("username")
        rating=int(request.data.get('rating',0))
        existing_rating = Rating.objects.filter(post=post, username=user).first()
        if existing_rating:
            existing_rating.value = rating
            existing_rating.save()
            return Response({'message': rating}, status=status.HTTP_200_OK)
        else :
         serializer = RatingSerializer(data={'post': post.id, 'username': user, 'value': rating})

         if serializer.is_valid():
            serializer.save()  
            return Response({'message': rating}, status=status.HTTP_200_OK)
         else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except  Submission.DoesNotExist:
            return Response({'error': 'Image not found'}, status=status.HTTP_404_NOT_FOUND)   
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)    
@api_view(['GET',])
def get_rating_post(request):
    try:
        id=request.GET.get('id')
        post=Submission.objects.get(pk=id)
        user=request.GET.get("username")
        existing_rating = Rating.objects.filter(post=post, username=user).first()
        if existing_rating:
           rating =existing_rating.value
        else :
          rating=0
        return Response({'rating': rating}, status=status.HTTP_200_OK)
    except  Submission.DoesNotExist:
            return Response({'error': 'Image not found'}, status=status.HTTP_404_NOT_FOUND)   
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)    

@api_view(['POST',])
def add_post_wishlist(request):
    try:
     post_id=request.data.get('id')
     post=Submission.objects.get(pk=post_id)
     user=request.data.get("username")
     print(user)
     obj= WishlistPost.objects.filter(post=post,username=user).first()
     print(obj)
     if obj:
        obj.delete()
        return Response({'message': False}, status=status.HTTP_200_OK)
     else :
        serializer = AddWishlistSerializer(data={'post': post.id, 'username': user})
        if serializer.is_valid():
                serializer.save()  
                return Response({'message': True}, status=status.HTTP_200_OK)
        else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)    
    
@api_view(['GET',])
def status_post_wishlist(request):
    try:
     post_id=request.GET.get('id')
     post=Submission.objects.get(pk=post_id)
     user=request.GET.get("username")
     obj= WishlistPost.objects.filter(post=post.id,username=user).exists()
     return Response({'message': obj}, status=status.HTTP_200_OK)
    except Exception as e:
       return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
          
@api_view(['GET',])
def leaderboard(request):
     
     competition_id=request.GET.get('id', None)
     print(competition_id)
     competition_name=CompetitionName.objects.get(pk=competition_id)
     if competition_name:
      leaderboard=Submission.objects.all().filter(competition_name=competition_name).order_by('-no_of_votes')[:10]
      serializer = LeaderboardSerializer(leaderboard,many=True)
      return Response({"data":serializer.data},status=status.HTTP_200_OK)
     return Response({"failure":"no such competition find"},status=status.HTTP_404_NOT_FOUND)


@api_view(['GET',])
def communtity_forum(request):
    try:
     start=int(request.GET.get('start',None))
     end=int(request.GET.get('end',None))
     comment=Community_forum.objects.all().order_by('-created')[start:end]

     serializer=CommunityForumSerializer(comment,many=True)
     return Response({"comment":serializer.data},status=status.HTTP_200_OK)
    except Exception as e:
       return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def add_comment_forum(request):
    try:
        comment=request.data.get('comment')
        username=request.data.get('username')
        # if comment.size <= 0:
        #      return Response({'error':'Please enter your comment'}, status=status.HTTP_400_BAD_REQUEST)
        data={'comment':comment,'commented_by':username}
        serializer=AddCommentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"comment":'comment added succesfully'},status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
       return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
        
@api_view(['GET'])
def view_profile(request):
    try:
        username=request.GET.get('id')
        profile=Users.objects.all().filter(pk=username).first()
        if profile is None:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer=ViewProfileSerializer(profile)
        return Response({"profile":serializer.data},status=status.HTTP_200_OK)
    except Exception as e:
       return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def edit_profile(request):
    try:
        username=request.data.get('username')
        about=request.data.get('about')
        profile=request.FILES.get('profilepic')
        data={'about':about,'username':username, 'profile':profile}
        serializer=EditProfileSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success':'Profile updated Succesfully'},status=status.HTTP_200_OK)
    except Exception as e:
       return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
def get_profile_posts(request):
    try:
        id=request.GET.get('id')
        posts=Submission.objects.filter(username=id)
        if posts is None:
             return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer=PostViewSerializer(posts,many=True)
        return Response({"posts":serializer.data},status=status.HTTP_200_OK)
    except Exception as e:
       return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
def get_past_competition_id(request):
    try:
         past_competition = CompetitionName.objects.filter(date_ended__lt=timezone.now()).order_by('-date_ended').first()
         if past_competition:
            past_competition_serializer = LiveCompetitionsSerializer(past_competition)
            past_competition_data = past_competition_serializer.data
         else:
            past_competition_data = None
         return Response({"data": past_competition_data}, status=status.HTTP_200_OK)
    except Exception as e:
       return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
def get_past_competition_details(request):
    try:
        competition_id = request.GET.get('competitionId', )
        if competition_id:
            leaderboard= Submission.objects.all().filter(competition_name=competition_id).order_by('-no_of_votes')[:3]
            if leaderboard.exists() :
               serializer=CompetitionViewSerializer(leaderboard,many=True)
               return Response({'data':serializer.data},status=status.HTTP_200_OK)
        return Response({"failure":"No Such Competition Exist"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
       return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_all_posts(request):
    try:
      data=Submission.objects.all()
      if data is None:
             return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
      serializer=PostViewSerializer(data,many=True)
      return Response({"data":serializer.data},status=status.HTTP_200_OK)
    except Exception as e:
       return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
          

        
