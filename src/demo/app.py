from fastapi import FastAPI, Response, Form
from typing import Optional

from .models import BaseForm

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


@app.post('/body')
def root(name: str = Form(...)):
    return Response(f'Hello, {name}!')


@app.post('/body')
def root(form: BaseForm):
    return Response(f'Hello, {form.name}!')
