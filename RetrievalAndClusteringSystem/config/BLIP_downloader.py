import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
import sys

if '__file__' in globals():
    current_dir = os.path.dirname(__file__)
else:
    current_dir = os.getcwd()

sys.path.append(os.path.abspath(os.path.join(current_dir, '..')))

from constants_paths import BLIP_MODEL


from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image

#pip install transformers pillow requests
import requests



# Load the BLIP model and processor
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

processor.save_pretrained(BLIP_MODEL)
model.save_pretrained(BLIP_MODEL)