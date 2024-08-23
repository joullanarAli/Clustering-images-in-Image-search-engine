import sys
import os
if '__file__' in globals():
    current_dir = os.path.dirname(__file__)
else:
    current_dir = os.getcwd()

sys.path.append(os.path.abspath(os.path.join(current_dir, '..')))
sys.path.append(os.path.abspath(os.path.join(current_dir, '..', 'RetrievalAndClusteringSystem')))

from fastapi import FastAPI,HTTPException
from typing import List, Dict
from RetrievalAndClusteringSystem.DatasetReader.FlickrDataset import FlickrDataset_reader
from RetrievalAndClusteringSystem.ModelsUsage.ModelReader.CLIP_reader import CLIP_reader
from fastapi.responses import HTMLResponse
from RetrievalAndClusteringSystem.RetrievalSystem.Faiss_Sen_Retrieval import Faiss_Sen_Retrieval
from RetrievalAndClusteringSystem.RetrievalSystem.Fiss_CLIP_Retrieval import Faiss_CLIP_Retrieval
from RetrievalAndClusteringSystem.Clustering.FaissKMeansClustering import FaissKMeansClustering
from RetrievalAndClusteringSystem.RetrievalSystem.my_retrieval import My_Retrieval
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

@app.get("/", response_class=HTMLResponse)
def read_root():
    with open("static/index.html") as f:
        return f.read()
# search api to return clusters
@app.get('/search')
def search_images(query: str):
    n_clusters = 2
    k=500
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

# the logic of the retrieval and clustering system
def get_similar_images(query: str,n_clusters,k,distance_metrice = 'cos_similarity'):
    dataset = FlickrDataset_reader()
    df, image_paths, captions = dataset.readDataset()
    my_retrieval = My_Retrieval(distance_metrice)
    alpha = 0.5
    cluster_centers, labels, top_images = my_retrieval.retrieveAndCluster(image_paths,captions,query,k,alpha,n_clusters)
    clusters = {}
    for label, image_path in zip(labels, top_images):
        if label not in clusters:
            clusters[label] = []
        clusters[label].append(image_path)
    return clusters


