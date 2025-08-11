# 🎨 Better GPT Image - Enhanced AI Image Generation

**Transform your ideas into stunning images with intelligent prompt optimization powered by GPT**

Better GPT Image is an advanced open-source image generation tool that automatically enhances your prompts using state-of-the-art language models before generating images. Get professional-quality results without being a prompt engineering expert!

## 🌟 Why Better GPT Image?

Traditional image generation requires careful prompt crafting. Better GPT Image solves this by:
- **Automatic Prompt Enhancement**: Uses GPT to optimize your prompts for superior results
- **90+ Artistic Styles**: From photorealistic to anime, oil painting to 3D renders
- **Professional Quality**: Leverages OpenAI's latest image generation models
- **Context-Aware**: Understands and improves vague or incomplete descriptions
- **Style Preservation**: Maintains your intended artistic vision while enhancing details

## ⚡ Quick Start

### Prerequisites
- Python 3.8 or higher
- OpenAI API key

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/preangelleo/better-gpt-image.git
cd better-gpt-image
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up your OpenAI API key**

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

4. **Run the interactive CLI**
```bash
python test_local.py
```

## 💡 Key Features

### 🚀 Intelligent Prompt Optimization
Our advanced system transforms simple descriptions into detailed, context-rich prompts:
- **Before**: "a cat"
- **After**: "A majestic tabby cat with striking green eyes, sitting elegantly on a vintage wooden windowsill, soft afternoon sunlight streaming through sheer curtains, creating a warm and peaceful atmosphere, highly detailed fur texture, professional photography"

### 🎨 90+ Style Presets
Choose from our curated collection:
- **Photorealistic**: Ultra-realistic photography with professional quality
- **Cinematic**: Movie-quality scenes with dramatic lighting
- **Anime/Manga**: Japanese animation styles including Studio Ghibli
- **3D Animation**: Pixar, Disney, DreamWorks styles
- **Traditional Art**: Oil painting, watercolor, pencil sketch
- **Modern Digital**: Concept art, cyberpunk, vaporwave
- **Historical**: Renaissance, Baroque, Art Nouveau
- And many more!

### 🛠️ Advanced Options
- **Multiple Sizes**: 1024x1024, 1536x1024, 1024x1536
- **Quality Settings**: Low, Medium, High, Auto
- **Reference Images**: Use existing images as style references
- **Mask Editing**: Edit specific parts of images
- **Transparent Backgrounds**: Generate images with transparency
- **Batch Generation**: Create multiple variations

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

## 📖 Python API Usage

### Basic Generation
```python
from src.prompt_optimizer import PromptOptimizer
from src.image_generator import ImageGenerator
import os

# Get API key from environment
api_key = os.getenv("OPENAI_API_KEY")

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
result = generator.edit_image_with_reference(
    prompt="Add a sunset in the background",
    reference_images=[
        {"base64": generator.image_to_base64("reference1.jpg")}
    ],
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
result = generator.edit_image_with_reference(
    prompt="Replace with a flower",
    reference_images=[{"base64": generator.image_to_base64("original.jpg")}],
    mask=mask
)
```

### Multi-turn Generation
```python
# First generation
result1 = generator.generate_image("A peaceful forest scene")

# Continue the conversation
result2 = generator.multi_turn_generation(
    new_prompt="Add a small cabin in the distance",
    previous_response_id=result1.get("response_id")
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
| `watercolor` | Soft, fluid painting style | Nature, portraits, abstract |
| `pencil_sketch` | Hand-drawn pencil art | Sketches, studies, drafts |
| `ghibli` | Studio Ghibli animation | Fantasy, whimsical, nature |
| `cyberpunk` | Futuristic neon aesthetic | Sci-fi, urban, technology |

See all 90+ styles in `src/style_presets.py`

## 📊 API Parameters

### Core Parameters
- `prompt` - Image description (required)
- `api_key` - Your OpenAI API key (or use environment variable)

### Style & Enhancement
- `optimize_prompt` - Auto-enhance prompt (default: true)
- `optimization_model` - Model for optimization (default: gpt-4)
- `style_preset` - Apply artistic style (default: none)
- `additional_modifiers` - Extra style keywords
- `custom_instructions` - Special generation instructions

### Image Settings
- `size` - Dimensions: "1024x1024", "1536x1024", "1024x1536"
- `quality` - Quality level: "low", "medium", "high", "auto"
- `num_images` - Number to generate (1-4)
- `seed` - Reproducibility seed (-1 for random)

### Advanced Features
- `reference_images` - Base64 or file paths for reference
- `mask_image` - Mask for selective editing
- `input_fidelity` - Preserve input details: "low" or "high"
- `background` - Background type: "auto", "transparent", "opaque"
- `negative_prompt` - What to avoid in the image

## 💰 Cost Estimation

The tool includes automatic cost calculation based on OpenAI's pricing:

```python
# Calculate cost before generating
cost_info = generator.calculate_cost(
    size="1024x1024",
    quality="high",
    n=2
)
print(f"Estimated cost: {cost_info['total_cost']}")
```

Token usage by quality:
| Quality | 1024×1024 | 1024×1536 | 1536×1024 |
|---------|-----------|-----------|-----------|
| Low | 272 tokens | 408 tokens | 400 tokens |
| Medium | 1,056 tokens | 1,584 tokens | 1,568 tokens |
| High | 4,160 tokens | 6,240 tokens | 6,208 tokens |

## 🧪 Testing

```bash
# Run interactive CLI (includes test features)
python test_local.py

# Run unit tests
pytest tests/

# Test specific functionality
python -m pytest tests/test_prompt_optimizer.py
```

## 📁 Project Structure

```
better-gpt-image/
├── src/
│   ├── prompt_optimizer.py    # Prompt enhancement logic
│   ├── image_generator.py     # Image generation API
│   ├── image_processor.py     # Image processing utilities
│   ├── style_presets.py       # 90+ artistic styles
│   └── utils.py                # Helper functions
├── examples/
│   ├── python_example.py      # Python usage examples
│   └── nodejs_example.js      # Node.js usage examples
├── tests/
│   └── test_*.py               # Unit tests
├── test_local.py               # Interactive CLI
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## 🔒 Security & Privacy

- **API keys are never stored**: Used only during runtime
- **No external logging**: Your prompts and images remain private
- **Direct API calls**: No intermediary servers
- **Open source**: Full transparency in our code

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

MIT License - see LICENSE file for details

## 🙏 Acknowledgments

- OpenAI for GPT and DALL-E models
- The open-source community for inspiration and support

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/preangelleo/better-gpt-image/issues)
- **Discussions**: [GitHub Discussions](https://github.com/preangelleo/better-gpt-image/discussions)

---

Built with ❤️ for the AI art community