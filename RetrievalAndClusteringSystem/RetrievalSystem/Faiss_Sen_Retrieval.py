from RetrievalAndClusteringSystem.RetrievalSystem.IRetrieval import IRetrieval
from RetrievalAndClusteringSystem.ModelsUsage.ModelReader.sen_sim_sem_search_reader import sen_sim_sem_search_reader
from RetrievalAndClusteringSystem.DataPreprocessing.Preprocess import PreprocessData
import faiss
import numpy as np
from RetrievalAndClusteringSystem.Indexing.faiss_indexer import faiss_indexer
class Faiss_Sen_Retrieval(IRetrieval):

    def __init__(self,distance_metrice):
        self.distance_metrice = distance_metrice
        self.embedder = 'sen'

    
    def search(self, query,image_paths,captions,k):
        self.normalized_sen_embeddings = np.load('.\\RetrievalAndClusteringSystem\\Dataset\\FlickrDataset\\sen_embeddings\\normalized_embeddings.npy')
        print('sssss')
        sen_model = sen_sim_sem_search_reader()
        model, tokenizer = sen_model.readModel()
        faiss_index = faiss_indexer(image_paths,captions)
        faiss_index.create_index(self.normalized_sen_embeddings)
        # data_processor = PreprocessData()
        # query = data_processor.preprocess_text(query)
        query_embedding = sen_model.get_batch_embeddings([query], batch_size=1)
        normalized_query_embedding = sen_model.normalize_embeddings_fun(query_embedding)
        similarities = []
        indices = []
        if(self.distance_metrice=='cos_similarity'):
            similarities, indices = faiss_index.get_nearest_images_cos_sim(normalized_query_embedding,k)
           # faiss_index.print_results()
           # faiss_index.save_to_retrieved_folder(dataset_folder)
        retrieved_embeddings = self.normalized_sen_embeddings[indices]
        #print('retrieved: ',retrieved_embeddings.shape)

        return faiss_index, similarities, indices, retrieved_embeddings
    

    def getNormalizedEmbeddings(self):
        return self.normalized_sen_embeddings