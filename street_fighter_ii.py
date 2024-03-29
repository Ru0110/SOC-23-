# -*- coding: utf-8 -*-
"""Street Fighter II.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/16T1ykyduocuPh6NZXL2D_NeW86_QPHOq
"""

!pip install stable-baselines[mpi]==2.10.0
!pip install gym-retro
!pip install tqdm

from tqdm import tqdm
import time
import retro
from stable_baselines.common.policies import MlpPolicy,MlpLstmPolicy, MlpLnLstmPolicy, CnnLnLstmPolicy, CnnPolicy, CnnLstmPolicy
from stable_baselines.common.vec_env import SubprocVecEnv, DummyVecEnv
from stable_baselines import PPO2, A2C



from google.colab import drive
drive.mount('/content/drive')

!python -m retro.import /gdrive/"My Drive"/"Where you Keep your Game Files"

#Create and Train Model on SFII Engine
gamename = 'StreetFighterIISpecialChampionEdition-Genesis'
modelname = 'Fighter_a2c_pt2' #whatever name you want to give it
env = DummyVecEnv([lambda: retro.make(gamename ,state='Champion.Level1.RyuVsGuile')])
model = A2C(CnnPolicy,env,n_steps=128, verbose=1)
#model = A2C.load('/gdrive/My Drive/ROMS/Fighter_a2c_pt2.zip')
model.set_env(env)
model.learn(total_timesteps=1000)
#Saves Model into
model.save("/gdrive/My Drive/"#"Whatever Your File Name is/" + modelname)
env.close()

#Training and Saving Your Model
#Use whatever you called your states without the .state extension
sts = ['RyuVsGuile','RyuVsBlanka','RyuVsRyu','RyuVsKen','RyuVsChunLi','RyuVsZangief','RyuVsDhalsim','RyuVsHonda','RyuVsBalrog','RyuVsVega','RyuVsSagat','RyuVsBison']
start_time = time.time()
for st in tqdm(sts, desc='Main Loop'):
  print(st)
  env = DummyVecEnv([lambda: retro.make('StreetFighterIISpecialChampionEdition-Genesis', state=st, scenario='scenario')])
  model.set_env(env)
  model.learn(total_timesteps=500000)
  model.save(modelname)
  env.close()
end_time = time.time() - start_time
print(f'\n The Training Took {end_time} seconds')

env = DummyVecEnv([lambda: retro.make('StreetFighterIISpecialChampionEdition-Genesis',state='RyuVsHonda-Easy', record='/gdrive/My Drive/'"Wherever you put file")])
model = A2C.load(modelname)
model.set_env(env)
obs = env.reset()
done = False
reward = 0
while not done:
  actions, _ = model.predict(obs)
  obs, rew, done, info = env.step(actions)
  reward += rew
print(reward)
### Convert BK2 to MP4 File
!python /usr/local/lib/python3.6/dist-packages/retro/scripts/playback_movie.py "/gdrive/My Drive/Level16.RyuVsHonda-Easy-000000.bk2"

