import json
import math
import random
import numpy as np
import pandas as pd

def read_data():
    fm = pd.read_excel(r"D:\Desktop\data visualization-dataset\Mental health Depression disorder Data.xlsx", sheet_name="Sheet1")  # 用该方法读取表格和表单里的单元格的数据
    print(fm)
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    read_data()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
