
#!/usr/bin/python3
# -*- coding:utf-8 -*-
# __author__ = '__Jack__'
import json
import time
import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

import os
from fastapi import FastAPI
from starlette.staticfiles import StaticFiles
from api import database
from api.endpoints import router as api_router 

app = FastAPI(title='FastAPI Application', version='1.0.0')


@app.middleware('http')
async def add_process_time_header(request: Request, call_next):  # call_next将接收request请求做为参数
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers['X-Process-Time'] = str(process_time)  # 添加自定义的以“X-”开头的请求头
    return response


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1",
        "http://127.0.0.1:8080"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Including your API routers
app.include_router(api_router, prefix='/api', tags=['GeneSets'])

test_list = ['Hs.233757', 'Hs.489142']
print(json.dumps(test_list))

if __name__ == '__main__':
    uvicorn.run('run:app', host='0.0.0.0', port=8000, reload=True, debug=True, workers=1) 