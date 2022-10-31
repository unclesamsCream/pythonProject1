import pandas as pd
from pyecharts.charts import Bar


df2 = pd.read_excel('Mental health Depression disorder Data.xlsx', sheet_name=2)
df3 = pd.read_excel('Mental health Depression disorder Data.xlsx', sheet_name=3)
# df.append(df1)

# prevalence-of-depression-by-age
data2 = df2[['Entity','Code','Year','10-14 years old (%)','15-49 years old (%)','50-69 years old (%)','70+ years old (%)','Age-standardized (%)','All ages (%)']]
data2.to_csv('age.csv')

# prevalence-of-depression-by-gender

data3 = df3[df3['Prevalence in males (%)'] >= 0]

# print(data)
years_count = data3["Year"]
years_count = years_count.value_counts()
x = years_count.index.tolist()
x = [int(num) for num in x]
y = years_count.values.tolist()
# y = years_list.loc[years_list.index].values
# print(type(x[0]))
# print(type(y[0]))
bar = Bar()
bar.add_xaxis(x)
bar.add_yaxis("year", y)
bar.render('1.html')
data3.to_csv('gender.csv')
print("to csv finished")