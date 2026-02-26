# AI Model Downloads

This document explains how AI models are downloaded and cached in FindMyPic.

## Overview

**FindMyPic does NOT ship with pre-downloaded AI models.** All models are downloaded automatically on first use from their respective sources. This keeps the repository small and ensures you always get the latest model versions.

## Model Download Process

### Automatic Download on First Run

All AI models are downloaded automatically when you first use a feature that requires them:

1. **CLIP Model** (Image & Text Embeddings)
   - Downloaded on first search or indexing
   - Source: HuggingFace Hub
   - Size: 300-600MB depending on hardware
   - Default: `openai/clip-vit-base-patch32` (CPU/Low VRAM)
   - High-end GPU: `openai/clip-vit-large-patch14` (8GB+ VRAM)

2. **FaceNet Model** (Face Detection & Recognition)
   - Downloaded on first face search
   - Source: facenet-pytorch package
   - Size: ~100MB
   - Model: InceptionResnetV1 pretrained on VGGFace2

3. **EasyOCR Models** (Text Extraction)
   - Downloaded on first OCR operation
   - Source: EasyOCR package
   - Size: ~50MB (English)
   - Additional languages can be configured

4. **Text Embedder** (Document Search)
   - Downloaded on first document indexing
   - Source: HuggingFace Hub
   - Size: ~90MB
   - Model: `sentence-transformers/all-MiniLM-L6-v2`

## Cache Locations

Models are cached locally to avoid re-downloading:

### Windows
- HuggingFace models: `C:\Users\<username>\.cache\huggingface\hub\`
- PyTorch models: `C:\Users\<username>\.cache\torch\`
- EasyOCR models: `C:\Users\<username>\.EasyOCR\`

### macOS/Linux
- HuggingFace models: `~/.cache/huggingface/hub/`
- PyTorch models: `~/.cache/torch/`
- EasyOCR models: `~/.EasyOCR/`

## Total Download Size

On first complete use (all features):
- **Minimum (CPU)**: ~540MB
- **Maximum (High-end GPU)**: ~850MB

Downloads only happen once. Subsequent runs use cached models.

## Environment Variables

You can customize cache locations using environment variables:

```bash
# HuggingFace cache
export TRANSFORMERS_CACHE=/path/to/cache
export HF_HOME=/path/to/cache

# PyTorch cache
export TORCH_HOME=/path/to/cache

# EasyOCR cache (set in code)
```

## Offline Usage

After models are downloaded once, FindMyPic works completely offline. No internet connection is required for searching or indexing.

## Model Selection

The application automatically selects optimal models based on your hardware during first run:

- **8GB+ VRAM GPU**: Large models for best accuracy
- **4-8GB VRAM GPU**: Base models for balanced performance
- **<4GB VRAM or CPU**: Smaller models optimized for speed

You can view your detected configuration in `data/config.json` after first run.

## Manual Model Pre-download

If you want to pre-download models before first use:

```python
# Run this Python script in the backend/.venv environment
from transformers import CLIPModel, CLIPProcessor, AutoTokenizer, AutoModel
from facenet_pytorch import MTCNN, InceptionResnetV1
import easyocr

# Download CLIP
CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

# Download text embedder
AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")

# Download FaceNet
InceptionResnetV1(pretrained="vggface2")

# Download EasyOCR
easyocr.Reader(["en"])

print("All models downloaded successfully!")
```

## Clearing Cache

To free up disk space or force re-download:

### Windows
```powershell
Remove-Item -Recurse -Force $env:USERPROFILE\.cache\huggingface
Remove-Item -Recurse -Force $env:USERPROFILE\.cache\torch
Remove-Item -Recurse -Force $env:USERPROFILE\.EasyOCR
```

### macOS/Linux
```bash
rm -rf ~/.cache/huggingface
rm -rf ~/.cache/torch
rm -rf ~/.EasyOCR
```

## Troubleshooting

### Download Fails
- Check internet connection
- Verify firewall/proxy settings
- Some corporate networks block HuggingFace - try VPN

### Disk Space Issues
- Ensure at least 2GB free space for model downloads
- Models are cached in user home directory by default

### Slow Downloads
- HuggingFace Hub can be slow in some regions
- Downloads are one-time - be patient on first run
- Consider using a mirror or VPN

## Security Note

All models are downloaded from official sources:
- **HuggingFace Hub**: Official transformers repository
- **facenet-pytorch**: PyPI package with checksums
- **EasyOCR**: PyPI package with checksums

Models are verified by the respective packages before use.
