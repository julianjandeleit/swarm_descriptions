#%%
import pandas as pd
path = "/tmp/test"
# %%
from swarm_descriptions.utils import load_mission_dataset

df = load_mission_dataset(path)
df.head()
# %%

