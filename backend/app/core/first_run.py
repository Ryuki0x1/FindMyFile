"""
First-run configuration wizard.
Detects hardware and creates personalized config on first launch.
"""

import os
import json
from pathlib import Path
from app.core.config import get_settings


def is_first_run() -> bool:
    """Check if this is the first time the app is running."""
    settings = get_settings()
    config_path = Path(settings.data_dir) / "config.json"
    
    if not config_path.exists():
        return True
    
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
            return config.get("first_run_completed") != True
    except:
        return True


def detect_hardware() -> dict:
    """Detect GPU and system specs."""
    import psutil
    
    hardware = {
        "has_cuda": False,
        "gpu_name": "CPU Only",
        "gpu_vram_gb": 0,
        "ram_gb": round(psutil.virtual_memory().total / (1024**3), 1),
        "cpu_count": psutil.cpu_count(),
    }
    
    try:
        import torch
        if torch.cuda.is_available():
            hardware["has_cuda"] = True
            hardware["gpu_name"] = torch.cuda.get_device_name(0)
            hardware["gpu_vram_gb"] = round(
                torch.cuda.get_device_properties(0).total_memory / (1024**3), 1
            )
    except:
        pass
    
    return hardware


def create_personalized_config(hardware: dict) -> dict:
    """Create config optimized for user's hardware."""
    settings = get_settings()
    
    # Determine optimal model and batch size based on hardware
    if hardware["has_cuda"]:
        vram = hardware["gpu_vram_gb"]
        
        if vram >= 8:
            # High-end GPU: Use large models
            clip_model = "openai/clip-vit-large-patch14"  # 768-dim, ~600MB
            batch_size = 32
            model_tier = "High-End (8GB+ VRAM)"
        elif vram >= 4:
            # Mid-range GPU: Use base models
            clip_model = "openai/clip-vit-base-patch32"  # 512-dim, ~350MB
            batch_size = 16
            model_tier = "Mid-Range (4-8GB VRAM)"
        else:
            # Low VRAM GPU: Use small models
            clip_model = "openai/clip-vit-base-patch16"  # 512-dim, ~300MB
            batch_size = 8
            model_tier = "Entry-Level (<4GB VRAM)"
    else:
        # CPU only - use smallest models
        clip_model = "openai/clip-vit-base-patch32"  # 512-dim, lightest
        if hardware["ram_gb"] >= 16:
            batch_size = 8
        else:
            batch_size = 4
        model_tier = "CPU Only"
    
    config = {
        "first_run_completed": True,
        "hardware_detected": hardware,
        "optimizations": {
            "batch_size": batch_size,
            "use_gpu": hardware["has_cuda"],
            "clip_model": clip_model,
            "model_tier": model_tier,
        },
        "indexed_folders": [],
        "excluded_folders": settings.excluded_folders,
        "setup_date": str(Path(settings.data_dir).stat().st_mtime),
    }
    
    # Save config
    config_path = Path(settings.data_dir) / "config.json"
    config_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)
    
    return config


def run_first_time_setup() -> dict:
    """Run first-time setup wizard."""
    print("\n" + "="*70)
    print("🎉 Welcome to FindMyPic!")
    print("="*70)
    print("\nDetecting your hardware to optimize performance...\n")
    
    hardware = detect_hardware()
    
    print(f"✅ Detected Hardware:")
    print(f"   • CPU: {hardware['cpu_count']} cores")
    print(f"   • RAM: {hardware['ram_gb']} GB")
    print(f"   • GPU: {hardware['gpu_name']}", end="")
    
    if hardware["has_cuda"]:
        print(f" ({hardware['gpu_vram_gb']} GB VRAM)")
        print(f"\n🚀 NVIDIA GPU detected! Using GPU acceleration for 10x faster indexing.")
    else:
        print("\n💡 No NVIDIA GPU detected. Using CPU (still fast for <10,000 photos).")
    
    print("\nCreating personalized configuration...")
    config = create_personalized_config(hardware)
    
    print(f"\n✅ Configuration created:")
    print(f"   • Model tier: {config['optimizations']['model_tier']}")
    print(f"   • CLIP model: {config['optimizations']['clip_model']}")
    print(f"   • Batch size: {config['optimizations']['batch_size']}")
    print(f"   • GPU acceleration: {'Enabled' if config['optimizations']['use_gpu'] else 'Disabled'}")
    
    # Show model download size estimate
    model_name = config['optimizations']['clip_model']
    if 'large' in model_name:
        model_size = "~600MB"
    elif 'base' in model_name:
        model_size = "~350MB"
    else:
        model_size = "~300MB"
    
    print(f"\n📦 Models to download on first search:")
    print(f"   • CLIP ({model_name.split('/')[-1]}): {model_size}")
    print(f"   • FaceNet (if using face search): ~100MB")
    print(f"   • EasyOCR (if images have text): ~50MB")
    
    print("\n" + "="*70)
    print("🎬 Setup complete! Starting FindMyPic...")
    print("="*70 + "\n")
    
    return config


def get_or_create_config() -> dict:
    """Get existing config or create one on first run."""
    if is_first_run():
        return run_first_time_setup()
    else:
        settings = get_settings()
        config_path = Path(settings.data_dir) / "config.json"
        with open(config_path, 'r') as f:
            return json.load(f)
