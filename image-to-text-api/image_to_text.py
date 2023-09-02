import warnings

from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration

warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=UserWarning)

itt_processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
itt_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")


# 이미지 캡셔닝
def image_to_text(image):
    image = Image.open(image).convert("RGB")
    image = itt_processor(image, return_tensors="pt")
    caption = itt_model.generate(**image)
    return itt_processor.batch_decode(caption, skip_special_tokens=True)


if __name__ == "__main__":
    pass
