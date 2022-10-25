from jinja2 import Environment, FileSystemLoader
from pyecharts.globals import CurrentConfig
from django.http import HttpResponse
import pandas as pd
# CurrentConfig.GLOBAL_ENV = Environment(loader=FileSystemLoader("./demo/templates"))

from pyecharts import options as opts
from pyecharts.charts import Bar
from pyecharts.charts import Map
from pyecharts.faker import Faker
from pyecharts import charts, options
from pyecharts.charts import Geo
def index(request):
    # print(request)
    sheet1 = pd.read_excel(r"Mental health Depression disorder Data.xlsx", sheet_name="prevalence-by-mental-and-substa")  # 用该方法读取表格和表单里的单元格的数据
    sheet2 =pd.read_excel(r"Mental health Depression disorder Data.xlsx", sheet_name="depression-by-level-of-educatio")
    sheet3 = pd.read_excel(r"Mental health Depression disorder Data.xlsx", sheet_name="prevalence-of-depression-by-age")
    sheet4 = pd.read_excel(r"Mental health Depression disorder Data.xlsx", sheet_name="prevalence-of-depression-males-")
    sheet5 = pd.read_excel(r"Mental health Depression disorder Data.xlsx", sheet_name="suicide-rates-vs-prevalence-of-")
    years_count = sheet1["Year"]
    years_count = years_count.value_counts()
    x = years_count.index.tolist()
    x = [int(num) for num in x]
    y = years_count.values.tolist()
    c = (
        Bar()
        .add_xaxis(x)
        .add_yaxis("year",y)
        .set_global_opts(title_opts=opts.TitleOpts(title="Bar-基本示例", subtitle="我是副标题"))
    )
    # print(c)
    c.render()
    return HttpResponse(c.render_embed())
def get_year_chart(year):
    data1 = pd.read_excel(r"Mental health Depression disorder Data.xlsx",sheet_name="prevalence-by-mental-and-substa")  # 用该方法读取表格和表单里的单元格的数据
    # print(type(data1))
    # print(data1['Year'])
    # print(data1[data1['Year'] == 1990.0])
    year_data = data1[data1["Year"] == float(year)]
    year_data = [list(z) for z in zip(year_data['Entity'], year_data['Depression (%)'])]
    # year_data = [year_data['Entity'],year_data]
    # print(year_data)
    c = (
        Geo()
        .add_coordinate(name="China", longitude=104.195, latitude=35.675)
        .add_coordinate(name="Australia", longitude=133.775, latitude=-25.274)
        .add_coordinate(name="Brazil", longitude=-51.925, latitude=-14.235)
        .add_coordinate(name="South Africa", longitude=22.937, latitude=-30.559)
        .add_coordinate(name="India", longitude=78.962, latitude=20.593)
        .add_coordinate(name="Peru", longitude=-75.015, latitude=-9.189)
        .add_coordinate(name="Iran", longitude=53.688, latitude=32.427)
        .add_coordinate(name="Ukraine", longitude=31.165, latitude=48.379)
        .add_coordinate(name="Canada", longitude=-106.346, latitude=56.130)
        .add_coordinate(name="Mongolia", longitude=103.847, latitude=46.862)
        .add_coordinate(name="Russia", longitude=37.618, latitude=55.751)
        .add_coordinate(name="Mauritania", longitude=21.008, latitude=-10.941)
        .add_coordinate(name="Kazakhstan", longitude=66.924, latitude=48.019)
        .add_coordinate(name="UAE", longitude=53.848, latitude=23.424)
        .add_coordinate(name="Malaysia", longitude=101.976, latitude=4.210)
        .add_coordinate(name="New Zealand", longitude=174.886, latitude=-40.900)
        .add_coordinate(name="Indonesia", longitude=113.921, latitude=-0.789)
        .add_coordinate(name="Sweden", longitude=18.643, latitude=60.128)
        .add_coordinate(name="Mexico", longitude=-102.553, latitude=23.634)
        .add_coordinate(name="Sierra Leone", longitude=-11.779, latitude=8.461)
        .add_schema(maptype="world")
        .add("geo", [("Australia",128326),
            ("Brazil",44037),
            ("South Africa",7649),
            ("India",3562),
            ("Peru",2779),
            ("Iran",2698),
            ("Ukrainie",2040),
            ("Canada",1792),
            ("Mongolia",1514),
            ("Russia",1069),
            ("Mauritania",1374),
            ("Kazakhsan",701),
            ("UAE",490),
            ("Malaysia",554),
            ("New Zealand",422),
            ("Indonesia",148),
            ("Sweden",113),
            ("Mexico",121),
            ("Sierra Leone",109),
           ])
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(
            visualmap_opts=opts.VisualMapOpts(),
            title_opts=opts.TitleOpts(title="Geo-基本示例"),
        )
        # Map()
        # .add("depression", year_data, "world")
        # .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        # .set_global_opts(
        #     title_opts=opts.TitleOpts(title="Map-世界地图"),
        #     visualmap_opts=opts.VisualMapOpts(max_=5),
        # )
    )
    return c
    # map_data = map_data.append()[[[x["name"], x["value"]] for x in d["data"]] for d in data1 if d["time"] == year][0]
def world_map(request):
    data1 = pd.read_excel(r"Mental health Depression disorder Data.xlsx", sheet_name="prevalence-by-mental-and-substa")  # 用该方法读取表格和表单里的单元格的数据
    # print(type(data1))
    years_count = data1["Year"]
    years_count = years_count.value_counts()
    x = years_count.index.tolist()
    time_list = [int(num) for num in x]
    time_list.sort()
    # print(x)
    timeline = charts.Timeline(init_opts=options.InitOpts(width='1200px', height='600px'))

    for year in time_list:
        c = get_year_chart(year)
        timeline.add(c,time_point=str(year))
    timeline.add_schema(
        orient="vertical",
        is_auto_play=True,
        is_inverse=True,
        play_interval=5000,
        pos_left="null",
        pos_right="5",
        pos_top="20",
        pos_bottom="20",
        width="50",
        label_opts=opts.LabelOpts(is_show=True, color="#fff"),
    )
    return HttpResponse(timeline.render_embed())