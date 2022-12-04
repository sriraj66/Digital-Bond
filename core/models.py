from django.db import models
from django.contrib.auth.models import User

    

class Department(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,default=0)
    name = models.CharField(max_length=255,blank=True,unique=True)
    desc = models.TextField()
    url_img = models.URLField(default="https://upload.wikimedia.org/wikipedia/commons/thumb/d/d1/Image_not_available.png/640px-Image_not_available.png")
    active = models.BooleanField(default=True)
    crisis = models.TextField()
    allocation_amount = models.IntegerField(default=0)

    presentation_url = models.URLField(default="")
    fund = models.FloatField(blank=True,default=0)
    eth = models.FloatField(blank=True,default=0)
    # hidden
    raised = models.BooleanField(default=False)
    email = models.EmailField()
    metamask_id = models.CharField(max_length=255)
    # times
    deadline = models.DateField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f"{self.name}"


class Inverst(models.Model):
    dept = models.ForeignKey(Department, on_delete=models.CASCADE )
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    org = models.CharField(max_length=255)
    amount = models.FloatField(default=0.0)
    id_proff = models.FileField(upload_to='idproof/')
    income_certificate = models.FileField(upload_to='income/')
    is_approved = models.BooleanField(default=False)
    email = models.EmailField()
    metamask_id = models.CharField(max_length=255,default='',blank=True)

    transction_hash = models.CharField(max_length=255,blank=True)
    passbook_copy = models.FileField(upload_to='passbook/')

    created = models.DateTimeField(auto_now_add=True)
    # updated = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f"{self.name}"

class InversterProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fname = models.CharField(blank=True,max_length=255)
    lname = models.CharField(blank=True,max_length=255)
    profile = models.ImageField(blank=True,upload_to='profile/')
    dob = models.DateField(blank=True)
    email = models.EmailField(blank=True)
    phone = models.IntegerField(blank=True)
    address = models.TextField(blank=True)
    org = models.CharField(max_length=255,blank=True)
    id_proff = models.FileField(upload_to='profileid/',blank=True)
    social_media = models.URLField(default='',blank=True)

    metamask_id = models.CharField(default='',blank=True,max_length=255)

    
    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.fname+self.lname


