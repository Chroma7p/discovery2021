import json

from fastapi import APIRouter
from typing import Optional

from pydantic import BaseModel

from pymongo import MongoClient


#方向
direction=["左","前","右","振れ"]
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
        if dir in word:
            deg=degchk(word)
            return dir,deg

rep={"左":"left","前":"center","右":"right"}
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


class Word_DB(object):
    def __init__(self):
        self.client =MongoClient('localhost', 27017)#ここローカルホストになってるので適宜変えてください
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

router = APIrouter()

DB=Word_DB()



@router.post("/records")
async def get_file(item:item):
  DB.add_words(item.words)


@router.get("/order")
async def out_file():
  return DB.get_words()