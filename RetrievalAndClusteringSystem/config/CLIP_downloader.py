import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
from PIL import Image
import requests
import sys
if '__file__' in globals():
    current_dir = os.path.dirname(__file__)
else:
    current_dir = os.getcwd()

sys.path.append(os.path.abspath(os.path.join(current_dir, '..')))

from constants_paths import CLIP_MODEL

from transformers import CLIPProcessor, CLIPModel

model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

processor.save_pretrained(CLIP_MODEL)
model.save_pretrained (CLIP_MODEL)