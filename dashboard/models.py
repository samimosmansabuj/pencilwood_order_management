from django.db import models

class Site_Settings(models.Model):
    fav_icon = models.ImageField(upload_to='logo/', blank=True, null=True)
    logo = models.ImageField(upload_to='logo/', blank=True, null=True)
    website_name = models.CharField(max_length=200, blank=True, null=True)
    website_title = models.CharField(max_length=1000, blank=True, null=True)
    copyright_company = models.CharField(max_length=200)
    copyright_year = models.CharField(max_length=4)
    
    def __str__(self) -> str:
        return f'Settings {self.id}'


