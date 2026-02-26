"""
GPU detection and model tier recommendation.
Detects NVIDIA/AMD GPUs, VRAM, and recommends the optimal model tier.
"""

import platform
import subprocess
import re
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class GPUInfo:
    name: str = "None"
    vram_mb: int = 0
    driver: str = "Unknown"
    cuda_available: bool = False


@dataclass
class TierRecommendation:
    tier: int  # 1-4
    tier_name: str
    description: str
    clip_model: str
    clip_size_mb: int
    captioner_model: str
    captioner_size_mb: int
    text_embed_model: str
    text_embed_size_mb: int
    total_size_mb: int
    estimated_speed: str  # e.g., "3-5 files/sec"


# Pre-defined tier configurations
TIERS: dict[int, TierRecommendation] = {
    1: TierRecommendation(
        tier=1,
        tier_name="CPU Mode",
        description="No GPU / Integrated Graphics — reliable but slower",
        clip_model="openai/clip-vit-base-patch32",
        clip_size_mb=90,
        captioner_model="moondream2:1.8b-q4",
        captioner_size_mb=1100,
        text_embed_model="sentence-transformers/all-MiniLM-L6-v2",
        text_embed_size_mb=90,
        total_size_mb=1300,
        estimated_speed="3-5 images/sec",
    ),
    2: TierRecommendation(
        tier=2,
        tier_name="Entry GPU",
        description="4-6 GB VRAM — good speed with GPU acceleration",
        clip_model="openai/clip-vit-base-patch16",
        clip_size_mb=350,
        captioner_model="moondream2:1.8b-q4",
        captioner_size_mb=1100,
        text_embed_model="sentence-transformers/all-MiniLM-L6-v2",
        text_embed_size_mb=90,
        total_size_mb=1600,
        estimated_speed="20-40 images/sec",
    ),
    3: TierRecommendation(
        tier=3,
        tier_name="Mid-Range GPU",
        description="8-12 GB VRAM — high accuracy, fast indexing",
        clip_model="openai/clip-vit-large-patch14",
        clip_size_mb=1700,
        captioner_model="llava:7b-v1.6-q4",
        captioner_size_mb=4100,
        text_embed_model="nomic-ai/nomic-embed-text-v1.5",
        text_embed_size_mb=270,
        total_size_mb=6100,
        estimated_speed="50-80 images/sec",
    ),
    4: TierRecommendation(
        tier=4,
        tier_name="High-End GPU",
        description="16+ GB VRAM — maximum accuracy and speed",
        clip_model="openai/clip-vit-large-patch14",
        clip_size_mb=1700,
        captioner_model="llava:13b-v1.6-q4",
        captioner_size_mb=7400,
        text_embed_model="nomic-ai/nomic-embed-text-v1.5",
        text_embed_size_mb=270,
        total_size_mb=10000,
        estimated_speed="100+ images/sec",
    ),
}


def detect_gpu() -> GPUInfo:
    """Detect the primary GPU on the system."""
    gpu = GPUInfo()

    # Try NVIDIA first (nvidia-smi)
    try:
        result = subprocess.run(
            ["nvidia-smi", "--query-gpu=name,memory.total,driver_version",
             "--format=csv,noheader,nounits"],
            capture_output=True, text=True, timeout=10,
        )
        if result.returncode == 0 and result.stdout.strip():
            parts = result.stdout.strip().split(",")
            if len(parts) >= 3:
                gpu.name = parts[0].strip()
                gpu.vram_mb = int(float(parts[1].strip()))
                gpu.driver = parts[2].strip()
                gpu.cuda_available = True
                return gpu
    except (FileNotFoundError, subprocess.TimeoutExpired, ValueError):
        pass

    # Try PyTorch CUDA detection
    try:
        import torch
        if torch.cuda.is_available():
            props = torch.cuda.get_device_properties(0)
            gpu.name = props.name
            gpu.vram_mb = props.total_mem // (1024 * 1024)
            gpu.cuda_available = True
            return gpu
    except ImportError:
        pass

    # Try Windows WMIC for any GPU info
    if platform.system() == "Windows":
        try:
            result = subprocess.run(
                ["wmic", "path", "win32_VideoController", "get",
                 "Name,AdapterRAM", "/format:csv"],
                capture_output=True, text=True, timeout=10,
            )
            if result.returncode == 0:
                lines = [l.strip() for l in result.stdout.strip().split("\n") if l.strip()]
                for line in lines[1:]:  # Skip header
                    parts = line.split(",")
                    if len(parts) >= 3:
                        adapter_ram = parts[1].strip()
                        name = parts[2].strip()
                        if adapter_ram and adapter_ram.isdigit():
                            vram = int(adapter_ram) // (1024 * 1024)
                            if vram > gpu.vram_mb:
                                gpu.name = name
                                gpu.vram_mb = vram
        except (FileNotFoundError, subprocess.TimeoutExpired, ValueError):
            pass

    return gpu


def recommend_tier(gpu: Optional[GPUInfo] = None) -> TierRecommendation:
    """Recommend a model tier based on detected GPU."""
    if gpu is None:
        gpu = detect_gpu()

    if not gpu.cuda_available or gpu.vram_mb < 4000:
        return TIERS[1]
    elif gpu.vram_mb < 7000:
        return TIERS[2]
    elif gpu.vram_mb < 15000:
        return TIERS[3]
    else:
        return TIERS[4]


def get_system_info() -> dict:
    """Get complete system info for display in the UI."""
    import psutil

    gpu = detect_gpu()
    tier = recommend_tier(gpu)

    return {
        "gpu": {
            "name": gpu.name,
            "vram_mb": gpu.vram_mb,
            "vram_gb": round(gpu.vram_mb / 1024, 1),
            "cuda_available": gpu.cuda_available,
            "driver": gpu.driver,
        },
        "system": {
            "ram_gb": round(psutil.virtual_memory().total / (1024 ** 3), 1),
            "cpu_count": psutil.cpu_count(logical=True),
            "os": platform.system(),
            "os_version": platform.version(),
        },
        "recommendation": {
            "tier": tier.tier,
            "tier_name": tier.tier_name,
            "description": tier.description,
            "clip_model": tier.clip_model,
            "captioner_model": tier.captioner_model,
            "text_embed_model": tier.text_embed_model,
            "total_download_mb": tier.total_size_mb,
            "estimated_speed": tier.estimated_speed,
        },
    }
