from django.shortcuts import render
from land.models import *
import os
from django.http import HttpResponse,HttpResponseRedirect,StreamingHttpResponse
# Create your views here.

def wother_views(request):
	#我上传的文件
	if request.method=='GET':
		nkname=request.GET['nkname']
		uname=request.GET['uname']
		L=Files.objects.filter(uname=uname,isActive=True)
		a='只能操作单个文件'
		return render(request,'other/file.html',locals())
	elif request.method=='POST':
		#获取登陆用户
		uname=request.POST['uname']
		#获取登陆用户的昵称
		nkname=Users.objects.get(uname=uname).nkname
		#获取要共享给的用户
		yonghu=request.POST['yonghu']
		#获取要共享出去的文件
		file=request.POST['wenjian']
		#得到登陆用户所有上传的文件L
		L=Files.objects.filter(uname=uname,isActive=True)
		L1=Files.objects.filter(uname=uname,isActive=False)
		#查看文件表中file文件是否为登陆用户上传，
		list1=Files.objects.filter(uname=uname,wenjian=file,isActive=True)
		#查看用户表是否存在yonghu的数据
		user_list=Users.objects.filter(uname=yonghu)
		if list1 :
			#如果是登陆用户上传，再判断共享给的用户yonghu是否拥有file文件
			list2=Files.objects.filter(uname=yonghu,lujing=list1[0].lujing,wenjian=file)
			if len(user_list)==0:
				a='%s'%yonghu+'不存在'
				return render(request,'other/file.html',locals())
			elif yonghu=='' or yonghu==uname:
				a='请选择要共享的用户'
				return render(request,'other/file.html',locals())
			elif list2 :
				#共享给的用户拥有file文件！共享不成功
				a='%s'%yonghu+'已拥有'+'%s'%file
				return render(request,'other/file.html',locals())
			else:
				#共享隔得用户没有file文件，添加数据到数据库保存，共享成功
				dic={'wenjian':file,'lujing':list1[0].lujing,'uname':yonghu,'isActive':False,'shareduser':uname}
				Files(**dic).save()
				a='共享成功'
				return render(request,'other/file.html',locals())
		else:
			#如果不是登陆用户上传，获取file文件信息，
			list3=Files.objects.filter(uname=uname,wenjian=file,isActive=False)
			#判断file文件是否已有用户共享给要共享的用户
			list4=Files.objects.filter(uname=yonghu,wenjian=file,lujing=list3[0].lujing)
			if len(user_list)==0:
				a='%s'%yonghu+'不存在'
				return render(request,'other/file.html',locals())
			elif yonghu=='' or yonghu==uname:
				a='请选择要共享的用户'
				return render(request,'other/file1.html',locals())
			elif list4 :
				#如果需共享的用户已拥有file文件
				a='%s'%yonghu+'已拥有'+'%s'%file
				return render(request,'other/file1.html',locals())
			else:
				#如果需共享的用户没有file文件，添加数据保存数据库，共享成功
				dic={'wenjian':file,'lujing':list3[0].lujing,'uname':yonghu,'isActive':False,'shareduser':uname}
				Files(**dic).save()
				a='共享成功'
				return render(request,'other/file1.html',locals())

def other_views(request):
	#别人共享给我的文件
	if request.method=='GET':
		nkname=request.GET['nkname']
		uname=request.GET['uname']
		L1=Files.objects.filter(uname=uname,isActive=False)
		return render(request,'other/file1.html',locals())

def open_views(request):
	if request.method=='GET':
		file=request.GET['i']
		uname=request.GET['uname']
		l=Files.objects.get(uname=uname,wenjian=file)
		f=open(l.lujing,'rb')
		#如果要打开的文件后缀为'.bmp','.jif','.jpg','.png'时打开方式为图片打开，否则直接打开源文件
		if os.path.splitext(l.lujing)[1]=='.bmp' or os.path.splitext(l.lujing)[1]=='.jif'\
		or os.path.splitext(l.lujing)[1]=='.jpg' or os.path.splitext(l.lujing)[1]=='.png':
			return StreamingHttpResponse(f,content_type="image/png")
		else:
			return StreamingHttpResponse(f)
	elif request.method=='POST':
		file=request.POST['wenjian']
		uname=request.POST['uname']
		lujing=request.POST['lujing']
		file_list=Files.objects.get(wenjian=file,uname=uname,lujing=lujing)
		f=open(file_list.lujing,'rb')
		response=HttpResponse(f)
		#文件下载类型选择未知
		response['Content-Type']='application/octet-stream'
		#选择下载类型弹出保存框,下载后文件名为wjm或x.wenjian
		response['Content-Disposition']="attachment;filename="+file_list.wenjian
		return response