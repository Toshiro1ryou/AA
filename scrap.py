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
def send_email(subject, body, to_email):
    sender_email = "alikaouia469@gmail.com"
    password = "iugvwosmlngjbqup"  
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = to_email
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls() 
        server.login(sender_email, password)
        server.send_message(msg)
        print("Email sent successfully!")
def scraper():
#scrap
    url = requests.get("https://www.goal.com/en/live-scores")
    soup = BeautifulSoup(url.text, 'html.parser')
    with open('matches.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['League', 'Team', 'Score','W/L/D' , 'Date']) 

        competitions = soup.find_all("div", class_="fco-competition-section")

        for competition in competitions:
            league = competition.find("span", class_="fco-competition-section__header-name")
            teams = competition.find_all("div", class_="fco-match-team-and-score")
            print("name of the league: " + league.text)

            for team in teams:
                all_teams = team.find_all("div", class_="fco-team-name fco-short-name")
                score = team.find_all("div", class_="fco-match-score")
                all_score = []     
                for index, (clubs, result) in enumerate(zip(all_teams, score)):
                    score_text = result.text.strip()
                    today = date.today()
                    if result.text == "-":
                        print("match hasn't started yet")
                        

                        writer.writerow([league.text.strip(), clubs.text.strip(), "not started yet" ," ",today])
                    else:
                        if (index + 1) % 2 == 1:
                            print("---- match started ----")
                        all_score.append(int(score_text))   
                        
                        print(clubs.text + " // " + result.text + " // " , today)
                        
                        
                        if (index + 1) % 2 == 0:
                            print("---- match ended ----")
                            
                            home_score, away_score = all_score
                            team1 = all_teams[index - 1].text.strip()
                            team2 = all_teams[index].text.strip()
                            if home_score > away_score:
                                res1, res2 = "W", "L"
                            elif home_score < away_score:
                                res1, res2 = "L", "W"
                            else:
                                res1, res2 = "D", "D"
                            

                            writer.writerow([league.text.strip(), team1, home_score, res1 , today])
                            writer.writerow([league.text.strip(), team2, away_score, res2 , today ])
                            #scraping teams are in matches.csv
     
     #store data in a  database                  
    db = "db.csv"
    temp = "matches.csv"
    df_main = pd.read_csv(db)
    df_new = pd.read_csv(temp)

    df_combined = pd.concat([df_main, df_new], ignore_index=True)
    df_combined.to_csv(db, index=False)

    df = pd.read_csv("db.csv")
    df = df[df["Score"] != "not started yet"]
    df.to_csv("db.csv", index=False)
    df.drop_duplicates(inplace=True)
    df.to_csv("db.csv", index=False)   
    
    send_email(
    subject="Match Update",
    body="database updated",
    to_email="alikaouia84@gmail.com")
    with open("teams.json", "r") as f:
        data = json.load(f)
        followed_teams = data["equipes_suivies"]
    df = pd.read_csv("matches.csv")
    scraped_teams = set(df['Team'].tolist()) 
    
    for team in scraped_teams:
        if team in followed_teams:
            print(f" Match of {team} is found!")
            send_email(
         subject="Match Update",
        body=f"{team} match has been found",
        to_email="alikaouia84@gmail.com"
    )
schedule.every(1).hours.do(scraper)
while True:
    schedule.run_pending()
    time.sleep(60)