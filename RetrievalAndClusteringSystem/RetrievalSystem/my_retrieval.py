from RetrievalAndClusteringSystem.RetrievalSystem.IRetrieval import IRetrieval
from RetrievalAndClusteringSystem.ModelsUsage.ModelReader.sen_sim_sem_search_reader import sen_sim_sem_search_reader
from RetrievalAndClusteringSystem.ModelsUsage.ModelReader.CLIP_reader import CLIP_reader
from RetrievalAndClusteringSystem.RetrievalSystem.Faiss_Sen_Retrieval import Faiss_Sen_Retrieval
from RetrievalAndClusteringSystem.RetrievalSystem.Fiss_CLIP_Retrieval import Faiss_CLIP_Retrieval
from RetrievalAndClusteringSystem.DataPreprocessing.Preprocess import PreprocessData
from RetrievalAndClusteringSystem.Clustering.FaissKMeansClustering import FaissKMeansClustering
from RetrievalAndClusteringSystem.constants_paths import IMAGE_EMBEDDINGS, CLUSTERS
import faiss
import pandas as pd
import torch
import numpy as np
from RetrievalAndClusteringSystem.Indexing.faiss_indexer import faiss_indexer
class My_Retrieval(IRetrieval):

    def __init__(self,distance_metrice='cos_similarity'):
        self.distance_metrice = distance_metrice
        self.embedder = 'sen and clip'

    def retrieveAndCluster(self,image_paths,captions,query,k,alpha,n_clusters):
        image_embeddings, top_images=self.search(query,image_paths,captions, k,alpha)
        cluster_centers,labels = self.cluster(image_embeddings,top_images,n_clusters)
        return cluster_centers,labels, top_images
    
    def delete_repeated_retrieves(self,sen_images,clip_images):
        mini_sen_images = []
        is_exist = False
        for sen_image in sen_images:
            for clip_image in clip_images:
                if sen_image == clip_image:
                    is_exist=True
            if is_exist==False:
                mini_sen_images.append(sen_image)
            is_exist=False
        return mini_sen_images
    
    def get_indices(self,mini_sen_images,samples_df):
        sen_indices=[]
        for image in mini_sen_images:
            for _,row in samples_df.iterrows():
                if image == row.image:
                    sen_indices.append(row.indexx)
                    break
        return sen_indices

    def search(self,query,image_paths,captions,k,alpha,distance_metrice='cos_similarity'):
        sen_retrieval = Faiss_Sen_Retrieval(distance_metrice)
        faiss_index, sen_similarities, indices, sen_retrieved_embeddings = sen_retrieval.search(query, image_paths, captions, k)
        # Step 2: Retrieve results using image similarity (CLIP)
        clip_retrieval = Faiss_CLIP_Retrieval(distance_metrice)
        clip_similarities, clip_indices, image_embeddings = clip_retrieval.search(query, k)
        samples = {
            "indexx": indices[0],
            "caption": [captions[i] for i in indices[0]],
            "image": [image_paths[i] for i in indices[0]],
            "similarities": sen_similarities[0],
        }
        samples_df = pd.DataFrame.from_dict(samples)
        sen_images_df=samples_df['image'].unique()
        sen_images=[]
        for row in sen_images_df:
            sen_images.append(row)
        clip_images=clip_indices['image'].unique().tolist()
        mini_sen_images= self.delete_repeated_retrieves(sen_images,clip_images)
        clip_embeddings=torch.load(IMAGE_EMBEDDINGS)
        # Convert clip_embeddings to a NumPy array if necessary
        if isinstance(clip_embeddings, torch.Tensor):
            clip_embeddings = clip_embeddings.numpy()
        sen_indices = self.get_indices(mini_sen_images,samples_df)
        sen_image_embeddings = []
        for i in sen_indices:
            j = int(i / 5)  # Compute the index for clip embeddings
            if 0 <= j < clip_embeddings.shape[0]:  # Ensure index is within bounds
                # Append the embedding, convert to numpy array if needed
                sen_image_embeddings.append(clip_embeddings[j])
            else:
                print(f"Warning: Index {j} is out of bounds for clip_embeddings.")
        clip_image_embeddings = []
        for i in clip_indices.index:
            j = int(i / 5)  # Compute the index for clip embeddings
            if 0 <= j < clip_embeddings.shape[0]:  # Ensure index is within bounds
                # Append the embedding, convert to numpy array if needed
                clip_image_embeddings.append(clip_embeddings[j])
            else:
                print(f"Warning: Index {j} is out of bounds for clip_embeddings.")
        for embedding in clip_image_embeddings:
            if isinstance(embedding, torch.Tensor):
                embedding = embedding.numpy()
            sen_image_embeddings.append(embedding)

        for image in clip_images:
            mini_sen_images.append(image)
        return sen_image_embeddings, mini_sen_images
    

    def cluster(self, image_embeddings, images, n_clusters):
        # Convert embeddings to numpy arrays
        processed_embeddings = []
        for embedding in image_embeddings:
            if isinstance(embedding, torch.Tensor):
                embedding = embedding.numpy()
            elif not isinstance(embedding, np.ndarray):
                raise TypeError("Embedding must be a numpy array or torch tensor.")
            
            if embedding.shape != (512,):
                raise ValueError("Embedding must have shape (512,).")
            
            processed_embeddings.append(embedding)
        
        image_embeddings = np.stack(processed_embeddings, axis=0).astype(np.float32)
        
        if image_embeddings.shape[1] != 512:
            raise ValueError("Unexpected embedding dimension.")
        
        d = image_embeddings.shape[1]
        kmeans = FaissKMeansClustering(d=d, n_clusters=n_clusters)
        cluster_centers, labels = kmeans.fit(image_embeddings)
        
        # Ensure types are converted to lists or Python native types
        cluster_centers = cluster_centers.tolist() if isinstance(cluster_centers, np.ndarray) else cluster_centers
        labels = labels.tolist() if isinstance(labels, np.ndarray) else labels
        
        indices = np.argsort(labels).tolist()  # Ensure indices is a list
        print(CLUSTERS)
        kmeans.cluster_and_save_images(image_embeddings, images, indices, root_folder=CLUSTERS)
        return cluster_centers, labels


    def getNormalizedEmbeddings(self):
        return getattr(self, 'normalized_sen_embeddings', None)

   


    def getNormalizedEmbeddings(self):
        return self.normalized_sen_embeddings