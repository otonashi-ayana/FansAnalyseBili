import pymysql, os, datetime, time
from datetime import timedelta
from pyecharts import options as opts
from pyecharts.charts import Pie, Bar, Page, Line
from pyecharts.commons.utils import JsCode
from pyecharts.globals import ThemeType

connect = pymysql.connect(
    host='localhost',
    user='root',
    password='0089ghj0087',
    database='fans_db',
    charset='utf8',
)
cursor = connect.cursor()


def level_distr():
    sql = """SELECT level FROM info """
    cursor.execute(sql)
    level_list = []
    val = []
    levels = cursor.fetchall()
    for level in levels:
        level_list.append(level[0])

    count = ['0', '1', '2', '3', '4', '5', '6']
    for i in range(7):
        val.append(level_list.count(count[i]))

    c = (
        Pie(init_opts=opts.InitOpts(width="500px", height="400px", chart_id="level"))
            .add(
            "",
            radius=["40%", "63%"],
            data_pair=[('0级', val[0]), ('1级', val[1]), ('2级', val[2]),
                       ('3级', val[3]), ('4级', val[4]), ('5级', val[5]), ('6级', val[6])],
            label_opts=opts.LabelOpts(formatter="{b}", ),
            tooltip_opts=opts.TooltipOpts(formatter="{b}: {c} ({d}%)"),
        )
            .add(
            "",
            data_pair=[('lv1', 20.03), ('lv2', 34.1), ('lv3', 19.8), ('lv4', 17.0),
                       ('lv5', 9.0), ('lv6', 0.07)],
            radius=[0, "28%"],
            label_opts=opts.LabelOpts(position="inner"),
            tooltip_opts=opts.TooltipOpts(formatter="{b}:  ({d}%)（全站数据）"),

        )
            .set_global_opts(
            title_opts=opts.TitleOpts(
                title="等级分布",
                subtitle="全站数据来源（2019.8）",
                pos_left="center",
                pos_top="20",
            ),

            legend_opts=opts.LegendOpts(is_show=False),
        )

            .set_colors(['#C1C1C1', '#717171', '#94DDB5', '#B7E1EE', '#FFB37C', '#FF7D1E', '#FF1F1F'])
    )
    return c


def sex_distr():
    sql = """SELECT sex FROM info """
    cursor.execute(sql)
    sex_list = []
    val = []
    sexs = cursor.fetchall()
    for sex in sexs:
        sex_list.append(sex[0])
    count = ['男', '女']
    for i in range(2):
        val.append(sex_list.count(count[i]))
    c = (
        Pie(init_opts=opts.InitOpts(width="500px", height="400px", chart_id="sex", ))
            .add(
            "",
            radius=["40%", "63%"],
            data_pair=[('男', val[0]), ('女', val[1]), ],
            label_opts=opts.LabelOpts(formatter="{b}", ),
            tooltip_opts=opts.TooltipOpts(formatter="{b}: {c} ({d}%)"),
        )
            .add(
            "",
            data_pair=[('男', 55.0), ('女', 45.0)],
            radius=[0, "28%"],
            label_opts=opts.LabelOpts(position="inner"),
            tooltip_opts=opts.TooltipOpts(formatter="{b}:  ({d}%)（全站数据）"),
        )
            .set_global_opts(
            title_opts=opts.TitleOpts(
                title="性别分布",
                subtitle="全站数据来源（2019.8）",
                pos_left="center",
                pos_top="20",
            ),

            legend_opts=opts.LegendOpts(is_show=False),
        )

            .set_colors(['#0099FF', '#F08080'])

    )
    return c


def follow_distr():
    l1 = l2 = l3 = l4 = l5 = 0
    sql = """SELECT following FROM info """
    cursor.execute(sql)
    follows = cursor.fetchall()
    follows = [int(follow[0]) for follow in follows]
    for num in follows:
        if num <= 20:
            l1 = l1 + 1
        elif num <= 100:
            l2 = l2 + 1
        elif num <= 200:
            l3 = l3 + 1
        elif num <= 500:
            l4 = l4 + 1
        else:
            l5 = l5 + 1
    sum = l1 + l2 + l3 + l4 + l5
    list1 = [
        {"value": l1, "percent": l1 / sum},
    ]
    list2 = [
        {"value": l2, "percent": l2 / sum},
    ]
    list3 = [
        {"value": l3, "percent": l3 / sum},
    ]
    list4 = [
        {"value": l4, "percent": l4 / sum},
    ]
    list5 = [
        {"value": l5, "percent": l5 / sum},
    ]

    c = (

        Bar(init_opts=opts.InitOpts(theme=ThemeType.LIGHT, chart_id="follow"))
            .add_xaxis([sum])
            .reversal_axis()
            .add_yaxis("<20 following", list1, stack="stack", bar_width=40, )
            .add_yaxis("20< following <100", list2, stack="stack", bar_max_width=25)
            .add_yaxis("100< following <200", list3, stack="stack", )
            .add_yaxis("200< following <500", list4, stack="stack", )
            .add_yaxis("500+ following", list5, stack="stack", )
            .set_global_opts(
            title_opts=opts.TitleOpts(
                title="粉丝关注情况",
                subtitle="粉丝关注up总数各范围占比",
                pos_left="left",
                pos_top="20",
            ),
            xaxis_opts=opts.AxisOpts(is_show=False),
            yaxis_opts=opts.AxisOpts(is_show=False)
        )
            .set_series_opts(
            label_opts=opts.LabelOpts(
                font_weight='bold',
                position="top",
                formatter=JsCode(
                    "function(x){return Number(x.data.percent * 100).toFixed() + '%';}"
                ),
            )
        )
    )
    return c


def fans_distr():
    l1 = l2 = l3 = 0
    sql = """SELECT follower FROM info """
    cursor.execute(sql)
    followers = cursor.fetchall()
    followers = [int(follower[0]) for follower in followers]
    for num in followers:
        if num == 0:
            l1 = l1 + 1
        elif num <= 10:
            l2 = l2 + 1
        else:
            l3 = l3 + 1
    sum = l1 + l2 + l3
    list1 = [
        {"value": l1, "percent": l1 / sum},
    ]
    list2 = [
        {"value": l2, "percent": l2 / sum},
    ]
    list3 = [
        {"value": l3, "percent": l3 / sum},
    ]

    c = (

        Bar(init_opts=opts.InitOpts(theme=ThemeType.LIGHT, chart_id="fans"))
            .add_xaxis([sum])
            .reversal_axis()
            .add_yaxis("0 follower", list1, stack="stack", bar_width=40, )
            .add_yaxis("0< follower <10", list2, stack="stack", bar_max_width=25)
            .add_yaxis("10< follower", list3, stack="stack", )
            .set_global_opts(
            title_opts=opts.TitleOpts(
                title="粉丝被关注情况",
                subtitle="粉丝被关注总数各范围占比",
                pos_left="left",
                pos_top="20",
            ),
            xaxis_opts=opts.AxisOpts(is_show=False),
            yaxis_opts=opts.AxisOpts(is_show=False)
        )
            .set_series_opts(
            label_opts=opts.LabelOpts(
                font_weight='bold',
                position="top",
                formatter=JsCode(
                    "function(x){return Number(x.data.percent * 100).toFixed() + '%';}"
                ),
            )
        )
    )
    return c


def vip_distr():
    sql = """SELECT vip_status FROM info """
    cursor.execute(sql)
    vip_list = []
    val = []
    vips = cursor.fetchall()
    for vip in vips:
        vip_list.append(vip[0])
    count = ['大会员', '非大会员']
    for i in range(2):
        val.append(vip_list.count(count[i]))
    c = (
        Pie(init_opts=opts.InitOpts(width="500px", height="400px", chart_id="vip"))
            .add(
            "",
            radius=["30%", "55%"],
            data_pair=[('会员', val[0]), ('非会员', val[1])],
            tooltip_opts=opts.TooltipOpts(formatter="{b}: {c} ({d}%)"),
        )

            .set_global_opts(
            title_opts=opts.TitleOpts(
                title="会员分布",
                pos_left="center",
                pos_top="20",
            ),
            legend_opts=opts.LegendOpts(is_show=False),
        )

            .set_colors(['#F282A5', '#717171'])
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}"))
    )
    return c


def TimeLine():
    today = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    str = today.replace("-", "")
    str2date = datetime.datetime.strptime(str, "%Y%m%d")

    def get_day_of_day(str2date, n=0):
        return str2date + timedelta(days=n)

    i = 1
    timeline = []
    while (True):
        i -= 1
        getDate = get_day_of_day(str2date, i).date().strftime("%Y-%m-%d")
        timeline.append(getDate)
        if (i == -6):
            return timeline


def num_increase():
    sql_month = """SELECT time_follow FROM info """
    cursor.execute(sql_month)
    times = cursor.fetchall()
    time_list = []
    val = []
    for time in times:
        time_list.append(time[0])
    count = TimeLine()
    for i in range(7):
        val.append(time_list.count(count[i]))
    x_data = count
    y_data = val

    c = (
        Line(init_opts=opts.InitOpts(width="500px", height="400px", chart_id="increase"))
            .set_global_opts(
            tooltip_opts=opts.TooltipOpts(is_show=False),
            xaxis_opts=opts.AxisOpts(type_="category", ),
            yaxis_opts=opts.AxisOpts(
                type_="value",
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(width=1, color="ffffff1f"),
                ),
                axislabel_opts=opts.LabelOpts(margin=20, color="#F282A5", font_weight='bold'),
                axistick_opts=opts.AxisTickOpts(is_show=False),
                splitline_opts=opts.SplitLineOpts(is_show=True),
                min_='dataMin',
            ),

        )
            .set_global_opts(
            title_opts=opts.TitleOpts(
                title="粉丝增长情况",
                pos_left="center",
                pos_top="20",
            )
        )
            .set_series_opts(
            linestyle_opts=opts.LineStyleOpts(width=1),
        )
            .add_xaxis(xaxis_data=x_data)
            .add_yaxis(
            color='#F282A5',
            series_name="",  # 标题
            y_axis=y_data,
            symbol="emptyCircle",  # 节点啥样
            is_symbol_show=True,  # 是否显示节点
            symbol_size=8,
            is_hover_animation=True,
            is_smooth=True,  # 是否丝滑
            label_opts=opts.LabelOpts(is_show=True),  # 粉丝数显示
            linestyle_opts=opts.LineStyleOpts(width=3)
        )
    )
    return c

# layout=Page.DraggablePageLayout
page = Page()
page.add(level_distr(), sex_distr(), follow_distr(), vip_distr(), num_increase(), fans_distr())
page.render()

Page.save_resize_html("render.html", cfg_dict=[
    {"cid": "level", "width": "430.666666px", "height": "467.666666px", "top": "28px", "left": "109px"},
    {"cid": "sex", "width": "445.666666px", "height": "467.666666px", "top": "29px", "left": "568px"},
    {"cid": "follow", "width": "748.666666px", "height": "372.666666px", "top": "1000px", "left": "37px"},
    {"cid": "vip", "width": "430.666666px", "height": "466.666666px", "top": "29px", "left": "1057px"},
    {"cid": "increase", "width": "1078.666666px", "height": "399.666666px", "top": "496px", "left": "246px"},
    {"cid": "fans", "width": "862.666666px", "height": "372.666666px", "top": "1000px", "left": "786px"}],
                      dest="fans.html")
try:
    os.remove("render.html")
except:
    pass
connect.close()
