#!/usr/bin/env python
#coding:utf-8
#__time__: 2020/3/9 17:40
#__author__ = 'ren_mcc'

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}


