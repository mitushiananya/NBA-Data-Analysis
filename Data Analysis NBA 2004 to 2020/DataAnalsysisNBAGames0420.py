import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.io as pio
pio.templates.default = "plotly_dark"
sns.set_style('darkgrid')

import time
import os

game_details = pd.read_csv('games_details.csv')
print("Game Details CSV Columns: ")
print(game_details.columns)
round(100*(game_details.isnull().sum()/len(game_details.index)),2)

game_details.drop(['GAME_ID','TEAM_ID','PLAYER_ID','START_POSITION','COMMENT','TEAM_ABBREVIATION'],axis = 1,inplace= True)
game_details['FTL'] = game_details['FTA'] - game_details['FTM']
game_details = game_details.dropna()
print("Total Rows and Columns that is the shape of the data: ",game_details.shape)
print("\nData Info: ")
print(game_details.info())

game_details['MIN'] = game_details['MIN'].str.strip(':').str[0:2]
df = game_details.copy()

# Players with the highest points in the NBA
top_activities = df.groupby('PLAYER_NAME')['PTS'].sum().sort_values(ascending =False).head(20).reset_index()
plt.figure(figsize=(15,10))
plt.xlabel('POINTS',fontsize=15)
plt.ylabel('PLAYER_NAME',fontsize=15)
plt.title('Top 20 Players with Highest Points in the NBA',fontsize = 20)
ax = sns.barplot(x=top_activities['PTS'],y = top_activities['PLAYER_NAME'], palette='viridis')
for i ,(value,name) in enumerate (zip(top_activities['PTS'],top_activities['PLAYER_NAME'])):
    ax.text(value, i-.05,f'{value:,.0f}',size = 10,ha='left',va='center')
ax.set(xlabel='POINTS',ylabel='PLAYER_NAME')
plt.show()

# Some stats of some legends: LeBron James, Stephen Curry, Kobe Bryant
# LBJ
player = df.groupby(['PLAYER_NAME'])
Bron = player.get_group('LeBron James')
plt.figure(figsize=(10,8))
plt.xlabel('POINTS',fontsize = 10)
sns.countplot(Bron['PTS'], palette='crest')
plt.title("LeBron James Stats")
plt.xticks(rotation = 90)
plt.show()

# Steph
player = df.groupby(['PLAYER_NAME'])
curry = player.get_group('Stephen Curry')
plt.figure(figsize=(10,8))
plt.xlabel('POINTS',fontsize = 10)
sns.countplot(curry['PTS'], palette='magma')
plt.title("Stephen Curry Stats")
plt.xticks(rotation = 90)
plt.show()

# Kobe
player = df.groupby(['PLAYER_NAME'])
kobe = player.get_group('Kobe Bryant')
plt.figure(figsize=(10,8))
plt.xlabel('POINTS',fontsize = 10)
sns.countplot(kobe['PTS'], palette='rocket_r')
plt.title("Kobe Bryant Stats")
plt.xticks(rotation = 90)
plt.show()

# LeBon James in Lakers vs Miami
Bron_Team = Bron.groupby('TEAM_CITY')
Bron_LA = Bron_Team.get_group('Los Angeles')
Bron_MIAMI = Bron_Team.get_group('Miami')
plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
plt.xlabel('POINTS', fontsize =10)
plt.title("LeBron in Los Angeles Lakers", fontsize = 12)
sns.countplot(Bron_LA['PTS'], palette='mako')
plt.xticks(rotation = 90)

plt.subplot(1, 2, 2)
plt.title("LeBron in Miami Heat", fontsize = 12)
plt.xlabel('POINTS', fontsize = 10)
sns.countplot(Bron_MIAMI['PTS'], palette='mako')
plt.xticks(rotation = 90)

plt.tight_layout()
plt.show()

# Top 3 Pointers in the NBA
# Obviously we dont even need to plot anything it is Steph Curry, the GOAT
top_3Pointers = df.groupby(by='PLAYER_NAME')['FG3M'].sum().sort_values(ascending =False).head(20).reset_index()
plt.figure(figsize=(15,10))
plt.xlabel('POINTS',fontsize=15)
plt.ylabel('PLAYER_NAME',fontsize=15)
plt.title('Top 20 - 3 point shooters in the NBA',fontsize = 20)
ax = sns.barplot(x=top_3Pointers['FG3M'],y = top_3Pointers['PLAYER_NAME'], palette='icefire')
for i ,(value,name) in enumerate (zip(top_3Pointers['FG3M'],top_3Pointers['PLAYER_NAME'])):
    ax.text(value, i-.05,f'{value:,.0f}',size = 10,ha='left',va='center')
ax.set(xlabel='POINTS',ylabel='PLAYER_NAME')
plt.show()

# Players with the worst free throw stats
df['FTL'] = df['FTA'] - df['FTM']
top_Shaqtin = df.groupby(by='PLAYER_NAME')['FTL'].sum().sort_values(ascending =False).head(20).reset_index()

plt.figure(figsize=(15,10))
plt.xlabel('POINTS',fontsize=15)
plt.ylabel('PLAYER_NAME',fontsize=15)
plt.title('Top 20 Players in the NBA with not-so-good free throw numbers',fontsize = 20)
ax = sns.barplot(x=top_Shaqtin['FTL'],y = top_Shaqtin['PLAYER_NAME'], palette='cubehelix')
for i ,(value,name) in enumerate (zip(top_Shaqtin['FTL'],top_Shaqtin['PLAYER_NAME'])):
    ax.text(value, i-.05,f'{value:,.0f}',size = 10,ha='left',va='center')
ax.set(xlabel='Free-Throw losses',ylabel='PLAYER_NAME')
plt.show()

# Players who have highest blocks done in the NBA
top_Blocks = df.groupby(by='PLAYER_NAME')['BLK'].sum().sort_values(ascending =False).head(20).reset_index()
plt.figure(figsize=(15,10))
plt.xlabel('BLOCKS',fontsize=15)
plt.ylabel('PLAYER_NAME',fontsize=15)
plt.title('Top 20 Players in the NBA League with highest blocks',fontsize = 20)
ax = sns.barplot(x=top_Blocks['BLK'],y = top_Blocks['PLAYER_NAME'], palette='vlag')
for i ,(value,name) in enumerate (zip(top_Blocks['BLK'],top_Blocks['PLAYER_NAME'])):
    ax.text(value, i-.05,f'{value:,.0f}',size = 10,ha='left',va='center')
ax.set(xlabel='Blocks',ylabel='PLAYER_NAME')
plt.show()