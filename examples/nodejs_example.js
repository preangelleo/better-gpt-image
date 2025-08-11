#!/usr/bin/env node
/**
 * Better GPT Image - Node.js Example
 * Complete example showing all parameters and usage patterns
 */

import Replicate from "replicate";

// Initialize Replicate client
const replicate = new Replicate({
  auth: process.env.REPLICATE_API_TOKEN,
});

// Check for required environment variables
if (!process.env.REPLICATE_API_TOKEN) {
  console.error("Please set REPLICATE_API_TOKEN environment variable");
  console.error("Get your token at: https://replicate.com/account/api-tokens");
  process.exit(1);
}

if (!process.env.OPENAI_API_KEY) {
  console.error("Please set OPENAI_API_KEY environment variable");
  console.error("Get your key at: https://platform.openai.com/api-keys");
  process.exit(1);
}

/**
 * Better GPT Image Generator Class
 */
class BetterGPTImage {
  constructor(openaiKey) {
    this.openaiKey = openaiKey;
    this.model = "preangelleo/better-gpt-image:latest";
  }

  /**
   * Generate images with all available parameters
   */
  async generate(options = {}) {
    // Default parameters - merge with user options
    const input = {
      // Required
      api_key: this.openaiKey,
      prompt: options.prompt || "",
      
      // Prompt optimization
      optimize_prompt: options.optimize_prompt !== undefined ? options.optimize_prompt : true,
      optimization_model: options.optimization_model || "gpt-5",
      
      // Style settings
      style_preset: options.style_preset || "none",
      
      // Image configuration
      size: options.size || "1024x1024",
      quality: options.quality || "high",
      num_images: options.num_images || 1,
      
      // Advanced features
      reference_images: options.reference_images || "",
      mask_image: options.mask_image || "",
      background: options.background || "auto",
      input_fidelity: options.input_fidelity || "low",
      
      // Conversation mode
      conversation_history: options.conversation_history || "[]",
      previous_response_id: options.previous_response_id || "",
      
      // Generation settings
      seed: options.seed || -1,
      negative_prompt: options.negative_prompt || "",
      additional_modifiers: options.additional_modifiers || "",
      custom_instructions: options.custom_instructions || ""
    };

    try {
      const output = await replicate.run(this.model, { input });
      return output;
    } catch (error) {
      console.error("Generation failed:", error);
      throw error;
    }
  }
}

// Example functions
async function basicExample() {
  console.log("\n🎨 Basic Example: Simple Generation");
  console.log("-".repeat(50));
  
  const generator = new BetterGPTImage(process.env.OPENAI_API_KEY);
  
  const result = await generator.generate({
    prompt: "A cozy mountain cabin in winter",
    style_preset: "photorealistic"
  });
  
  console.log(`Generated ${result.length} image(s)`);
  result.forEach((url, i) => {
    console.log(`Image ${i + 1}: ${url}`);
  });
  
  return result;
}

async function animeStyleExample() {
  console.log("\n🎌 Anime Style Example");
  console.log("-".repeat(50));
  
  const generator = new BetterGPTImage(process.env.OPENAI_API_KEY);
  
  const result = await generator.generate({
    prompt: "A young wizard studying ancient spells in a magical library",
    style_preset: "ghibli",
    size: "1536x1024",
    quality: "high",
    additional_modifiers: "studio quality, detailed background, soft lighting"
  });
  
  console.log(`Generated Ghibli-style image: ${result[0]}`);
  return result;
}

async function conceptArtExample() {
  console.log("\n🎮 Concept Art Example");
  console.log("-".repeat(50));
  
  const generator = new BetterGPTImage(process.env.OPENAI_API_KEY);
  
  const result = await generator.generate({
    prompt: "Futuristic city with flying vehicles and neon signs",
    style_preset: "cyberpunk",
    optimize_prompt: true,
    num_images: 2,
    quality: "high",
    custom_instructions: "Blade Runner aesthetic, rain-slicked streets, dense urban environment"
  });
  
  console.log(`Generated ${result.length} cyberpunk variations`);
  return result;
}

async function customStyleExample() {
  console.log("\n🎨 Custom Style Example");
  console.log("-".repeat(50));
  
  const generator = new BetterGPTImage(process.env.OPENAI_API_KEY);
  
  const result = await generator.generate({
    prompt: "Ancient tree of life with glowing fruits",
    style_preset: "custom",
    optimize_prompt: true,
    custom_instructions: "Ethereal fantasy art, bioluminescent, Avatar-inspired, mystical atmosphere",
    negative_prompt: "dark, scary, horror",
    additional_modifiers: "magical realism, soft glow, dreamy quality"
  });
  
  console.log(`Generated custom style image: ${result[0]}`);
  return result;
}

async function batchGenerationExample() {
  console.log("\n📦 Batch Generation Example");
  console.log("-".repeat(50));
  
  const generator = new BetterGPTImage(process.env.OPENAI_API_KEY);
  
  const subject = "A lighthouse on a stormy coast";
  const styles = ["photorealistic", "oil_painting", "watercolor", "3d_render"];
  
  const results = {};
  for (const style of styles) {
    console.log(`Generating ${style} version...`);
    const result = await generator.generate({
      prompt: subject,
      style_preset: style,
      optimize_prompt: true
    });
    results[style] = result[0];
    console.log(`  ✓ ${style}: ${result[0]}`);
  }
  
  return results;
}

// Quick one-liner examples
async function quickExamples() {
  console.log("\n⚡ Quick One-Liner Examples");
  console.log("-".repeat(50));
  
  // Minimal parameters
  const simple = await replicate.run(
    "preangelleo/better-gpt-image:latest",
    {
      input: {
        api_key: process.env.OPENAI_API_KEY,
        prompt: "A beautiful sunset"
      }
    }
  );
  console.log("Simple generation:", simple[0]);
  
  // With style
  const styled = await replicate.run(
    "preangelleo/better-gpt-image:latest",
    {
      input: {
        api_key: process.env.OPENAI_API_KEY,
        prompt: "A samurai warrior",
        style_preset: "anime"
      }
    }
  );
  console.log("Anime style:", styled[0]);
  
  // High quality landscape
  const landscape = await replicate.run(
    "preangelleo/better-gpt-image:latest",
    {
      input: {
        api_key: process.env.OPENAI_API_KEY,
        prompt: "Mountain valley with river",
        style_preset: "photorealistic",
        size: "1536x1024",
        quality: "high"
      }
    }
  );
  console.log("Landscape:", landscape[0]);
}

// Main execution
async function main() {
  console.log("\n" + "=".repeat(60));
  console.log("🚀 Better GPT Image - Node.js Examples");
  console.log("=".repeat(60));
  
  try {
    // Run all examples
    await basicExample();
    await animeStyleExample();
    await conceptArtExample();
    await customStyleExample();
    await batchGenerationExample();
    await quickExamples();
    
    console.log("\n" + "=".repeat(60));
    console.log("✅ All examples completed successfully!");
    console.log("=".repeat(60));
    
  } catch (error) {
    console.error("\n❌ Error:", error.message);
    console.error("\nTroubleshooting:");
    console.error("1. Check your API keys are valid");
    console.error("2. Ensure you have credits in both Replicate and OpenAI");
    console.error("3. Check the model at: https://replicate.com/preangelleo/better-gpt-image");
  }
}

// Run if called directly
if (import.meta.url === `file://${process.argv[1]}`) {
  main();
}

// Export for use as module
export { BetterGPTImage };
export default BetterGPTImage;