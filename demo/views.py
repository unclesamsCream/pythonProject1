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

def world_map(request):
    sheet1 = pd.read_excel(r"Mental health Depression disorder Data.xlsx", sheet_name="prevalence-by-mental-and-substa")  # 用该方法读取表格和表单里的单元格的数据
    years_count = sheet1["Year"]
    years_count = years_count.value_counts()
    x = years_count.index.tolist()
    time_list = [int(num) for num in x]
    time_list.sort()
    print(x)
    timeline = charts.Timeline(init_opts=options.InitOpts(width='1200px', height='600px'))
    map_data = [
        [[x["name"], x["value"]] for x in d["data"]] for d in data if d["time"] == year
    ][0]
    min_data, max_data = (
        min([d[1][0] for d in map_data]),
        max([d[1][0] for d in map_data]),
    )
    c = (

        Map()
        .add("depression", [list(z) for z in zip(Faker.country, Faker.values())], "world")
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(
            title_opts=opts.TitleOpts(title="Map-世界地图"),
            visualmap_opts=opts.VisualMapOpts(max_=200),
        )
    )
    for year in time_list:
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