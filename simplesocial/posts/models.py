from django.db import models
from django.urls import reverse
# Create your models here.
#posts models.py
#reverse is used to where to send it back to when posted
import misaka
#misaka is used so that people can use markdown
from groups.models import Group

from django.contrib.auth import get_user_model
User=get_user_model()
#that is how we can link the post to current user who is logged in

class Post(models.Model):
    user=models.ForeignKey(User,related_name='posts',on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now=True)
    #auto now automatically generates the time when posted a post no need to type manually. This will be available for admin. It can be displayed or not.
    message=models.TextField()
    message_html=models.TextField(editable=False)
    #message_html is html markdown version of messages written above
    group=models.ForeignKey(Group,related_name='posts',null=True,blank=True,on_delete=models.CASCADE)

    def __str__(self):
        return self.message
    
    def save(self,*args,**kwargs):
        self.message_html=misaka.html(self.message)
        super().save(*args,**kwargs)

    def get_absolute_url(self):
        return reverse('posts:single',kwargs={'username':self.user.username,
                                              'pk':self.pk})
    class Meta:
        ordering=['-created_at']
        unique_together=['user','message']

