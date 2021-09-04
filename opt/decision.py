from fastapi import FastAPI
from typing import Optional

from pydantic import BaseModel




#����
direction=["��","�O","�E"]
#���x
degree=[
    ["������","�������"],
    ["�܂��܂�"],
    ["���Ȃ�","�߂�����","��"]
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

rep={"��":"l","�O":"c","�E":"r"}
def decision(words):
    all=0
    ret={"left":0,"center":0,"right":0,"swing":False}
    for word in words:
        dir,deg=wordchk(word)
        ret[rep[dir]]+=deg
        all+=deg
    for i in ["l","c","r"]:
        ret[i]/=all
    return ret

class Item(BaseModel):
    words:list
app = FastAPI()
@app.get("/order")
async def root(item:Item):
    return decision(item.words)