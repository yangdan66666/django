from django.db import models

# Create your models here.
class Users(models.Model):
	# 密码 - CharField()
	upwd = models.CharField(max_length=18)
	# 用户名 - CharField()
	uname = models.CharField(max_length=14)
	# 用户昵称
	nkname = models.CharField(max_length=10)
	# 用户邮箱！
	email = models.EmailField(max_length=50)
	# 启用/禁用 - BooleanField(),默认值为True
	isActive = models.BooleanField(default=True)
class Files(models.Model):
	#文件名
	wenjian = models.CharField(max_length=20)
	#文件路径
	lujing = models.CharField(max_length=60)
	#拥有此文件用户
	uname = models.CharField(max_length=14)
	#用户如何拥有的文件，默认True为上传，False为别人共享
	isActive = models.BooleanField(default=True)
	#共享给我的用户名，默认为null
	shareduser = models.CharField(max_length=14)