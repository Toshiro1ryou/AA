import requests
from bs4 import BeautifulSoup
from datetime import date

async def root():
    url = requests.get("https://www.goal.com/en/live-scores")
    soup = BeautifulSoup(url.text, 'html.parser')
    results = []
    competitions = soup.find_all("div", class_="fco-competition-section")

    for competition in competitions:
        league = competition.find("span", class_="fco-competition-section__header-name")
        teams = competition.find_all("div", class_="fco-match-team-and-score")
        today = date.today()

        for team in teams:
            all_teams = team.find_all("div", class_="fco-team-name fco-short-name")
            score = team.find_all("div", class_="fco-match-score")
            all_score = []

            for index, (clubs, result) in enumerate(zip(all_teams, score)):
                score_text = result.text.strip()

                if result.text == "-":
                    team1 = all_teams[index - 1].text.strip()
                    team2 = all_teams[index].text.strip()
                    results.append({
                        "league": league.text.strip(),
                        "team1": team1,
                        "score": "not started yet",
                        "team2": team2,
                        "date": str(today)
                    })
                else:
                    all_score.append(int(score_text))
                    if (index + 1) % 2 == 0:
                        home_score, away_score = all_score
                        team1 = all_teams[index - 1].text.strip()
                        team2 = all_teams[index].text.strip()
                        results.append({
                            "league": league.text.strip(),
                            "team1": team1,
                            "score": f"{home_score}-{away_score}",
                            "team2": team2,
                            "date": str(today)
                        })
    
    return results
