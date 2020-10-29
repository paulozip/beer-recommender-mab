import pandas as pd
from fastapi import FastAPI
from typing import Dict

from bandits import EpsilonGreedy

beers_df = pd.read_csv('data/csv/raw_dataset.csv')

BEER = beers_df['brand'].unique() # Unique beer values

app = FastAPI()
bandit = EpsilonGreedy(len(BEER), epsilon=0.3)

@app.get('/all_rewards')
def get_rewards():
    # Return the rewards of all arms
    return { 'arms_rewards': bandit._arms_rewards, 'brands': beers_df['brand'] }

@app.post('/pull')
def pull_arm():
    # Select an arms
    arm, dilemma, rewards = bandit.pull()
    return { 'arm': int(arm), 'brand': BEER[arm], 'brand_image': beers_df.loc[beers_df['brand'] == BEER[arm], 'image_url'], 'dilemma': dilemma, 'rewards': rewards }

@app.post('/reward')
def reward_arm(payload: Dict):
    arm = payload.get('arm')
    reward = payload.get('reward')

    bandit.update(arm, reward)
    return { 'arm': int(arm), 'brand': BEER[arm], 'reward_update': reward }

@app.get('/health')
def health_check():
    return 'It\'s alive!!'