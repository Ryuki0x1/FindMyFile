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
    
    # Determine optimal batch size based on hardware
    if hardware["has_cuda"]:
        if hardware["gpu_vram_gb"] >= 8:
            batch_size = 32  # High-end GPU
        elif hardware["gpu_vram_gb"] >= 4:
            batch_size = 16  # Mid-range GPU
        else:
            batch_size = 8   # Low-end GPU
    else:
        # CPU only - use smaller batches
        if hardware["ram_gb"] >= 16:
            batch_size = 8
        else:
            batch_size = 4
    
    config = {
        "first_run_completed": True,
        "hardware_detected": hardware,
        "optimizations": {
            "batch_size": batch_size,
            "use_gpu": hardware["has_cuda"],
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
    print(f"   • Batch size: {config['optimizations']['batch_size']} (optimized for your hardware)")
    print(f"   • GPU acceleration: {'Enabled' if config['optimizations']['use_gpu'] else 'Disabled'}")
    
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
