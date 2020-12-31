import numpy as np
import pandas as pd
import plotly
import plotly.graph_objs as go
import plotly.express as px
import lxml

url = 'https://www.basketball-reference.com/players/c/curryst01/gamelog-playoffs/'
df = pd.read_html(url)[-1]
print("\nFirst 5 rows of the playoffs:")
print(df.head())

# Drop rows with NaN values
# FIN - Finals
df = df.fillna('unknown')
df_Finals = df[df['Series'].str.contains('FIN')]
print("\nFirst 5 rows with Series = FIN (Finals):")
print(df_Finals.head())

# Mean of Field Goal Percentage (FG%), 3-Point Field Goals (3P), 3-Point Field Goal Attempts (3PA),
# 3-Point Field Goal Percentage (3P%), Total Rebounds (TRB), Assists (AST), Points (PTS)
columns = ['FG%','3P','3PA','3P%','TRB','AST','PTS']
df_Finals = df_Finals[columns].astype(float)
df_Finals_overall = df_Finals.mean()
print("\nMean values of FG%, 3P, 3PA, 3P%, TRB, AST, PTS:")
print(df_Finals_overall)

# Christmas day games
df_Christmas = pd.DataFrame()
for year in range(2010, 2021):
    url = 'https://www.basketball-reference.com/players/c/curryst01/gamelog/' + str(year)
    df = pd.read_html(url)[-1]
    df_Christmas = df_Christmas.append(df[df['Date'].str.contains('12-25')])
df_Christmas = df_Christmas[~pd.isna(df_Christmas['G'])]
print("\nChristmas or Big day games rows")
print(df_Christmas)
print("\nChristmas day games info:")
print(df_Christmas.info())

columns = ['FG%','3P','3PA','3P%','TRB','AST','PTS']
df_Christmas = df_Christmas[columns].astype(float)
print("\nChristmas day games info; FG%, 3P, 3PA, 3P%, TRB, AST, PTS:")
print(df_Christmas.info)

df_Christmas_overall = df_Christmas.mean()
print("\nChristmas day games mean of FG%, 3P, 3PA, 3P%, TRB, AST, PTS:")
print(df_Christmas_overall)

url = 'https://www.basketball-reference.com/players/c/curryst01.html'
df_overall = pd.read_html(url)[-1]
df_overall = df_overall.iloc[-1,:]
df_overall = df_overall[columns]
print(df_overall)

# Join the two dataframes (overall christmas and overall)
df2 = pd.DataFrame()
df2['Regular Season'] = df_overall
df2['Christmas'] = df_Christmas_overall
df2['index'] = df2.index
df2['Finals'] = df_Finals_overall
print("\nChristmas and Regular Combines:")
print(df2)

# Statistics of Stephen Curry - Regular Season, Christmas and Finals
# Bar Plots
fig = go.Figure(data=[
    go.Bar(name='Regular Season', x=df2['index'], y=df2['Regular Season']),
    go.Bar(name='Christmas', x=df2['index'], y=df2['Christmas']),
    go.Bar(name='Finals', x=df2['index'], y=df2['Finals']),
])
fig.update_layout(barmode='group')
fig.update_layout(title_text='Stephen Curry Stats - Regular Season, Christmas and Finals')
fig.show()

# Statistics of Stephen Curry - Regular Season and Finals
fig = go.Figure(data=[
    go.Bar(name='Regular Season', x=df2['index'], y=df2['Regular Season']),
    go.Bar(name='Finals', x=df2['index'], y=df2['Finals']),
])
fig.update_layout(barmode='group')
fig.update_layout(title_text='Stephen Curry Stats - Regular Season and Finals')
fig.show()

# FG%, 3P, 3P%, AST, TRB of Regular Season, Christmas and Finals
df3 = df2.drop('index',axis=1).T
print("\nFG%, 3P, 3P%, AST, TRB, PTS, 3PA of Regular Season, Christmas and Finals")
print(df3)

# Comparison of Stephen Curry's Points - Regular Season, Christmas and Finals
# Pie Charts
fig = go.Figure(data=[go.Pie(labels=df3.index, values=df3['PTS'])])
fig.update_layout(title_text="Comparison of Stephen Curry's Points - Regular Season, Christmas and Finals")
fig.show()

# Comparison of Stephen Curry's 3-Pointers - Regular Season and Christmas
fig = go.Figure(data=[go.Pie(labels=df3.index[df3.index != 'Finals'], values=df3.loc[df3.index != 'Finals','3P%'])])
fig.update_layout(title_text="Comparison of Stephen Curry's 3-Pointers - Regular Season and Christmas")
fig.show()