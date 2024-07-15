from django.contrib import admin

# Register your models here.
from .models.submissions import CompetitionName,Submission,Rating,WishlistPost
from .models.community_forum import Community_forum
from .models.user import Users

admin.site.register(CompetitionName)
admin.site.register(Submission)
admin.site.register(Rating)
admin.site.register(WishlistPost)
admin.site.register(Community_forum)
admin.site.register(Users)
