from django.shortcuts import render
from .models import Xinlang
# Create your views here.
def index(request):
	# 获取新闻
	news_list = Xinlang.objects.values('pub_time','news').all().order_by('-pub_time')[:10]
	# 分配数据
	context = {'news_list':news_list}
	# 返回模版
	return render(request,'./index.html',context)