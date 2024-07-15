# views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Styling, Photos,Products
from divas.models.user import Users
from .serializers import StylingSerializer, PhotoSerializer

@api_view(['POST'])
def submit_photos(request):
  try:
    username = request.data.get('username')
    photo_files = request.FILES.getlist('photos')
    product_ids = request.data.get('product_ids')
    try:
        # Get the user instance
        user = Users.objects.get(pk=username)
    except Users.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


    # Retrieve or create the styling submission
    styling, created = Styling.objects.get_or_create(
        username=user,
    )

    for photo_file, product_id in zip(photo_files, product_ids):
        photo_serializer = PhotoSerializer(data={'photos': photo_file, 'productId': product_id})
        print(product_id)
        if photo_serializer.is_valid():
            photo = photo_serializer.save()
            styling.photo.add(photo)
        else:
            return Response(photo_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response({'message': 'Photos submitted successfully'}, status=status.HTTP_201_CREATED)
  except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
  
@api_view(['GET'])
def get_styling_with_photos(request):
    stylings = Styling.objects.all()  # Retrieve all Styling instances
    response_data = []

    for styling in stylings:
        photos = styling.photo.all()  # Retrieve associated photos
        photo_data = [{'id': photo.id, 'photo_url': photo.photos.url} for photo in photos]

        response_data.append({
            'styling_id': styling.id,
            'username': styling.username.username,
            'likes': styling.likes,
            'photos': photo_data,
        })

    return Response({'data':response_data}, status=200)

@api_view(['GET'])
def get_all_phtos(request):
 try:
    product= Products.objects.all()
    serializer=PhotoSerializer(data=product)
    if serializer.is_valid():
        return Response({'data':serializer.data},status=status.HTTP_200_OK)
    else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 

