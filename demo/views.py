from jinja2 import Environment, FileSystemLoader
from pyecharts.globals import CurrentConfig
from django.http import HttpResponse
import pandas as pd
# CurrentConfig.GLOBAL_ENV = Environment(loader=FileSystemLoader("./demo/templates"))

from pyecharts import options as opts
from pyecharts.charts import Bar


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