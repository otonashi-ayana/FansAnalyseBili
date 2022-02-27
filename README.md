# FansAnalyseBili / b站粉丝数据爬取&可视化分析
#### 对b站创作中心粉丝统计尝试复现，此外提供几项统计图可用于判断该账号近期的异常粉丝情况（如买粉）。

### 源码说明：

Requests+BeautifulSoup+Selenium简单多线程爬取 & 处理并导入数据库 [main.py](https://github.com/otonashi-ayana/FansAnalyseBili/blob/main/main.py)  
--

输入uid查询，数据存入数据库。

由于近年官方限制，自有账号每次可获取1000条粉丝信息，非自有账号每次250条。

若要查询自有账号，需要登录该账号并提供 [SESSDATA](https://blog.csdn.net/qq_31201781/article/details/118147745?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522164595499516780261984485%2522%252C%2522scm%2522%253A%252220140713.130102334.pc%255Fall.%2522%257D&request_id=164595499516780261984485&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~first_rank_ecpm_v1~rank_v31_ecpm-2-118147745.pc_search_result_cache&utm_term=b%E7%AB%99SESSDATA&spm=1018.2226.3001.4187) 

![图片](https://user-images.githubusercontent.com/98382726/155877887-3203b3f2-0cc6-4b24-939d-d5824c11363f.png)

提取信息：fans_uid、name、sex、level、vip_status、follower、time_follow

注：部分数据爬取使用selenium框架，默认配合firefox浏览器执行。



Pyecharts 生成统计图（html） [charts.py](https://github.com/otonashi-ayana/FansAnalyseBili/blob/main/charts.py)  
--

执行该文件,连接数据库后生成统计图（fans.html）


（内圈为全站范围相应比例 [来源](https://www.bilibili.com/video/BV1J4411f75W/?spm_id_from=333.788.recommend_more_video.18)  ）

光标停留查看具体数据

依据等级分布、关注&被关注情况和变化可判断up粉丝水分，检测近期是否有买粉行为。

粉丝各等级分布、性别分布、大会员分布：

![图片](https://user-images.githubusercontent.com/98382726/155878055-330a80a6-a7a2-4880-905c-c2f6b4f38515.png)

近7天粉丝增长情况：

![图片](https://user-images.githubusercontent.com/98382726/155878068-b2d64042-6079-4ca6-94aa-43cb159d27d8.png)

粉丝用户关注与被关注数范围分布：

![图片](https://user-images.githubusercontent.com/98382726/155854490-f226fe7a-fc2a-4177-b429-3bd40a176d27.png)

![图片](https://user-images.githubusercontent.com/98382726/155854498-2bd2884a-3940-49ac-9d37-e5529375188b.png)

### 一些感悟：

因为b站最近把不少接口关闭了，诸如复现用户地区、年龄统计图的想法没能实现。他人粉丝列表读取限制到只有250，这个也没办法解决（悲 。部署到服务器上或许可以解决该不足

编写过程有些艰难的大概是使用pyecharts，排版和绘制以及安排数据看了好久的官方文档。初次使用到了数据库和selenium框架，框架读取时间过长，
因此首次尝试了简单的多线程（还有点bug orz）整个项目学到了不少东西，也多了些自己的想法写出的功能。

接下来打算对粉丝动态数、获赞、关注、等级、头像等特征分析，过滤三无账户，或许可以进一步地判断买粉行为。



