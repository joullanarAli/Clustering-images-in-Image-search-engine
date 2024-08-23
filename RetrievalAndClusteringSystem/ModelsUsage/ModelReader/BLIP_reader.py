from transformers import BlipProcessor, BlipForConditionalGeneration
from RetrievalAndClusteringSystem.ModelsUsage.ModelReader.IModelReader import IModelReader
from RetrievalAndClusteringSystem.constants_paths import BLIP_MODEL
class BLIP_reader(IModelReader):


    def __init__(self):
        self.model_path = BLIP_MODEL
        

    def readModel(self):
        self.processor = BlipProcessor.from_pretrained(self.model_path)
        self.model = BlipForConditionalGeneration.from_pretrained(self.model_path)
        return self.processor, self.model