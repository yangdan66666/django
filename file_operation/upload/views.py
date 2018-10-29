from django.shortcuts import render
from land.models import *
import os
# Create your views here.

def upload_views(request):
	# 请求方法为POST时,进行处理;
	if request.method == "POST":
		# 获取上传的用户名称
		nkname = request.POST['nkname']
		uname = request.POST['uname']
		#查询File表中与登录的用户一致的文件数据
		L = Files.objects.filter(uname=uname,isActive=True)
		L1 = Files.objects.filter(uname=uname,isActive=False)
		# 获取上传的文件,如果没有文件,则默认为None;
		File = request.FILES.get("myfile", None)
		if File is None:
			a='请选择上传文件!'
			return render(request,'upload/fp.html',locals())
		else:
			#判断该用户上传文件目录下是否有本次上传文件
			lujing = "./文件/"+"%s"%str(uname)+"/"+"%s"%File.name
			#用户已上传本次上传文件
			if File.name in os.listdir(r"./文件/"+"%s"%str(uname)):
				a='你已上传%s,上传失败!'%File.name
				return render(request,'upload/fp.html',locals())
			else:
				# 打开特定的文件进行二进制的写操作;
				with open(lujing,'wb+') as f:
					# 分块写入文件;
					for chunk in File.chunks():
						f.write(chunk)
				#文件信息存储到数据库
				dic={
					'wenjian':File.name,
					'lujing':lujing,
					'uname':uname,
				}
				Files(**dic).save()
				a='上传成功!!'
				return render(request,'upload/fp.html',locals())