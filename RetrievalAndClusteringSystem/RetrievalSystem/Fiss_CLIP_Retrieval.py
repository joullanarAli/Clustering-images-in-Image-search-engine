from RetrievalAndClusteringSystem.RetrievalSystem.IRetrieval import IRetrieval
from RetrievalAndClusteringSystem.ModelsUsage.ModelReader.CLIP_reader import CLIP_reader
from RetrievalAndClusteringSystem.DataPreprocessing.Preprocess import PreprocessData
import faiss
import numpy as np
import pandas as pd
import torch
from RetrievalAndClusteringSystem.Indexing.faiss_indexer import faiss_indexer
from RetrievalAndClusteringSystem.DatasetReader.FlickrDataset import FlickrDataset_reader

class Faiss_CLIP_Retrieval(IRetrieval):

    def __init__(self,distance_metrice):
        self.distance_metrice = distance_metrice
        self.embedder = 'clip'

    def search(self, query,k=300):
        self.image_embeddings = torch.load('RetrievalAndClusteringSystem\\image_embeddings.pt')
        clip_model = CLIP_reader()
        processor, model = clip_model.readModel()
        
        dataset = FlickrDataset_reader()
        df, image_paths, captions= dataset.readDataset()
        unique_images = df.drop_duplicates(subset=['image'])

        
        
        # Encode the query
        inputs = processor(text=query, return_tensors="pt", padding=True, truncation=True)
        with torch.no_grad():
            query_embedding = model.get_text_features(**inputs)

        # Compute similarity with each image
        similarities = []
        for i in range(len(unique_images)):
            image_embedding = self.image_embeddings[i]
            similarity = torch.nn.functional.cosine_similarity(query_embedding, image_embedding.unsqueeze(0)).item()
            similarities.append(similarity)

        # Rank images based on similarity
        unique_images.loc[:, 'similarity_score'] = similarities
        sorted_df = unique_images.sort_values(by='similarity_score', ascending=False)
        
        self.retrieved = sorted_df.head(k)
        return similarities, self.retrieved, self.image_embeddings
    
    def evaluate_retrieval_blip_caption(self,df, threshold,top_k=10):
        all_precisions = []
        all_recalls = []
        
        unique_images = df['image'].unique()
        
        # Iterate over each unique image to evaluate using only the blip_caption
        for image in unique_images:
            # Get the BLIP caption for this image
            blip_caption = df[df['image'] == image]['blip_caption'].iloc[0]
            
            # Perform the search with the BLIP caption
            #retrieved_images, _ = self.search(query=blip_caption,k=top_k)
            similarities, retrieved_images, image_embeddings= self.get_nearest_images_cos_sim(query=blip_caption,top_k=top_k,threshold=threshold)
            # The ground truth for evaluation is the image corresponding to the BLIP caption
            ground_truth_images = df[df['blip_caption'] == blip_caption]['image'].unique().tolist()
            
            # Evaluate precision and recall
            precision, recall = self.evaluate_retrieval(retrieved_images[:top_k], ground_truth_images)
            all_precisions.append(precision)
            all_recalls.append(recall)

        # Compute the average precision and recall
        avg_precision = sum(all_precisions) / len(all_precisions) if all_precisions else 0
        avg_recall = sum(all_recalls) / len(all_recalls) if all_recalls else 0
    
        return avg_precision, avg_recall

    def evaluate_retrieval(self,retrieved_images, ground_truth_images):
        # Ensure retrieved_images and ground_truth_images are lists
        if isinstance(retrieved_images, pd.DataFrame):
            retrieved_images = retrieved_images.iloc[:, 0].tolist()
        
        if isinstance(ground_truth_images, pd.DataFrame):
            ground_truth_images = ground_truth_images.iloc[:, 0].tolist()
        
        if isinstance(retrieved_images, pd.Series):
            retrieved_images = retrieved_images.tolist()
        
        if isinstance(ground_truth_images, pd.Series):
            ground_truth_images = ground_truth_images.tolist()
        
        relevant_count = len(set(retrieved_images) & set(ground_truth_images))
        
        precision = relevant_count / len(retrieved_images) if len(retrieved_images) > 0 else 0
        recall = relevant_count / len(ground_truth_images) if len(ground_truth_images) > 0 else 0
        
        return precision, recall
    
    def get_nearest_images_cos_sim(self, query,top_k,threshold):
        k=2
        self.similarities = []
        self.retrieved= []
        self.image_embeddings=[]
        self.difference = 1
        while self.difference > threshold and k<top_k:
            del self.similarities, self.retrieved,self.image_embeddings
            k= k+1
            self.similarities, self.retrieved, self.image_embeddings = self.search(query, k) 
            self.difference = self.similarities[k-1]/self.similarities[0] 
        return self.similarities, self.retrieved, self.image_embeddings


    

    
    
        