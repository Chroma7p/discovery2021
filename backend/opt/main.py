import json

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from typing import Optional

from pydantic import BaseModel

from pymongo import MongoClient



#方向
direction=[["左","ひだり"],["前","まえ"],["右","みぎ"],"ふれ"]
#程度
degree=[
    ["ちょっと","少し"],
    ["そこそこ","まあまあ"],
    ["かなり","すごく","めっちゃ"]
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
      for d in dir:
        if d in word:
            deg=degchk(word)
            if dir==direction[-1]:
              return dir,deg
            return dir[0],deg

rep={"左":"left","前":"center","右":"right","ふれ":"swing"}
def decision(words):
    all=0
    ret={"left":0,"center":0,"right":0,"swing":0}
    for word in words:
        dir,deg=wordchk(word)
        ret[rep[dir]]+=deg
        all+=(rep[dir]!="swing")*deg
    if all==0:
      if ret["swing"]==0:
        return {"left":0,"center":0,"right":0,"swing":False}
      else:
        return {"left":0,"center":0,"right":0,"swing":True}
    for i in ["left","center","right"]:
      if ret[i]!=0:
        ret[i]/=all
    ret["swing"]=ret["swing"]>(1/3)
    return ret

class Item(BaseModel):
    words:list


class Word_DB(object):
    def __init__(self):
        self.client =MongoClient('mongodb://%s:%s@mongo:27017' % ('root', 'hack2021tofu'))#ここローカルホストになってるので適宜変えてください
        self.db=self.client["word_db"]
  
    def add_words(self,words):
        wjson={}
        for w in words:
            self.db.word_db.insert_one({"word":w})

    def get_words(self):
        ret= list(self.db.word_db.find())
        self.db.word_db.delete_many({})
        return [i["word"]for i in ret]

    def print_DB(self):
        print(list(self.db.word_db.find()))

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB=Word_DB()

@app.post("/records")
async def get_file(item:Item):
  DB.add_words(item.words)

@app.get("/order")
async def out_file():
  return decision(DB.get_words())