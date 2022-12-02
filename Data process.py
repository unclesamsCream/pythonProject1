import pandas as pd
import plotly.express as px
from functools import reduce

df2 = pd.read_excel('Mental health Depression disorder Data.xlsx', sheet_name=2)
df3 = pd.read_excel('Mental health Depression disorder Data.xlsx', sheet_name=3)
df4 = pd.read_excel('Mental health Depression disorder Data.xlsx', sheet_name=4)

# df.append(df1)
data_c = pd.read_csv('all.csv')
data_country =data_c[['name','alpha-3','region']]
# print(data_country)
data2 = df2[['Entity','Code','Year','10-14 years old (%)','15-49 years old (%)','50-69 years old (%)','70+ years old (%)','Age-standardized (%)','All ages (%)']]
data3 = df3[df3['Prevalence in males (%)'] >= 0]
data4 = df4[df4['Suicide rate (deaths per 100,000 individuals)'] >= 0]
dfs = [data2,data3,data4]
data_fusion = reduce(lambda left,right: pd.merge(left,right,how='inner',on=['Entity','Year']), dfs)
data_fusion = data_fusion.drop(['Code_x','Code_y','Population_x','Population_y'], axis=1)

data_result = pd.merge(left=data_fusion, right=data_country, left_on='Code', right_on='alpha-3', how='inner')
data_result = data_result.drop(columns = ['alpha-3', 'name'])
years_count = data_result["Year"]
years_count = years_count.value_counts()
x = years_count.index.tolist()
data_x = [int(num) for num in x]
data_y = years_count.values.tolist()
fig = px.bar(
    x=data_x,
    y=data_y,
)
fig.show()
data_result.to_csv('data_fusion.csv')
# print(data_fusion)
# data_fusion = pd.merge(left=data2, right=data3, on = ['Entity','Year'], how='inner').merge(data_fusion,)
# data fusion
# data_fusion = None
# for d2 in data2:
#     for d3 in data3:
#         for d4 in data4:
#             if d2['Entity'] == d3['Entity'] == d4['Entity'] and d2['Year'] == d3['Year'] == d4['Year']:
#                 data_fusion = data_fusion.append()
# prevalence-of-depression-by-age



# data2_result = pd.merge(left=data2, right=data_country, left_on='Code', right_on='alpha-3', how='inner')
# data2_result.drop(columns = ['alpha-3', 'name'])
# years_count = data2_result["Year"]
# years_count = years_count.value_counts()
# x = years_count.index.tolist()
# data_x = [int(num) for num in x]
# data_y = years_count.values.tolist()
# fig = px.bar(
#     x=data_x,
#     y=data_y,
# )
# fig.show()
# # print(data2_result)
# data2_result.to_csv('age.csv')
#
# # prevalence-of-depression-by-gender
#
# data3_result = pd.merge(left=data3, right=data_country, left_on='Code', right_on='alpha-3', how='inner')
# data3_result.drop(columns = ['alpha-3', 'name'])
# # print(data)
# years_count = data3_result["Year"]
# years_count = years_count.value_counts()
# x = years_count.index.tolist()
# data_x = [int(num) for num in x]
# data_y = years_count.values.tolist()
# fig = px.bar(
#     x=data_x,
#     y=data_y,
# )
# fig.show()
# data3_result.to_csv('gender.csv')
# print("to csv finished")
#
# #suicide data
#
# data4_result = pd.merge(left=data4, right=data_country, left_on='Code', right_on='alpha-3', how='inner')
# data4_result.drop(columns = ['alpha-3', 'name'])
# years_count = data4_result["Year"]
# years_count = years_count.value_counts()
# x = years_count.index.tolist()
# data_x = [int(num) for num in x]
# data_y = years_count.values.tolist()
# fig = px.bar(
#     x=data_x,
#     y=data_y,
# )
# fig.show()
# data4_result.to_csv('suicide.csv')
# print("data4 to csv finished")