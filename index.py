import requests
from bs4 import BeautifulSoup
import csv
import shutil
import pandas as pd
import smtplib
from email.mime.text import MIMEText
import json
import matplotlib.pyplot as plt
def send_outlook_email(subject, body, to_email):
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
#def scraper():
url = requests.get("https://www.goal.com/en/live-scores")
soup = BeautifulSoup(url.text, 'html.parser')
with open('matches.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['League', 'Team', 'Score','W/L/D']) 

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
                if result.text == "-":
                    print("match hasn't started yet")

                    writer.writerow([league.text.strip(), clubs.text.strip(), "not started yet"])
                else:
                    if (index + 1) % 2 == 1:
                        print("---- match started ----")
                    all_score.append(int(score_text))    
                    print(clubs.text + " // " + result.text)
                    
                     
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
                        writer.writerow([league.text.strip(), team1, home_score, res1])
                        writer.writerow([league.text.strip(), team2, away_score, res2])
source_file = "matches.csv"
destination_file = "your_matches.csv"
df1 = pd.read_csv(source_file)
df2 = pd.read_csv(destination_file)
with open("teams.json", "r") as f:
    data = json.load(f)
    followed_teams = data["equipes_suivies"]
df = pd.read_csv("db.csv")
scraped_teams = set(df['Team'].tolist()) 
matches_followed = df[df["Team"].isin(followed_teams)]
num_matches = len(matches_followed)

team_followed_score_display = False
while team_followed_score_display:
    print(f"Number of matches for followed teams: {num_matches}")
    matches_count_per_team = matches_followed["Team"].value_counts()
    print(matches_count_per_team)
    team_followed_score_display = False
for i, team in enumerate(followed_teams):

    team_matches = df[df["Team"].str.lower() == team.lower()]
    
    if not team_matches.empty:
        scores = team_matches["Score"].tolist()
        scores = [int(s) for s in scores] 
        print(f"// {team} - Scores: {scores}")
        
        plt.plot((range(1, len(scores) + 1)), scores, marker="o", label=team)
    else:
        print(f"No matches found for: {team}")
plt.title("Score Progression for Followed Teams")
plt.xlabel("Matches played")
plt.ylabel("goals scored")
plt.legend()
plt.show()

for team in scraped_teams:
    if team in followed_teams:
        print(f" Match of {team} is found!")
        send_outlook_email(
    subject="Match Update",
    body=f"{team} match has been found",
    to_email="alikaouia84@gmail.com"
)

if df1.equals(df2):
    print("same")
    
    
else:
   shutil.copy(source_file, destination_file)
   print(f"'{source_file}' copied to '{destination_file}' successfully.")
   print("different")
   send_outlook_email(
    subject="Match Update",
    body="there are new matches",
    to_email="alikaouia84@gmail.com")
   db = "db.csv"
   temp = "matches.csv"
   df_main = pd.read_csv(db)
   df_new = pd.read_csv(temp)
   df_combined = pd.concat([df_main, df_new], ignore_index=True)
   df_combined.to_csv(db, index=False)
   
    


                            
#while True:
   # schedule.run_pending()
    #time.sleep(60)




    



    




