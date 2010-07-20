from django.db import models

class URLMetatags(models.Model):
	url = models.CharField(db_column="path",max_length=255,help_text="Could be a url name or a path. Begin paths with '/'")
	title = models.TextField(null=True,blank=True,max_length=255,help_text="Will be stuck within the title attribute")
	description = models.TextField(null=True,blank=True,help_text="Meta-Description")
	keywords = models.TextField(null=True,blank=True,help_text="Meta-Keywords")
