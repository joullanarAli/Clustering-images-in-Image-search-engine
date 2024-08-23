import os
import sys
if '__file__' in globals():
    current_dir = os.path.dirname(__file__)
else:
    current_dir = os.getcwd()

sys.path.append(os.path.abspath(os.path.join(current_dir, '..')))

from constants_paths import SEN_MODEL

from sentence_transformers import SentenceTransformer, InputExample, losses
import pandas as pd
from sentence_transformers import SentenceTransformer, InputExample
from torch.utils.data import DataLoader
from sentence_transformers import SentenceTransformer, util
from transformers import AutoTokenizer, AutoModel

model_name="Sakil/sentence_similarity_semantic_search"
model = SentenceTransformer(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)
model.save_pretrained (SEN_MODEL)