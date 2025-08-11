# 🎨 Better GPT Image

An enhanced image generation tool that optimizes prompts and leverages OpenAI's GPT-Image-1 model for superior results. Deploy on Replicate or run locally!

## ⚠️ IMPORTANT: API Key Required

**This model requires YOUR OWN OpenAI API key to function.** The API key is:
- ✅ Used only for the current generation
- ✅ Never stored or logged
- ✅ Billed directly to your OpenAI account
- ✅ Kept completely private and secure

Get your API key at: https://platform.openai.com/api-keys

## ✨ Features

### 🚀 Core Capabilities
- **Intelligent Prompt Enhancement** - Automatically optimizes your prompts using GPT-5 for better image quality
- **Multiple Generation Modes**:
  - Standard text-to-image generation
  - Image editing with reference images
  - Mask-based inpainting
  - Multi-turn conversational editing
- **Style Presets** - Pre-configured styles for consistent results:
  - Photorealistic
  - Cinematic
  - Anime
  - Oil Painting
  - 3D Render
  - Concept Art

### 🎯 Advanced Features
- **High Input Fidelity** - Preserve details from reference images
- **Transparent Backgrounds** - Generate images with transparency
- **Streaming Support** - Watch images generate in real-time
- **Batch Processing** - Generate multiple variations at once
- **Cost Estimation** - Know your token usage before generating

## 🚀 Quick Start on Replicate

### Use the Model (No Setup Required!)

1. **Visit the model page**: https://replicate.com/preangelleo/better-gpt-image
2. **Enter your OpenAI API key** in the `api_key` field
3. **Type your prompt** and click "Run"
4. **That's it!** Your enhanced image will be generated

### Deploy Your Own Version

1. **Fork this repository**
2. **Sign up for Replicate**: https://replicate.com
3. **Install Cog** (if deploying locally):
```bash
sudo curl -o /usr/local/bin/cog -L https://github.com/replicate/cog/releases/latest/download/cog_`uname -s`_`uname -m`
sudo chmod +x /usr/local/bin/cog
```
4. **Push to Replicate**:
```bash
cog login
cog push r8.im/YOUR_USERNAME/better-gpt-image
```

## 🛠️ Installation

### Local Setup

1. **Clone the repository**
```bash
git clone https://github.com/preangelleo/better-gpt-image.git
cd better-gpt-image
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up your API key**

Option A: Environment Variable (Recommended)
```bash
# macOS/Linux
export OPENAI_API_KEY='your-api-key-here'

# Windows
set OPENAI_API_KEY=your-api-key-here
```

Option B: .env File
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

4. **Run Interactive CLI**
```bash
python test_local.py
```

The interactive CLI will:
- Create `input/` folder for your reference images
- Create `output/` folder for generated images
- Guide you through all features with an easy menu
- Save all outputs with timestamps

### Replicate Deployment

1. **Install Cog**
```bash
sudo curl -o /usr/local/bin/cog -L https://github.com/replicate/cog/releases/latest/download/cog_`uname -s`_`uname -m`
sudo chmod +x /usr/local/bin/cog
```

2. **Test with Cog**
```bash
cog predict \
  -i api_key="your-openai-api-key" \
  -i prompt="a majestic lion in a sunset" \
  -i optimize_prompt=true \
  -i style_preset="photorealistic"
```

3. **Push to Replicate**
```bash
cog login
cog push r8.im/your-username/better-gpt-image
```

## 🎮 Interactive CLI

The easiest way to use Better GPT Image is through the interactive CLI:

```bash
python test_local.py
```

### Features:
- **Generate Image** - Create images from text prompts with style presets
- **Edit with Reference** - Modify images using reference images from `input/` folder
- **Prompt Optimization** - Test different style presets without generating
- **Cost Estimates** - View token usage before generating
- **Session Management** - All outputs organized by timestamp in `output/` folder

### Workflow:
1. Place any reference images in the `input/` folder
2. Run the CLI and select your desired function
3. Follow the interactive prompts
4. Find your generated images in `output/YYYYMMDD_HHMMSS/`

## 📖 Usage

### Basic Generation
```python
from src.prompt_optimizer import PromptOptimizer
from src.image_generator import ImageGenerator

# Initialize
optimizer = PromptOptimizer(api_key)
generator = ImageGenerator(api_key)

# Optimize prompt
enhanced_prompt, negative_prompt, metadata = optimizer.enhance_prompt(
    "a cat sitting on a windowsill",
    style_preset="photorealistic"
)

# Generate image
result = generator.generate_image(
    prompt=enhanced_prompt,
    size="1024x1024",
    quality="high"
)

# Save image
if result["success"]:
    generator.save_image(result["images"][0]["b64_json"], "output.png")
```

### Image Editing with Reference
```python
# Edit an image using references
result = generator.edit_image(
    prompt="Add a sunset in the background",
    images=["reference1.jpg", "reference2.jpg"],
    input_fidelity="high"
)
```

### Mask-based Inpainting
```python
from src.image_processor import ImageProcessor

processor = ImageProcessor()

# Create a mask
mask = processor.create_mask(
    "original.jpg",
    mask_type="center",
    mask_data={"size_ratio": 0.5}
)

# Edit with mask
result = generator.edit_image(
    prompt="Replace with a flower",
    images=["original.jpg"],
    mask=mask
)
```

### Multi-turn Generation
```python
# First generation
result1 = generator.generate_image("A peaceful forest scene")
response_id = result1["response_id"]

# Refine in next turn
result2 = generator.multi_turn_generation(
    conversation_history=[{"prompt": "A peaceful forest scene", "image_id": "..."}],
    new_prompt="Add a small cabin in the distance",
    previous_response_id=response_id
)
```

## 🎨 Style Presets

| Preset | Description | Best For |
|--------|-------------|----------|
| `photorealistic` | Ultra-realistic photographs | Portraits, landscapes, products |
| `cinematic` | Movie-like dramatic shots | Scenes, storytelling, mood |
| `anime` | Japanese animation style | Characters, fantasy, vibrant |
| `oil_painting` | Traditional painted look | Artistic, classical, portraits |
| `3d_render` | CGI/3D graphics | Products, architecture, games |
| `concept_art` | Professional illustrations | Games, movies, design |

## 📊 API Parameters

### Required
- `api_key` - Your OpenAI API key

### Basic Options
- `prompt` - Image description
- `optimize_prompt` - Auto-enhance prompt (default: true)
- `style_preset` - Apply style (default: none)
- `size` - Image dimensions (1024x1024, 1536x1024, 1024x1536)
- `quality` - Quality level (low, medium, high)
- `num_images` - Number to generate (1-4)

### Advanced Options
- `reference_images` - Comma-separated paths/URLs
- `mask_image` - Mask for inpainting
- `input_fidelity` - Preserve input details (low/high)
- `background` - Background type (auto/transparent/opaque)
- `previous_response_id` - For multi-turn editing
- `conversation_history` - JSON conversation context

## 💰 Cost Estimation

Token usage varies by size and quality:

| Quality | 1024×1024 | 1024×1536 | 1536×1024 |
|---------|-----------|-----------|-----------|
| Low | 272 tokens | 408 tokens | 400 tokens |
| Medium | 1,056 tokens | 1,584 tokens | 1,568 tokens |
| High | 4,160 tokens | 6,240 tokens | 6,208 tokens |

Use `generator.estimate_cost()` to calculate before generating.

## 🧪 Testing

Run the test suite:
```bash
# Basic tests (no API calls)
python test_local.py

# Full tests (requires API key)
pytest tests/
```

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Add tests for new features
4. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details

## 🙏 Acknowledgments

- OpenAI for GPT-5 and GPT-Image-1 models
- Replicate for the deployment platform
- Cog for containerization tools

## 📞 Support

- Issues: [GitHub Issues](https://github.com/yourusername/better-gpt-image/issues)
- Discussions: [GitHub Discussions](https://github.com/yourusername/better-gpt-image/discussions)

---

Built with ❤️ for the AI art community