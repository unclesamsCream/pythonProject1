from jinja2 import Environment, FileSystemLoader
from pyecharts.globals import CurrentConfig
from django.http import HttpResponse
import pandas as pd
# CurrentConfig.GLOBAL_ENV = Environment(loader=FileSystemLoader("./demo/templates"))

from pyecharts import options as opts
from pyecharts.charts import Bar
from pyecharts.charts import Map
from pyecharts.faker import Faker
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
    c = (
        Map()
        .add("depression", [list(z) for z in zip(Faker.country, Faker.values())], "world")
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(
            title_opts=opts.TitleOpts(title="Map-世界地图"),
            visualmap_opts=opts.VisualMapOpts(max_=200),
        )
    )
    return HttpResponse(c.render_embed())