from RetrievalAndClusteringSystem.Indexing.IndexingInterface import IndexingInterface
from RetrievalAndClusteringSystem.Indexing.IndexingEvaluationInterface import IndexingEvaluationInterface
from abc import ABC , abstractmethod
from RetrievalAndClusteringSystem.DatasetReader.FlickrDataset import FlickrDataset_reader
from RetrievalAndClusteringSystem.ModelsUsage.Embeddings import Embeddings
from RetrievalAndClusteringSystem.ModelsUsage.ModelReader.sen_sim_sem_search_reader import sen_sim_sem_search_reader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import normalize
from RetrievalAndClusteringSystem.DataPreprocessing.Preprocess import PreprocessData
from RetrievalAndClusteringSystem.constants_paths import PRPROCESS_TFIDF_VECTORIZER, DATASET_DIR, RETRIEVED_IMG
import pandas as pd
import pandas as pd
from PIL import Image
import os
import shutil
import joblib

class GenericIndexer(IndexingInterface,IndexingEvaluationInterface,ABC):
    

    def __init__():
        pass
    
    @abstractmethod
    def create_index(self,data):
        
        pass

    def get_nearest_images_cos_sim(self, normalized_query_embedding,top_k):
        k=2
        self.similarities = []
        self.indices= []
        self.difference = 1
        while self.difference > 0.6 and k<top_k:
            del self.similarities, self.indices
            k= k+1
            self.similarities, self.indices = self.index.search(normalized_query_embedding, k) 
            self.difference = self.similarities[0][k-1]/self.similarities[0][0] 
        return self.similarities, self.indices
    
    def evaluate_nearest_images_cos_sim(self, normalized_query_embedding,k=100):
        self.similarities, self.indices = self.index.search(normalized_query_embedding, k) 
        return self.similarities, self.indices
    

    def print_results(self):
        samples = {
            "caption": [self.captions[i] for i in self.indices[0]],
            "image": [self.image_paths[i] for i in self.indices[0]],
            "similarities": self.similarities[0],
        }
        self.samples_df = pd.DataFrame.from_dict(samples)
        self.samples_df["similarities"] = self.similarities[0]
        self.samples_df.sort_values("similarities", ascending=False, inplace=True)
        for _, row in self.samples_df.iterrows():
            print(f"Caption: {row.caption}")
            print(f"Similarity: {row.similarities}")
            print(f"Image: {row.image}")
            print("=" * 50)
            print()

    def getSamplesDF(self):
        return self.samples_df

    def save_to_retrieved_folder(self,dataset='flickr'):
        
        if dataset == 'flickr':
            
            images_folder = DATASET_DIR+'\\Images'
            retrieved_folder = RETRIEVED_IMG

        # Ensure the retrieved_faiss directory exists
        os.makedirs(retrieved_folder, exist_ok=True)

        for _, row in self.samples_df.iterrows():

            # Construct the full path to the image file
            image_path = os.path.join(images_folder, row.image)

            # Open and save the image to the retrieved_faiss folder
            if os.path.exists(image_path):
                image = Image.open(image_path)
                #image.show()
                # Construct the path to save the image in the retrieved_faiss folder
                save_path = os.path.join(retrieved_folder, row.image)
                image.save(save_path)
                print(f"Image saved to {save_path}")
            else:
                print(f"Image file {image_path} not found.")
            print()  # Add a blank line for better readability




    def evaluate_index(self, k):
        sen_model = sen_sim_sem_search_reader()
        sen_model.readModel()
        
        dataset = FlickrDataset_reader()   
        df, image_paths, captions, BLIP_captions = dataset.read_BLIPDataset()
        
        unique_df = df.drop_duplicates(subset=['image'])
        BLIP_captions = unique_df['blip_caption']
        unique_images = unique_df['image']

        total_queries = len(BLIP_captions)
        precision_scores = []
        recall_scores = []

        for i, blip_caption in enumerate(BLIP_captions):
            query = blip_caption
            true_image = unique_images.iloc[i]
            # data_processor = PreprocessData()
            # query = data_processor.preprocess_text(query)
            query_embedding = sen_model.get_batch_embeddings([query], batch_size=1)
            normalized_query_embedding = sen_model.normalize_embeddings_fun(query_embedding)
            
            similarities, results = self.evaluate_nearest_images_cos_sim(normalized_query_embedding, k)

            samples = {
                "caption": [self.captions[i] for i in results[0]],
                "image": [self.image_paths[i] for i in results[0]],
                "similarities": similarities[0],
            }
            
            samples_df = pd.DataFrame.from_dict(samples)
            samples_df["similarities"] = similarities[0]
            samples_df.sort_values("similarities", ascending=False, inplace=True)
            
            retrieved_images = samples_df["image"].tolist()
            
            # Calculate precision
            relevant_retrieved = int(true_image in retrieved_images)
            precision = relevant_retrieved / k
            precision_scores.append(precision)
            
            # Calculate recall
            total_relevant = 1  # Since we are dealing with a single query and its corresponding true_image
            recall = relevant_retrieved / total_relevant
            recall_scores.append(recall)

        avg_precision = sum(precision_scores) / total_queries
        avg_recall = sum(recall_scores) / total_queries

        print(f"Average Precision: {avg_precision * 100:.2f}%")
        print(f"Average Recall: {avg_recall * 100:.2f}%")

        return avg_precision, avg_recall

    

    def evaluate_tfidf_index(self, k):
        dataset = FlickrDataset_reader()   
        df, image_paths, captions, BLIP_captions = dataset.read_BLIPDetailedDataset()
        unique_df = df.drop_duplicates(subset=['image'])
        BLIP_captions = unique_df['blip_caption']
        unique_images = unique_df['image']

        total_queries = len(BLIP_captions)
        precision_scores = []
        recall_scores = []

        for i, blip_caption in enumerate(BLIP_captions):
            query = blip_caption
            true_image = unique_images.iloc[i]
            data_processor = PreprocessData()
            query = data_processor.preprocess_text(query)
            # Create TF-IDF vectorizer
            vectorizer = joblib.load(PRPROCESS_TFIDF_VECTORIZER)
            tfidf_query_embeddings = vectorizer.transform([query]).toarray()

            # Normalize TF-IDF embeddings
            normalized_tfidf_embeddings = normalize(tfidf_query_embeddings, norm='l2')
            
            similarities, results = self.evaluate_nearest_images_cos_sim(normalized_tfidf_embeddings, k)

            samples = {
                "caption": [self.captions[i] for i in results[0]],
                "image": [self.image_paths[i] for i in results[0]],
                "similarities": similarities[0],
            }
            
            samples_df = pd.DataFrame.from_dict(samples)
            samples_df["similarities"] = similarities[0]
            samples_df.sort_values("similarities", ascending=False, inplace=True)
            
            retrieved_images = samples_df["image"].tolist()
            
            # Calculate precision
            relevant_retrieved = int(true_image in retrieved_images)
            precision = relevant_retrieved / k
            precision_scores.append(precision)
            
            # Calculate recall
            total_relevant = 1  # Since we are dealing with a single query and its corresponding true_image
            recall = relevant_retrieved / total_relevant
            recall_scores.append(recall)

        avg_precision = sum(precision_scores) / total_queries
        avg_recall = sum(recall_scores) / total_queries

        print(f"Average Precision: {avg_precision * 100:.2f}%")
        print(f"Average Recall: {avg_recall * 100:.2f}%")

        return avg_precision, avg_recall
    
    def evaluate_my_retrieval(retrieval_system, dataset, k=5, alpha=0.5, n_clusters=10):
        # Load the dataset
        df, image_paths, captions, BLIP_captions = dataset.read_BLIPDataset()
        unique_df = df.drop_duplicates(subset=['image'])
        BLIP_captions = unique_df['blip_caption']
        unique_images = unique_df['image']

        # Initialize lists to store precision and recall scores
        precision_scores = []
        recall_scores = []

        # Iterate over all BLIP captions and their corresponding true images
        for i, blip_caption in enumerate(BLIP_captions):
            query = blip_caption
            true_image = unique_images.iloc[i]
            
            # Use the retrieval system to get top images
            _, _, retrieved_images = retrieval_system.retrieveAndCluster(image_paths, captions, query, k, alpha, n_clusters)

            # Calculate precision
            relevant_retrieved = int(true_image in retrieved_images)
            precision = relevant_retrieved / k
            precision_scores.append(precision)

            # Calculate recall
            total_relevant = 1  # Since we are dealing with a single query and its corresponding true_image
            recall = relevant_retrieved / total_relevant
            recall_scores.append(recall)

        # Calculate average precision and recall
        avg_precision = sum(precision_scores) / len(precision_scores)
        avg_recall = sum(recall_scores) / len(recall_scores)

        print(f"Average Precision: {avg_precision * 100:.2f}%")
        print(f"Average Recall: {avg_recall * 100:.2f}%")

        return avg_precision, avg_recall