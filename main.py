from fastapi import FastAPI
from scr.wallets.router import router as wallets_router

app = FastAPI()


@app.get('/')
def home():
    return {'messages': 'Hello world', 'status': 200}


app.include_router(wallets_router)

app.add_event_handler('startup', lambda: print("API startup"))
app.add_event_handler('shutdown', lambda: print("API shutdown"))
