-- 创建推荐布局数据表格
CREATE TABLE `laypicdata` ( 
   `layname` char(20) NOT NULL,
   `laydata` text,
   PRIMARY KEY (`layname`)
 ) ;
-- 创建用户知识图谱工程数据表格
CREATE TABLE `picdata` (
   `Userpro` char(20) NOT NULL,
   `PicData` text,
   PRIMARY KEY (`Userpro`)
 ) ;
-- 创建用户名密码数据表格
CREATE TABLE `usermessage` (
   `Username` varchar(45) NOT NULL,
   `Password` varchar(45) NOT NULL,
   PRIMARY KEY (`Username`),
   UNIQUE KEY `Username_UNIQUE` (`Username`)
 );
