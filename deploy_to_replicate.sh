#!/bin/bash

# Deployment script for Better GPT Image to Replicate

echo "🚀 Better GPT Image - Replicate Deployment Script"
echo "================================================"

# Check if REPLICATE_API_TOKEN is set
if [ -z "$REPLICATE_API_TOKEN" ]; then
    echo "❌ Error: REPLICATE_API_TOKEN environment variable is not set"
    echo ""
    echo "Please set your token:"
    echo "  export REPLICATE_API_TOKEN='your-token-here'"
    echo ""
    echo "Get your token at: https://replicate.com/account/api-tokens"
    exit 1
fi

echo "✅ Replicate API token found"

# Use the downloaded cog
COG_PATH="/tmp/cog"

# Check if cog exists
if [ ! -f "$COG_PATH" ]; then
    echo "📦 Downloading Cog..."
    curl -o $COG_PATH -L "https://github.com/replicate/cog/releases/latest/download/cog_$(uname -s)_$(uname -m)"
    chmod +x $COG_PATH
fi

echo "📋 Cog version:"
$COG_PATH --version

# Login to Replicate
echo ""
echo "🔐 Logging in to Replicate..."
$COG_PATH login --token $REPLICATE_API_TOKEN

# Build the model
echo ""
echo "🔨 Building the model..."
$COG_PATH build

# Push to Replicate
echo ""
echo "📤 Pushing to Replicate..."
echo "   Target: r8.im/preangelleo/better-gpt-image"
$COG_PATH push r8.im/preangelleo/better-gpt-image

echo ""
echo "✨ Deployment complete!"
echo "🌐 Your model will be available at:"
echo "   https://replicate.com/preangelleo/better-gpt-image"
echo ""
echo "📝 Note: Users will need to provide their own OpenAI API keys to use the model."