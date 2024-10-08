from RetrievalAndClusteringSystem.ModelsUsage.Embeddings.Embeddings import Embeddings
from RetrievalAndClusteringSystem.ModelsUsage.ModelReader.IModelReader import IModelReader
from transformers import AutoTokenizer, AutoModel
from RetrievalAndClusteringSystem.constants_paths import SEN_MODEL
class sen_sim_sem_search_reader(Embeddings,IModelReader):


    def __init__(self):
        self.model_path = SEN_MODEL
        

    def readModel(self):

        # Load the tokenizer from the local directory
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)

        # Load the model from the local directory
        self.model = AutoModel.from_pretrained(self.model_path,from_tf=False, use_safetensors=True)
        return self.model, self.tokenizer