from django.db import models

# Create your models here.

class Xinlang(models.Model):
	# 新闻时间 
	pub_time = models.DateTimeField()
	# 时间ID 
	time_id = models.CharField(max_length=255)
	# 新闻内容
	news = models.CharField(max_length=1000)

	class Meta:
		db_table = 'xinlang'