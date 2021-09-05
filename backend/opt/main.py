import json

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from typing import Optional

from pydantic import BaseModel

from pymongo import MongoClient

import socketio

#方向
direction=[["左","ひだり"],["前","まえ"],["右","みぎ"],"ふれ"]
#程度
degree=[
    ["ちょっと","少し"],
    [],
    ["かなり","すごく"]
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
              return dir,deg,-1
            return dir[0],deg,-1
    return -1,-1,degchk(word)

rep={"左":"left","前":"center","右":"right","ふれ":"swing"}
def decision(words):
    all=0
    stock=0
    ret={"left":0,"center":0,"right":0,"swing":0}
    for word in words:
        dir,deg,stk=wordchk(word)
        if stk!=-1:
          stock+=stk
          continue
        ndeg=deg+stock
        ret[rep[dir]]+=ndeg
        all+=(rep[dir]!="swing")*ndeg
        stock=0
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

# setup socketio
sio = socketio.AsyncServer(async_mode='asgi')
app_socketio = socketio.ASGIApp(sio)

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
  await sio.emit("word",{"words":item.words})
  DB.add_words(item.words)

@app.get("/order")
async def out_file():
  return decision(DB.get_words())