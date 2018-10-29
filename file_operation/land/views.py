from django.shortcuts import render
from .models import *
import os

# Create your views here.

def login_views(request):
	if request.method == 'GET':
		return render(request,'land/login.html')
	elif request.method == 'POST':
		uname = request.POST['uname']
		upwd = request.POST['upwd']
		uList = Users.objects.filter(uname=uname,upwd=upwd)
		if uList:
			#登陆失败
			if uList[0].isActive is False:
				a='该用户已被禁用!'
				return render(request,'land/login.html',locals())
			#登陆成功
			elif uList[0].isActive is True:
				nkname=uList[0].nkname
				#查询数据库wenjian表将用户名为uname的相关数据列表传输给浏览器
				L = Files.objects.filter(uname=uname,isActive=True)
				L1 = Files.objects.filter(uname=uname,isActive=False)
				return render(request,'upload/fp.html',locals())
		#登陆失败
		else:
			a='用户或密码错误!'
			return render(request,'land/login.html',locals())

def register_views(request):
	if request.method == 'GET':
		return render(request,'land/register.html')
	elif request.method == 'POST':
		uname = request.POST['uname']
		upwd = request.POST['upwd']
		nkname = request.POST['nkname']
		uemail =request.POST['uemail']
		uList = Users.objects.filter(uname=uname)
		uList1 = Users.objects.filter(nkname=nkname)
		#注册失败
		if uList:
			a='注册失败!用户名已存在!'
			return render(request,'land/register.html',locals())
		elif uList1:
			a='用户昵称已存在!请重新注册!'
			return render(request,'land/register.html',locals())
		#注册成功
		else:
			#用户信息导入数据库
			dic={
				'uname':uname,'upwd':upwd,'nkname':nkname,'email':uemail
			}
			Users(**dic).save()
			#在服务器存储文件下创建注册用户名的文件夹用来存储用户上传文件以及区分
			LJ='./文件'
			folder_name='%s'%str(uname)
			if os.path.isdir(LJ):
				os.mkdir(os.path.join(LJ,folder_name))
				b='注册成功！'
				return render(request,'land/login.html',locals())