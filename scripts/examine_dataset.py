#%%
import pandas as pd
path = "/tmp/test"
# %%
df = pd.read_feather(path)
df.head()
# %%
df.loc[0].description_type
# %%
from importlib import import_module
mod = import_module(df.loc[0].description_type)
mod
# %%
df.loc[0].describer
# %%
getattr(mod, df.loc[0].describer)
# %% [markdown]
# map strings to types again

# %%
import_from = lambda row: getattr(row.iloc[1],row.iloc[0])

def instantiate_dict(row):
    dct = row.iloc[0]
    # to_feather makes dict contain keys that were not originally present
    for k,v  in list(dct.items()):
        if v is None:
            del dct[k]

    return row.iloc[1](**dct)

df.mission_type = df.mission_type.map(import_module)
df.description_type = df.description_type.map(import_module)
df.describer = df[["describer", "description_type"]].apply(import_from, axis=1)
df.get_mission = df[["get_mission", "mission_type"]].apply(import_from, axis=1)
df.params_type = df[["params_type", "mission_type"]].apply(import_from, axis=1)
df.params = df[["params", "params_type"]].apply(instantiate_dict,axis=1)
# %%
df.head()
# %%
from swarm_descriptions.utils import load_mission_dataset

df = load_mission_dataset(path)
df.head()
# %%
