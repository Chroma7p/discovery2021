from fastapi import FastAPI
from typing import Optional

from pydantic import BaseModel

#方向
direction=["左","前","右","振れ"]
#程度
degree=[
    ["すこし","ちょっと"],
    ["まあまあ"],
    ["かなり","めっちゃ","超"]
    ]

def degchk(word):
    sco=0
    for i, deg in enumerate(degree):
        for d in deg:
            if d in word:
                sco+=(i+1)
    if sco==0:
        sco=2
    return sco

def wordchk(word):
    for dir in direction:
        if dir in word:
            deg=degchk(word)
            return dir,deg

rep={"左":"l","前":"c","右":"r"}
def decision(words):
    all=0
    ret={"left":0,"center":0,"right":0,"swing":0}
    for word in words:
        dir,deg=wordchk(word)
        ret[rep[dir]]+=deg
        all+=(dir!="swing")
    for i in ["left","center","right"]:
        ret[i]/=all
    ret["swing"]=ret["swing"]>(1/3)
    return ret

class Item(BaseModel):
    words:list
app = FastAPI()
@app.get("/order")
async def root(item:Item):
    return decision(item.words)
