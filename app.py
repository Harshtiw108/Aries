from flask import Flask, request, jsonify, send_file
from transformers import CLIPTextModel, CLIPTokenizer
from diffusers import StableDiffusionPipeline
import torch
from PIL import Image
import io

app = Flask(__name__)

# Check if a GPU is available and use it if possible
device = "cuda" if torch.cuda.is_available() else "cpu"

# Load the tokenizer and the model
tokenizer = CLIPTokenizer.from_pretrained("openai/clip-vit-large-patch14")
text_encoder = CLIPTextModel.from_pretrained("openai/clip-vit-large-patch14")
pipeline = StableDiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4").to(device)

@app.route('/generate', methods=['POST'])
def generate_image():
    data = request.json
    prompt = data.get('prompt')
    
    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400

    # Generate images
    images = pipeline([prompt], guidance_scale=7.5)["sample"]

    # Save the image to a byte buffer
    img = images[0]
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)

    return send_file(buf, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
 
