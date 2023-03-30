import copy
import json
from py2neo import *           # *中常用的是Node,Relationship,Graph
from pandas import DataFrame

graph = Graph("http://localhost:7474", auth=("neo4j", "123456"))
laydata = '{"container":{"height":1100,"width":2000},"blocks":[{"top":170,"left":280,"componentKey":"impnode","adjustPosition":false,"focus":false,"zIndex":3,"hasResize":false,"props":{"size":70,"text":"贾宝玉","type":"","classes":"Person"}},{"top":48,"left":296,"componentKey":"node","adjustPosition":false,"focus":false,"zIndex":3,"hasResize":false,"props":{"size":60,"text":"晴雯","classes":"Person"}},{"top":63,"left":200,"componentKey":"node","adjustPosition":false,"focus":false,"zIndex":3,"hasResize":false,"props":{"size":60,"text":"袭人","type":"","classes":"Person"}},{"top":152,"left":144,"componentKey":"node","adjustPosition":false,"focus":false,"zIndex":3,"hasResize":false,"props":{"size":70,"text":"薛宝钗","type":"primary","classes":"Person"}},{"top":90,"left":385,"componentKey":"node","adjustPosition":false,"focus":false,"zIndex":3,"hasResize":false,"props":{"size":60,"text":"秋纹","type":"","classes":"Person"}},{"top":259,"left":190,"componentKey":"node","adjustPosition":false,"focus":false,"zIndex":3,"hasResize":false,"props":{"size":60,"text":"麝月","type":"","classes":"Person"}},{"top":170,"left":527,"componentKey":"impnode","adjustPosition":false,"focus":false,"zIndex":3,"hasResize":false,"props":{"size":70,"text":"贾探春","type":"","classes":"Person"}},{"top":63,"left":470,"componentKey":"node","adjustPosition":false,"focus":false,"zIndex":3,"hasResize":false,"props":{"size":60,"text":"侍书","type":"","classes":"Person"}},{"top":48,"left":594,"componentKey":"node","adjustPosition":false,"focus":false,"zIndex":3,"hasResize":false,"props":{"size":60,"text":"翠墨","type":"","classes":"Person"}},{"top":152,"left":665,"componentKey":"node","adjustPosition":false,"focus":false,"zIndex":3,"hasResize":false,"props":{"size":60,"text":"小婵","type":"","classes":"Person"}},{"top":312,"left":447,"componentKey":"impnode","adjustPosition":false,"focus":false,"zIndex":3,"hasResize":false,"props":{"size":80,"text":"贾政","type":"","classes":"Person"}},{"top":312,"left":287,"componentKey":"impnode","adjustPosition":false,"focus":false,"zIndex":3,"hasResize":false,"props":{"size":70,"text":"贾环","type":"","classes":"Person"}},{"top":567,"left":454,"componentKey":"impnode","adjustPosition":false,"focus":false,"zIndex":3,"hasResize":false,"props":{"size":70,"text":"贾珠","type":"","classes":"Person"}},{"top":440,"left":200,"componentKey":"impnode","adjustPosition":false,"focus":false,"zIndex":3,"hasResize":false,"props":{"size":70,"text":"贾元春","type":"","classes":"Person"}},{"top":386,"left":64,"componentKey":"node","adjustPosition":false,"focus":false,"zIndex":3,"hasResize":false,"props":{"size":60,"text":"琴韵","type":"","classes":"Person"}},{"top":515,"left":64,"componentKey":"node","adjustPosition":false,"focus":false,"zIndex":3,"hasResize":false,"props":{"size":60,"text":"抱琴","type":"","classes":"Null"}},{"top":583,"left":167,"componentKey":"node","adjustPosition":false,"focus":false,"zIndex":3,"hasResize":false,"props":{"size":60,"text":"青芸","type":"","classes":"Person"}},{"top":471,"left":330,"componentKey":"impnode","adjustPosition":false,"focus":false,"zIndex":3,"hasResize":false,"props":{"size":80,"text":"王夫人","type":"","classes":"Person"}},{"top":676,"left":385,"componentKey":"impnode","adjustPosition":false,"focus":false,"zIndex":3,"hasResize":false,"props":{"size":70,"text":"李纨","type":"","classes":"Null"}},{"top":682,"left":527,"componentKey":"node","adjustPosition":false,"focus":false,"zIndex":3,"hasResize":false,"props":{"size":60,"text":"贾兰","type":"","classes":"Person"}},{"top":480,"left":565,"componentKey":"node","adjustPosition":false,"focus":false,"zIndex":3,"hasResize":false,"props":{"size":70,"text":"赵姨娘","type":"","classes":"Person"}},{"top":265,"left":607,"componentKey":"node","adjustPosition":false,"focus":false,"zIndex":3,"hasResize":false,"props":{"size":70,"text":"周姨娘","type":"","classes":"Person"}},{"top":440,"left":728,"componentKey":"impnode","adjustPosition":false,"focus":false,"zIndex":3,"hasResize":false,"props":{"size":90,"text":"贾代善","type":"","classes":"Person"}},{"top":243,"left":735,"componentKey":"impnode","adjustPosition":false,"focus":false,"zIndex":3,"hasResize":false,"props":{"size":90,"text":"史太君","type":""}},{"top":327,"left":890,"componentKey":"impnode","adjustPosition":false,"focus":false,"zIndex":3,"hasResize":false,"props":{"size":80,"text":"贾敏","type":"","classes":"Person"}},{"top":273,"left":1045,"componentKey":"impnode","adjustPosition":false,"focus":false,"zIndex":3,"hasResize":false,"props":{"size":80,"text":"林如海","type":"","classes":"Person"}},{"top":185,"left":932,"componentKey":"impnode","adjustPosition":false,"focus":false,"zIndex":3,"hasResize":false,"props":{"size":70,"text":"林黛玉","type":"","classes":"Null"}},{"top":90,"left":829,"componentKey":"node","adjustPosition":false,"focus":false,"zIndex":3,"hasResize":false,"props":{"size":60,"text":"紫鹃","type":"","classes":"Person"}},{"top":48,"left":941,"componentKey":"node","adjustPosition":false,"focus":false,"zIndex":3,"hasResize":false,"props":{"size":60,"text":"雪雁","type":"","classes":"Person"}},{"top":99,"left":1045,"componentKey":"node","adjustPosition":false,"focus":false,"zIndex":3,"hasResize":false,"props":{"size":60,"text":"春纤","type":"","classes":"Person"}},{"top":480,"left":900,"componentKey":"impnode","adjustPosition":false,"focus":false,"zIndex":3,"hasResize":false,"props":{"size":100,"text":"贾源","type":"","classes":"Person"}},{"top":647,"left":745,"componentKey":"impnode","adjustPosition":false,"focus":false,"zIndex":3,"hasResize":false,"props":{"size":80,"text":"贾赦","type":"","classes":"Person"}},{"top":613,"left":890,"componentKey":"node","adjustPosition":false,"focus":false,"zIndex":3,"hasResize":false,"props":{"size":70,"text":"贾琮","type":"","classes":"Person"}},{"top":583,"left":600,"componentKey":"impnode","adjustPosition":false,"focus":false,"zIndex":3,"hasResize":false,"props":{"size":80,"text":"邢夫人","type":"","classes":"Person"}},{"top":812,"left":687,"componentKey":"impnode","adjustPosition":false,"focus":false,"zIndex":3,"hasResize":false,"props":{"size":70,"text":"贾琏","type":""}},{"top":756,"left":565,"componentKey":"node","adjustPosition":false,"focus":false,"zIndex":3,"hasResize":false,"props":{"size":60,"text":"秋桐","type":"","classes":"Person"}},{"top":855,"left":543,"componentKey":"node","adjustPosition":false,"focus":false,"zIndex":3,"hasResize":false,"props":{"size":60,"text":"贾巧姐","type":"","classes":"Person"}},{"top":957,"left":749,"componentKey":"node","adjustPosition":false,"focus":false,"zIndex":3,"hasResize":false,"props":{"size":60,"text":"尤二姐","type":"","classes":"Person"}},{"top":872,"left":808,"componentKey":"node","adjustPosition":false,"focus":false,"zIndex":3,"hasResize":false,"props":{"size":60,"text":"平儿","type":""}},{"top":947,"left":623,"componentKey":"impnode","adjustPosition":false,"focus":false,"zIndex":3,"hasResize":false,"props":{"size":70,"text":"王熙凤","type":"","classes":"Person"}},{"top":448,"left":1077,"componentKey":"dgnode","adjustPosition":false,"focus":false,"zIndex":3,"hasResize":false,"props":{"size":110,"text":"贾家","type":"","classes":"Organization"}},{"top":750,"left":900,"componentKey":"impnode","adjustPosition":false,"focus":false,"zIndex":3,"hasResize":false,"props":{"size":70,"text":"贾迎春","type":"","classes":"Person"}},{"top":682,"left":1026,"componentKey":"node","adjustPosition":false,"focus":false,"zIndex":3,"hasResize":false,"props":{"size":60,"text":"莲花儿","type":"","classes":"Person"}},{"top":807,"left":1045,"componentKey":"node","adjustPosition":false,"focus":false,"zIndex":3,"hasResize":false,"props":{"size":60,"text":"司棋","type":"","classes":"Person"}},{"top":877,"left":957,"componentKey":"node","adjustPosition":false,"focus":false,"zIndex":3,"hasResize":false,"props":{"size":60,"text":"绣橘","type":"","classes":"Person"}},{"top":375,"left":1237,"componentKey":"impnode","adjustPosition":false,"focus":false,"zIndex":3,"hasResize":false,"props":{"size":100,"text":"贾演","type":"","classes":"Person"}},{"top":480,"left":1367,"componentKey":"impnode","adjustPosition":false,"focus":false,"zIndex":3,"hasResize":false,"props":{"size":90,"text":"贾代化","type":"","classes":"Person"}},{"top":595,"left":1263,"componentKey":"impnode","adjustPosition":false,"focus":false,"zIndex":3,"hasResize":false,"props":{"size":80,"text":"贾敷","type":"","classes":"Person"}},{"top":448,"left":1531,"componentKey":"impnode","adjustPosition":false,"focus":false,"zIndex":3,"hasResize":false,"props":{"size":80,"text":"贾敬","type":"","classes":"Person"}},{"top":295,"left":1572,"componentKey":"impnode","adjustPosition":false,"focus":false,"zIndex":3,"hasResize":false,"props":{"size":70,"text":"贾惜春","type":"","classes":"Person"}},{"top":220,"left":1468,"componentKey":"node","adjustPosition":false,"focus":false,"zIndex":3,"hasResize":false,"props":{"size":60,"text":"彩屏"}},{"top":170,"left":1583,"componentKey":"node","adjustPosition":false,"focus":false,"zIndex":3,"hasResize":false,"props":{"size":60,"text":"入画","type":"","classes":"Person"}},{"top":232,"left":1683,"componentKey":"node","adjustPosition":false,"focus":false,"zIndex":3,"hasResize":false,"props":{"size":60,"text":"彩儿","type":"","classes":"Person"}},{"top":628,"left":1548,"componentKey":"impnode","adjustPosition":false,"focus":false,"zIndex":3,"hasResize":false,"props":{"size":70,"text":"贾珍","type":"","classes":"Person"}},{"top":682,"left":1409,"componentKey":"node","adjustPosition":false,"focus":false,"zIndex":3,"hasResize":false,"props":{"size":60,"text":"贾蔷","type":""}},{"top":762,"left":1548,"componentKey":"impnode","adjustPosition":false,"focus":false,"zIndex":3,"hasResize":false,"props":{"size":70,"text":"尤氏","type":"","classes":"Person"}},{"top":619,"left":1746,"componentKey":"impnode","adjustPosition":false,"focus":false,"zIndex":3,"hasResize":false,"props":{"size":70,"text":"贾蓉","type":"","classes":"Person"}},{"top":503,"left":1814,"componentKey":"impnode","adjustPosition":false,"focus":false,"zIndex":3,"hasResize":false,"props":{"size":70,"text":"秦可卿","type":"","classes":"Event"}},{"top":619,"left":1894,"componentKey":"node","adjustPosition":false,"focus":true,"zIndex":3,"hasResize":false,"props":{"size":60,"text":"瑞珠","type":"","classes":"Person"}},{"top":732,"left":1840,"componentKey":"node","adjustPosition":false,"focus":false,"zIndex":3,"hasResize":false,"props":{"size":60,"text":"宝珠","type":"","classes":"Person"}}],"arrows":[{"num_start":0,"num_end":4,"text":"丫鬟"},{"num_start":0,"num_end":1,"text":"丫鬟"},{"num_start":0,"num_end":2,"text":"丫鬟"},{"num_start":0,"num_end":3,"text":"夫妻"},{"num_start":0,"num_end":5,"text":"丫鬟"},{"num_start":6,"num_end":7,"text":"丫鬟"},{"num_start":6,"num_end":8,"text":"丫鬟"},{"num_start":6,"num_end":9,"text":"丫鬟"},{"num_start":10,"num_end":6,"text":"子女"},{"num_start":10,"num_end":0,"text":"子女"},{"num_start":10,"num_end":11,"text":"子女"},{"num_start":10,"num_end":12,"text":"子女"},{"num_start":10,"num_end":13,"text":"子女"},{"num_start":13,"num_end":14,"text":"丫鬟"},{"num_start":13,"num_end":15,"text":"丫鬟"},{"num_start":13,"num_end":16,"text":"丫鬟"},{"num_start":10,"num_end":17,"text":"夫妻"},{"num_start":12,"num_end":18,"text":"夫妻"},{"num_start":12,"num_end":19,"text":"子女"},{"num_start":10,"num_end":20,"text":"小妾"},{"num_start":10,"num_end":21,"text":"小妾"},{"num_start":22,"num_end":10,"text":"关系"},{"num_start":22,"num_end":23,"text":"夫妻"},{"num_start":22,"num_end":24,"text":"子女"},{"num_start":24,"num_end":25,"text":"关系"},{"num_start":24,"num_end":26,"text":"子女"},{"num_start":26,"num_end":27,"text":"丫鬟"},{"num_start":26,"num_end":28,"text":"丫鬟"},{"num_start":26,"num_end":29,"text":"丫鬟"},{"num_start":30,"num_end":22,"text":"子女"},{"num_start":22,"num_end":31,"text":"子女"},{"num_start":31,"num_end":33,"text":"夫妻"},{"num_start":31,"num_end":32,"text":"子女"},{"num_start":31,"num_end":34,"text":"子女"},{"num_start":34,"num_end":35,"text":"小妾"},{"num_start":34,"num_end":38,"text":"小妾"},{"num_start":34,"num_end":39,"text":"夫妻"},{"num_start":34,"num_end":37,"text":"小妾"},{"num_start":34,"num_end":36,"text":"子女"},{"num_start":40,"num_end":30,"text":"继承"},{"num_start":31,"num_end":41,"text":"子女"},{"num_start":41,"num_end":42,"text":"丫鬟"},{"num_start":41,"num_end":43,"text":"丫鬟"},{"num_start":41,"num_end":44,"text":"丫鬟"},{"num_start":40,"num_end":45,"text":"继承"},{"num_start":45,"num_end":46,"text":"子女"},{"num_start":46,"num_end":47,"text":"子女"},{"num_start":46,"num_end":48,"text":"子女"},{"num_start":48,"num_end":49,"text":"子女"},{"num_start":49,"num_end":50,"text":"丫鬟"},{"num_start":49,"num_end":51,"text":"丫鬟"},{"num_start":49,"num_end":52,"text":"丫鬟"},{"num_start":48,"num_end":53,"text":"子女"},{"num_start":53,"num_end":54,"text":"子女"},{"num_start":53,"num_end":55,"text":"夫妻"},{"num_start":53,"num_end":56,"text":"子女"},{"num_start":56,"num_end":57,"text":"夫妻"},{"num_start":56,"num_end":58,"text":"丫鬟"},{"num_start":56,"num_end":59,"text":"丫鬟"}]}'
laydatadeal = eval(laydata.replace('false', "'" + 'false' + "'").replace('true', "'" + 'true'+"'"))


def InsertRecLayNode(layname,laydata):
    insertstr = 'MERGE (:'+layname+':coin{name:'+"'"+layname+"'"+',data:'+"'"+laydata+"'"+'})'
    try:
        graph.run(insertstr)
        print('NeoRec InsertRecLayNode成功插入推荐布局数据结点')
    except:
        print('NeoRec InsertRecLayNode出现错误1')
        return 'ERROR1'


def InsertRecLayDis(layname,laydata):
    countnumber = 0;
    clearstr = 'MATCH(n:' + layname + ':dis' + ') DETACH DELETE n'
    graph.run(clearstr)
    constr = 'MERGE(:' + layname + ':dis' + '{height:%d' % (laydata['container']['height']) + ',width:%d' % (laydata['container']['width']) + ',name:' + "'" + 'container' + "'" + '})'
    try:
        graph.run(clearstr)
        graph.run(constr)
    except:
        print('NeoRec InsertRecLayDis出现错误1')
        return 'ERROR1'
    print('NeoRec InsertRecLayDis清除原数据与加推荐布局成功')
    for block in laydata['blocks']:
        nodestr = 'MERGE(n:' + layname + ':dis' + '{top:%d' % block['top'] + ',left:%d' % block[
            'left'] + ',componentKey:' + "'" + '%s' % block['componentKey'] + "'" + ',adjustPosition:%s' % block[
                      'adjustPosition'] + ',focus:%s' % block['focus'] + ',zIndex:%d' % block[
                      'zIndex'] + ',hasResize:%s' % block['hasResize']
        for key, value in block['props'].items():
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
                typename = value;
                nodestr = nodestr + ',pclasses:' + "'" + '%s' % value + "'"
        nodestr += ',countnumber:%d})' % countnumber
        countnumber = countnumber + 1
        if len(typename) != 0:
            nodestr += 'SET n:%s' % typename
        typename = ''
        try:
            graph.run(nodestr)
        except:
            print('NeoRec InsertRecLayDis出现错误2')
            return 'ERROR1'
    print('NeoRec InsertRecLayDis加入结点成功')
    for relation in laydata['arrows']:
        realstr = 'MATCH(n:' + layname + ':dis' + '{countnumber:%d' % relation[
            'num_start'] + '}),(m:' + layname + ':dis' + '{countnumber:%d' % relation['num_end'] + '})'
        realstr = realstr + 'MERGE (n)-[:%s]->(m)' % relation['text']
        try:
            graph.run(realstr)
        except:
            print('NeoRec InsertRecLayDis出现错误3')
            return 'ERROR1'
    print('NeoRec InsertRecLayDis成功创建展示推荐布局')
    return 'OK'


def SelectRecLayByNode(layname):
    selstr = 'MATCH(n:'+layname+':coin) RETURN n'
    try:
        seldata = graph.run(selstr).data()
        seldata = DataFrame(seldata)
    except:
        print('NeoRec SelectRecLayByNode出现错误1')
        return 'ERROR1'
    if seldata.empty:
        print('NeoRec SelectRecLayByNode出现错误2')
        return 'ERROR2'
    else:
        nodedata = seldata['n'].drop_duplicates().values.tolist()
        nodedata = nodedata[0]
        laydata = dict(nodedata)['data']
        print('NeoRec SelectRecLayByNode成功查询推荐布局数据结点')
        return laydata


def SelectDisConatiner(layname):
    selstr = 'MATCH(n:'+layname+':dis'+'{name:'+"'container'"+'}) RETURN n'
    try:
        container = graph.run(selstr).data()
        container = dict(container[0]['n'])
    except:
        print('NeoRec SelectDisContainer出现错误1')
        return 'ERROR1'
    containerdata = {}
    containerdata['height'] = container['height']
    containerdata['width'] = container['width']
    print('NeoRec SelectDisContainer成功查询推荐布局画布数据')
    return containerdata


def SelectRecLayByDis(layname):
    dicdata = {}
    block = []
    tempblock = {}
    tempprops = {}
    arrows = []
    temparrow = {}
    container = {}
    selstrnode = 'MATCH(n:' + layname + ':dis' + ')WHERE n.name<>' + "'" + 'container' + "'" + 'RETURN n'
    try:
        selnodedata = graph.run(selstrnode).data()
    except:
        print('NeoRec SelectRecLayByDis出现错误1')
        return 'ERROR1'
    selnodedata = DataFrame(selnodedata)
    selnodedata = selnodedata['n'].drop_duplicates().values.tolist()
    container = SelectDisConatiner(layname)
    if container:
        dicdata['container'] = container
    else:
        print('NeoRec SelectRecLayByDis出现错误2')
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

    selrelnodestr = 'MATCH(n:' + layname + ':dis' + ')-[r]->(m:' + layname + ':dis'+ ') RETURN n,m,type(r) as r'
    try:
        selrelnoddata = DataFrame(graph.run(selrelnodestr).data())
    except:
        print('NeoRec SelectRecLayByDis出现错误3')
        return 'ERROR1'
    if not selrelnoddata.empty:
        for index, row in selrelnoddata.iterrows():
            num_start = selnodedata.index(row['n'])
            num_end = selnodedata.index(row['m'])
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
        print('NeoRec SelectRecLayByDis成功查询推荐布局信息')
        return dicdata
    else:
        print('NeoRec SelectRecLayByDis出现错误4')
        return 'ERROR2'


def DeleteRecNode(layname):#删除推荐布局信息节点
    selstr = 'Match (n:'+layname+':coin) RETURN n'
    delstr = 'Match (n:' + layname + ':coin) DELETE n'
    try:
        nodedata = graph.run(selstr).data()
        nodedata = DataFrame(nodedata)
    except:
        print('NeoRec DeleteRecNode出现错误1')
        return 'ERROR1'
    if not nodedata.empty:
        try:
            graph.run(delstr)
        except:
            print('NeoRec DeleteRecNode出现错误2')
            return 'ERROR1'
    else:
        print('NeoRec DeleteRecNode查无此推荐布局节点')
        return 'ERROR2'
    print('NeoRec DeleteRecNode成功删除推荐布局节点')


def DeleteRecDis(layname):#删除推荐布局信息节点与关系
    selstr = 'Match (n:'+layname+':dis) RETURN n'
    delstr = 'Match (n:' + layname + ':dis) DETACH DELETE n'
    try:
        nodedata = graph.run(selstr).data()
        nodedata = DataFrame(nodedata)
    except:
        print('NeoRec DeleteRecDis出现错误1')
        return 'ERROR1'
    if not nodedata.empty:
        try:
            graph.run(delstr)
        except:
            print('NeoRec DeleteRecDis出现错误2')
            return 'ERROR1'
    else:
        print('NeoRec DeleteRecRecDis查无此推荐布局节点与关系')
        return 'ERROR2'
    print('NeoRec DeleteRecRecDis成功删除推荐布局信息')







