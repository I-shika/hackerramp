from django.db import models
from django.utils import timezone
from .user import Users
from math import log

class CompetitionName(models.Model):
    competition_name=models.CharField(max_length=100,verbose_name="Competition Name")
    date_started=models.DateTimeField()
    date_ended=models.DateTimeField()

class Submission(models.Model):
    username=models.ForeignKey(Users, related_name='user',on_delete=models.CASCADE)
    no_of_votes=models.BigIntegerField(default=0)
    design_image=models.ImageField(verbose_name="designs",upload_to='images/')
    wishlist_no=models.BigIntegerField(default=0)
    created=models.DateTimeField(default=timezone.now)
    updated=models.DateTimeField(auto_now=True)
    competition_name=models.ForeignKey(CompetitionName,on_delete=models.CASCADE)
    def update_ratings(self):
        # Use the default reverse relation name 'rating_set'
        ratings = self.rating_set.all()
        total_value = sum(rating.value for rating in ratings)
        no_of_ratings = ratings.count()

        # Calculate average rating
        if no_of_ratings > 0:
            average_rating = total_value / no_of_ratings
        else:
            average_rating = 0

        # Update no_of_votes with the average rating
        self.no_of_votes = average_rating
        # Update the user's ranking based on the formula
        self.username.ranking = average_rating + (0.5 * log(no_of_ratings + 1))
        self.save()
        self.username.save()



class Rating(models.Model):
    username=models.ForeignKey(Users, on_delete=models.CASCADE)
    post = models.ForeignKey(Submission, on_delete=models.CASCADE)
    value=models.IntegerField()
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.post.update_ratings()

    def delete(self, *args, **kwargs):
        post = self.post
        super().delete(*args, **kwargs)
        post.update_ratings()

    class Meta:
        unique_together = ('username', 'post')

class WishlistPost(models.Model):
    post=models.ForeignKey(Submission, on_delete=models.CASCADE)
    username=models.ForeignKey(Users, on_delete=models.CASCADE)

