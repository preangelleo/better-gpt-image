#!/bin/bash

# Better GPT Image - cURL/REST API Examples
# Complete examples showing all parameters and usage patterns

# Set your API tokens
REPLICATE_API_TOKEN="your-replicate-api-token"
OPENAI_API_KEY="your-openai-api-key"

# Model endpoint
MODEL="preangelleo/better-gpt-image:latest"
API_URL="https://api.replicate.com/v1/predictions"

echo "======================================"
echo "Better GPT Image - cURL Examples"
echo "======================================"

# Function to make API call
make_request() {
    local input_json=$1
    local description=$2
    
    echo ""
    echo "📍 $description"
    echo "----------------------------------------"
    
    response=$(curl -s -X POST \
        -H "Authorization: Token $REPLICATE_API_TOKEN" \
        -H "Content-Type: application/json" \
        -d "$input_json" \
        "$API_URL")
    
    echo "$response" | jq '.'
    echo ""
}

# ========================================
# EXAMPLE 1: Basic Generation
# ========================================
echo ""
echo "🎨 Example 1: Basic Image Generation"
echo "========================================="

make_request '{
  "version": "latest",
  "input": {
    "api_key": "'$OPENAI_API_KEY'",
    "prompt": "A serene Japanese garden with koi pond",
    "style_preset": "photorealistic",
    "optimize_prompt": true
  }
}' "Basic generation with style preset"

# ========================================
# EXAMPLE 2: Complete Parameters
# ========================================
echo ""
echo "📋 Example 2: All Parameters (with defaults)"
echo "========================================="

cat << EOF
{
  "version": "latest",
  "input": {
    "api_key": "$OPENAI_API_KEY",           // Required - Your OpenAI API key
    "prompt": "",                            // Required - Image description
    
    // Prompt Optimization
    "optimize_prompt": true,                 // Auto-enhance prompt
    "optimization_model": "gpt-5",           // GPT model for optimization
    
    // Style Settings
    "style_preset": "none",                  // 90+ style options
    
    // Image Configuration
    "size": "1024x1024",                    // Image dimensions
    "quality": "high",                      // Generation quality
    "num_images": 1,                        // Number of images
    
    // Advanced Features
    "reference_images": "",                 // Reference image URLs
    "mask_image": "",                       // Mask for editing
    "background": "auto",                   // Background type
    "input_fidelity": "low",               // Input preservation
    
    // Conversation Mode
    "conversation_history": "[]",           // Previous exchanges
    "previous_response_id": "",            // Previous generation ID
    
    // Generation Settings
    "seed": -1,                            // Reproducibility seed
    "negative_prompt": "",                 // What to avoid
    "additional_modifiers": "",            // Extra modifiers
    "custom_instructions": ""              // Special instructions
  }
}
EOF

# ========================================
# EXAMPLE 3: Anime Style
# ========================================
echo ""
echo "🎌 Example 3: Anime/Ghibli Style"
echo "========================================="

make_request '{
  "version": "latest",
  "input": {
    "api_key": "'$OPENAI_API_KEY'",
    "prompt": "A flying castle in the clouds",
    "style_preset": "ghibli",
    "size": "1536x1024",
    "quality": "high",
    "optimize_prompt": true,
    "additional_modifiers": "studio quality, detailed, magical atmosphere"
  }
}' "Studio Ghibli style generation"

# ========================================
# EXAMPLE 4: Concept Art
# ========================================
echo ""
echo "🎮 Example 4: Game Concept Art"
echo "========================================="

make_request '{
  "version": "latest",
  "input": {
    "api_key": "'$OPENAI_API_KEY'",
    "prompt": "Alien marketplace on distant planet",
    "style_preset": "concept_art",
    "optimize_prompt": true,
    "num_images": 2,
    "quality": "high",
    "custom_instructions": "sci-fi, detailed environment, atmospheric"
  }
}' "Concept art with multiple variations"

# ========================================
# EXAMPLE 5: Custom Style
# ========================================
echo ""
echo "🎨 Example 5: Custom Style (No Preset)"
echo "========================================="

make_request '{
  "version": "latest",
  "input": {
    "api_key": "'$OPENAI_API_KEY'",
    "prompt": "Victorian steampunk laboratory",
    "style_preset": "custom",
    "optimize_prompt": true,
    "custom_instructions": "brass and copper machinery, vintage scientific equipment, warm lighting",
    "negative_prompt": "modern, plastic, neon",
    "additional_modifiers": "intricate details, atmospheric, moody lighting"
  }
}' "Custom style with specific instructions"

# ========================================
# EXAMPLE 6: Oil Painting Style
# ========================================
echo ""
echo "🖼️ Example 6: Traditional Art Style"
echo "========================================="

make_request '{
  "version": "latest",
  "input": {
    "api_key": "'$OPENAI_API_KEY'",
    "prompt": "Stormy seascape with lighthouse",
    "style_preset": "oil_painting",
    "optimize_prompt": true,
    "quality": "high",
    "additional_modifiers": "masterpiece, museum quality, dramatic brushstrokes"
  }
}' "Oil painting style"

# ========================================
# EXAMPLE 7: Batch Processing
# ========================================
echo ""
echo "📦 Example 7: Batch Generation Script"
echo "========================================="

echo "Script to generate multiple styles of the same subject:"
cat << 'BATCH_SCRIPT'
#!/bin/bash

SUBJECT="A majestic phoenix rising from flames"
STYLES=("photorealistic" "anime" "oil_painting" "3d_render" "watercolor")

for style in "${STYLES[@]}"; do
    echo "Generating $style version..."
    
    curl -s -X POST \
        -H "Authorization: Token $REPLICATE_API_TOKEN" \
        -H "Content-Type: application/json" \
        -d '{
          "version": "latest",
          "input": {
            "api_key": "'$OPENAI_API_KEY'",
            "prompt": "'$SUBJECT'",
            "style_preset": "'$style'",
            "optimize_prompt": true
          }
        }' \
        "$API_URL" | jq '.urls.get'
    
    sleep 2  # Rate limiting
done
BATCH_SCRIPT

# ========================================
# MONITORING PREDICTION
# ========================================
echo ""
echo "📊 Monitoring a Prediction"
echo "========================================="

cat << 'MONITOR_SCRIPT'
# Start a prediction and get the ID
PREDICTION_ID=$(curl -s -X POST \
    -H "Authorization: Token $REPLICATE_API_TOKEN" \
    -H "Content-Type: application/json" \
    -d '{...}' \
    "$API_URL" | jq -r '.id')

# Poll for completion
while true; do
    STATUS=$(curl -s \
        -H "Authorization: Token $REPLICATE_API_TOKEN" \
        "https://api.replicate.com/v1/predictions/$PREDICTION_ID" | jq -r '.status')
    
    if [ "$STATUS" = "succeeded" ]; then
        echo "✅ Generation complete!"
        break
    elif [ "$STATUS" = "failed" ]; then
        echo "❌ Generation failed"
        break
    else
        echo "⏳ Status: $STATUS"
        sleep 2
    fi
done
MONITOR_SCRIPT

# ========================================
# TIPS AND NOTES
# ========================================
echo ""
echo "💡 Tips and Notes"
echo "========================================="
echo "1. Replace REPLICATE_API_TOKEN and OPENAI_API_KEY with your actual keys"
echo "2. Install jq for JSON parsing: brew install jq (macOS) or apt-get install jq (Linux)"
echo "3. API endpoint: https://api.replicate.com/v1/predictions"
echo "4. Get prediction status: GET /v1/predictions/{prediction_id}"
echo "5. Cancel prediction: POST /v1/predictions/{prediction_id}/cancel"
echo ""
echo "📚 Available Style Presets:"
echo "   photorealistic, cinematic, anime, ghibli, oil_painting, watercolor,"
echo "   digital_art, 3d_render, 3d_cartoon, pixar, disney, concept_art,"
echo "   pencil_sketch, cyberpunk, steampunk, vaporwave, and 80+ more!"
echo ""
echo "💰 Pricing:"
echo "   - Replicate: $0.01 per generation"
echo "   - OpenAI: Your API costs (typically $0.04-0.08 per image)"
echo ""
echo "🔗 Resources:"
echo "   - Model: https://replicate.com/preangelleo/better-gpt-image"
echo "   - GitHub: https://github.com/preangelleo/better-gpt-image"
echo "   - Replicate API Docs: https://replicate.com/docs/api"