import os

# Define the current directory based on the location of constants.py or the current working directory
if '__file__' in globals():
    CURRENT_DIR = os.path.dirname(__file__)
else:
    CURRENT_DIR = os.getcwd()

# Define the constant paths
PARENT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, '.'))

NLTK_DATA_PATH= 'D:\\nltk_data'
# Dataset paths
DATASET_DIR = os.path.abspath(os.path.join(PARENT_DIR, 'Dataset','FlickrDataset'))
IMAGES_DATASET=os.path.abspath(os.path.join(DATASET_DIR,'Images'))
CAPTIONS_DATASET = os.path.abspath(os.path.join(DATASET_DIR,'captions.csv'))
#SEN Data
SEN_DATA = os.path.abspath(os.path.join(DATASET_DIR,'sen_embeddings'))
NORM_EMBED_SEN_DATA = os.path.abspath(os.path.join(SEN_DATA,'normalized_embeddings.npy'))
PREPROCESS_EMBED_SEN_DATA = os.path.abspath(os.path.join(SEN_DATA,'preprocessed_normalized_embeddings.npy'))

# TFIDF DATA
TFIDF_DATA = os.path.abspath(os.path.join(DATASET_DIR,'TFIDF_embeddings'))
NORM_EMBED_TFIDF_DATA = os.path.abspath(os.path.join(TFIDF_DATA,'normalized_tfidf_embeddings.npy'))
PREPROCESS_EMBED_TFIDF_DATA = os.path.abspath(os.path.join(TFIDF_DATA,'preprocessed_normalized_tfidf_embeddings.npy'))
TFIDF_VECTORIZER=os.path.abspath(os.path.join(PARENT_DIR,'tfidf_vectorizer'))
PRPROCESS_TFIDF_VECTORIZER=os.path.abspath(os.path.join(PARENT_DIR,'preprocessed_tfidf_vectorizer.pkl'))

#BLIP Data
BLIP_DATASET = os.path.abspath(os.path.join(DATASET_DIR,'flickr_dataset_with_BLIP_captions.csv'))
BLIP_DETAILED_DATASET = os.path.abspath(os.path.join(DATASET_DIR,'flickr_dataset_with_BLIP_detailed_captions.csv'))

#CLIP Data
IMAGE_EMBEDDINGS = os.path.abspath(os.path.join(PARENT_DIR,'image_embeddings.pt'))



# Pretrained Models
PRETRAINED_MODELS_DIR = os.path.abspath(os.path.join(PARENT_DIR,'PretrainedModels'))
SEN_MODEL = os.path.abspath(os.path.join(PRETRAINED_MODELS_DIR,'model'))

# Image Captioning
IMAGE_CAPTIONING_DIR=os.path.abspath(os.path.join(PRETRAINED_MODELS_DIR,'ImageCaptioning_models'))
BLIP_MODEL = os.path.abspath(os.path.join(IMAGE_CAPTIONING_DIR,'BLIP_model'))
CLIP_MODEL = os.path.abspath(os.path.join(IMAGE_CAPTIONING_DIR,'CLIP_model'))
# Dataset reader
DATASET_READER_DIR = os.path.abspath(os.path.join(PARENT_DIR, 'DatasetReader'))

# Pretrained Models Reader
MODELS_USAGE_DIR = os.path.abspath(os.path.join(PARENT_DIR, 'ModelsUsage'))
MODEL_READER_DIR = os.path.abspath(os.path.join(MODELS_USAGE_DIR,'ModelReader'))
#SEN_READER = os.path.abspath(os.path.join(MODEL_READER_DIR,'model'))

RETRIEVED_IMG = os.path.abspath(os.path.join(PARENT_DIR, '..' , 'static','Retrieved'))
CLUSTERS= os.path.abspath(os.path.join(PARENT_DIR, '..' , 'static','clusters'))
print('CLUSTERS',CLUSTERS)
