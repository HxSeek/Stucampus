#-*- coding: UTF-8 -*-   

from django.shortcuts import render
from django.core.paginator import InvalidPage,Paginator
from django.http import *
from django.core.urlresolvers import reverse
from django.views.generic import View

from stucampus.dreamer.models import Register
from stucampus.dreamer.forms import Register_Form
from stucampus.account.permission import check_perms

from django.db.models import Q
import datetime

class SignUp(View):

	def get(self, request):
		return render(request, 'dreamer/apply.html', {'form': Register_Form()})

	def post(self, request):
		msg = Register()
		tmp = Register_Form(request.POST)
		if request.META.has_key('HTTP_X_FORWARDED_FOR'):  
			msg.ip = request.META['HTTP_X_FORWARDED_FOR']
		else:
			msg.ip = request.META['REMOTE_ADDR'] 
		msg.status = True
		now = datetime.date.today()
		if tmp.is_valid():
			msg.name = tmp.cleaned_data['name']
			msg.gender = tmp.cleaned_data['gender']
			msg.stu_ID = tmp.cleaned_data['stu_ID']
			msg.college = tmp.cleaned_data['college']
			msg.mobile = tmp.cleaned_data['mobile']
			msg.dept1 = tmp.cleaned_data['dept1']
			msg.dept2 = tmp.cleaned_data['dept2']
			msg.self_intro = tmp.cleaned_data['self_intro']
			same_SID = Register.objects.filter(stu_ID = msg.stu_ID, status=True).count()

			if same_SID > 0:
				return render(request, 'dreamer/failed.html')
			else:
				if Register.objects.filter(sign_up_date=now).filter(ip=msg.ip).count()>5:  
					return HttpResponse("您当前IP已于同一天成功报名五次，请等候第二天或换另一台电脑再进行报名.")
				else:
					msg.save()
					reply = msg
					if(reply.gender=='male'):
						reply.gender = '男';
					else:
						reply.gender = '女';

					if(reply.dept1=='jsb'):
						reply.dept1 = '技术部';
					elif(reply.dept1=='sjb'):
						reply.dept1 = '设计部';
					elif(reply.dept1=='cbb'):
						reply.dept1 = '采编部';
					elif(reply.dept1=='xzb'):
						reply.dept1 = '行政部';
					else:
						reply.dept1 = '运营部';

					if(reply.dept2=='jsb'):
						reply.dept2 = '技术部';
					elif(reply.dept2=='sjb'):
						reply.dept2 = '设计部';
					elif(reply.dept2=='cbb'):
						reply.dept2 = '采编部';
					elif(reply.dept1=='xzb'):
						reply.dept1 = '行政部';
					else:
						reply.dept2 = '运营部';
					return render(request, 'succeed.html', {'form': msg})
		else:
			return HttpResponse('failed.html')


def index(request):
	if request.method == 'GET':
		return render(request, 'dreamer/index.html')


class CheckMsg(View):

	def get(self, request):
		return render(request, 'dreamer/check_msg.html')

	def post(self, request):
		search=req.POST['search']
		objects = Register.objects.filter(Q(name=search)|Q(stuID=search)&Q(status=True)).count()
		if objects>0:
			return HttpResponse("已报名成功")
		else:
			return HttpResponse("尚未进行报名或报名不成功，若有疑问请在群里反映.")


def succeed(request):
	return render(request, 'dreamer/succeed.html')

def check(request):
	aaa = Register.objects.all().count()
	return HttpResponse(aaa)


def alldetail(request):
    aall = Register.objects.filter(status=True)
    user = request.user

    cbb1 = aall.filter(first_dept="cbb")
    cbb2 = aall.filter(second_dept="cbb")
    cbbb = cbb1.filter(gender="boy").count()+cbb2.filter(gender="boy").count()
    cbbg = cbb1.filter(gender="girl").count()+cbb2.filter(gender="girl").count()

    jsb1 = aall.filter(first_dept="jsb")
    jsb2 = aall.filter(second_dept="jsb")
    jsbb = jsb1.filter(gender="boy").count()+jsb2.filter(gender="boy").count()
    jsbg = jsb1.filter(gender="girl").count()+jsb2.filter(gender="girl").count()

    sjb1 = aall.filter(first_dept="sjb")
    sjb2 = aall.filter(second_dept="sjb")
    sjbb = sjb1.filter(gender="boy").count()+sjb2.filter(gender="boy").count()
    sjbg = sjb2.filter(gender="girl").count()+sjb1.filter(gender="girl").count()

    xzb1 = aall.filter(first_dept="xzb")
    xzb2 = aall.filter(second_dept="xzb")
    xzbb = xzb1.filter(gender="boy").count()+xzb2.filter(gender="boy").count()
    xzbg = xzb1.filter(gender="girl").count()+xzb2.filter(gender="girl").count()

    yyb1 = aall.filter(first_dept="yyb")
    yyb2 = aall.filter(second_dept="yyb")
    yybb = yyb1.filter(gender="boy").count()+yyb2.filter(gender="boy").count()
    yybg = yyb1.filter(gender="girl").count()+yyb2.filter(gender="girl").count()

    return render(request,'dreamer/situation.html',{"jsb1":jsb1.count(),"jsb2":jsb2.count(),"jsbb":jsbb,"jsbg":jsbg,
                                                    "sjb1":sjb1.count(),"sjb2":sjb2.count(),"sjbb":sjbb,"sjbg":sjbg,
                                                    "xzb1":xzb1.count(),"xzb2":xzb2.count(),"xzbb":xzbb,"xzbg":xzbg,
                                                    "yyb1":yyb1.count(),"yyb2":yyb2.count(),"yybb":yybb,"yybg":yybg,
                                                    "cbb1":cbb1.count(),"cbb2":cbb2.count(),"cbbb":cbbb,"cbbg":cbbg,
                                                    "all" :aall.count(),"user":user})

@check_perms('dreamer.apply_manage')
def alllist(request):
    applyall = Register.objects.filter(status=True).order_by('apply_date')
    paginator = Paginator(applyall,8)
    page = request.GET.get('page')
    try:
        page = paginator.page(page)
    except InvalidPage:
        page = paginator.page(1)
    return render(request,'dreamer/list.html',{'page':page})

@check_perms('dreamer.apply_manage')
def delete(request):
    apply_id = request.GET.get('id')
    app = get_object_or_404(Register,id=apply_id)
    app.status = False
    app.save()
    return HttpResponseRedirect('/dreamer/management')

@check_perms('dreamer.apply_manage')
def search(request):
    search=request.POST.get('search')
    app = Register.objects.filter(status=True).filter(Q(name=search)|Q(stuID=search))
    paginator = Paginator(app,8)
    page = request.GET.get('page')
    try:
        page = paginator.page(page)
    except InvalidPage:
        page = paginator.page(1)
    return render(request,'dreamer/list.html',{'page':page})

@check_perms('dreamer.apply_manage')
def detail(request):
    apply_id = request.GET.get('id')
    app = get_object_or_404(Register,id=apply_id)
    return render(request,'dreamer/detail.html',{'app':app})
