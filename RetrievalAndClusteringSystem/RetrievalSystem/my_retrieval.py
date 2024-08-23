from RetrievalAndClusteringSystem.RetrievalSystem.IRetrieval import IRetrieval
from RetrievalAndClusteringSystem.ModelsUsage.ModelReader.sen_sim_sem_search_reader import sen_sim_sem_search_reader
from RetrievalAndClusteringSystem.ModelsUsage.ModelReader.CLIP_reader import CLIP_reader
from RetrievalAndClusteringSystem.RetrievalSystem.Faiss_Sen_Retrieval import Faiss_Sen_Retrieval
from RetrievalAndClusteringSystem.RetrievalSystem.Fiss_CLIP_Retrieval import Faiss_CLIP_Retrieval
from RetrievalAndClusteringSystem.DataPreprocessing.Preprocess import PreprocessData
from RetrievalAndClusteringSystem.Clustering.FaissKMeansClustering import FaissKMeansClustering
import faiss
import pandas as pd
import torch
import numpy as np
from RetrievalAndClusteringSystem.Indexing.faiss_indexer import faiss_indexer
class My_Retrieval(IRetrieval):

    def __init__(self,distance_metrice):
        self.distance_metrice = distance_metrice
        self.embedder = 'sen and clip'

    def retrieveAndCluster(self,image_paths,captions,query,k,alpha,n_clusters):
        image_embeddings, top_images=self.search(query,image_paths,captions, k,alpha)
        # print (len(image_embeddings))
        # print(len(top_images))
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
        print('indices',len(indices[0]))
        # Step 2: Retrieve results using image similarity (CLIP)
        clip_retrieval = Faiss_CLIP_Retrieval(distance_metrice)
        clip_similarities, clip_indices, image_embeddings = clip_retrieval.search(query, k)
        print('clip_indices',len(clip_indices))
        print('image_embeddings',len(image_embeddings))
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
        print('sen_images',len(sen_images))
        clip_images=clip_indices['image'].unique().tolist()
        print('clip_images',len(clip_images))
        mini_sen_images= self.delete_repeated_retrieves(sen_images,clip_images)
        print('mini_sen_images',len(mini_sen_images))
        clip_embeddings=torch.load('RetrievalAndClusteringSystem\\image_embeddings.pt')
        # Convert clip_embeddings to a NumPy array if necessary
        if isinstance(clip_embeddings, torch.Tensor):
            clip_embeddings = clip_embeddings.numpy()
        sen_indices = self.get_indices(mini_sen_images,samples_df)
        print('sen_indices',len(sen_indices))
        sen_image_embeddings = []
        for i in sen_indices:
            j = int(i / 5)  # Compute the index for clip embeddings
            if 0 <= j < clip_embeddings.shape[0]:  # Ensure index is within bounds
                # Append the embedding, convert to numpy array if needed
                sen_image_embeddings.append(clip_embeddings[j])
            else:
                print(f"Warning: Index {j} is out of bounds for clip_embeddings.")
        print('sen_image_embeddings',len(sen_image_embeddings))
        clip_image_embeddings = []
        for i in clip_indices.index:
            j = int(i / 5)  # Compute the index for clip embeddings
            if 0 <= j < clip_embeddings.shape[0]:  # Ensure index is within bounds
                # Append the embedding, convert to numpy array if needed
                clip_image_embeddings.append(clip_embeddings[j])
            else:
                print(f"Warning: Index {j} is out of bounds for clip_embeddings.")
        print('clip_image_embeddings',len(clip_image_embeddings))
        for embedding in clip_image_embeddings:
            if isinstance(embedding, torch.Tensor):
                embedding = embedding.numpy()
            sen_image_embeddings.append(embedding)
        print('sen_clip_image_embeddings',len(sen_image_embeddings))
        print('mini_sen_images',len(mini_sen_images))
        print('clip_images',len(clip_images))

        for image in clip_images:
            mini_sen_images.append(image)
        print('sen_images',len(mini_sen_images))
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
        kmeans.cluster_and_save_images(image_embeddings, images, indices, root_folder='static\\clusters')
        return cluster_centers, labels


    def getNormalizedEmbeddings(self):
        return getattr(self, 'normalized_sen_embeddings', None)

    # def search(self, query, image_paths, captions, k, alpha):
    #     # Step 1: Retrieve results using sentence similarity (semantic search)
    #     sen_retrieval = Faiss_Sen_Retrieval(self.distance_metrice)
    #     faiss_index, sen_similarities, indices, sen_retrieved_embeddings = sen_retrieval.search(query, image_paths, captions, k)
        
    #     # Step 2: Retrieve results using image similarity (CLIP)
    #     clip_retrieval = Faiss_CLIP_Retrieval(self.distance_metrice)
    #     clip_similarities, clip_indices, image_embeddings = clip_retrieval.search(query, k)
        
    #     # Convert clip_similarities to numpy array
    #     clip_similarities = np.array(clip_similarities)
        
    #     # Convert clip_indices DataFrame to list of filenames (if necessary)
    #     if isinstance(clip_indices, pd.DataFrame):
    #         clip_indices = clip_indices.iloc[:, 0].tolist()
    #     elif not isinstance(clip_indices, list):
    #         clip_indices = list(clip_indices)
        
    #     # Ensure indices and sen_similarities are numpy arrays
    #     indices = np.array(indices).flatten()  # Flatten to ensure it's 1D
    #     sen_similarities = np.array(sen_similarities).flatten()  # Flatten to ensure it's 1D
        
    #     # Create mappings from indices to similarities for sentence similarity
    #     sen_index_map = {int(idx): float(sim) for idx, sim in zip(indices, sen_similarities)}
        
    #     # Create mappings from clip_indices (filenames) to similarities for CLIP
    #     if all(isinstance(i, str) for i in clip_indices):
    #         image_path_to_index = {path: idx for idx, path in enumerate(image_paths)}
    #         clip_index_map = {image_path_to_index.get(filename, -1): float(sim) for filename, sim in zip(clip_indices, clip_similarities)}
    #     else:
    #         clip_index_map = {int(idx): float(sim) for idx, sim in zip(clip_indices, clip_similarities)}
        
    #     # Find common indices
    #     common_indices = set(sen_index_map.keys()).intersection(clip_index_map.keys())
        
    #     # Create lists for common similarities
    #     common_sen_similarities = np.array([sen_index_map[idx] for idx in common_indices])
    #     common_clip_similarities = np.array([clip_index_map[idx] for idx in common_indices])
        
    #     # Normalize the similarities
    #     common_sen_similarities = (common_sen_similarities - common_sen_similarities.min()) / (common_sen_similarities.max() - common_sen_similarities.min())
    #     common_clip_similarities = (common_clip_similarities - common_clip_similarities.min()) / (common_clip_similarities.max() - common_clip_similarities.min())
        
    #     # Combine similarities
    #     combined_scores = alpha * common_sen_similarities + (1 - alpha) * common_clip_similarities
        
    #     # Sort by combined score
    #     sorted_indices = np.array(list(common_indices))[combined_scores.argsort()[::-1]]
        
    #     # Retrieve top k results
    #     top_indices = sorted_indices[:k]
    #     top_images = [image_paths[i] for i in top_indices]
    #     top_scores = combined_scores[np.isin(common_indices, top_indices)]
        
    #     # Return the top k results
    #     return top_images, top_scores




    # def cluster(self, images, n_clusters, image_paths):
    #     # Load image embeddings
    #     image_embeddings = torch.load('image_embeddings.pt')
    #     print("Image Embeddings Loaded:", type(image_embeddings))

    #     # Create a unique mapping of image filenames to their embeddings
    #     unique_images_set = set(images)
    #     if isinstance(image_embeddings, dict):
    #         selected_embeddings = np.array([image_embeddings[filename] for filename in unique_images_set if filename in image_embeddings])
    #     elif isinstance(image_embeddings, torch.Tensor):
    #         # Map filenames to indices, only keeping unique filenames
    #         image_filename_to_index = {filename: idx for idx, filename in enumerate(image_paths)}
    #         selected_indices = [image_filename_to_index[filename] for filename in unique_images_set if filename in image_filename_to_index]
            
    #         # Validate and filter selected indices
    #         valid_indices = [idx for idx in selected_indices if idx < image_embeddings.shape[0]]
    #         if len(valid_indices) < len(selected_indices):
    #             print(f"Warning: {len(selected_indices) - len(valid_indices)} indices were out of bounds and were removed.")
            
    #         selected_embeddings = image_embeddings[valid_indices]
    #     else:
    #         raise TypeError("Unsupported type for image_embeddings")

    #     if selected_embeddings.size == 0:
    #         raise ValueError("No valid embeddings found for the selected images.")

    #     print("Selected Embeddings Shape:", selected_embeddings.shape)

    #     # Step 2: Cluster the selected embeddings
    #     d = selected_embeddings.shape[1]
    #     kmeans = FaissKMeansClustering(d=d, n_clusters=n_clusters)
    #     cluster_centers, labels = kmeans.fit(selected_embeddings)

    #     # Sort indices based on cluster labels
    #     indices = np.argsort(labels)

    #     # Save clustered images
    #     kmeans.cluster_and_save_images(selected_embeddings, images, indices, root_folder='static\\clusters')

    #     return cluster_centers, labels




    def getNormalizedEmbeddings(self):
        return self.normalized_sen_embeddings