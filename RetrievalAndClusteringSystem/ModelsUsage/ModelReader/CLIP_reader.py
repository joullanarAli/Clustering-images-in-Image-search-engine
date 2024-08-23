from transformers import CLIPProcessor, CLIPModel
from RetrievalAndClusteringSystem.ModelsUsage.ModelReader.IModelReader import IModelReader
from RetrievalAndClusteringSystem.constants_paths import CLIP_MODEL
class CLIP_reader(IModelReader):


    def __init__(self):
        self.model_path = CLIP_MODEL
        

    def readModel(self):
        self.processor = CLIPProcessor.from_pretrained(self.model_path)
        self.model = CLIPModel.from_pretrained(self.model_path)
        return self.processor, self.model