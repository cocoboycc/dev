import json
import re
import pandas as pd
from pathlib import Path

with open("gyms_final.json", "r", encoding="utf-8") as f: 
    gyms = json.load(f)


gym_without_owner=[]
for gym in gyms:
    if gym.get("owner")== None:
        gym_without_owner.append(gym)

print (len(gym_without_owner))
print (len(gyms))
 
