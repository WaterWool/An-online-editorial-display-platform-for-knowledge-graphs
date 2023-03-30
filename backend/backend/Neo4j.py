import copy
import json
from py2neo import *           # *中常用的是Node,Relationship,Graph
from pandas import DataFrame
graph = Graph("http://localhost:7474", auth=("neo4j", "123456"))
def InsertPic(username,pro,data):   #将数据插入到neo4j数据库中
    countnumber=0;
    clearstr = 'MATCH(n:'+username+':'+pro+') DETACH DELETE n'
    graph.run(clearstr)
    constr = 'MERGE(:'+username+':'+pro+'{height:%d'%(data['container']['height'])+',width:%d'%(data['container']['width'])+',name:'+"'"+'container'+"'"+'})'
    try:
        graph.run(clearstr)
        graph.run(constr)
    except:
        print('Neo4j InsertPic出现错误1')
        return 'ERROR1'
    print('Neo4j InsertPic清空结点与创建容器成功')
    for block in data['blocks']:
        nodestr = 'MERGE(n:'+username+':'+pro+'{top:%d'%block['top']+',left:%d'%block['left']+',componentKey:'+"'"+'%s'%block['componentKey']+"'"+',adjustPosition:%s'%block['adjustPosition']+',focus:%s'%block['focus']+',zIndex:%d'%block['zIndex']+',hasResize:%s'%block['hasResize']
        for key,value in block['props'].items():
            if key != 'classes':
                if type(value) == type('abc'):
                    if key == 'text':
                        nodestr = nodestr + ',name:'+"'"+'%s'% value+"'"
                    elif key == 'type':
                        value = "'"+value+"'"
                        nodestr = nodestr + ',p%s' % key + ':%s' % value
                    else:
                        nodestr = nodestr + ',p%s' % key + ':%s' % value
                elif isinstance(value,int):
                    nodestr = nodestr + ',p%s' % key + ':%d'%value
            else:
                typename = value;
                nodestr = nodestr + ',pclasses:' + "'" + '%s' % value + "'"
        nodestr +=',countnumber:%d})'%countnumber
        countnumber=countnumber+1
        if len(typename) != 0:
            nodestr +='SET n:%s'%typename
        typename=''
        try:
            graph.run(nodestr)
        except:
            print('Neo4j InsertPic出现错误2')
            return 'ERROR1'
    print('Neo4j InsertPic加入结点成功')
    for relation in data['arrows']:
        realstr = 'MATCH(n:'+username+':'+pro+'{countnumber:%d'%relation['num_start']+'}),(m:'+username+':'+pro+'{countnumber:%d'%relation['num_end']+'})'
        realstr = realstr + 'MERGE (n)-[:%s]->(m)'%relation['text']
        try:
            graph.run(realstr)
        except:
            print('Neo4j InsertPic出现错误3')
            return 'ERROR1'
    print('Neo4j InsertPic创建关系成功')
    return 'OK'


def InsertPicByNode(username,pro,nodedata):#以单个结点的形式存储整个pro的内容
    insertstr = 'MERGE (:' + username + ':'+pro+':coin{data:' + "'" + nodedata + "'" + '})'
    try:
        graph.run(insertstr)
        print('Neo4j InsertPicBynode创建结点工程数据成功')
        return 'OK'
    except:
        print('Neo4j InsertPicByNode出现错误1')
        return 'ERROR1'


def InsertOneNode(username ,pro, nodedata): #插入单个结点
    nodestr = 'MERGE(n:' + username + ':' + pro + '{top:%d' % nodedata['top'] + ',left:%d' % nodedata[
        'left'] + ',componentKey:' + "'" + '%s' % nodedata['componentKey'] + "'" + ',adjustPosition:%s' % nodedata[
                  'adjustPosition'] + ',focus:%s' % nodedata['focus'] + ',zIndex:%d' % nodedata['zIndex'] + ',hasResize:%s' % \
              nodedata['hasResize']
    for key, value in nodedata['props'].items():
        if key != 'classes':
            if type(value) == type('abc'):
                if key == 'text':
                    nodestr = nodestr + ',name:' + "'" + '%s' % value + "'"
                elif key == 'type':
                    value = "'" + value + "'"
                    nodestr = nodestr + ',p%s' % key + ':%s' % value
                else:
                    nodestr = nodestr + ',p%s' % key + ':%s' % value
            elif isinstance(value, int):
                nodestr = nodestr + ',p%s' % key + ':%d' % value
        else:
            typename = value
            nodestr = nodestr + ',pclasses:' + "'" + '%s' % value +"'"
    nodestr = nodestr + '})'
    if len(typename) != 0:
        nodestr += 'SET n:%s' % typename
    try:
        graph.run(nodestr)
        print('Neo4j InsertOneNode插入结点成功')
        return 'OK'
    except:
        print('Neo4j InsertOneNode出现错误1')
        return 'ERROR1'


def InsertOneRel(username,pro,firnode,secnode,relname): #创建单个关系
    firselstr = 'MATCH (n:'+username+':'+pro+')WHERE n.name = ' + "'"+firnode+"'" + 'RETURN n'
    secselstr = 'MATCH (m:' + username + ':' + pro + ')WHERE m.name = ' + "'"+secnode+"'"+ 'RETURN m'
    try:
        firdata = DataFrame(graph.run(firselstr).data())
    except:
        print('Neo4j InsertOneRel出现错误1')
        return 'ERROR1'
    try:
        secdata = DataFrame(graph.run(secselstr).data())
    except:
        print('Neo4j InsertOneRel出现错误2')
        return 'ERROR1'
    if firdata.empty or secdata.empty:
        print('Neo4j InsertOneRel出现错误3')
        return 'ERROR2'
    else:
        insertstr = 'MATCH (n:'+username+':'+pro+'{name:'+"'"+firnode+"'"+'}),(m:'+username+':'+pro+'{name:'+"'"+secnode+"'"+'})'
        insertstr = insertstr+'\nMERGE (n)-[r:'+relname+']->(m)'
        try:
            graph.run(insertstr)
            print('Neo4j InsertOneRel创建单个关系成功')
            return 'OK'
        except:
            print('Neo4j InsertOneRel出现错误4')
            return 'ERROR1'

#Select(查找相关函数)------------------------------------------


def SelectProByNode(username,pro):#通过单个结点查询pro的内容
    selstr = 'MATCH(n:' + username +':'+ pro + ':coin) RETURN n'
    try:
        seldata = graph.run(selstr).data()
        seldata = DataFrame(seldata)
    except:
        print('Neo4j SelectProByNode出现错误1')
        return 'ERROR1'
    if seldata.empty:
        print('Neo4j SelectProByNode出现错误2')
        return 'ERROR2'
    else:
        nodedata = seldata['n'].drop_duplicates().values.tolist()
        nodedata = nodedata[0]
        seldata = dict(nodedata)['data']
        print('Neo4j SelectProByNode成功查询项目数据')
        return seldata


def SelectOneNode(username,pro,nodename):   #查询单个node不包含关系
    tempprops = {}
    tempblock = {}
    blocks = []
    dicdata = {}
    selstr = 'MATCH (n:'+username+':'+pro+'{name:'+"'"+nodename+"'"+'})  return n'
    containerdata = SelectConatiner(username, pro)
    if containerdata:
        dicdata['container'] = containerdata
    else:
        print('Neo4j SelectOneNode出现错误1')
        return 'ERROR1'
    try:
        targetnode = graph.run(selstr).data()
        if targetnode:
            targetnode = dict(targetnode[0]['n'])
    except:
        print('Neo4j SelectOneNode出现错误2')
        return "ERROR1"
    if targetnode:
        for key, value in targetnode.items():
            if value == False:
                value = 'false'
            if key[0] == 'p':
                tempprops[key[1:]] = value
            elif key != 'countnumber':
                if key == 'name':
                    tempprops['text'] = value
                else:
                    tempblock[key] = value
        tempblock['props'] = tempprops
        print('Neo4j SelectOneNode成功查询单个结点数据')
        blocks.append(copy.deepcopy(tempblock))
        dicdata['blocks'] = blocks
    else:
        print('Neo4j SelectOneNode查无单个节点')
        return 'ERROR2'
    dicdata = json.dumps(dicdata, ensure_ascii=False)
    dicdata = dicdata.replace('"' + 'false' + '"', 'false').replace('"' + 'true' + '"', 'true')
    print('Neo4j SelectOneNode成功查询单个结点信息')
    print(dicdata)
    return dicdata


def SelectOneNodeAndRel(username,pro,nodename): #查询单个node包含指向它和它指向的所关系和结点
    flag = 0
    countnumber = 0
    rellist=[]
    dictdata = {}
    block=[]
    tempblock={}
    tempprops={}
    arrows=[]
    temparrow = {}
    onlynode = {}
    containerdata = SelectConatiner(username,pro)
    if containerdata:
        dictdata['container']=containerdata
    else:
        print('Neo4j SelectOneNodeAndRel出现错误1')
        return 'ERROR3'
    selstrin = 'MATCH (m:'+username+':'+pro+')-[r]->(n:'+username+':'+pro+'{name:'+"'"+nodename+"'"+'})  return m,type(r) as r,n'
    selstrout = 'MATCH (a:'+username+':'+pro+'{name:'+"'"+nodename+"'"+'})-[b]->(c:'+username+':'+pro+')  return a,type(b) as b,c'
    try:
        seldatain = graph.run(selstrin).data()
        seldatain = DataFrame(seldatain)
        seldataout = graph.run(selstrout).data()
        seldataout = DataFrame(seldataout)
    except:
        print('Neo4j SelectOneNodeAndRel出现错误2')
        return 'ERROR1'

    if not seldatain.empty:
        rellist = seldatain['r'].values.tolist()
        targetnode = dict(seldatain.loc[0]['n'])

    if not seldataout.empty:
        outrellist = seldataout['b'].values.tolist()
        targetnode = dict(seldataout.loc[0]['a'])
        rellist.extend(outrellist)

    if not seldataout.empty or not seldatain.empty:
        for key, value in targetnode.items():
            if value == False:
                value = 'false'
            if key[0] == 'p':
                tempprops[key[1:]] = value
            elif key != 'countnumber':
                if key == 'name':
                    tempprops['text'] = value
                else:
                    tempblock[key] = value
        tempblock['props'] = tempprops
        block.append(copy.deepcopy(tempblock))
        tempprops.clear()
        tempblock.clear()

    if not seldatain.empty:
        inlist = seldatain['m'].drop_duplicates().values.tolist()
        for node in inlist:
            countnumber = countnumber + 1
            nodedict = dict(node)
            for key,value in nodedict.items():
                if value == False:
                    value = 'false'
                if key[0] == 'p':
                    tempprops[key[1:]] = value
                elif key != 'countnumber':
                    if key == 'name':
                        tempprops['text'] = value
                    else:
                        tempblock[key] = value
            tempblock['props'] = tempprops
            block.append(copy.deepcopy(tempblock))
            tempprops.clear()
            tempblock.clear()
            temparrow['num_start'] = countnumber
            temparrow['num_end'] = 0
            temparrow['text'] = rellist[countnumber-1]
            arrows.append(copy.deepcopy(temparrow))
            temparrow.clear()

    if not seldataout.empty:
        outlist = seldataout['c'].drop_duplicates().values.tolist()
        for node in outlist:
            countnumber = countnumber + 1
            nodedict = dict(node)
            for key, value in nodedict.items():
                if value == False:
                    value = 'false'
                if key[0] == 'p':
                    tempprops[key[1:]] = value
                elif key != 'countnumber':
                    if key == 'name':
                        tempprops['text'] = value
                    else:
                        tempblock[key] = value
            tempblock['props'] = tempprops
            block.append(copy.deepcopy(tempblock))
            tempprops.clear()
            tempblock.clear()
            temparrow['num_start'] = 0
            temparrow['num_end'] = countnumber
            temparrow['text'] = rellist[countnumber - 1]
            arrows.append(copy.deepcopy(temparrow))
            temparrow.clear()

    if block:
        dictdata['blocks'] = block
    else:
        onlynode = SelectOneNode(username,pro,nodename)
        if onlynode:
            block.append(onlynode)
            dictdata['blocks'] = block
        else:
            flag=1

    if arrows:
        dictdata['arrows'] = arrows

    if flag ==0:
        dictdata = json.dumps(dictdata,ensure_ascii=False)
        dictdata = dictdata.replace('"' + 'false' + '"','false').replace('"' + 'true' + '"','true')
        print('Neo4j SelectOneNodeAndRel成功查询单个结点和关系')
        return dictdata

    else:
        print('Neo4j SelectOneNodeAndRel出现错误3')
        return 'ERROR2'


def SelectOneNodeAndRelIn(username,pro,nodename):
    blocks = []
    arrows = []
    tempprops = {}
    tempblock = {}
    temparrow = {}
    selnodelist = []
    dicdata = {}
    selstr = 'MATCH(n:'+username+":"+pro+'{name:'+'"'+nodename+'"}) RETURN n'
    selrelinstr = 'MATCH(m:'+username+':'+pro+')-[r]->'+'(n:' + username + ":" + pro + '{name:' + '"' + nodename + '"})  RETURN m,type(r) as r,n'
    condata = SelectConatiner(username,pro)
    if condata:
        dicdata['container'] = condata
    else:
        print('Neo4j SelectOneNodeAndRelIn出现错误1')
        return 'ERROR3'
    try:
        seldata = graph.run(selstr).data()
    except:
        print('Neo4j SelectOneNodeAndRelIn出现错误2')
        return 'ERROR1'
    if seldata:
        try:
            selrelindata = DataFrame(graph.run(selrelinstr).data())
        except:
            print('Neo4j SelectOneNodeAndRelIn出现错误3')
            return 'ERROR1'
        if not selrelindata.empty:
            selnodelist = selrelindata['n'].drop_duplicates().values.tolist()
            selnodelist = selnodelist + selrelindata['m'].drop_duplicates().values.tolist()
            selnodelist = set(selnodelist)
            selnodelist = list(selnodelist)
            if selnodelist:
                for node in selnodelist:
                    nodedict = dict(node)
                    for key, value in nodedict.items():
                        if value == False:
                            value = 'false'
                        if key[0] == 'p':
                            tempprops[key[1:]] = value
                        elif key != 'countnumber':
                            if key == 'name':
                                tempprops['text'] = value
                            else:
                                tempblock[key] = value
                    tempblock['props'] = tempprops
                    blocks.append(copy.deepcopy(tempblock))
                    tempprops.clear()
                    tempblock.clear()

                for index, row in selrelindata.iterrows():
                    num_start = selnodelist.index(row['m'])
                    num_end = selnodelist.index(row['n'])
                    relname = row['r']
                    temparrow['num_start'] = num_start
                    temparrow['num_end'] = num_end
                    temparrow['text'] = relname
                    arrows.append(copy.deepcopy(temparrow))

                if blocks:
                    dicdata['blocks'] = blocks
                    dicdata['arrows'] = arrows

                if dicdata:
                    dicdata = json.dumps(dicdata, ensure_ascii=False)
                    dicdata = dicdata.replace('"' + 'false' + '"', 'false').replace('"' + 'true' + '"', 'true')
                    print('Neo4j SelectOneNodeAndRelIn成功查询结点和其对应指向的关系')
                    return dicdata
                else:
                    print('Neo4j SelectOneNodeAndRelIn出现错误4')
                    return 'ERROR1'
        else:
            dicdatastr = SelectOneNode(username,pro,nodename)
            print('Neo4j SelectOneNodeAndRelIn没有指向内的关系')
            return dicdatastr
    else:
        print('Neo4j SelectOneNodeAndRelIn在数据库中查无此节点')
        return 'ERROR2'


def SelectOneNodeAndRelOut(username,pro,nodename):
    blocks = []
    arrows = []
    tempprops = {}
    tempblock = {}
    temparrow = {}
    selnodelist = []
    dicdata = {}
    selstr = 'MATCH(n:' + username + ":" + pro + '{name:' + '"' + nodename + '"}) RETURN n'
    selreloutstr = 'MATCH(n:' + username + ':' + pro + '{name:' + '"' + nodename + '"'+'})-[r]->' + '(m:' + username + ":" + pro + ')  RETURN n,type(r) as r,m'
    condata = SelectConatiner(username, pro)
    if condata:
        dicdata['container'] = condata
    else:
        print('Neo4j SelectOneNodeAndRelOut出现错误1')
        return 'ERROR3'
    try:
        seldata = graph.run(selstr).data()
    except:
        print('Neo4j SelectOneNodeAndRelOut出现错误2')
        return 'ERROR1'
    if seldata:
        try:
            selreldata = DataFrame(graph.run(selreloutstr).data())
        except:
            print('Neo4j SelectOneNodeAndRelOut出现错误3')
            return 'ERROR1'
        if not selreldata.empty:
            selnodelist = selreldata['n'].drop_duplicates().values.tolist()
            selnodelist = selnodelist + selreldata['m'].drop_duplicates().values.tolist()
            selnodelist = set(selnodelist)
            selnodelist = list(selnodelist)
            for node in selnodelist:
                nodedata = dict(node)
                for key, value in nodedata.items():
                    if value == False:
                        value = 'false'
                    if key[0] == 'p':
                        tempprops[key[1:]] = value
                    elif key != 'countnumber':
                        if key == 'name':
                            tempprops['text'] = value
                        else:
                            tempblock[key] = value
                tempblock['props'] = tempprops
                blocks.append(copy.deepcopy(tempblock))
                tempprops.clear()
                tempblock.clear()
            for index, row in selreldata.iterrows():
                num_start = selnodelist.index(row['n'])
                num_end = selnodelist.index(row['m'])
                relname = row['r']
                temparrow['num_start'] = num_start
                temparrow['num_end'] = num_end
                temparrow['text'] = relname
                arrows.append(copy.deepcopy(temparrow))
                temparrow.clear()

            if blocks:
                dicdata['blocks'] = blocks
            if arrows:
                dicdata['arrows'] = arrows
            if dicdata:
                dicdata = json.dumps(dicdata, ensure_ascii=False)
                dicdata = dicdata.replace('"' + 'false' + '"', 'false').replace('"' + 'true' + '"', 'true')
                print('Neo4j SelectOneNodeAndRelOut成功查询结点和对应指出关系')
                print(dicdata)
                return dicdata
            else:
                print('Neo4j SelectOneNodeAndRelOut出现错误4')
                return 'ERROR3'
        else:
            dicdatastr = SelectOneNode(username,pro,nodename)
            print('Neo4j SelectOneNodeAndRelOut因没有出的关系所以输出此结点信息')
            return dicdatastr
    else:
        print('Neo4j SelectOneNodeAndRelOut数据库查无此结点')
        return 'ERROR2'


def SelectConatiner(username,pro):
    selstr = 'MATCH(n:'+username+':'+pro+'{name:'+"'container'"+'}) RETURN n'
    try:
        container = graph.run(selstr).data()
        if container:
            container = dict(container[0]['n'])
    except:
        print('Neo4j SelectContainer出现错误1')
        return 'ERROR1'
    containerdata = {}
    containerdata['height'] = container['height']
    containerdata['width'] = container['width']
    print('Neo4j SelectContainer成功查询画布数据')
    return containerdata


def SelectOnePro(username,pro):     #查询一个用户的一整个pro中所有的结点和关系
    dictdata = {}
    block = []
    tempblock = {}
    tempprops = {}
    arrows = []
    temparrow = {}
    container = {}
    selstrnode = 'MATCH(n:'+username+':'+pro+')WHERE n.name<>'+"'"+'container'+"'"+'RETURN n'
    try:
        selnodedata = graph.run(selstrnode).data()
    except:
        print('Neo4j SelectOnePro出现错误1')
        return 'ERROR1'
    selnodedata = DataFrame(selnodedata)
    selnodedata = selnodedata['n'].drop_duplicates().values.tolist()
    container = SelectConatiner(username,pro)
    if container:
        dictdata['container'] = container
    else:
        print('Neo4j SelectOnePro出现错误2')
        return 'ERROR3'
    if selnodedata:
        for node in selnodedata:
            nodedict = dict(node)
            for key, value in nodedict.items():
                if value == False:
                    value = 'false'
                if key[0] == 'p':
                    tempprops[key[1:]] = value
                elif key != 'countnumber':
                    if key == 'name':
                        tempprops['text'] = value
                    else:
                        tempblock[key] = value
            tempblock['props'] = tempprops
            block.append(copy.deepcopy(tempblock))
            tempprops.clear()
            tempblock.clear()

    selrelnodestr = 'MATCH(n:'+username+':'+pro+')-[r]->(m:'+username+':'+pro+') RETURN n,m,type(r) as r'
    try:
        selrelnodedata = DataFrame(graph.run(selrelnodestr).data())
    except:
        print('Neo4j SelectOnePro出现错误3')
        return 'ERROR1'
    if not selrelnodedata.empty:
        for index,row in selrelnodedata.iterrows():
            num_start = selnodedata.index(row['n'])
            num_end = selnodedata.index(row['m'])
            relname = row['r']
            temparrow['num_start'] = num_start
            temparrow['num_end'] = num_end
            temparrow['text'] = relname
            arrows.append(copy.deepcopy(temparrow))
            temparrow.clear()

    if block:
        dictdata['blocks'] = block
    if arrows:
        dictdata['arrows'] = arrows
    if dictdata:
        dictdata = json.dumps(dictdata,ensure_ascii=False)
        dictdata = dictdata.replace('"' + 'false' + '"', 'false').replace('"' + 'true' + '"', 'true')
        print('Neo4j SelectOnePro成功查询工程数据')
        return dictdata
    else:
        print('Neo4j SelectOnePro出现错误4')
        return 'ERROR2'



def SelectOneRel(username,pro,relname):#查询一个pro中有这样关系的所有结点和关系
    dicdata = {}
    block = []
    tempblock = {}
    tempprops = {}
    arrows = []
    temparrow = {}
    container = {}
    container = SelectConatiner(username,pro)
    if container:
        dicdata['container'] = container
    else:
        print('Neo4j SelectOneRel出现错误1')
        return 'ERROR3'
    selrelnodestr = 'MATCH(n:' + username + ':' + pro + ')-[r:'+relname+']->(m:' + username + ':' + pro + ') RETURN n,m,type(r) as r'
    try:
        selrelnodedata = DataFrame(graph.run(selrelnodestr).data())
    except:
        print('Neo4j SelectOneRel出现错误2')
        return 'ERROR1'
    selnodelist = selrelnodedata['n'].drop_duplicates().values.tolist()
    selnodelist = selnodelist+selrelnodedata['m'].drop_duplicates().values.tolist()
    selnodelist = set(selnodelist)
    selnodelist = list(selnodelist)
    if selnodelist:
        for node in selnodelist:
            nodedict = dict(node)
            for key, value in nodedict.items():
                if value == False:
                    value = 'false'
                if key[0] == 'p':
                    tempprops[key[1:]] = value
                elif key != 'countnumber':
                    if key == 'name':
                        tempprops['text'] = value
                    else:
                        tempblock[key] = value
            tempblock['props'] = tempprops
            block.append(copy.deepcopy(tempblock))
            tempprops.clear()
            tempblock.clear()

        for index,row in selrelnodedata.iterrows():
            num_start = selnodelist.index(row['n'])
            num_end = selnodelist.index(row['m'])
            temparrow['num_start'] = num_start
            temparrow['num_end'] = num_end
            temparrow['text'] = relname
            arrows.append(copy.deepcopy(temparrow))

        if block:
            dicdata['blocks'] = block
        if arrows:
            dicdata['arrows'] = arrows
        if dicdata:
            dicdata = json.dumps(dicdata, ensure_ascii=False)
            dictdata = dicdata.replace('"' + 'false' + '"', 'false').replace('"' + 'true' + '"', 'true')
            print('Neo4j SelectOneRel成功查询关系数据')
            return dictdata
        else:
            print('Neo4j SelectOneRel出现错误3')
            return 'ERROR2'
    else:
        print('Neo4j SelectOneRel查无此关系数据')
        return 'ERROR2'


def SelectOneTypeAndRel(username,pro,typename):   #查询一个类别的结点和其对应的关系
    dicdata = {}
    block = []
    tempblock = {}
    tempprops = {}
    arrows = []
    temparrow = {}
    container = {}
    container = SelectConatiner(username, pro)
    if container:
        dicdata['container'] = container
    else:
        print('Neo4j SelectOneTypeAndRel出现错误1')
        return 'ERROR3'
    selstrallnoe = 'MATCH(n:' + username + ':' + pro + ':'+typename+')RETURN n'
    selrelnodestrout = 'MATCH(n:' + username + ':' + pro + ':' +typename + ')-[r]->(m:' + username + ':' + pro + ') RETURN n,m,type(r) as r'
    selrelnodestrin = 'MATCH(n:' + username + ':' + pro + ')-[r]->(m:' + username + ':' + pro + ':'+typename + ') RETURN n,m,type(r) as r'
    try:
        nodedatall = graph.run(selstrallnoe).data()
        nodedatall = DataFrame(nodedatall)
        if not nodedatall.empty:
            nodelist = nodedatall['n'].drop_duplicates().values.tolist()
    except:
        print('Neo4j SelectOneTypeAndRel出现错误2')
        return 'ERROR1'
    try:
        nodedataout = graph.run(selrelnodestrout).data()
        nodedataout = DataFrame(nodedataout)
        if not nodedataout.empty:
            nodelist = nodelist + nodedataout['n'].drop_duplicates().values.tolist() + nodedataout['m'].drop_duplicates().values.tolist()
    except:
        print('Neo4j SelectOneTypeAndRel出现错误3')
        return 'ERROR1'
    try:
        nodedatain = graph.run(selrelnodestrin).data()
        nodedatain = DataFrame(nodedatain)
        if not nodedatain.empty:
            nodelist = nodelist + nodedatain['n'].drop_duplicates().values.tolist() + nodedatain['m'].drop_duplicates().values.tolist()
    except:
        print('Neo4j SelectOneTypeAndRel出现错误4')
        return 'ERROR1'
    nodelist = set(nodelist)
    nodelist = list(nodelist)
    if nodelist:
        for node in nodelist:
            nodedict = dict(node)
            for key, value in nodedict.items():
                if value == False:
                    value = 'false'
                if key[0] == 'p':
                    tempprops[key[1:]] = value
                elif key != 'countnumber':
                    if key == 'name':
                        tempprops['text'] = value
                    else:
                        tempblock[key] = value
            tempblock['props'] = tempprops
            block.append(copy.deepcopy(tempblock))
            tempprops.clear()
            tempblock.clear()

    if not nodedataout.empty:
        for index, row in nodedataout.iterrows():
            num_start = nodelist.index(row['n'])
            num_end = nodelist.index(row['m'])
            relname = row['r']
            temparrow['num_start'] = num_start
            temparrow['num_end'] = num_end
            temparrow['text'] = relname
            arrows.append(copy.deepcopy(temparrow))
            temparrow.clear()

    if not nodedatain.empty:
        for index, row in nodedatain.iterrows():
            num_start = nodelist.index(row['n'])
            num_end = nodelist.index(row['m'])
            relname = row['r']
            temparrow['num_start'] = num_start
            temparrow['num_end'] = num_end
            temparrow['text'] = relname
            arrows.append(copy.deepcopy(temparrow))
            temparrow.clear()

    if block:
        dicdata['blocks'] = block
    if arrows:
        dicdata['arrows'] = arrows
    if dicdata:
        dicdata = json.dumps(dicdata, ensure_ascii=False)
        dicdata = dicdata.replace('"' + 'false' + '"', 'false').replace('"' + 'true' + '"', 'true')
        print('Neo4j SelectOneTypeAndRel成功查询类型结点与关系')
        return dicdata
    else:
        print('Neo4j SelectOneTypeAndRel出现错误5')
        return 'ERROR2'


def SelectOneTypeNoRel(username,pro,typename):#查找一个类型的结点与其有关系的结点(所有结点都为这个类型)
    dicdata = {}
    block = []
    tempblock = {}
    tempprops = {}
    arrows = []
    temparrow = {}
    container = {}
    container = SelectConatiner(username,pro)
    if container:
        dicdata['container'] = container
    else:
        print('Neo4j SelectOneTypeNoRel出现错误1')
        return 'ERROR3'
    selstrallnode  = 'MATCH(n:' + username + ':' + pro + ':'+typename+') RETURN n'
    selrelnodestrrel = 'MATCH(n:' + username + ':' + pro + ':'+typename+')-[r]->(m:' + username + ':' + pro + ':'+typename+') RETURN n,m,type(r) as r'
    try:
        nodedatall = graph.run(selstrallnode).data()
        nodedatall = DataFrame(nodedatall)
        nodelist = nodedatall['n'].drop_duplicates().values.tolist()
    except:
        print('Neo4j SelectOneTypeNoRel出现错误2')
        return 'ERROR1'
    try:
        nodedatarel = graph.run(selrelnodestrrel).data()
        nodedatarel = DataFrame(nodedatarel)
    except:
        print('Neo4j SelectOneTypeNoRel出现错误3')
        return 'ERROR1'

    if nodelist:
        for node in nodelist:
            nodedict = dict(node)
            for key, value in nodedict.items():
                if value == False:
                    value = 'false'
                if key[0] == 'p':
                    tempprops[key[1:]] = value
                elif key != 'countnumber':
                    if key == 'name':
                        tempprops['text'] = value
                    else:
                        tempblock[key] = value
            tempblock['props'] = tempprops
            block.append(copy.deepcopy(tempblock))
            tempprops.clear()
            tempblock.clear()

    if not nodedatarel.empty:
        for index, row in nodedatarel.iterrows():
            num_start = nodelist.index(row['n'])
            num_end = nodelist.index(row['m'])
            relname = row['r']
            temparrow['num_start'] = num_start
            temparrow['num_end'] = num_end
            temparrow['text'] = relname
            arrows.append(copy.deepcopy(temparrow))
            temparrow.clear()

    if block:
        dicdata['blocks'] = block
    if arrows:
        dicdata['arrows'] = arrows
    if dicdata:
        dicdata = json.dumps(dicdata, ensure_ascii=False)
        dicdata = dicdata.replace('"' + 'false' + '"', 'false').replace('"' + 'true' + '"', 'true')
        print('Neo4j SelectOneTypeNoRel成功查询类型结点数据')
        return dicdata
    else:
        print('Neo4j SelectOneTypeNoRel出现错误4')
        return 'ERROR2'


def SelectOneClourNoRel(username,pro,clourname):#查找一个颜色的结点与其有关系的结点(所有结点都为这个颜色)
    dicdata = {}
    block = []
    tempblock = {}
    tempprops = {}
    arrows = []
    temparrow = {}
    container = {}
    container = SelectConatiner(username, pro)
    if container:
        dicdata['container'] = container
    else:
        print('Neo4j SelectOneClourNoRel出现错误1')
        return 'ERROR3'
    selstrallnoe = 'MATCH(n:' + username + ':' + pro + ') WHERE n.ptype=' + "'" + clourname + "'" + ' or (n.ptype=' + "'" + "'" + ' and n.componentKey=' + "'" + clourname + "'" + ') RETURN n'
    selrelnodestr = 'MATCH(n:' + username + ':' + pro + ')-[r]->(m:' + username + ':' + pro + ') WHERE (n.ptype=' + "'" + clourname + "'" + ' or (n.ptype=' + "'" + "'" + ' and n.componentKey=' + "'" + clourname + "'" + ')) and (m.ptype=' + "'" + clourname + "'" + ' or (m.ptype=' + "'" + "'" + ' and m.componentKey=' + "'" + clourname + "'" + ')) RETURN n,m,type(r) as r'
    try:
        nodedatall = graph.run(selstrallnoe).data()
        nodedatall = DataFrame(nodedatall)
        if not nodedatall.empty:
            nodelist = nodedatall['n'].drop_duplicates().values.tolist()
    except:
        print('Neo4j SelectOneClourNoRel出现错误2')
        return 'ERROR1'
    try:
        nodedata = graph.run(selrelnodestr).data()
        nodedata = DataFrame(nodedata)
        if not nodedata.empty:
            nodelist = nodelist + nodedata['n'].drop_duplicates().values.tolist() + nodedata['m'].drop_duplicates().values.tolist()
    except:
        print('Neo4j SelectOneClourNoRel出现错误3')
        return 'ERROR1'

    nodelist = set(nodelist)
    nodelist = list(nodelist)
    if nodelist:
        for node in nodelist:
            nodedict = dict(node)
            for key, value in nodedict.items():
                if value == False:
                    value = 'false'
                if key[0] == 'p':
                    tempprops[key[1:]] = value
                elif key != 'countnumber':
                    if key == 'name':
                        tempprops['text'] = value
                    else:
                        tempblock[key] = value
            tempblock['props'] = tempprops
            block.append(copy.deepcopy(tempblock))
            tempprops.clear()
            tempblock.clear()

    if not nodedata.empty:
        for index, row in nodedata.iterrows():
            num_start = nodelist.index(row['n'])
            num_end = nodelist.index(row['m'])
            relname = row['r']
            temparrow['num_start'] = num_start
            temparrow['num_end'] = num_end
            temparrow['text'] = relname
            arrows.append(copy.deepcopy(temparrow))
            temparrow.clear()

    if block:
        dicdata['blocks'] = block
    if arrows:
        dicdata['arrows'] = arrows
    if dicdata:
        dicdata = json.dumps(dicdata, ensure_ascii=False)
        dicdata = dicdata.replace('"' + 'false' + '"', 'false').replace('"' + 'true' + '"', 'true')
        print('Neo4j SelectOneClourNoRel成功查询此颜色结点')
        return dicdata
    else:
        print('Neo4j SelectOneClourNoRel出现错误4')
        return 'ERROR2'

def SelectOneClourAndRel(username,pro,clourname):#查找一个颜色的结点与其有关系的结点(包含不是这个颜色的结点)
    dicdata = {}
    block = []
    tempblock = {}
    tempprops = {}
    arrows = []
    temparrow = {}
    container = {}
    container = SelectConatiner(username,pro)
    if container:
        dicdata['container'] = container
    else:
        print('Neo4j SelectOneClourAndRel出现错误1')
        return 'ERROR3'
    selstrallnoe  = 'MATCH(n:' + username + ':' + pro + ') WHERE n.ptype='+"'"+clourname+"'"+' or (n.ptype='+"'"+"'"+' and n.componentKey='+"'"+clourname+"'"+') RETURN n'
    selrelnodestrout = 'MATCH(n:' + username + ':' + pro + ')-[r]->(m:' + username + ':' + pro + ') WHERE n.ptype='+"'"+clourname+"'"+' or (n.ptype='+"'"+"'"+' and n.componentKey='+"'"+clourname+"'"+') RETURN n,m,type(r) as r'
    selrelnodestrin = 'MATCH(n:' + username + ':' + pro + ')-[r]->(m:' + username + ':' + pro + ') WHERE m.ptype=' + "'" + clourname + "'" + ' or (m.ptype=' + "'" + "'" + ' and m.componentKey=' + "'" + clourname + "'" + ') RETURN n,m,type(r) as r'
    try:
        nodedatall = graph.run(selstrallnoe).data()
        nodedatall = DataFrame(nodedatall)
        nodelist = nodedatall['n'].drop_duplicates().values.tolist()
    except:
        print('Neo4j SelectOneClourAndRel出现错误2')
        return 'ERROR1'
    try:
        nodedataout = graph.run(selrelnodestrout).data()
        nodedataout = DataFrame(nodedataout)
        if not nodedataout.empty:
            nodelist = nodelist+nodedataout['n'].drop_duplicates().values.tolist()+nodedataout['m'].drop_duplicates().values.tolist()
    except:
        print('Neo4j SelectOneClourAndRel出现错误3')
        return 'ERROR1'
    try:
        nodedatain = graph.run(selrelnodestrin).data()
        nodedatain = DataFrame(nodedatain)
        if not nodedatain.empty:
            nodelist = nodelist+nodedatain['n'].drop_duplicates().values.tolist()+nodedatain['m'].drop_duplicates().values.tolist()
    except:
        print('Neo4j SelectOneClourAndRel出现错误4')
        return 'ERROR1'
    nodelist = set(nodelist)
    nodelist = list(nodelist)
    if nodelist:
        for node in nodelist:
            nodedict = dict(node)
            for key, value in nodedict.items():
                if value == False:
                    value = 'false'
                if key[0] == 'p':
                    tempprops[key[1:]] = value
                elif key != 'countnumber':
                    if key == 'name':
                        tempprops['text'] = value
                    else:
                        tempblock[key] = value
            tempblock['props'] = tempprops
            block.append(copy.deepcopy(tempblock))
            tempprops.clear()
            tempblock.clear()

    if not nodedataout.empty:
        for index, row in nodedataout.iterrows():
            num_start = nodelist.index(row['n'])
            num_end = nodelist.index(row['m'])
            relname = row['r']
            temparrow['num_start'] = num_start
            temparrow['num_end'] = num_end
            temparrow['text'] = relname
            arrows.append(copy.deepcopy(temparrow))
            temparrow.clear()


    if not nodedatain.empty:
        for index, row in nodedatain.iterrows():
            num_start = nodelist.index(row['n'])
            num_end = nodelist.index(row['m'])
            relname = row['r']
            temparrow['num_start'] = num_start
            temparrow['num_end'] = num_end
            temparrow['text'] = relname
            arrows.append(copy.deepcopy(temparrow))
            temparrow.clear()

    if block:
        dicdata['blocks'] = block
    if arrows:
        dicdata['arrows'] = arrows
    if dicdata:
        dicdata = json.dumps(dicdata, ensure_ascii=False)
        dicdata = dicdata.replace('"' + 'false' + '"', 'false').replace('"' + 'true' + '"', 'true')
        print('Neo4j SelectOneClourAndRel成功查询颜色结点与关系')
        return dicdata
    else:
        print('Neo4j SelectOneClourAndRel出现错误5')
        return 'ERROR2'


def SelectTwoNode(username,pro,nodename1,nodename2):#单独查询两个节点之间的信息
    dicdata = {}
    blocks = []
    arrows = []
    temppropers = {}
    tempblock = {}
    selstr = 'MATCH (n:' + username + ':' + pro+') where n.name = '+"'"+nodename1+"'"+'or n.name = '+"'"+nodename2+"'"+'return n'
    container = SelectConatiner(username, pro)
    if container:
        dicdata['container'] = container
    else:
        print('Neo4j SelectTwoNode出现错误1')
        return 'ERROR3'
    try:
        nodedataall = graph.run(selstr).data()
        nodedataall = DataFrame(nodedataall)
        nodelist = nodedataall['n'].drop_duplicates().values.tolist()
    except:
        print('Neo4j SelectTwoNode出现错误2')
        return 'ERROR1'
    if nodelist:
        for node in nodelist:
            nodedict = dict(node)
            for key, value in nodedict.items():
                if value == False:
                    value = 'false'
                if key[0] == 'p':
                    temppropers[key[1:]] = value
                elif key != 'countnumber':
                    if key == 'name':
                        temppropers['text'] = value
                    else:
                        tempblock[key] = value
            tempblock['props'] = temppropers
            blocks.append(copy.deepcopy(tempblock))
            temppropers.clear()
            tempblock.clear()

        if blocks:
            dicdata['blocks'] = blocks
        if arrows:
            dicdata['arrows'] = arrows
        if dicdata:
            dicdata = json.dumps(dicdata, ensure_ascii=False)
            dicdata = dicdata.replace('"' + 'false' + '"', 'false').replace('"' + 'true' + '"', 'true')
            print('Neo4j SelectTwoNode成功查询两个单独的结点')
            print(dicdata)
            return dicdata
        else:
            print('Neo4j SelectTwoNode出现错误4')
            return 'ERROR1'
    else:
        print('Neo4j SelectTwoNode查无两个节点中的任意一个')
        return 'ERROR2'


def SelectTwoNodePath(username,pro,nodename1,nodename2):#查询两个节点之间所有的路径
    dicdata = {}
    blocks = []
    arrows = []
    temppropers = {}
    tempblock = {}
    temparrow = {}
    selstr = 'match p = (a:'+username+':'+pro+'{name:'+'"'+nodename1+'"'+'})-[r*]->(b:'+username+':'+pro+'{name:'+'"'+nodename2+'"'+'}) where all ( n1 in nodes(p) where size([n2 in nodes(p) where id(n1) = id(n2)])=1 ) with r match(n:'+username+':'+pro+')-[w]->(m:'+username+':'+pro+') where w in r return n,type(w) as w,m'
    container = SelectConatiner(username, pro)
    if container:
        dicdata['container'] = container
    else:
        print('Neo4j SelectTwoNodePath出现错误1')
        return 'ERROR3'
    try:
        nodedataall = graph.run(selstr).data()
        nodedataall = DataFrame(nodedataall)
    except:
        print('Neo4j SelectTwoNodePath出现错误2')
        return 'ERROR1'
    if not nodedataall.empty:
        nodelist = nodedataall['n'].drop_duplicates().values.tolist()
        nodelist = nodelist + nodedataall['m'].drop_duplicates().values.tolist()
        nodelist = set(nodelist)
        nodelist = list(nodelist)
        for node in nodelist:
            nodedict = dict(node)
            for key, value in nodedict.items():
                if value == False:
                    value = 'false'
                if key[0] == 'p':
                    temppropers[key[1:]] = value
                elif key != 'countnumber':
                    if key == 'name':
                        temppropers['text'] = value
                    else:
                        tempblock[key] = value
            tempblock['props'] = temppropers
            blocks.append(copy.deepcopy(tempblock))
            temppropers.clear()
            tempblock.clear()

        for index, row in nodedataall.iterrows():
            num_start = nodelist.index(row['n'])
            num_end = nodelist.index(row['m'])
            relname = row['w']
            temparrow['num_start'] = num_start
            temparrow['num_end'] = num_end
            temparrow['text'] = relname
            arrows.append(copy.deepcopy(temparrow))
            temparrow.clear()

        if blocks:
            dicdata['blocks'] = blocks
        if arrows:
            dicdata['arrows'] = arrows
        if dicdata:
            dicdata = json.dumps(dicdata, ensure_ascii=False)
            dicdata = dicdata.replace('"' + 'false' + '"', 'false').replace('"' + 'true' + '"', 'true')
            print('Neo4j SelectTwoNodePath成功查询两个结点之间的所有通路')
            return dicdata
        else:
            print('Neo4j SelectTwoNodePath出现错误3')
            return 'ERROR1'
    else:
        print('Neo4j SelectTwoNodePath查无连个结点之间的通路')
        twonodedata = SelectTwoNode(username,pro,nodename1,nodename2)
        if type(twonodedata) != 'str':
            return twonodedata
        elif twonodedata == 'ERROR2':
            print('Neo4j SelectTwoNodePath查无此两个节点')
            return 'ERROR2'
        else:
            print('Neo4j SelectTwoNodePath出现错误4')
            return 'ERROR1'


def SelectTwoNodeShortPath(username,pro,nodename1,nodename2):#查询两个节点之间的最短路径
    dicdata = {}
    blocks = []
    arrows = []
    temppropers = {}
    tempblock = {}
    temparrow = {}
    selstr = 'match p = shortestpath((a:'+username+':'+pro+'{name:'+'"'+nodename1+'"'+'})-[r*]->(b:'+username+':'+pro+'{name:'+'"'+nodename2+'"'+'})) where all ( n1 in nodes(p) where size([n2 in nodes(p) where id(n1) = id(n2)])=1 ) with r match(n:'+username+':'+pro+')-[w]->(m:'+username+':'+pro+') where w in r return n,type(w) as w,m'
    container = SelectConatiner(username, pro)
    if container:
        dicdata['container'] = container
    else:
        print('Neo4j SelectTwoNodeShortPath出现错误1')
        return 'ERROR3'
    try:
        nodedataall = graph.run(selstr).data()
        nodedataall = DataFrame(nodedataall)
    except:
        print('Neo4j SelectTwoNodeShortPath出现错误2')
        return 'ERROR1'
    if not nodedataall.empty:
        nodelist = nodedataall['n'].drop_duplicates().values.tolist()
        nodelist = nodelist + nodedataall['m'].drop_duplicates().values.tolist()
        nodelist = set(nodelist)
        nodelist = list(nodelist)
        for node in nodelist:
            nodedict = dict(node)
            for key, value in nodedict.items():
                if value == False:
                    value = 'false'
                if key[0] == 'p':
                    temppropers[key[1:]] = value
                elif key != 'countnumber':
                    if key == 'name':
                        temppropers['text'] = value
                    else:
                        tempblock[key] = value
            tempblock['props'] = temppropers
            blocks.append(copy.deepcopy(tempblock))
            temppropers.clear()
            tempblock.clear()

        for index, row in nodedataall.iterrows():
            num_start = nodelist.index(row['n'])
            num_end = nodelist.index(row['m'])
            relname = row['w']
            temparrow['num_start'] = num_start
            temparrow['num_end'] = num_end
            temparrow['text'] = relname
            arrows.append(copy.deepcopy(temparrow))
            temparrow.clear()

        if blocks:
            dicdata['blocks'] = blocks
        if arrows:
            dicdata['arrows'] = arrows
        if dicdata:
            dicdata = json.dumps(dicdata, ensure_ascii=False)
            dicdata = dicdata.replace('"' + 'false' + '"', 'false').replace('"' + 'true' + '"', 'true')
            print('Neo4j SelectTwoNodeShortPath成功查询两个结点之间的最短路径')
            return dicdata
        else:
            print('Neo4j SelectTwoNodeShortPath出现错误3')
            return 'ERROR1'
    else:
        print('Neo4j SelectTwoNodeShortPath查无连个结点之间的通路')
        twonodedata = SelectTwoNode(username,pro,nodename1,nodename2)
        if type(twonodedata) != 'str':
            return twonodedata
        elif twonodedata == 'ERROR2':
            print('Neo4j SelectTwoNodeShortPath查无此两个节点')
            return 'ERROR2'
        else:
            print('Neo4j SelectTwoNodeShortPath出现错误4')
            return 'ERROR1'


def SelectTwoNodeAllShortPath(username,pro,nodename1,nodename2):#查询两个节点之间所有的最短路径
    dicdata = {}
    blocks = []
    arrows = []
    temppropers = {}
    tempblock = {}
    temparrow = {}
    selstr = 'match p = allshortestpaths((a:'+username+':'+pro+'{name:'+'"'+nodename1+'"'+'})-[r*]->(b:'+username+':'+pro+'{name:'+'"'+nodename2+'"'+'})) where all ( n1 in nodes(p) where size([n2 in nodes(p) where id(n1) = id(n2)])=1 ) with r match(n:'+username+':'+pro+')-[w]->(m:'+username+':'+pro+') where w in r return n,type(w) as w,m'
    container = SelectConatiner(username, pro)
    if container:
        dicdata['container'] = container
    else:
        print('Neo4j SelectTwoNodeAllShortPath出现错误1')
        return 'ERROR3'
    try:
        nodedataall = graph.run(selstr).data()
        nodedataall = DataFrame(nodedataall)
    except:
        print('Neo4j SelectTwoNodeAllShortPath出现错误2')
        return 'ERROR1'
    if not nodedataall.empty:
        nodelist = nodedataall['n'].drop_duplicates().values.tolist()
        nodelist = nodelist + nodedataall['m'].drop_duplicates().values.tolist()
        nodelist = set(nodelist)
        nodelist = list(nodelist)
        for node in nodelist:
            nodedict = dict(node)
            for key, value in nodedict.items():
                if value == False:
                    value = 'false'
                if key[0] == 'p':
                    temppropers[key[1:]] = value
                elif key != 'countnumber':
                    if key == 'name':
                        temppropers['text'] = value
                    else:
                        tempblock[key] = value
            tempblock['props'] = temppropers
            blocks.append(copy.deepcopy(tempblock))
            temppropers.clear()
            tempblock.clear()

        for index, row in nodedataall.iterrows():
            num_start = nodelist.index(row['n'])
            num_end = nodelist.index(row['m'])
            relname = row['w']
            temparrow['num_start'] = num_start
            temparrow['num_end'] = num_end
            temparrow['text'] = relname
            arrows.append(copy.deepcopy(temparrow))
            temparrow.clear()

        if blocks:
            dicdata['blocks'] = blocks
        if arrows:
            dicdata['arrows'] = arrows
        if dicdata:
            dicdata = json.dumps(dicdata, ensure_ascii=False)
            dicdata = dicdata.replace('"' + 'false' + '"', 'false').replace('"' + 'true' + '"', 'true')
            print('Neo4j SelectTwoNodeShortPath成功查询两个结点之间所有的最短路径')
            return dicdata
        else:
            print('Neo4j SelectTwoNodeAllShortPath出现错误3')
            return 'ERROR1'
    else:
        print('Neo4j SelectTwoNodeAllShortPath查无连个结点之间的通路')
        twonodedata = SelectTwoNode(username,pro,nodename1,nodename2)
        if type(twonodedata) != 'str':
            return twonodedata
        elif twonodedata == 'ERROR2':
            print('Neo4j SelectTwoNodeAllShortPath查无此两个节点')
            return 'ERROR2'
        else:
            print('Neo4j SelectTwoNodeAllShortPath出现错误4')
            return 'ERROR1'



def SelectCircuit(username,pro,nodename):#查询经过此结点的回路
    dicdata = {}
    blocklist = []
    arrowlist = []
    tempblock = {}
    temparrow = {}
    temppropers = {}
    containerdata = SelectConatiner(username, pro)
    if containerdata:
        dicdata['container'] = containerdata
    else:
        print('Neo4j Selectcircuit出现错误1')
        return 'ERROR3'
    selonestr = 'match (n:'+username+':'+pro+'{name:'+'"'+nodename+'"'+'}) return n'
    try:
        onedata = graph.run(selonestr).data()
        onedata = DataFrame(onedata)
    except:
        print('Neo4j Selectcircuit出现错误2')
        return 'ERROR1'
    if onedata.empty:
        print('Neo4j Selectcircuit查无此节点')
        return 'ERROR2'
    selstr = 'match p = (n:'+username+':'+pro+'{name:'+'"'+nodename+'"'+'})-[r*]->(n) with r match(a:'+username+':'+pro+')-[w]->(b:'+username+':'+pro+') where w in r return a,type(w) as w,b'
    try:
        alldata = graph.run(selstr).data()
        alldata = DataFrame(alldata)
    except:
        print('Neo4j Selectcircuit出现错误3')
        return 'ERROR1'
    if not alldata.empty:
        nodelist = alldata['a'].drop_duplicates().values.tolist()
        nodelist = nodelist + alldata['b'].drop_duplicates().values.tolist()
        nodelist = set(nodelist)
        nodelist = list(nodelist)

        for node in nodelist:
            nodedict = dict(node)
            for key, value in nodedict.items():
                if value == False:
                    value = 'false'
                if key[0] == 'p':
                    temppropers[key[1:]] = value
                elif key != 'countnumber':
                    if key == 'name':
                        temppropers['text'] = value
                    else:
                        tempblock[key] = value
            tempblock['props'] = temppropers
            blocklist.append(copy.deepcopy(tempblock))
            temppropers.clear()
            tempblock.clear()

        for index, row in alldata.iterrows():
            num_start = nodelist.index(row['a'])
            num_end = nodelist.index(row['b'])
            relname = row['w']
            temparrow['num_start'] = num_start
            temparrow['num_end'] = num_end
            temparrow['text'] = relname
            arrowlist.append(copy.deepcopy(temparrow))
            temparrow.clear()

        if blocklist:
            dicdata['blocks'] = blocklist
        if arrowlist:
            dicdata['arrows'] = arrowlist
        if dicdata:
            dicdata = json.dumps(dicdata, ensure_ascii=False)
            dicdata = dicdata.replace('"' + 'false' + '"', 'false').replace('"' + 'true' + '"', 'true')
            print('Neo4j Selectcircuit成功查询此节点所在的回路')
            return dicdata
        else:
            print('Neo4j Selectcircuit出现错误4')
            return 'ERROR1'
    else:
        nodedata = SelectOneNode(username,pro,nodename)
        if type(nodedata) != "str":
            print("Neo4j Selectcircuit不存在经过此节点的回路")
            return nodedata
        else:
            return 'ERROR1'


def SelectDeepNode(username,pro,nodes,depth):
    dicdata={}
    blocks = []
    arrows = []
    temppropers = {}
    tempblock = {}
    temparrow = {}
    containerdata = SelectConatiner(username, pro)
    if containerdata:
        dicdata['container'] = containerdata
    else:
        print('Neo4j SelectDeepNode出现错误1')
        return 'ERROR3'
    nodes = json.dumps(nodes, ensure_ascii=False)
    selstr = 'Match(n:'+username+':'+pro+')-[r*1..%d'%depth+']->(m:'+username+':'+pro+') where n.name in '+nodes+' with r match (a:'+username+':'+pro+')-[w]->(b:'+username+':'+pro+') where w in r return a,type(w) as w,b'
    try:
        alldata = graph.run(selstr).data()
        alldata = DataFrame(alldata)
    except:
        print('Neo4j SelectDeepNode出现错误2')
        return 'ERROR1'
    if not alldata.empty:
        nodelist = alldata['a'].drop_duplicates().values.tolist()
        nodelist = nodelist + alldata['b'].drop_duplicates().values.tolist()
        nodelist = set(nodelist)
        nodelist = list(nodelist)

        for node in nodelist:
            nodedict = dict(node)
            for key, value in nodedict.items():
                if value == False:
                    value = 'false'
                if key[0] == 'p':
                    temppropers[key[1:]] = value
                elif key != 'countnumber':
                    if key == 'name':
                        temppropers['text'] = value
                    else:
                        tempblock[key] = value
            tempblock['props'] = temppropers
            blocks.append(copy.deepcopy(tempblock))
            temppropers.clear()
            tempblock.clear()

        for index, row in alldata.iterrows():
            num_start = nodelist.index(row['a'])
            num_end = nodelist.index(row['b'])
            relname = row['w']
            temparrow['num_start'] = num_start
            temparrow['num_end'] = num_end
            temparrow['text'] = relname
            arrows.append(copy.deepcopy(temparrow))
            temparrow.clear()

        if blocks:
            dicdata['blocks'] = blocks
        if arrows:
            dicdata['arrows'] = arrows
        if dicdata:
            dicdata = json.dumps(dicdata, ensure_ascii=False)
            dicdata = dicdata.replace('"' + 'false' + '"', 'false').replace('"' + 'true' + '"', 'true')
            print('Neo4j SelectDeepNode成功查询节点和对应层数的信息')
            print(dicdata)
            return dicdata
        else:
            print('Neo4j Selectcircuit出现错误3')
            return 'ERROR1'

    else:
        print('Neo4j SelectDeepNode查无这些节点与对应的关系')
        return 'ERROR2'


def DeleteOneNodeByName(username,pro,nodename):#通过名字的方式删除一个结点，如果这个结点还有关系的话会返回Tip，如果没有则直接删除
    selstr = 'MATCH (n:'+username+':'+pro+'{name:'+"'"+nodename+"'"+'})  return n'
    try:
        nodedata = graph.run(selstr).data()
        nodedata = DataFrame(nodedata)
    except:
        print('Neo4j DeleteOndeNodeByName出现错误1')
        return 'ERROR1'
    if not nodedata.empty:
        firrelstr = 'MATCH (n:'+username+':'+pro+'{name:'+"'"+nodename+"'"+'})-[r]->(m:'+username+':'+pro+')'+'return n,m,type(r) as r'
        secrelstr = 'MATCH (n:' + username + ':' + pro + ')-[r]->(m:' + username + ':' + pro + '{name:' + "'" + nodename + "'" + '}) return n,m,type(r) as r'
        try:
            firnodedata = graph.run(firrelstr).data()
            firnodedata = DataFrame(firnodedata)
        except:
            print('Neo4j DeleteOndeNodeByName出现错误2')
            return 'ERROR1'
        try:
            secnodedata = graph.run(secrelstr).data()
            secnodedata = DataFrame(secnodedata)
        except:
            print('Neo4j DeleteOndeNodeByName出现错误3')
            return 'ERROR1'
        if secnodedata.empty and firnodedata.empty:
            delstr = 'MATCH (n:'+username+':'+pro+'{name:'+"'"+nodename+"'"+'}) DELETE n'
            try:
                graph.run(delstr)
                print('Neo4j DeleteOndeNodeByName成功删除结点')
                return 'OK'
            except:
                print('Neo4j DeleteOndeNodeByName出现错误4')
                return 'ERROR1'
        else:
            print('Neo4j DeleteOndeNodeByName此结点还存在关系')
            return 'Tip'
    else:
        print('Neo4j DeleteOndeNodeByName查无此结点')
        return 'ERROR2'


def DeleteOneNodeCom(username,pro,nodename):#强制通过名字查找删除一个结点（包括其保有的关系）
    selstr = 'MATCH (n:' + username + ':' + pro + '{name:' + "'" + nodename + "'" + '}) RETURN n'
    delstr = 'MATCH (n:' + username + ':' + pro + '{name:' + "'" + nodename + "'" + '}) DETACH DELETE n'
    try:
        nodedata = graph.run(selstr).data()
        nodedata = DataFrame(nodedata)
    except:
        print('Neo4j DeleteOndeNodeCom出现错误1')
        return 'ERROR1'
    if not nodedata.empty:
        try:
           graph.run(delstr)
           print('Neo4j DeleteOndeNodeCom成功删除结点')
           return 'OK'
        except:
            print('Neo4j DeleteOndeNodeCom出现错误2')
            return 'ERROR1'
    else:
        print('Neo4j DeleteOndeNodeCom查无此结点')
        return 'ERROR2'


def DeleteOneClourNode(username,pro,clour):#强制通过颜色查找删除所有结点（包括其保有的关系）
    selstr = 'MATCH(n:' + username + ':' + pro + ') WHERE n.ptype='+"'"+clour+"'"+' or (n.ptype='+"'"+"'"+' and n.componentKey='+"'"+clour+"'"+') RETURN n'
    delstr =  'MATCH(n:' + username + ':' + pro + ') WHERE n.ptype='+"'"+clour+"'"+' or (n.ptype='+"'"+"'"+' and n.componentKey='+"'"+clour+"'"+') DETACH DELETE n'
    try:
        nodedata = graph.run(selstr).data()
        nodedata = DataFrame(nodedata)
    except:
        print('Neo4j DeleteOneClourNode出现错误1')
        return 'ERROR1'
    if not nodedata.empty:
        try:
           graph.run(delstr)
           print('Neo4j DeleteOneClourNode成功删除一个颜色的所有结点')
           return 'OK'
        except:
            print('Neo4j DeleteOneClourNode出现错误2')
            return 'ERROR1'
    else:
        print('Neo4j DeleteOneClourNode查无此颜色结点')
        return 'ERROR2'


def DeleteOneTypeNode(username,pro,typename):#强制通过类别查找删除所有结点（包括其保有的关系）
    selstr = 'MATCH(n:' + username + ':' + pro + ') WHERE n.pclasses='+"'"+typename + "'" + 'RETURN n'
    delstr = 'MATCH(n:' + username + ':' + pro + ') WHERE n.pclasses='+"'"+typename + "'" + 'DETACH DELETE n'
    print(selstr)
    print(delstr)
    try:
        nodedata = graph.run(selstr).data()
        nodedata = DataFrame(nodedata)
    except:
        print('Neo4j DeleteOneTypeNode出现错误1')
        return 'ERROR1'
    if not nodedata.empty:
        try:
           graph.run(delstr)
           print('Neo4j DeleteOneTypeNode成功删除一个类别的所有结点')
           return 'OK'
        except:
            print('Neo4j DeleteOneTypeNode出现错误2')
            return 'ERROR1'
    else:
        print('Neo4j DeleteOneTypeNode查无此颜色结点')
        return 'ERROR2'


def DeletePro(username,pro):#强制删除一个pro的结点和关系
    selstr = 'MATCH (n:' + username + ':' + pro + ') RETURN n'
    delstr = 'MATCH (n:' + username + ':' + pro + ') DETACH DELETE n'
    try:
        nodedata = graph.run(selstr).data()
        nodedata = DataFrame(nodedata)
    except:
        print('Neo4j DeletePro出现错误1')
        return 'ERROR1'
    if not nodedata.empty:
        try:
            graph.run(delstr)
            print('Neo4j DeletePro成功删除工程内容')
            return 'OK'
        except:
            print('Neo4j DeletePro出现错误2')
            return 'ERROR1'
    else:
        print('Neo4j DeletePro查无此工程结点')
        return 'ERROR2'


def DeleteProByNode(username,pro):#删除工程信息节点
    selstr = 'MATCH (n:' + username + ':' + pro + ':coin) RETURN n'
    delstr = 'MATCH (n:' + username + ':' + pro + ':coin) DELETE n'
    try:
        nodedata = graph.run(selstr).data()
        nodedata = DataFrame(nodedata)
    except:
        print('Neo4j DeleteProByNode出现错误1')
        return 'ERROR1'
    print(nodedata)
    if not nodedata.empty:
        try:
            graph.run(delstr)
            print('Neo4j DeleteProByNode成功删除工程节点')
            return 'OK'
        except:
            print('Neo4j DeleteProByNode出现错误2')
            return 'ERROR1'
    else:
        print('Neo4j DeleteProByNode查无此工程节点')
        return 'ERROR2'


def DeleteOneRel(username,pro,firnode,secnode,relname):#删除两个结点之间的指定关系
    selstr = 'MATCH (n:'+username+':'+pro+'{name:'+"'"+firnode+"'"+'})-[r:'+relname+']->(m:'+username+':'+pro+'{name:'+"'"+secnode+"'"+'}) RETURN type(r) as r'
    delstr = 'MATCH (n:'+username+':'+pro+'{name:'+"'"+firnode+"'"+'})-[r:'+relname+']->(m:'+username+':'+pro+'{name:'+"'"+secnode+"'"+'})'
    delstr = delstr+'\nDELETE r'
    try:
        nodedata = graph.run(selstr).data()
        nodedata = DataFrame(nodedata)
    except:
        print('Neo4j DeleteOneRel出现错误1')
        return 'ERROR1'
    if not nodedata.empty:
        try:
            graph.run(delstr)
            print('Neo4j DeleteOneRel成功删除指定关系')
            return 'OK'
        except:
            print('Neo4j DeleteOneRel出现错误2')
            return 'ERROR1'
    else:
        print('Neo4j DeleteOneRel查无此关系')
        return 'ERROR2'


def DeleteAllRel(username,pro,firnode,secnode):#删除两个结点之间的所有关系关系
    selstr = 'MATCH (n:' + username + ':' + pro + '{name:' + "'" + firnode + "'" + '})-[r]->(m:' + username + ':' + pro + '{name:' + "'" + secnode + "'" + '}) RETURN type(r) as r'
    delstr = 'MATCH (n:'+username+':'+pro+'{name:'+"'"+firnode+"'"+'})-[r]->(m:'+username+':'+pro+'{name:'+"'"+secnode+"'"+'})'
    delstr = delstr + '\nDELETE  r'
    try:
        nodedata = graph.run(selstr).data()
        nodedata = DataFrame(nodedata)
    except:
        print('Neo4j DeleteAllRel出现错误1')
        return 'ERROR1'
    if not nodedata.empty:
        try:
            graph.run(delstr)
            print('Neo4j DeleteAllRel成功删除所有关系')
            return 'OK'
        except:
            print('Neo4j DeleteAllRel出现错误2')
            return 'ERROR1'
    else:
        print('Neo4j DeleteAllRel查无关系')
        return 'ERROR2'


def DeleteNodeAtt(username,pro,nodename,attname):#删除一个结点的属性
    selstrnode = 'MATCH (n:' + username + ':' + pro + '{name:' + "'" + nodename + "'" + '}) RETURN n'
    selstratt = 'MATCH (n:' + username + ':' + pro + '{name:' + "'" + nodename + "'" + '}) RETURN n.'+attname + 'as n'
    delstr = 'MATCH (n:' + username + ':' + pro + '{name:' + "'" + nodename + "'" + '}) REMOVE n.'+attname
    try:
        nodedata = graph.run(selstrnode).data()
        nodedata = DataFrame(nodedata)
    except:
        print('Neo4j DeleteNodeAtt出现错误1')
        return 'ERROR1'
    if not nodedata.empty:
        try:
            attdata = graph.run(selstratt).data()
            attdata = DataFrame(attdata)
        except:
            print('Neo4j DeleteNodeAtt出现错误2')
            return 'ERROR1'
        if not attdata.empty:
            try:
                graph.run(delstr)
                print('Neo4j DeleteNodeAtt成功删除结点单个属性')
                return 'OK'
            except:
                print('Neo4j DeleteNodeAtt出现错误3')
                return 'ERROR1'
        else:
            print('Neo4j DeleteNodeAtt查无结点此属性')
            return 'ERROR3'
    else:
        print('Neo4j DeleteNodeAtt查无此结点')
        return 'ERROR2'


def DeleteNodeLab(username,pro,nodename,labname):#删除一个结点的标签
    selstr = 'MATCH (n:' + username + ':' + pro + '{name:' + "'" + nodename + "'" + '}) RETURN n'
    delstr = 'MATCH (n:' + username + ':' + pro + '{name:' + "'" + nodename + "'" + '}) REMOVE n:'+labname
    try:
        nodedata = graph.run(selstr).data()
        nodedata = DataFrame(nodedata)
    except:
        print('Neo4j DeleteNodeLab出现错误1')
        return 'ERROR1'
    if not nodedata.empty:
        try:
            graph.run(delstr)
            print('Neo4j DeleteNodeLab成功删除结点标签')
            return 'OK'
        except:
            print('Neo4j DeleteNodeLab出现错误2')
            return 'ERROR1'
    else:
        print('Neo4j DeleteNodeLab查无此结点')
        return 'ERROR2'


def AddNodeAtt(username,pro,nodename,attname,attvalue):#给一个结点增加属性
    selstr = 'MATCH (n:' + username + ':' + pro + '{name:' + "'" + nodename + "'" + '}) RETURN n'
    addstr = 'MATCH (n:' + username + ':' + pro + '{name:' + "'" + nodename + "'" + '}) SET n.' + attname+'='+attvalue
    try:
        nodedata = graph.run(selstr).data()
        nodedata = DataFrame(nodedata)
    except:
        print('Neo4j AdeNodeAtt出现错误1')
        return 'ERROR1'
    if not nodedata.empty:
        try:
            graph.run(addstr)
            print('Neo4j AddNodeAtt成功增加结点属性')
            return 'OK'
        except:
            print('Neo4j AdeNodeAtt出现错误2')
            return 'ERROR1'
    else:
        print('Neo4j AdeNodeAtt查无此结点')
        return 'ERROR2'


def AddNodeLab(username,pro,nodename,labname):#给一个结点增加标签
    selstr = 'MATCH (n:' + username + ':' + pro + '{name:' + "'" + nodename + "'" + '}) RETURN n'
    addstr = 'MATCH (n:' + username + ':' + pro + '{name:' + "'" + nodename + "'" + '}) SET n:' + labname
    try:
        nodedata = graph.run(selstr).data()
        nodedata = DataFrame(nodedata)
    except:
        print('Neo4j AddNodeLab出现错误1')
        return 'ERROR1'
    if not nodedata.empty:
        try:
            graph.run(addstr)
            print('Neo4j AddNodeLab成功增加结点标签')
            return 'OK'
        except:
            print('Neo4j AddNodeLab出现错误2')
            return 'ERROR1'
    else:
        print('Neo4j AddNodeLab查无此结点')
        return 'ERROR2'


def SetNodeAtt(username,pro,nodename,attname,attvalue):#给一个结点重新设置属性
    selstrnode = 'MATCH (n:' + username + ':' + pro + '{name:' + "'" + nodename + "'" + '}) RETURN n'
    selstratt = 'MATCH (n:' + username + ':' + pro + '{name:' + "'" + nodename + "'" + '}) RETURN n.'+attname+'as n'
    setstr = 'MATCH (n:' + username + ':' + pro + '{name:' + "'" + nodename + "'" + '}) SET n.' + attname+'='+attvalue
    try:
        nodedata = graph.run(selstrnode).data()
        nodedata = DataFrame(nodedata)
    except:
        print('Neo4j SetNodeAtt出现错误1')
        return 'ERROR1'
    if not nodedata.empty:
        try:
            attdata = graph.run(selstratt).data()
            attdata = DataFrame(attdata)
        except:
            print('Neo4j SetNodeAtt出现错误2')
            return 'ERROR1'
        if not attdata.empty:
            try:
                graph.run(setstr)
                print('Neo4j SetNodeAtt成功设置结点属性')
                return 'OK'
            except:
                print('Neo4j SetNodeAtt出现错误3')
                return 'ERROR1'
        else:
            print('Neo4j SetNodeAtt查无此结点此属性')
            return 'ERROR3'
    else:
        print('Neo4j SetNodeAtt查无此结点')
        return 'ERROR2'


def SetRelName(username,pro,firnode,secnode,oldrelname,newrelname):#给两个结点之前重新设置关系
    selstr = 'MATCH (n:'+username+':'+pro+'{name:'+"'"+firnode+"'"+'})-[r:'+oldrelname+']->(m:'+username+':'+pro+'{name:'+"'"+secnode+"'"+'}) RETURN type(r) as r'
    setstr = 'MATCH (n:'+username+':'+pro+'{name:'+"'"+firnode+"'"+'})-[r:'+oldrelname+']->(m:'+username+':'+pro+'{name:'+"'"+secnode+"'"+'})'
    setstr = setstr+'\nDELETE r'
    setstr = setstr+'\nMERGE (n)-[:'+newrelname+']->(m)'
    try:
        nodedata = graph.run(selstr).data()
        nodedata = DataFrame(nodedata)
    except:
        print('Neo4j SetRelName出现错误1')
        return 'ERROR1'
    if not nodedata.empty:
        try:
            graph.run(setstr)
            print(setstr)
            print('Neo4j SetRelName成功重新设置结点间关系')
            return 'OK'
        except:
            print('Neo4j SetRelName出现错误2')
            return 'ERROR1'
    else:
        print('Neo4j SetRelName查无此关系')
        return 'ERROR2'
