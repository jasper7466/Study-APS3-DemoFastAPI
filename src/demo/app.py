from fastapi import FastAPI, Response
from typing import Optional

app = FastAPI()


@app.get('/')
def root():
    return 'Hello, World!'


@app.get('/')
def root():
    return Response('Hello, World!')


@app.get('/greet/{name}')
def root(name: str):
    return Response(f'Hello, {name}!')


@app.get('/greet')
def root(name: Optional[str] = None):
    return Response(f'Hello, {name}!')
