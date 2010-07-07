from django.db import models

class URLMetatags(models.Model):
	path = models.CharField(max_length=255)
	title = models.CharField(null=True,blank=True,max_length=255)
	description = models.TextField(null=True,blank=True)
	keywords = models.TextField(null=True,blank=True)
	def as_dict(self):
		return self
