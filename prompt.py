import os
import base64
import google.generativeai as genai
from dotenv import load_dotenv
import pandas as pd
import json


load_dotenv()

genai.configure(api_key=os.environ["GEMINI_API_KEY"])
generation_config = {
    "temperature" : 1,
    "top_p" : 0.95,
    "top_k": 40,
    "max_output_tokens": 81100,
}
model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    generation_config=generation_config,
    system_instruction="You are a professional football analyst with expertise in match performance evaluation, tactical breakdowns, and team form analysis. Your job is to examine the latest match results, highlight key strengths and weaknesses, point out standout players, and identify tactical patterns. Use clear, insightful language suitable for sports journalism, and provide data-driven observations. End your analysis with predictions for the team’s next match, including possible scorelines and factors that could influence the outcome",

)
chat_session = model.start_chat(
    history=[

    ]
)
with open("teams.json", "r") as f:
    data = json.load(f)
    followed_teams = data["equipes_suivies"]
df = pd.read_csv("db.csv")

matches_followed = df[df["Team"].isin(followed_teams)]
num_matches = len(matches_followed)
print("RESPONSE IS GENERATING...")
response = chat_session.send_message(f"heres the results of {str(followed_teams)} : {str(matches_followed)} write me a resume about their performances, and can you also give some predictions for their next games ")
print(response.text)
