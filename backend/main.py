from fastapi import FastAPI, HTTPException, Request, Depends, Security, status
from fastapi.security import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
import string
import random
from pydantic import BaseModel
from datetime import datetime, timedelta
from dotenv import load_dotenv
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import os

# load env
load_dotenv()

# env variables
ENVIRONMENT = os.getenv("ENVIRONMENT")
EXPIRATION_HOURS = int(os.getenv("SNIPPET_EXPIRATION_HOURS"))
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS")
RATE_LIMIT = os.getenv("POST_RATE_LIMIT")
API_KEY = os.getenv("API_KEY")

# split the allowed origins
origins = [origin.strip() for origin in ALLOWED_ORIGINS.split(",")]

# setup api key
api_key_header = APIKeyHeader(
    name="Authorization",
    auto_error=False
)

# configure api key detection
def verify_api_key(api_key:str = Security(api_key_header)):
    
    print(f"Received: {api_key}")
    print(f"Expected: Bearer {API_KEY}")
    
    if api_key != f"Bearer {API_KEY}":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key"
        )
    
    return api_key

# set the api rate limiter
limiter = Limiter(key_func=get_remote_address)
# init fastapi
app = FastAPI()
app.state.limiter = limiter # add a state for fast api
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler) # add an error handler for api limiting

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_headers=['Content-Type', 'Authorization'],
    allow_methods=['GET', 'POST', 'OPTIONS'],
    allow_credentials=True,
)

# In memory storage for the json data
db = {}

# parses incoming POST request 
class SnippetRequest(BaseModel):
    content: str

@app.post("/v1/snippets", status_code=201)
@limiter.limit(RATE_LIMIT)
def read_snippets(request: Request ,payload: SnippetRequest, _: str = Depends(verify_api_key)):
    # combine alphabet and numbers
    id_generate = string.ascii_letters + string.digits
    # randomize sequence of numbers and string in a length of 0-6
    id_generate = ''.join(random.choice(id_generate) for _ in range(0,6))

    now = datetime.now()
    expiration_time = now + timedelta(hours=EXPIRATION_HOURS)
    
    # stores the markdown content
    db[id_generate] = {
        "content": payload.content,
        "expires_at": expiration_time,
    }
    
    print(db)
    
    # post payload
    return {
        "id": f"{id_generate}" ,
        "content": f"{payload.content}",
        "expires_at": f"{expiration_time}"
        }

@app.get("/v1/snippets/{id}")
@limiter.limit(RATE_LIMIT)
def read_root(request: Request,id: str, _: str = Depends(verify_api_key)):
    if id not in db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Snippet not found")
    
    #  check id
    snippet = db[id]
    # check if expiration time met
    if datetime.now() > snippet['expires_at']:
        del db[id]
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Snippet has expired")
    
    return {"id": f"{id}","content": f"{snippet['content']}"}

# to show api configuration
@app.get("/v1/config")
def get_config():
    return {
        "environment": ENVIRONMENT,
        "snippet_ttl_seconds": EXPIRATION_HOURS
    }