from django.shortcuts import render
from ssp.models import SspModels
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import jieba
# Create your views here.

def selectProjects(request):
    return render(request,'selectProjects.html')
def selectProjectsByConditions(request):
    # xmpzh=request.POST['xmpzh']
    # xmlb=request.POST['xmlb']
    # szssq=request.POST['szssq']
    # gzdw=request.POST['gzdw']
    # xmfzr=request.POST['xmfzr']
    # lxsj=request.POST['lxsj']
    # xkfl=request.POST['xkfl']
    # xmmc=request.POST['xmmc']
    #数据过滤字典中的内容为空时，查询所有数据，否则按照字典内容进行数据筛选
    print('session:',request.session.get('mydic'))
    if request.POST:
        mydic={}
        preMydic(mydic,request)
        request.session['mydic']=mydic#存进session字典
        print('mydic',mydic)
        # print(mydic)

        if mydic:#如果字典不为空 则进行过滤
            datas=SspModels.objects.filter(**mydic)
        else:
            datas=SspModels.objects.all()
    if request.GET:
        mydic=request.session.get('mydic')#取出上一次的session字典
        if mydic:  # 如果字典不为空 则进行过滤
            datas = SspModels.objects.filter(**mydic).order_by('sspid')
        else:
            datas = SspModels.objects.all().order_by('sspid')
    paginator = Paginator(datas, 25)  # 分页器 Show 25 contacts per page

    page = request.GET.get('page')
    print('page', page)
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)
        # 调用词云函数
    wordclouds=preWordclouds(datas)
    # print(wordclouds)
    #饼图数据准备,调用饼图韩束
    xmlb_data=preXmlbdata(datas)
    #调用柱状图函数 工作单位
    x_data,y_data=preGzdwdata(datas)
    map_data=preMap(datas)

    return render(request,'selectProjects.html',
                  context={'contacts':contacts,'wordclouds':wordclouds,
                           'xmlb_data':xmlb_data,'x_data':x_data,'y_data':y_data,'map_data':map_data})
    # return render(request,'selectProjects.html',context={'contacts':contacts,'wordclouds':wordclouds})

# wordclouds=[{'name':'abc',"value":1234}]
def preWordclouds(datas):
    xmmc_ls=[]
    for item in datas:
        xmmc_ls.append(item.xmmc)#加载项目名称
    # print(xmmc_ls)
    xmmc_str=''.join(xmmc_ls)
    word_ls=jieba.lcut(xmmc_str)
    word_dict={}
    #词频统计
    for  item in word_ls:
        if item not in [word.strip() for word in open('ssp/hit_stopwords.txt','r',encoding='utf-8').readlines()]:
            word_dict[item]=word_dict.get(item,0)+1#没有出现过词频为0 ，出现过词频+1
    wordclouds=[]
    for item in word_dict.items():
        wordclouds.append({'name':item[0],'value':item[1]})
    return wordclouds

def preMydic(mydic,request):
    xmpzh = request.POST['xmpzh']
    xmlb = request.POST['xmlb']
    szssq = request.POST['szssq']
    gzdw = request.POST['gzdw']
    xmfzr = request.POST['xmfzr']
    lxsj = request.POST['lxsj']
    xkfl = request.POST['xkfl']
    xmmc = request.POST['xmmc']
    if xmpzh != '':
        mydic['xmpzh'] = xmpzh
    if xmlb != '0':
        mydic['xmlb'] = xmlb
    if xkfl != '0':
        mydic['xkfl'] = xkfl
    if xmmc != '':
        mydic['xmmc__contains'] = xmmc#模糊查询，like语句
    if lxsj != '0':
        mydic['lxsj__year'] = lxsj
    if xmfzr != '':
        mydic['xmfzr'] = xmfzr
    if gzdw != '':
        mydic['gzdw'] = gzdw
    if szssq != '0':
        mydic['szssq'] = szssq
    return  mydic
#项目类别饼图
# ['重大项目','重点项目','一般项目','青年项目','西部项目','后期资助项目','中华学术外译项目','成果文库']
def preXmlbdata(datas):
    xmlb_ls=[]
    for item in datas:
        xmlb_ls.append(item.xmlb)
    xmlb_dict={}
    for item in xmlb_ls:
        xmlb_dict[item]=xmlb_dict.get(item,0)+1 #第一次出现赋值为0 否则+1

    xmlb_data=[]
    print(xmlb_dict)
    for item in xmlb_dict.items():
        xmlb_data.append({'name':item[0],'value':item[1]})
    print(xmlb_data)
    return  xmlb_data
def preGzdwdata(datas):
    gzdw_ls=[]
    for item in datas:
        gzdw_ls.append(item.gzdw)
    gzdw_dict={}
    for item in gzdw_ls:
        gzdw_dict[item]=gzdw_dict.get(item,0)+1

    x_data=[]
    y_data=[]
    # 为字典作出排序 获取前20名
    gzdw_ls=list(gzdw_dict.items())#(工作单位,数量)
    gzdw_ls.sort(key=lambda x:x[1],reverse=True)
    for item in gzdw_ls[:10]:
        x_data.append(item[0])
        y_data.append(item[1])
    # for item in gzdw_dict.items():
    #     x_data.append(item[0])
    #     y_data.append(item[1])
    return x_data,y_data

def preMap(datas):
    szsqs_ls=[]
    for  item in datas:
        szsqs_ls.append(item.szssq)
    szsqs_dict={}
    for item in szsqs_dict:
        szsqs_dict[item]=szsqs_dict.get(item,0)+1
    map_data=[]
    sf_ls = [line.strip() for line in open('ssp/sf.txt', 'r', encoding='utf-8').readlines()]
    print(sf_ls)
    for item in szsqs_dict.items():
        #所在省市区在所有省列表中的情况
        if item[0] in sf_ls:
            map_data.append({'name':item[0],'value':item[1]})

    for item in sf_ls:
        #不在时，设置为0，否则地图上显示NaN
        if item not in szsqs_dict.keys():
            map_data.append({'name':item,'value':0})
    print(map_data)
    return map_data


