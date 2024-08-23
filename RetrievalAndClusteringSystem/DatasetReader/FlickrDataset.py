from RetrievalAndClusteringSystem.DatasetReader.IDataset_reader import IDataset_reader
from RetrievalAndClusteringSystem.constants_paths import CAPTIONS_DATASET , BLIP_DATASET, BLIP_DETAILED_DATASET
import numpy as np
import pandas as pd

class FlickrDataset_reader(IDataset_reader):


    def __init__(self):
        self.data = CAPTIONS_DATASET
        self.BLIP_data =  BLIP_DATASET
        self.BLIP_detailed_data = BLIP_DETAILED_DATASET
        
    def read(self, dataset):
        self.df = pd.read_csv(dataset)
        self.image_paths = self.df['image'].tolist()
        self.captions = self.df['caption'].tolist()
        return self.df, self.image_paths, self.captions
    
    def readDataset(self):
        return self.read(self.data)
    

    def readBLIP(self, dataset):
        self.BLIP_df = pd.read_csv(dataset)
        self.image_paths = self.BLIP_df['image'].tolist()
        self.captions = self.BLIP_df['caption'].tolist()
        self.BLIP_captions = self.BLIP_df['blip_caption'].tolist()
        return self.BLIP_df, self.image_paths, self.captions, self.BLIP_captions

    def read_BLIPDataset(self):
        return self.readBLIP(self.BLIP_data)
    
    def read_BLIPDetailedDataset(self):
        return self.readBLIP(self.BLIP_detailed_data)