import json
import math
import random
import numpy as np
import pandas as pd
from pyecharts.charts import Bar
def read_data():
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
    # y = years_list.loc[years_list.index].values
    print(type(x[0]))
    print(type(y[0]))
    bar = Bar()
    bar.add_xaxis(x)
    bar.add_yaxis("year",y)
    bar.render()

    # print(sheet1)
    # print(sheet2)
    # print(sheet3)
    # print(sheet4)
    # print(sheet5)
# Press the green button in the gutter to run the script.
import pyecharts.options as opts
from pyecharts.charts import MapGlobe
from pyecharts.faker import POPULATION

def test():
    data = [x for _, x in POPULATION[1:]]
    low, high = min(data), max(data)
    c = (
        MapGlobe()
        .add_schema()
        .add(
            maptype="world",
            series_name="World Population",
            data_pair=POPULATION[1:],
            is_map_symbol_show=False,
            label_opts=opts.LabelOpts(is_show=False),
        )
        .set_global_opts(
            visualmap_opts=opts.VisualMapOpts(
                min_=low,
                max_=high,
                range_text=["max", "min"],
                is_calculable=True,
                range_color=["lightskyblue", "yellow", "orangered"],
            )
        )
        .render("map_globe_base.html")
    )

if __name__ == '__main__':
    test()
    # read_data()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
