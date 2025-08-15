import requests
from bs4 import BeautifulSoup
import csv
import shutil
import pandas as pd
import smtplib
from email.mime.text import MIMEText
import json
import time
import schedule
import matplotlib.pyplot as plt
from datetime import date
with open("teams.json", "r") as f:
    data = json.load(f)
    followed_teams = data["equipes_suivies"]
df = pd.read_csv("db.csv")
scraped_teams = set(df['Team'].tolist()) 
matches_followed = df[df["Team"].isin(followed_teams)]
num_matches = len(matches_followed)
#display teams from json file that exsists in db.csv(currently off)
team_followed_score_display = False
while team_followed_score_display:
    print(f"Number of matches for followed teams: {num_matches}")
    matches_count_per_team = matches_followed["Team"].value_counts()
    print(matches_count_per_team)
    team_followed_score_display = False
#display graph of the following teams    
for  team in followed_teams:

    team_matches = df[df["Team"].str.lower() == team.lower()]
    
    if not team_matches.empty:
        scores = team_matches["Score"].tolist()
        scores = [int(o) for o in scores ] 
        #print(f"// {team} - Scores: {scores}")
        
        plt.plot((range(1, len(scores) + 1)), scores, marker="o", label=team)
    else:
        print(f"No matches found for: {team}")
plt.title("Score Progression for Followed Teams")
plt.xlabel("Matches played")
plt.ylabel("goals scored")
plt.legend()
plt.show()
for  ft in followed_teams:

    team_matches = df[df["Team"].str.lower() == ft.lower()]
    
    if not team_matches.empty:
        stats = team_matches["W/L/D"].tolist()
        print(ft + ": ")
        print(stats)
        win_count = stats.count("W")
        draw_count = stats.count("D")
        loss_count = stats.count("L")
        labels = ['Wins', 'Draws', 'Losses']
        sizes = [win_count, draw_count, loss_count]
        sizes, labels = zip(*[(size, label) for size, label in zip(sizes, labels) if size > 0])

        if sum(sizes) > 0:
            plt.figure()
            plt.pie(sizes, labels=labels, startangle=140, autopct="%1.1f%%")
            plt.title(f"Stats of {ft} in {sum(sizes)} matches")
            plt.axis("equal")
            
    else:
        print(f"No stats for: {ft}")

    
for r in ft:
    plt.show()

for  team in followed_teams:

    team_matches = df[df["Team"].str.lower() == team.lower()]
    
    if not team_matches.empty:
        scores = team_matches["Score"].tolist()
        scores = [int(s) for s in scores] 
        plt.bar(team, sum(scores), color='skyblue')
    else:
        print(f"No matches found for: {team}")

plt.ylabel("Goals")
plt.title("Goals by followed teams")
plt.show()