from fastapi import FastAPI, HTTPException, Request, Depends, Security, status
from fastapi.security import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
import string
import random
from pydantic import BaseModel
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import os
from .firebase_config import db_firestore

# load env
load_dotenv()

# env variables
ENVIRONMENT = os.getenv("ENVIRONMENT", 'development')
EXPIRATION_HOURS = int(os.getenv("SNIPPET_EXPIRATION_HOURS", "2"))
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*")
RATE_LIMIT = os.getenv("POST_RATE_LIMIT", "5/minute") # default 5 requests per minute
API_KEY = os.getenv("API_KEY", "")

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

 # get db collection
docs = db_firestore.collection("snippets")

# parses incoming POST request 
class SnippetRequest(BaseModel):
    content: str

#  for status check of the api
@app.get("/", status_code=200)
@limiter.limit(RATE_LIMIT)
def check_api_status(request: Request):
    return {
        "status": "ok", 
        "message": "API is running!"
        }

@app.post("/api/v1/snippets", status_code=201)
@limiter.limit(RATE_LIMIT)
def add_snippets(request: Request ,payload: SnippetRequest, api_security: str = Depends(verify_api_key)):
    # combine alphabet and numbers
    id_generate = string.ascii_letters + string.digits
    # randomize sequence of numbers and string in a length of 0-6
    id_generate = ''.join(random.choice(id_generate) for _ in range(0,6))

    now = datetime.now(timezone.utc)
    expiration_time = now + timedelta(hours=EXPIRATION_HOURS)
    
    docs.document(id_generate).set({
        "content": payload.content,
        "expiration_at": expiration_time
    })
    
    # post payload
    return {
        "id": f"{id_generate}" ,
        "content": f"{payload.content}",
        "expires_at": f"{expiration_time}"
        }

# to view all active snippets in db
@app.get("/api/v1/snippets/all", status_code=200)
@limiter.limit(RATE_LIMIT)
def get_snippets_list(request: Request, api_security: str = Depends(verify_api_key)):
    docs_list = docs.stream()

    snippets = []

    now = datetime.now(timezone.utc)
    
    for doc in docs_list:
        
        if now > doc.to_dict()['expiration_at']:
            doc.reference.delete()
            
        snippets.append({
            "id": doc.id,
            "content": doc.to_dict()["content"],
            "expiration_at": doc.to_dict()["expiration_at"]
        })

    return snippets

@app.get("/api/v1/snippets/{id}", status_code=200)
@limiter.limit(RATE_LIMIT)
def get_snippet_id(request: Request,id: str, api_security: str = Depends(verify_api_key)):
    
    found_snippet = docs.document(id).get()
    
    # error if snippet not found
    if not found_snippet.exists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Snippet not found")
    
    # expiration check for the snippet
    now = datetime.now(timezone.utc)
    if now > found_snippet.to_dict()['expiration_at']:
        found_snippet.reference.delete()
    
    return {
        "id": f"{found_snippet.id}", 
        "content": f"{found_snippet.to_dict()['content']}",
        "expration_at": f"{found_snippet.to_dict()['expiration_at']}"
        }

# to show api configuration
@app.get("/api/v1/config", status_code=200)
@limiter.limit(RATE_LIMIT)
def get_api_config(request: Request, api_security: str = Depends(verify_api_key)):
    return {
        "environment": ENVIRONMENT,
        "snippet_ttl_hours": EXPIRATION_HOURS
    }