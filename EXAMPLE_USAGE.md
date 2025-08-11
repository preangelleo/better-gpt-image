# Better GPT Image - Example Usage

This guide shows how to use Better GPT Image via the Replicate API with all available parameters.

## 🚀 Quick Start

### Python Example

```python
import replicate

# Run the model with minimal parameters
output = replicate.run(
    "preangelleo/better-gpt-image:latest",
    input={
        "api_key": "your-openai-api-key",  # Required - will be masked on UI
        "prompt": "A magical forest at sunset"
    }
)

print(output)
```

## 📋 Complete Parameter Reference

### All Parameters with Default Values

```python
import replicate

output = replicate.run(
    "preangelleo/better-gpt-image:latest",
    input={
        # ===== REQUIRED PARAMETERS =====
        "api_key": "your-openai-api-key",          # Your OpenAI API key (required)
        
        # ===== BASIC PARAMETERS =====
        "prompt": "",                               # Image description (required)
        "optimize_prompt": True,                    # Auto-enhance prompt with GPT
        "optimization_model": "gpt-5",              # Model for optimization: gpt-4.1, gpt-4, gpt-5
        
        # ===== STYLE PARAMETERS =====
        "style_preset": "none",                     # Choose from 90+ styles or "custom"
        # Available styles: photorealistic, cinematic, anime, ghibli, oil_painting,
        # watercolor, digital_art, 3d_render, 3d_cartoon, pixar, disney, dreamworks,
        # concept_art, pencil_sketch, ink_drawing, comic_book, manga, cyberpunk,
        # steampunk, vaporwave, synthwave, minimalist, pop_art, and 80+ more
        
        # ===== IMAGE SETTINGS =====
        "size": "1024x1024",                       # Image size: 1024x1024, 1536x1024, 1024x1536
        "quality": "high",                          # Quality: low, medium, high, auto
        "num_images": 1,                            # Number of images (1-4)
        
        # ===== ADVANCED FEATURES =====
        "reference_images": "",                     # URLs of reference images (comma-separated)
        "mask_image": "",                           # URL of mask for editing
        "background": "auto",                       # Background: auto, transparent, white, black
        "input_fidelity": "low",                    # Fidelity: low, medium, high
        
        # ===== CONVERSATION MODE =====
        "conversation_history": "[]",               # JSON array of previous exchanges
        "previous_response_id": "",                 # ID from previous generation
        
        # ===== GENERATION SETTINGS =====
        "seed": -1,                                 # Seed for reproducibility (-1 for random)
        
        # ===== OPTIONAL NEGATIVE PROMPT =====
        "negative_prompt": "",                      # What to avoid in the image
        
        # ===== CUSTOM PROMPT ADDITIONS =====
        "additional_modifiers": "",                 # Extra quality modifiers
        "custom_instructions": ""                   # Special instructions
    }
)
```

## 💡 Common Use Cases

### 1. Simple Image Generation
```python
output = replicate.run(
    "preangelleo/better-gpt-image:latest",
    input={
        "api_key": "your-api-key",
        "prompt": "A cozy coffee shop on a rainy day",
        "style_preset": "photorealistic"
    }
)
```

### 2. Anime Style Art
```python
output = replicate.run(
    "preangelleo/better-gpt-image:latest",
    input={
        "api_key": "your-api-key",
        "prompt": "A warrior princess in a magical kingdom",
        "style_preset": "ghibli",
        "size": "1536x1024",
        "quality": "high"
    }
)
```

### 3. Concept Art for Games
```python
output = replicate.run(
    "preangelleo/better-gpt-image:latest",
    input={
        "api_key": "your-api-key",
        "prompt": "Futuristic space station interior",
        "style_preset": "concept_art",
        "optimize_prompt": True,
        "num_images": 4
    }
)
```

### 4. Oil Painting Style
```python
output = replicate.run(
    "preangelleo/better-gpt-image:latest",
    input={
        "api_key": "your-api-key",
        "prompt": "Mountain landscape with a lake",
        "style_preset": "oil_painting",
        "additional_modifiers": "masterpiece, museum quality"
    }
)
```

### 5. Custom Style with Manual Control
```python
output = replicate.run(
    "preangelleo/better-gpt-image:latest",
    input={
        "api_key": "your-api-key",
        "prompt": "A dragon guarding treasure",
        "style_preset": "custom",
        "optimize_prompt": False,  # Don't auto-enhance
        "custom_instructions": "In the style of classic fantasy book covers",
        "negative_prompt": "modern, cartoon, anime"
    }
)
```

## 🌐 REST API Example (curl)

```bash
curl -X POST \
  -H "Authorization: Token YOUR_REPLICATE_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "version": "latest",
    "input": {
      "api_key": "your-openai-api-key",
      "prompt": "A beautiful sunset over mountains",
      "style_preset": "photorealistic",
      "optimize_prompt": true,
      "size": "1536x1024",
      "quality": "high"
    }
  }' \
  https://api.replicate.com/v1/predictions
```

## 🟨 JavaScript/Node.js Example

```javascript
import Replicate from "replicate";

const replicate = new Replicate({
  auth: process.env.REPLICATE_API_TOKEN,
});

const output = await replicate.run(
  "preangelleo/better-gpt-image:latest",
  {
    input: {
      api_key: process.env.OPENAI_API_KEY,
      prompt: "A cyberpunk city at night",
      style_preset: "cyberpunk",
      optimize_prompt: true,
      size: "1536x1024",
      quality: "high",
      num_images: 2
    }
  }
);

console.log(output);
```

## 🔧 Environment Setup

### Python
```bash
pip install replicate
export REPLICATE_API_TOKEN="your-replicate-token"
```

### Node.js
```bash
npm install replicate
export REPLICATE_API_TOKEN="your-replicate-token"
```

## 📝 Style Preset Options

Here are all available style presets:

**Realistic Styles:**
- `photorealistic` - Ultra-realistic photography
- `cinematic` - Movie-quality dramatic scenes
- `portrait` - Professional portrait photography

**Artistic Styles:**
- `oil_painting` - Classic oil painting
- `watercolor` - Soft watercolor art
- `pencil_sketch` - Detailed pencil drawings
- `ink_drawing` - Pen and ink illustrations
- `charcoal_drawing` - Charcoal sketches
- `pastel_art` - Soft pastel artwork

**Animation Styles:**
- `anime` - Japanese anime style
- `ghibli` - Studio Ghibli style
- `manga` - Black and white manga
- `pixar` - Pixar 3D animation
- `disney` - Disney animation style
- `dreamworks` - DreamWorks animation

**Digital Art Styles:**
- `digital_art` - Modern digital painting
- `concept_art` - Professional concept art
- `3d_render` - Photorealistic 3D
- `3d_cartoon` - Stylized 3D animation
- `low_poly` - Low polygon 3D art
- `pixel_art` - Retro pixel art

**Genre Styles:**
- `cyberpunk` - Neon-lit futuristic
- `steampunk` - Victorian mechanical
- `vaporwave` - 80s/90s aesthetic
- `synthwave` - Retro-futuristic neon
- `gothic` - Dark gothic style
- `fantasy` - High fantasy art
- `sci_fi` - Science fiction

**Art Movements:**
- `impressionist` - Impressionism
- `expressionist` - Expressionism
- `surrealist` - Surrealism
- `pop_art` - Pop art style
- `art_nouveau` - Art Nouveau
- `art_deco` - Art Deco
- `minimalist` - Minimalism
- `abstract` - Abstract art

And 50+ more styles available!

## 🔑 API Keys

- **OpenAI API Key**: Required for image generation. Get it at https://platform.openai.com/api-keys
- **Replicate API Token**: Required for API access. Get it at https://replicate.com/account/api-tokens

## 💰 Pricing

- **Replicate**: $0.01 per generation
- **OpenAI**: Based on your OpenAI usage (typically $0.04-0.08 per image)

## 🤝 Support

- **GitHub**: https://github.com/preangelleo/better-gpt-image
- **Issues**: https://github.com/preangelleo/better-gpt-image/issues
- **Replicate**: https://replicate.com/preangelleo/better-gpt-image