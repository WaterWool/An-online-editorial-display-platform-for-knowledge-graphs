import pymysql
import json
db = pymysql.connect(host="127.0.0.1", user="root", password="123456", database="my_db_01", port=3306, charset='utf8')
cursor = db.cursor()


def InsertPic(username,pro,data):#MySQL中插入工程布局数据
    strsql = "replace into picdata set userpro="+'"'+username+pro+'"'+",picData="+"'"+data+"'"
    try:
        cursor.execute(strsql)
        db.commit()
    except:
        print('MySQL InsertPic出现错误1')
        return "ERROR1"
    print("MySQL InsertPic成功插入图谱数据")
    return 'OK'


def InsertLayData(layname,laydata):#MySQL中插入推荐布局信息
    insertstr = "replace into laypicdata set layname="+'"'+layname+'"'+",laydata="+"'"+laydata+"'"
    print(insertstr)
    try:
        cursor.execute(insertstr)
        db.commit()
    except:
        print('MySQL InsertLayData现错误1')
        return "ERROR1"
    print("MySQL InsertLayData成功插入推荐图谱数据")
    return 'OK'


def InsertUser(username,password):#MySQL中插入用户名和密码
    strsql = "select Username from usermessage where username=" + '"' + username + '"'
    try:
        cursor.execute(strsql)
        resultname=cursor.fetchall()
        if str(resultname) == "()":
            strsql = "replace into usermessage set username=" + '"' + username + '"' + ",password=" + '"' + password + '"'
            try:
                cursor.execute(strsql)
                db.commit()
            except:
                print('MySQL InsertUser出现错误1')
                return "ERROR1"
        else:
            print("MySQL InsertUser抱歉，此用户名已经存在")
            return "ERROR2"
    except:
        print('MySQL InsertUser出现错误2')
        return "ERROR1"
    print("MySQL InsertUser成功插入新的用户和密码")
    return 'OK'


def SelectPic(username,pro):#在MySQL中查询工程数据
    strsql="select PicData from picdata where userpro="+'"'+username+pro+'"'
    try:
        cursor.execute(strsql)
        resultpic = cursor.fetchall()
        # resultpic = ''.join(resultpic[0][0])
        if resultpic == None:
            print('MySQL SelectPic出现错误1')
            return 'ERROR2'
        else:
            resultpic = json.loads(resultpic[0][0])
            resultpic = json.dumps(resultpic)
            print('MySQL SelectPic成功查询图谱数据')
            return resultpic
    except:
        print('MySQL SelectPic出现错误2')
        return "ERROR1"


def SelectPass(username):#在MySQL中查询用户密码
    strsql="select Username from usermessage where username="+'"'+username+'"'
    try:
        cursor.execute(strsql)
        resultname=cursor.fetchone()
        if resultname != None:
            try:
                strsql="select password from usermessage where username="+'"'+username+'"'
                cursor.execute(strsql)
                resultpass=cursor.fetchall()
                print("MySQL SelectPass成功查询用户密码")
                return resultpass[0][0]
            except:
                print('MySQL SelectPass出现错误1')
                return "ERROR1"
        else:
            print("MySQL SelectPass抱歉，此用户还没有注册")
            return "ERROR2"
    except:
        print('MySQL SelectPass出现错误2')
        return "ERROR1"


def SelectLayData(layname):#MySQL中查询推荐布局信息
    strsql = "select laydata from laypicdata where layname=" + '"' + layname + '"'
    try:
        cursor.execute(strsql)
        laydata = cursor.fetchone()
        if laydata != None:
            laydata = json.loads(laydata[0])
            laydata = json.dumps(laydata)
            print('MySQL SelectLatData成功查询推荐布局数据')
            return laydata
        else:
            print("MySQL SelectLayData查无此推荐布局信息")
            return "ERROR2"
    except:
        print('MySQL SelectLayData出现错误1')
        return "ERROR1"


def DeleteOnePro(username,pro):
    strsql = "select Userpro from picdata where Userpro=" + '"' + username + pro + '"'
    try:
        cursor.execute(strsql)
        resultuserpro = cursor.fetchall()
        if str(resultuserpro) == "()":
            print("MySQL DeleteOnePro没有查询到此工程内容")
            return 'ERROR2'
        else:
            delstr = "delete from picdata where Userpro=" + "'" + username + pro + "'"
            try:
                cursor.execute(delstr)
                db.commit()
            except:
                print('MySQL DeleteOnePro出现错误1')
                return "ERROR1"
    except:
        print('MySQL DeleteOnePro出现错误2')
        return "ERROR1"
    print('MySQL DeleteOnePro成功删除工程信息')
    return 'OK'


def DeleteOneLay(layname):
    strsql = "select layname from laypicdata where layname=" + '"' + layname + '"'
    try:
        cursor.execute(strsql)
        resultuserpro = cursor.fetchall()
        if str(resultuserpro) == "()":
            print("MySQL DeletOneLay没有查询到此推荐布局内容")
            return 'ERROR2'
        else:
            delstr = "delete from laypicdata where layname=" + "'" + layname + "'"
            try:
                cursor.execute(delstr)
                db.commit()
            except:
                print('MySQL DeletOneLay出现错误1')
                return "ERROR1"
    except:
        print('MySQL DeletOneLay出现错误2')
        return "ERROR1"
    print('MySQL DeletOneLay成功删除推荐布局信息')
    return 'OK'