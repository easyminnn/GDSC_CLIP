from transformers import CLIPProcessor, CLIPModel

class CLIPHandler:
    def __init__(self):
        # Load the CLIP model and processor
        self.model = CLIPModel.from_pretrained("openai/clip-vit-base-patch16")
        self.processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch16")

    def process(self, images, text):
        # Preprocess images and text
        inputs = self.processor(text=text, images=images, return_tensors="pt", padding=True)
        outputs = self.model(**inputs)
        return outputs.logits_per_image  # Logits for image-text similarity
