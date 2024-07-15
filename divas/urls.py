from django.urls import path
from .views import live_competition,competition_images,alter_rating_post,add_post_wishlist,leaderboard,get_rating_post,status_post_wishlist,communtity_forum,add_comment_forum,view_profile,edit_profile,get_all_posts,get_profile_posts,submission,get_past_competition_details,get_past_competition_id


urlpatterns=[
    path('competitionname/',live_competition),
    path('competitionentries/',competition_images),
    path('ratepost/',alter_rating_post),
    path('wishlist/',add_post_wishlist),
    path('leaderboard/',leaderboard),
    path('getrating/',get_rating_post),
    path('wishlist/status',status_post_wishlist),
    path('community/show/',communtity_forum),
    path('community/add/',add_comment_forum),
    path('profile/',view_profile),
    path('profile/edit',edit_profile),
    path('posts/',get_profile_posts),
    path('submission/',submission),
    path('competition/winner/',get_past_competition_details),
    path('competition/pastid/',get_past_competition_id),
    path('allposts/',get_all_posts)
]