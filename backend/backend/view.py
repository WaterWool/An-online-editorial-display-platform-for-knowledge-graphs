from django.http import HttpResponse
from django.shortcuts import render
from . import MySQL
from . import Neo4j
from . import Neo4jRecLayout
from django.http import JsonResponse


def InsertRecLay(request):#插入推荐布局（目前只是在Neo4j中插入单个结点保存推荐布局json的str和以结点的形式保存布局）
    layname = request.POST.get('layname')
    laydata = request.POST.get('laydata')
    resultMy = MySQL.InsertLayData(layname,laydata)
    dellaydata = laydata
    laydata = laydata.replace('false', "'" + 'false' + "'").replace('true', "'" + 'true' + "'")
    laydata = eval(laydata)
    resultdel = Neo4jRecLayout.DeleteRecNode(layname)
    resultdis = Neo4jRecLayout.InsertRecLayByDis(layname,laydata)
    resultnode = Neo4jRecLayout.InsertRecLayNode(layname, dellaydata)
    if resultnode == "ERROR1":
        print('View InsertRecLay出现错误1')
        return HttpResponse("对数据库操作出现错误")
    elif resultdis == 'ERROR1':
        print('View InsertRecLay出现错误2')
        return HttpResponse("对数据库操作出现错误")
    elif resultMy == 'ERROR1':
        print('View InsertRecLay出现错误3')
        return HttpResponse("对数据库操作出现错误")
    elif resultdel == 'ERROR1':
        print('View InsertRecLay出现错误4')
        return HttpResponse("对数据库操作出现错误")
    else:
        print('View InsertRecLay成功插入推荐布局数据')
        return HttpResponse("成功插入推荐布局信息")


def InsertRecLayMy(request):#在MySQL中插入推荐布局信息
    layname = request.POST.get('layname')
    laydata = request.POST.get('laydata')
    result = MySQL.InsertLayData(layname, laydata)
    if result == "ERROR1":
        print('View InsertRecLayMy出现错误1')
        return HttpResponse("对数据库操作出现错误")
    else:
        print('View InsertRecLayMy成功插入推荐布局信息结点')
        return HttpResponse("成功插入推荐布局信息")


def InsertRecLayByNode(request):#在Neo4j中单个结点中插入推荐布局JSON的str内容
    layname = request.POST.get('layname')
    laydata = request.POST.get('laydata')
    result = Neo4jRecLayout.InsertRecLayNode(layname,laydata)
    if result == "ERROR1":
        print('View InsertRecLayByNode出现错误1')
        return HttpResponse("对数据库操作出现错误")
    else:
        print('View InsertRecLayByNode成功插入推荐布局信息结点')
        return HttpResponse("成功插入推荐布局信息")


def InsertRecLayByDis(request):#在Neo4j中以结点和关系的形式插入推荐布局内容
    layname = request.POST.get('layname')
    laydata = request.POST.get('laydata')
    laydata = laydata.replace('false', "'" + 'false' + "'").replace('true', "'" + 'true' + "'")
    laydata = eval(laydata)
    result = Neo4jRecLayout.InsertRecLayDis(layname,laydata)
    if result == "ERROR1":
        print('View InsertRecLayByDis出现错误1')
        return HttpResponse("对数据库操作出现错误")
    else:
        print('View InsertRecLayByDis成功插入推荐布局结点与关系')
        return HttpResponse("成功插入推荐布局信息")


def InsertOneNode(request):#在Neoj中插入单个pro结点（实时更新各个结点内容）
    username = request.POST.get('username')
    pro = request.POST.get('pro')
    block = request.POST.get('block')
    block = block.replace('false', "'" + 'false' + "'").replace('true', "'" + 'true' + "'")
    block = eval(block)
    result = Neo4j.InsertOneNode(username,pro,block)
    if result == "ERROR1":
        print('View InsertOneNode出现错误1')
        return HttpResponse("对数据库操作出现错误")
    else:
        UpdataPro(username,pro)
        print('View InsertOneNode成功插入单个结点')
        return HttpResponse('插入单个结点成功')


def InsertOneRel(request):#在Neo4j中插入单个关系（实时更新各个结点内容）
    username = request.POST.get('username')
    pro = request.POST.get('pro')
    firnode = request.POST.get('firnode')
    secnode = request.POST.get('secnode')
    relname = request.POST.get('relname')
    result = Neo4j.InsertOneRel(username,pro,firnode,secnode,relname)
    if result == "ERROR1":
        print('View InsertOneRel出现错误1')
        return HttpResponse("对数据库操作出现错误")
    elif result == "ERROR2":
        print('View InsertOneRel出现错误2')
        return HttpResponse("没有查找到需要创建关系的结点")
    else:
        UpdataPro(username, pro)
        print('View InsertOneRel成功插入单个关系')
        return HttpResponse('创建结点关系成功')


def InsertPic(request):#在MySQL和Neo4j中插入pro的Json数据
    username=request.POST.get('username')
    pro=request.POST.get('pro')
    data=request.POST.get('data')
    resultMY = MySQL.InsertPic(username, pro, data)
    if resultMY == 'ERROR1':
        print('View InsertPic出现错误1')
        return HttpResponse("对数据库操作出现错误")
    deldata = data
    data = data.replace('false', "'" + 'false' + "'").replace('true', "'" + 'true'+"'")
    data = eval(data)
    resultdel = Neo4j.DeleteProByNode(username, pro)
    if resultdel == 'ERROR1':
        print('View InsertPic出现错误2')
        return HttpResponse("对数据库操作出现错误")
    resultNeo = Neo4j.InsertPic(username,pro,data)
    if resultNeo=='ERROR1':
        print('View InsertPic出现错误3')
        return HttpResponse("对数据库操作出现错误")
    resultNeoNode = Neo4j.InsertPicByNode(username, pro, deldata)
    if resultNeoNode == 'ERROR1':
        print('View InsertPic出现错误4')
        return HttpResponse("对数据库操作出现错误")
    else:
        print('View InsertPic成功在双数据库中插入工程数据')
        return HttpResponse("恭喜你，插入谱图成功")


def InsertUser(request):#在用户和密码的MySQL的数据表中插入用户和其对应的密码
    username = request.POST.get('username')
    password = request.POST.get('password')
    result = MySQL.InsertUser(username,password)
    if result == "ERROR1":
        print('View InsertUser出现错误1')
        return HttpResponse("对数据库操作出现错误")
    elif result == "ERROR2":
        print('View InsertUser出现错误2')
        return HttpResponse("抱歉，此用户名已经被注册，请重新注册")
    else:
        print('View InsertUser成功创建新用户')
        return HttpResponse("恭喜你，新建用户成功")


def SelectPic(request):#在MySQL和Neo4j数据库中查询pro内容，如果出现了冲突就将MySQL的内容加载到Neo4j中
    #返回的数据类型是生成pro的json字符串，数据类型：str
    username = request.POST.get('username')
    pro = request.POST.get('pro')
    resultMy = MySQL.SelectPic(username,pro)
    resultNeo = Neo4j.SelectProByNode(username,pro)
    if resultMy=="ERROR1":
        print('View SelectPic出现错误1')
        return HttpResponse("对数据库操作出现错误")
    elif resultMy == 'ERROR2':
        print('View SelectPic出现错误2')
        return HttpResponse("MySQL中没有查找到相关工程数据")
    if resultNeo == 'ERROR1':
        print('View SelectPic出现错误3')
        return HttpResponse("对数据库操作出现错误")
    elif resultNeo == 'ERROR2':
        print('View SelectPic出现错误4')
        return HttpResponse("Neo4j中没有查找到相关工程数据")
    if resultNeo == resultNeo:
        print('View SelectPiccj成功查询图谱数据')
        return HttpResponse(resultNeo)
    else:
        data = resultMy
        data = data.replace('false', "'" + 'false' + "'").replace('true', "'" + 'true' + "'")
        data = eval(data)
        resultNeo = Neo4j.InsertPic(username, pro, data)
        if resultNeo == 'ERROR1':
            print('View SelectPic出现错误5')
            return HttpResponse("对数据库操作出现错误")
        resultNeoNode = Neo4j.InsertPicByNode(username, pro, resultMy)
        if resultNeoNode == 'ERROR1':
            print('View SelectPic出现错误6')
            return HttpResponse("对数据库操作出现错误")
        else:
            print('View SelectPic成功查询图谱数据')
            return HttpResponse(resultMy)


def SelectRecLay(request):#查询推荐布局
    layname = request.POST.get('layname')
    resultMy = MySQL.SelectLayData(layname)
    resultNeo = Neo4jRecLayout.SelectRecLayByNode(layname)
    if resultMy=="ERROR1":
        print('View SelectRecLay出现错误1')
        return HttpResponse("对数据库操作出现错误")
    elif resultMy == 'ERROR2':
        print('View SelectRecLay出现错误2')
        return HttpResponse("MySQL中没有查找到相关推荐布局信息")
    if resultNeo == 'ERROR1':
        print('View SelectRecLay出现错误3')
        return HttpResponse("对数据库操作出现错误")
    elif resultNeo == 'ERROR2':
        print('View SelectRecLay出现错误4')
        return HttpResponse("Neo4j中没有查找到相关推荐布局信息")
    if resultNeo == resultNeo:
        print('View SelectRecLay成功查询推荐布局信息')
        return HttpResponse(resultNeo)
    else:
        data = resultMy
        data = data.replace('false', "'" + 'false' + "'").replace('true', "'" + 'true' + "'")
        data = eval(data)
        resultNeoRec = Neo4jRecLayout.InsertRecLayDis(layname,data)
        if resultNeoRec == 'ERROR1':
            print('View SelectRecLay出现错误5')
            return HttpResponse("对数据库操作出现错误")
        else:
            resultNeo = Neo4jRecLayout.InsertRecLayNode(layname,resultMy)
            if resultNeo == 'ERROR1':
                print('View SelectRecLay出现错误6')
                return HttpResponse("对数据库操作出现错误")
            else:
                print('View SelectRecLay成功查询推荐布局信息')
                return HttpResponse(resultMy)


def SelectRecLayByNode(request):#在Neo4j中查找推荐布局（通过结点data进行查询）
    #返回值为布局的json字符串 数据类型：str
    layname = request.POST.get('layname')
    result = Neo4jRecLayout.SelectRecLayByNode(layname)
    if result == "ERROR1":
        print('View SelectRecLayByNode出现错误1')
        return HttpResponse("对数据库操作出现错误")
    elif result == 'ERROR2':
        print('View SelectRecLayByNode出现错误2')
        return HttpResponse("抱歉，没有查到相关推荐布局信息")
    else:
        print('View SelectRecLayByNode成功查询推荐布局信息')
        return HttpResponse(result)


def SelectRecLayByDis(request):#在Neo4j中查找推荐布局（通过查找所有布局结点和关系查询）
    # 返回值为布局的json字符串 数据类型：str
    layname = request.POST.get('layname')
    result = Neo4jRecLayout.SelectRecLayByDis(layname)
    if result == "ERROR1":
        print('View SelectRecLayByDis出现错误1')
        return HttpResponse("对数据库操作出现错误")
    elif result == "ERROR2":
        print('View SelectRecLayByDis出现错误2')
        return HttpResponse("抱歉，没有查到相关推荐布局信息")
    elif result == "ERROR3":
        print('View SelectRecLayByDis出现错误3')
        return HttpResponse("没有画布无法展示推荐信息")
    else:
        print('View SelectRecLayByDis成功查询推荐布局信息')
        return HttpResponse(result)


def SelectPass(request):#查询用户的密码
    #返回的是用户的密码 数据类型：str
    username = request.POST.get('username')
    result = MySQL.SelectPass(username)
    if result == "ERROR1":
        print('View SelectPass出现错误1')
        return HttpResponse("对数据库操作出现错误")
    elif result == "ERROR2":
        print('View SelectPass出现错误2')
        return HttpResponse("抱歉，此用户还没有注册")
    else:
        print('View SelectPass成功查询用户密码')
        return HttpResponse(result)


def SelectOneNodeByName(request):#通过node的名字查找一个node和其对应的关系
    #返回的是这个node和其有关系的结点和关系的json字符串 数据类型：str
    username = username = request.POST.get('username')
    pro = request.POST.get('pro')
    nodename = request.POST.get('nodename')
    result = Neo4j.SelectOneNodeAndRel(username,pro,nodename)
    if result == "ERROR1":
        print('View SelectOneNodeByName出现错误1')
        return HttpResponse("对数据库操作出现错误")
    elif result == "ERROR2":
        print('View SelectOneNodeByName出现错误2')
        return HttpResponse("抱歉，不存在此结点")
    elif result == 'ERROR3':
        print('View SelectOneNodeByName出现错误3')
        return HttpResponse("抱歉，没有相关的画布信息，无法展示编辑结点")
    else:
        print('View SelectOneNodeByName成功查询结点与其关系结点数据')
        return HttpResponse(result)


def SelectOneNodeNoRel(request):#通过node的名字查找一个node没有其对应的关系，只有这一个node
    #返回的是这个node的json字符串 数据类型：str
    username = request.POST.get('username')
    pro = request.POST.get('pro')
    nodename = request.POST.get('nodename')
    result = Neo4j.SelectOneNode(username,pro,nodename)
    if result == "ERROR1":
        print('View SelectOneNode出现错误1')
        return HttpResponse("对数据库操作出现错误")
    elif result == "ERROR2":
        print('View SelectOneNode出现错误2')
        return HttpResponse("抱歉，不存在此结点")
    else:
        print('View SelectOneNode成功查询单个结点数据')
        return HttpResponse(result)


def SelectOneNodeAndRelIn(request):#通过node的名字查找一个node有其对应的入度关系
    #返回的是这个node的json字符串 数据类型：str
    username = request.POST.get('username')
    pro = request.POST.get('pro')
    nodename = request.POST.get('nodename')
    result = Neo4j.SelectOneNodeAndRelIn(username,pro,nodename)
    if result == "ERROR1":
        print('View SelectOneNodeAndRelIn出现错误1')
        return HttpResponse("对数据库操作出现错误")
    elif result == "ERROR2":
        print('View SelectOneNodeAndRelIn出现错误2')
        return HttpResponse("抱歉，不存在此结点")
    elif result == "ERROR3":
        print('View SelectOneNodeAndRelIn出现错误3')
        return HttpResponse("抱歉，没有相关的画布信息，无法展示编辑结点")
    else:
        print('View SelectOneNodeAndRelIn成功查询单个结点数据')
        return HttpResponse(result)


def SelectOneNodeAndRelOut(request):#通过node的名字查找一个node有其对应的出度关系
    #返回的是这个node的json字符串 数据类型：str
    username = request.POST.get('username')
    pro = request.POST.get('pro')
    nodename = request.POST.get('nodename')
    result = Neo4j.SelectOneNodeAndRelIn(username,pro,nodename)
    if result == "ERROR1":
        print('View SelectOneNodeAndRelOut出现错误1')
        return HttpResponse("对数据库操作出现错误")
    elif result == "ERROR2":
        print('View SelectOneNodeAndRelOut出现错误2')
        return HttpResponse("抱歉，不存在此结点")
    elif result == "ERROR3":
        print('View SelectOneNodeAndRelOut出现错误3')
        return HttpResponse("抱歉，没有相关的画布信息，无法展示编辑结点")
    else:
        print('View SelectOneNodeAndRelOut成功查询单个结点数据')
        return HttpResponse(result)

def SelectOnePro(request):#在Neo4j中查找一个pro中所有结点和关系
    #返回值这个pro的json字符串 数据类型：str
    username = username = request.POST.get('username')
    pro = request.POST.get('pro')
    result = Neo4j.SelectOnePro(username,pro)
    if result == "ERROR1":
        print('View SelectOnePro出现错误1')
        return HttpResponse("对数据库操作出现错误")
    elif result == "ERROR2":
        print('View SelectOnePro出现错误2')
        return HttpResponse("抱歉，此项目中不存在结点和关系")
    elif result == 'ERROR3':
        print('View SelectOnePro出现错误3')
        return HttpResponse("抱歉，没有相关的画布信息，无法展示编辑结点")
    else:
        print('View SelectOnePro成功查询工程数据')
        return HttpResponse(result)


def SelectOneRel(request):#从Neo4j中查询一个关系对应的关系和关系相关的结点
    #返回值为所有关系和对应结点的json，数据类型:str
    username = request.POST.get('username')
    pro = request.POST.get('pro')
    relname = request.POST.get('relname')
    result = Neo4j.SelectOneRel(username,pro,relname)
    if result == "ERROR1":
        print('View SelectOneRel出现错误1')
        return HttpResponse("对数据库操作出现错误")
    elif result == "ERROR2":
        print('View SelectOneRel出现错误2')
        return HttpResponse("抱歉，此项目中不存在此关系")
    elif result == 'ERROR3':
        print('View SelectOneRel出现错误3')
        return HttpResponse("抱歉，没有相关的画布信息，无法展示编辑结点")
    else:
        print('View SelectOneRel成功查询关系数据')
        return HttpResponse(result)


def SelectOneTypeAndRel(request):#从Neo4j中查询一个类型结点对应的结点和相关的结点
    #返回值为所有关系和对应结点的json，数据类型:str
    username = request.POST.get('username')
    pro = request.POST.get('pro')
    typename = request.POST.get('typename')
    result = Neo4j.SelectOneTypeAndRel(username,pro,typename)
    if result == "ERROR1":
        print('View SelectOneTypeAndRel出现错误1')
        return HttpResponse("对数据库操作出现错误")
    elif result == "ERROR2":
        print('View SelectOneTypeAndRel出现错误2')
        return HttpResponse("抱歉，此项目中不存在此属性的结点")
    elif result == 'ERROR3':
        print('View SelectOneTypeAndRel出现错误3')
        return HttpResponse("抱歉，没有相关的画布信息，无法展示编辑结点")
    else:
        print('View SelectOneTypeAndRel成功查询类型数据')
        return HttpResponse(result)


def SelectOneTypeNoRel(request):#从Neo4j中查询一个类型结点对应的结点和相关的结点,所有的结点都是这个类型的
    #返回值为所有关系和对应结点的json，数据类型:str
    username = request.POST.get('username')
    pro = request.POST.get('pro')
    typename = request.POST.get('typename')
    result = Neo4j.SelectOneTypeNoRel(username,pro,typename)
    if result == "ERROR1":
        print('View SelectOneTypeNoRel出现错误1')
        return HttpResponse("对数据库操作出现错误")
    elif result == "ERROR2":
        print('View SelectOneTypeNoRel出现错误2')
        return HttpResponse("抱歉，此项目中不存在此属性的结点")
    elif result == 'ERROR3':
        print('View SelectOneTypeNoRel出现错误3')
        return HttpResponse("抱歉，没有相关的画布信息，无法展示编辑结点")
    else:
        print('View SelectOneTypeNoRel成功查询类型结点数据')
        return HttpResponse(result)


def SelectOneClourAndRel(request):#查找一个pro中一个颜色的结点和与其有关系的结点
    # 返回值为布局的json字符串 数据类型：str
    username = request.POST.get('username')
    pro = request.POST.get('pro')
    clour = request.POST.get('clour')
    result = Neo4j.SelectOneClourAndRel(username,pro,clour)
    if result == "ERROR1":
        print('View SelectOneClourAndRel出现错误1')
        return HttpResponse("对数据库操作出现错误")
    elif result == "ERROR2":
        print('View SelectOneClourAndRel出现错误2')
        return HttpResponse("没有查找到此颜色的结点")
    elif result == "ERROR3":
        print('View SelectOneClourAndRel出现错误3')
        return HttpResponse("抱歉，没有相关的画布信息，无法展示编辑结点")
    else:
        print('View SelectOneClourAndRel成功查询单个颜色结点和关系信息')
        return HttpResponse(result)


def SelectOneClourNoRel(request):#查找一个pro中所有一个颜色的结点与其之间的关系
    # 返回值为布局的json字符串 数据类型：str
    username = request.POST.get('username')
    pro = request.POST.get('pro')
    clour = request.POST.get('clour')
    result = Neo4j.SelectOneClourNoRel(username,pro,clour)
    if result == "ERROR1":
        print('View SelectOneClourNoRel出现错误1')
        return HttpResponse("对数据库操作出现错误")
    elif result == "ERROR2":
        print('View SelectOneClourNoRel出现错误2')
        return HttpResponse("没有查找到此颜色的结点")
    elif result == "ERROR3":
        print('View SelectOneClourNoRel出现错误3')
        return HttpResponse("抱歉，没有相关的画布信息，无法展示编辑结点")
    else:
        print('View SelectOneClourNoRel成功查询单个颜色结点信息')
        return HttpResponse(result)


def SelectTwoNodePath(request):
    username = request.POST.get('username')
    pro = request.POST.get('pro')
    nodename1 = request.POST.get('nodename1')
    nodename2 = request.POST.get('nodename2')
    pathresult = Neo4j.SelectTwoNodePath(username,pro,nodename1,nodename2)
    if pathresult == "ERROR1":
        print('View SelectTwoNodePath出现错误1')
        return HttpResponse("对数据库操作出现错误")
    elif pathresult == "ERROR2":
        print('View SelectTwoNodePath出现错误2')
        return HttpResponse("查找不到两个节点")
    elif pathresult == "ERROR3":
        print('View SelectTwoNodePath出现错误3')
        return HttpResponse("抱歉，没有相关的画布信息，无法展示编辑结点与通路")
    else:
        print('View SelectTwoNodePath成功两节点之间的所有通路')
        return HttpResponse(pathresult)


def SelectTwoNodeShortPath(request):
    username = request.POST.get('username')
    pro = request.POST.get('pro')
    nodename1 = request.POST.get('nodename1')
    nodename2 = request.POST.get('nodename2')
    pathresult = Neo4j.SelectTwoNodeShortPath(username,pro,nodename1,nodename2)
    if pathresult == "ERROR1":
        print('View SelectTwoNodeShortPath出现错误1')
        return HttpResponse("对数据库操作出现错误")
    elif pathresult == "ERROR2":
        print('View SelectTwoNodeShortPath出现错误2')
        return HttpResponse("查找不到指定的两个节点")
    elif pathresult == "ERROR3":
        print('View SelectTwoNodeShortPath出现错误3')
        return HttpResponse("抱歉，没有相关的画布信息，无法展示编辑结点与通路")
    else:
        print('View SelectTwoNodeShortPath成功两节点之间的最短路径')
        return HttpResponse(pathresult)


def SelectTwoNodeAllShortPath(request):
    username = request.POST.get('username')
    pro = request.POST.get('pro')
    nodename1 = request.POST.get('nodename1')
    nodename2 = request.POST.get('nodename2')
    pathresult = Neo4j.SelectTwoNodeAllShortPath(username,pro,nodename1,nodename2)
    if pathresult == "ERROR1":
        print('View SelectTwoNodeAllShortPath出现错误1')
        return HttpResponse("对数据库操作出现错误")
    elif pathresult == "ERROR2":
        print('View SelectTwoNodeAllShortPath出现错误2')
        return HttpResponse("查找不到指定的两个节点")
    elif pathresult == "ERROR3":
        print('View SelectTwoNodeAllShortPath出现错误3')
        return HttpResponse("抱歉，没有相关的画布信息，无法展示编辑结点与关系")
    else:
        print('View SelectTwoNodeAllShortPath成功两节点之间的所有的最短路径')
        return HttpResponse(pathresult)


def SelectCircuit(request):
    username = request.POST.get('username')
    pro = request.POST.get('pro')
    nodename = request.POST.get('nodename')
    result = Neo4j.SelectCircuit(username,pro,nodename)
    if result == "ERROR1":
        print('View SelectCircuit出现错误1')
        return HttpResponse("对数据库操作出现错误")
    elif result == "ERROR2":
        print('View SelectCircuit出现错误2')
        return HttpResponse("查找不到指定的节点")
    elif result == "ERROR3":
        print('View SelectCircuit出现错误3')
        return HttpResponse("抱歉，没有相关的画布信息，无法展示编辑结点与关系")
    else:
        print('View SelectCircuit成功查询经过此节点的回路')
        return HttpResponse(result)


def SelectDeepNode(request):
    username = request.POST.get('username')
    pro = request.POST.get('pro')
    nodes = request.POST.get('nodes')
    depth = request.POST.get('depth')
    result = Neo4j.SelectDeepNode(username, pro, nodes,depth)
    if result == "ERROR1":
        print('View SelectDeepNode出现错误1')
        return HttpResponse("对数据库操作出现错误")
    elif result == "ERROR2":
        print('View SelectDeepNode查找不到对应的节点与关系')
        return HttpResponse("查找不到指定的节点与关系")
    elif result == "ERROR3":
        print('View SelectDeepNode出现错误3')
        return HttpResponse("抱歉，没有相关的画布信息，无法展示编辑结点与关系")
    else:
        print('View SelectDeepNode成功查询指定节点与对应关系')
        return HttpResponse(result)


def DeleteAllPro(request):#在三种不同的保存形式下删除所有工程内容
    username = request.POST.get('username')
    pro = request.POST.get('pro')
    resultMy = MySQL.DeleteOnePro(username,pro)
    if resultMy == 'ERROR1':
        print('View DeleteAllPro出现错误1')
        return HttpResponse("对数据库操作出现错误")
    elif resultMy == 'ERROR2':
        print('View DeleteAllPro MySQL中查无此工程信息')
        return HttpResponse("MySQL中查无此工程信息")
    resultNeoNode = Neo4j.DeleteProByNode(username, pro)
    if resultNeoNode == 'ERROR1':
        print('View DeleteAllPro出现错误2')
        return HttpResponse("对数据库操作出现错误")
    elif resultNeoNode == 'ERROR2':
        print('View DeleteAllPro Neo4j中查无此工程节点信息')
        return HttpResponse("Neo4j中查无此工程节点信息")
    resultNeo = Neo4j.DeletePro(username, pro)
    if resultNeo == 'ERROR1':
        print('View DeleteAllPro出现错误3')
        return HttpResponse("对数据库操作出现错误")
    elif resultNeo == 'ERROR2':
        print('View DeleteAllPro Neo4j中查无此工程信息')
        return HttpResponse("Neo4j中查无此工程信息")
    print('View DeleteAllPro 成功删除工程信息')
    return HttpResponse("成功删除工程信息")


def DeleteLay(request):#三个数据库中删除对应推荐布局信息
    layname = request.POST.get('layname')
    resultMy = MySQL.DeleteOneLay(layname)
    if resultMy == 'ERROR1':
        print('View DeletLay出现错误1')
        return HttpResponse("对数据库操作出现错误")
    elif resultMy == 'ERROR2':
        print('View DeletLay MySQL中查无此推荐布局信息')
        return HttpResponse("MySQL中查无此推荐布局信息")
    resultNeoNode = Neo4jRecLayout.DeleteRecNode(layname)
    if resultNeoNode == 'ERROR1':
        print('View DeletLay出现错误2')
        return HttpResponse("对数据库操作出现错误")
    elif resultNeoNode == 'ERROR2':
        print('View DeletLay Neo4j中查无此推荐布局节点信息')
        return HttpResponse("Neo4j中查无此推荐布局节点信息")
    resultNeo = Neo4jRecLayout.DeleteRecDis(layname)
    if resultNeo == 'ERROR1':
        print('View DeletLay出现错误3')
        return HttpResponse("对数据库操作出现错误")
    elif resultNeo == 'ERROR2':
        print('View DeletLay Neo4j中查无此推荐布局信息')
        return HttpResponse("Neo4j中查无此推荐布局信息")
    print('View DeletLay 成功删除推荐布局信息')
    return HttpResponse("成功删除推荐布局信息")


def DeleteOneNodeByName(request):#通过名字的方式删除一个结点，如果此结点还与其他结点有关系则返回Tip字符串
    username = request.POST.get('username')
    pro = request.POST.get('pro')
    nodename = request.POST.get('nodename')
    result = Neo4j.DeleteOneNodeByName(username,pro,nodename)
    if result == "ERROR1":
        print('View DeleteOneNodeByName出现错误1')
        return HttpResponse("对数据库操作出现错误")
    elif result == "ERROR2":
        print('View DeleteOneNodeByName出现错误2')
        return HttpResponse("抱歉，查无此结点无法删除")
    elif result == 'Tip':
        print('View DeleteOneNodeByName此结点仍然存在关系')
        return HttpResponse("此结点仍存在关系，确定要删除吗?")
    else:
        print('View DeleteOneNodeByName成功删除单个结点')
        UpdataPro(username,pro)
        return HttpResponse("删除单个结点成功")


def DeleteOneNodeCom(request):#通过名字查询的方式，强制删除一个结点
    username = request.POST.get('username')
    pro = request.POST.get('pro')
    nodename = request.POST.get('nodename')
    result = Neo4j.DeleteOneNodeCom(username,pro,nodename)
    if result == "ERROR1":
        print('View DeleteOneNodeCom出现错误1')
        return HttpResponse("对数据库操作出现错误")
    elif result == "ERROR2":
        print('View DeleteOneNodeComc查无此结点')
        return HttpResponse("查无此结点")
    else:
        print('View DeleteOneNodeCom强制删除单个结点成功')
        UpdataPro(username, pro)
        return HttpResponse("强制删除单个结点成功")


def DeleteOneClourNode(request):#删除一个颜色所有的结点包括与其所有的关系（强制删除）
    username = request.POST.get('username')
    pro = request.POST.get('pro')
    clour = request.POST.get('clour')
    result = Neo4j.DeleteOneClourNode(username,pro,clour)
    if result == "ERROR1":
        print('View DeleteOneClourNode出现错误1')
        return HttpResponse("对数据库操作出现错误")
    elif result == "ERROR2":
        print('View DeleteOneClourNode查无此颜色结点')
        return HttpResponse("查无此颜色结点")
    else:
        print('View DeleteOneClourNode删除对应颜色结点与关系成功')
        UpdataPro(username, pro)
        return HttpResponse("删除对应颜色结点与关系成功")


def DeleteOneTypeNode(request):#删除一个类别所有的结点包括与其所有的关系（强制删除）
    username = request.POST.get('username')
    pro = request.POST.get('pro')
    typename = request.POST.get('typename')
    result = Neo4j.DeleteOneTypeNode(username,pro,typename)
    if result == "ERROR1":
        print('View DeleteOneTypeNode出现错误1')
        return HttpResponse("对数据库操作出现错误")
    elif result == "ERROR2":
        print('View DeleteOneTypeNode查无此颜色结点')
        return HttpResponse("查无此颜色结点")
    else:
        print('View DeleteOneTypeNode删除对应颜色结点与关系成功')
        UpdataPro(username, pro)
        return HttpResponse("删除对应颜色结点与关系成功")


def DeletePro(request):#删除一个pro中所有结点和关系的数据
    username = request.POST.get('username')
    pro = request.POST.get('pro')
    result = Neo4j.DeletePro(username,pro)
    if result == "ERROR1":
        print('View DeletePro出现错误1')
        return HttpResponse("对数据库操作出现错误")
    elif result == "ERROR2":
        print('View DeletePro查无此工程内容')
        return HttpResponse("查无此工程内容")
    else:
        print('View DeletePro删除工程内容成功')
        return HttpResponse("删除工程内容成功")


def DeleteOneRel(request):#删除两个结点之间的指定关系
    username = request.POST.get('username')
    pro = request.POST.get('pro')
    firnode = request.POST.get('firnode')
    secnode = request.POST.get('secnode')
    relname = request.POST.get('relname')
    result = Neo4j.DeleteOneRel(username, pro, firnode, secnode, relname)
    if result == "ERROR1":
        print('View DeleteOneRel出现错误1')
        return HttpResponse("对数据库操作出现错误")
    elif result == "ERROR2":
        print('View DeleteOneRel查无此关系')
        return HttpResponse("查无此关系")
    else:
        print('View DeleteOneRel删除指定关系成功')
        UpdataPro(username, pro)
        return HttpResponse("删除关系成功")


def DeleteAllRel(request):#删除两个结点之间的所有关系
    username = request.POST.get('username')
    pro = request.POST.get('pro')
    firnode = request.POST.get('firnode')
    secnode = request.POST.get('secnode')
    result = Neo4j.DeleteAllRel(username,pro,firnode,secnode)
    if result == "ERROR1":
        print('View DeleteAllRel出现错误1')
        return HttpResponse("对数据库操作出现错误")
    elif result == "ERROR2":
        print('View DeleteAllRel查无两个结点间关系')
        return HttpResponse("查无两个结点间关系")
    else:
        print('View DeleteAllRel删除所有关系成功')
        UpdataPro(username, pro)
        return HttpResponse("删除关系成功")


def DeleteNodeAtt(request):#删除单个结点的某个属性值
    username = request.POST.get('username')
    pro = request.POST.get('pro')
    nodename = request.POST.get('nodename')
    attname = request.POST.get('attname')
    result = Neo4j.DeleteNodeAtt(username,pro,nodename,attname)
    if result == "ERROR1":
        print('View DeleteNodeAtt出现错误1')
        return HttpResponse("对数据库操作出现错误")
    elif result == "ERROR2":
        print('View DeleteNodeAtt查无此结点')
        return HttpResponse("查无此结点")
    elif result == "ERROR3":
        print('View DeleteNodeAtt查无此结点此属性')
        return HttpResponse("查无此结点此属性")
    else:
        print('View DeleteNodeAtt删除结点属性成功')
        UpdataPro(username, pro)
        return HttpResponse("删除结点属性成功")


def DeleteNodeLab(request):#删除单个结点某个标签
    username = request.POST.get('username')
    pro = request.POST.get('pro')
    nodename = request.POST.get('nodename')
    labname = request.POST.get('labname')
    result = Neo4j.DeleteNodeLab(username,pro,nodename,labname)
    if result == "ERROR1":
        print('View DeleteNodeLab出现错误1')
        return HttpResponse("对数据库操作出现错误")
    elif result == "ERROR2":
        print('View DeleteNodeLab查无此结点')
        return HttpResponse("查无此结点")
    else:
        print('View DeleteNodeLab删除结点标签成功')
        UpdataPro(username, pro)
        return HttpResponse("删除结点标签成功")


def AddNodeAtt(request):#给某个结点增加属性与属性值
    username = request.POST.get('username')
    pro = request.POST.get('pro')
    nodename = request.POST.get('nodename')
    attname = request.POST.get('attname')
    attvalue = request.POST.get('attvalue')
    result = Neo4j.AddNodeAtt(username,pro,nodename,attname,attvalue)
    if result == "ERROR1":
        print('View AddNodeAtt出现错误1')
        return HttpResponse("对数据库操作出现错误")
    elif result == "ERROR2":
        print('View AddNodeAtt查无此结点')
        return HttpResponse("查无此结点")
    else:
        print('View AddNodeAtt增加新的结点属性值成功')
        UpdataPro(username, pro)
        return HttpResponse("增加新的结点属性值成功")


def AddNodeLab(request):#给某个结点增加标签
    username = request.POST.get('username')
    pro = request.POST.get('pro')
    nodename = request.POST.get('nodename')
    labname = request.POST.get('labname')
    result = Neo4j.AddNodeLab(username,pro,nodename,labname)
    if result == "ERROR1":
        print('View AddNodeLab出现错误1')
        return HttpResponse("对数据库操作出现错误")
    elif result == "ERROR2":
        print('View AddNodeLab查无此结点')
        return HttpResponse("查无此结点")
    else:
        print('View AddNodeLab增加新的结点标签成功')
        UpdataPro(username, pro)
        return HttpResponse("增加新的结点标签成功")


def SetNodeAtt(request):#给某个结点重新设置属性值
    username = request.POST.get('username')
    pro = request.POST.get('pro')
    nodename = request.POST.get('nodename')
    attname = request.POST.get('attname')
    attvalue = request.POST.get('attvalue')
    result = Neo4j.SetNodeAtt(username,pro,nodename,attname,attvalue)
    if result == "ERROR1":
        print('View SetNodeAtt出现错误1')
        return HttpResponse("对数据库操作出现错误")
    elif result == "ERROR2":
        print('View SetNodeAtt查无此结点')
        return HttpResponse("查无此结点")
    elif result == "ERROR3":
        print('View SetNodeAtt查无此结点此属性')
        return HttpResponse("查无此结点此属性")
    else:
        print('View SetNodeAtt更改新的结点属性值成功')
        UpdataPro(username, pro)
        return HttpResponse("更改新的结点属性值成功")


def SetRelName(request):#给两个结点之间重新设置关系
    username = request.POST.get('username')
    pro = request.POST.get('pro')
    firnode = request.POST.get('firnode')
    secnode = request.POST.get('secnode')
    oldrelname = request.POST.get('oldrelname')
    newrelname = request.POST.get('newrelname')
    result = Neo4j.SetRelName(username,pro,firnode,secnode,oldrelname,newrelname)
    if result == "ERROR1":
        print('View SetRelName出现错误1')
        return HttpResponse("对数据库操作出现错误")
    elif result == "ERROR2":
        print('View SetRelName查无此关系')
        return HttpResponse("查无此关系")
    else:
        print('View SetRelName更改结点间新的关系成功')
        UpdataPro(username, pro)
        return HttpResponse("更改新的关系成功")


def UpdataPro(username,pro):#更新数据库中pro内容
    data = Neo4j.SelectOnePro(username,pro)
    if data == "ERROR1":
        print('View UpdataPro出现错误1')
        return HttpResponse("对数据库操作出现错误")
    elif data == "ERROR2":
        print('View UpdataPro Neo4j数据库中查无此工程信息')
        return HttpResponse("抱歉，此项目中不存在结点和关系")
    elif data == 'ERROR3':
        print('View UpdataPro出现错误3')
        return HttpResponse("抱歉，没有相关的画布信息，无法展示编辑结点")
    resultMY = MySQL.InsertPic(username, pro, data)
    if resultMY == 'ERROR1':
        print('View UpdataPro出现错误4')
        return HttpResponse("对数据库操作出现错误")
    dealdata = data
    data = data.replace('false', "'" + 'false' + "'").replace('true', "'" + 'true' + "'")
    data = eval(data)
    resultNeoNode = Neo4j.DeleteProByNode(username,pro)
    if resultNeoNode == 'ERROR1':
        print('View UpdataPro出现错误5')
        return HttpResponse("对数据库操作出现错误")
    elif resultNeoNode == 'ERROR2':
        print('View UpdataPro Neo4j数据库查无此工程节点')
        return HttpResponse("抱歉，查无此工程节点")
    resultNeo = Neo4j.InsertPic(username, pro, data)
    if resultNeo == 'ERROR1':
        print('View UpdataPro出现错误6')
        return HttpResponse("对数据库操作出现错误")
    resultNeoNode = Neo4j.InsertPicByNode(username, pro, dealdata)
    if resultNeoNode == 'ERROR1':
        print('View UpdataPro出现错误7')
        return HttpResponse("对数据库操作出现错误")
    else:
        print('View UpdataPro更新图谱数据成功')
        return HttpResponse("恭喜你，更新谱图数据成功")


def UpdataLayNode(layname):
    data = MySQL.SelectLayData(layname)
    if data == 'ERROR1':
        print('View UpdataLayNode出现错误1')
        return HttpResponse("对数据库操作出现错误")
    elif data == 'ERROR2':
        print('View UpdataLayNode MYSQL数据库中不存在此推荐布局信息')
        return HttpResponse("数据库中不存在此推荐布局信息")
    dataresult = Neo4jRecLayout.InsertRecLayNode(layname,data)
    if dataresult == 'ERROR1':
        print('View UpdataLayNode出现错误2')
        return HttpResponse("对数据库操作出现错误")
    deldata = Neo4jRecLayout.DeleteRecDis(layname)
    if deldata == 'ERROR1':
        print('View UpdataLayNode出现错误3')
        return HttpResponse("对数据库操作出现错误")
    elif deldata == 'ERROR2':
        print('View UpdataLayNode出现错误4')
        return HttpResponse("数据库中不存在此推荐布局信息")
    insdata = data
    insdata = insdata.replace('false', "'" + 'false' + "'").replace('true', "'" + 'true' + "'")
    insdata = eval(insdata)
    insresult = Neo4jRecLayout.InsertRecLayDis(layname,insdata)
    if insresult == 'ERROR1':
        print('View UpdataLayNode出现错误5')
        return HttpResponse("对数据库操作出现错误")


def UpdataProByTime(request):#更新数据库中pro内容（前端调用）
    username = request.POST.get('username')
    pro = request.POST.get('pro')
    resultMy = MySQL.SelectPic(username,pro)
    if resultMy == "ERROR1":
        print('View UpdataProByTime出现错误1')
        return HttpResponse("对数据库操作出现错误")
    elif resultMy == "ERROR2":
        print('View UpdataProByTime MySQL数据库查无此工程信息')
        return HttpResponse("抱歉，此项目中不存在结点和关系")
    resultNeoNode = Neo4j.SelectProByNode(username, pro)
    if resultNeoNode == 'ERROR1':
        print('View UpdataProByTime出现错误2')
        return HttpResponse("对数据库操作出现错误")
    elif resultMy == "ERROR2":
        print('View UpdataProByTime Neo4j数据库查无此工程信息节点')
        return HttpResponse("抱歉，此项目中不存在结点和关系")
    if resultMy == resultNeoNode:
        print('View UpdataProByTime 数据对比一致')
        return HttpResponse("OK")
    else:
        dealdata = resultMy
        data = resultMy.replace('false', "'" + 'false' + "'").replace('true', "'" + 'true' + "'")
        data = eval(data)
        resultNeoNode = Neo4j.DeleteProByNode(username, pro)
        if resultNeoNode == 'ERROR1':
            print('View UpdataProByTime出现错误3')
            return HttpResponse("对数据库操作出现错误")
        resultNeo = Neo4j.InsertPic(username, pro, data)
        if resultNeo == 'ERROR1':
            print('View UpdataProByTime出现错误4')
            return HttpResponse("对数据库操作出现错误")
        resultNeoNode = Neo4j.InsertPicByNode(username, pro, dealdata)
        if resultNeoNode == 'ERROR1':
            print('View UpdataProByTime出现错误5')
            return HttpResponse("对数据库操作出现错误")
        else:
            print('View UpdataProByTime不一致下更新图谱数据成功')
            return HttpResponse("恭喜你，不一致下更新谱图数据成功")


def UpdataLayByTime(request):#更新数据库中推荐布局内容（前端调用）
    layname = request.POST.get('layname')
    resultMy = MySQL.SelectLayData(layname)
    if resultMy == "ERROR1":
        print('View UpdataLayByTime出现错误1')
        return HttpResponse("对数据库操作出现错误")
    elif resultMy == "ERROR2":
        print('View UpdataLayByTime MySQL数据库查无此布局信息')
        return HttpResponse("抱歉，此推荐布局中不存在结点和关系")
    resultNeoNode = Neo4jRecLayout.SelectRecLayByNode(layname)
    if resultNeoNode == 'ERROR1':
        print('View UpdataLayByTime出现错误2')
        return HttpResponse("对数据库操作出现错误")
    elif resultMy == "ERROR2":
        print('View UpdataLayByTime Neo4j数据库查无此布局信息节点')
        return HttpResponse("抱歉，此推荐布局中不存在结点和关系")
    if resultMy == resultNeoNode:
        print('View UpdataLayByTime 数据对比一致')
        return HttpResponse("OK")
    else:
        dealdata = resultMy
        laydata = resultMy.replace('false', "'" + 'false' + "'").replace('true', "'" + 'true' + "'")
        laydata = eval(laydata)
        resultNeoNode = Neo4jRecLayout.DeleteRecNode(layname)
        if resultNeoNode == 'ERROR1':
            print('View UpdataLayByTime出现错误3')
            return HttpResponse("对数据库操作出现错误")
        resultNeo = Neo4jRecLayout.InsertRecLayDis(layname,laydata)
        if resultNeo == 'ERROR1':
            print('View UpdataLayByTime出现错误4')
            return HttpResponse("对数据库操作出现错误")
        resultNeoNode = Neo4jRecLayout.InsertRecLayNode(layname,dealdata)
        if resultNeoNode == 'ERROR1':
            print('View UpdataLayByTime出现错误5')
            return HttpResponse("对数据库操作出现错误")
        else:
            print('View UpdataLayByTime不一致下更新推荐布局数据成功')
            return HttpResponse("恭喜你，不一致下更新推荐布局数据成功")


