import sys
import os
if '__file__' in globals():
    current_dir = os.path.dirname(__file__)
else:
    current_dir = os.getcwd()

sys.path.append(os.path.abspath(os.path.join(current_dir, '..')))
sys.path.append(os.path.abspath(os.path.join(current_dir, '..', 'RetrievalAndClusteringSystem')))
sys.path.append(os.path.abspath(os.path.join(current_dir, '..', 'DatBase')))
from fastapi import FastAPI,HTTPException
from typing import List, Dict
from RetrievalAndClusteringSystem.DatasetReader.FlickrDataset import FlickrDataset_reader
from RetrievalAndClusteringSystem.ModelsUsage.ModelReader.CLIP_reader import CLIP_reader
from fastapi.responses import HTMLResponse
from RetrievalAndClusteringSystem.RetrievalSystem.Faiss_Sen_Retrieval import Faiss_Sen_Retrieval
from RetrievalAndClusteringSystem.RetrievalSystem.Fiss_CLIP_Retrieval import Faiss_CLIP_Retrieval
from RetrievalAndClusteringSystem.Clustering.FaissKMeansClustering import FaissKMeansClustering
from RetrievalAndClusteringSystem.RetrievalSystem.my_retrieval import My_Retrieval
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from typing import Optional
from DataBase.create_database import SessionLocal, User  # Import SQLAlchemy setup and models
from schemas import UserCreate, UserLogin, UserResponse  # Import Pydantic schemas
import pandas as pd
import numpy as np
from fastapi.staticfiles import StaticFiles
import logging
from fastapi.responses import JSONResponse

import torch
from fastapi.middleware.cors import CORSMiddleware


import uvicorn


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5000, reload=True)


app = FastAPI()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.mount("/static", StaticFiles(directory="static"), name="static")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Helper functions
def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: UserCreate):
    db_user = User(username=user.username, email=user.email, password=get_password_hash(user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Registration endpoint
@app.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user(db=db, user=user)

# Login endpoint
@app.post("/login")
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, user.email)
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Invalid email or password")
    # In a real application, you should return a session token or JWT
    return {"message": "Login successful", "user": UserResponse.from_orm(db_user)}

@app.get("/", response_class=HTMLResponse)
def read_root():
    with open("static/index.html") as f:
        return f.read()
# search api to return clusters
@app.get('/search')
def search_images(query: str, n_clusters: Optional[int] = 2):
    #n_clusters = 2
    print(query)
    k=300
    clusters = get_similar_images(query,n_clusters,k)
    return {"query": query, "clusters": clusters}

# get cluster api to return the images in the cluster
@app.get("/cluster")
async def get_cluster(cluster: str):
    cluster_dir = os.path.join("static", "clusters", f"cluster_{cluster}")
    if not os.path.isdir(cluster_dir):
        raise HTTPException(status_code=404, detail="Cluster not found")
    
    images = [img for img in os.listdir(cluster_dir) if img.lower().endswith(('png', 'jpg', 'jpeg'))]
    
    return JSONResponse({"images": images})

def get_similar_images(query: str, n_clusters: int, k: int, distance_metric: str = 'cos_similarity'):
    dataset = FlickrDataset_reader()
    df, image_paths, captions = dataset.readDataset()
    my_retrieval = My_Retrieval(distance_metric)
    alpha = 0.5
    cluster_centers, labels, top_images = my_retrieval.retrieveAndCluster(image_paths, captions, query, k, alpha, n_clusters)
    
    clusters = {}
    
    # Ensure that labels are of a hashable type
    for label, image_path in zip(labels, top_images):
        # Check if label is a list and convert it to a scalar if necessary
        if isinstance(label, list):
            # Convert label to an integer by selecting the first element
            label = label[0] if len(label) > 0 else None
        
        # Ensure label is an integer (or convert to a valid hashable type)
        if isinstance(label, int):  # You can add more checks if your label is expected to be of another type
            if label not in clusters:
                clusters[label] = []
            clusters[label].append(image_path)
        else:
            print(f"Warning: Found non-hashable or unexpected label type: {label}")
    
    return clusters

# the logic of the retrieval and clustering system
# def get_similar_images(query: str,n_clusters,k,distance_metrice = 'cos_similarity'):
    # dataset = FlickrDataset_reader()
    # df, image_paths, captions = dataset.readDataset()
    # my_retrieval = My_Retrieval(distance_metrice)
    # alpha = 0.5
    # cluster_centers, labels, top_images = my_retrieval.retrieveAndCluster(image_paths,captions,query,k,alpha,n_clusters)
    # clusters = {}
    
    # for label, image_path in zip(labels, top_images):
        
    #     if label not in clusters:
    #         clusters[label] = []
    #     clusters[label].append(image_path)
    # return clusters


