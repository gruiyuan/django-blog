## 说明
该博客项目是本人学习Django时,依照  [追梦人物的博客](https://www.zmrenwu.com/)  教程做的,并予以相对详细的注释.

------

# 本地运行方法
### 1. 克隆项目到本地
在要保存的路径上执行命令
```
git clone https://github.com/gruiyuan/django-blog.git
```
### 2. pip安装依赖模块
在项目路径下,执行
```
pip install -r requirements.txt
```
### 3. 修改 `blogproject/settings.py`中的数据库相关配置
根据本地的数据库,修改配置文件中的`DATABASES`字典
### 4. 迁移数据库
在`manage.py`所在目录(即项目的一级目录)下,分别执行:
```
python manage.py makemigrations
python manage.py migrate
```
### 5. 创建超级管理员
在上一步的目录下,执行:
```
python manage.py createsuperuser
```
根据提示完成创建
### 6. 建立索引文件
执行:
```
python manage.py rebuild_index
```
会在`./whoosh_index/`下生成索引文件(在`settings.py`中的`HAYSTACK_CONNECTIONS`配置),用于django-Haystack应用实现搜索功能
### 7. 运行开发服务器
```
python manage.py runserver
```
本地浏览器打开 http://localhost:8000/ 即为博客首页