#!/usr/bin/env python3
"""
Environment Sanity & Diagnostic Verification Script
Author: Penumala Harshitha (M.Tech, IIIT Allahabad)
Project: Benchmarking Factual Accuracy of LLMs Across Scientific Domains

Purpose:
Checks local execution environment, verifies directory structure, tests
deterministic random seed controls, and audits available packages.
"""

import sys
import os
import platform
import json
import random

def run_diagnostics():
    print("=" * 70)
    print("ENVIRONMENT SANITY & REPRODUCIBILITY DIAGNOSTIC TEST")
    print("=" * 70)
    
    # 1. System & Architecture
    py_version = sys.version.split()[0]
    os_name = platform.system()
    os_release = platform.release()
    arch = platform.machine()
    print(f"[*] Python Version:      {py_version} ({'64-bit' if sys.maxsize > 2**32 else '32-bit'})")
    print(f"[*] Operating System:    {os_name} {os_release} ({arch})")
    print(f"[*] Current Directory:   {os.path.abspath(os.getcwd())}")
    
    # 2. Hardware / GPU Check
    gpu_available = False
    gpu_name = "None detected (Running on Host CPU)"
    try:
        import torch
        if torch.cuda.is_available():
            gpu_available = True
            gpu_name = f"CUDA GPU: {torch.cuda.get_device_name(0)} (Count: {torch.cuda.device_count()})"
        else:
            gpu_name = "PyTorch installed, but CUDA is unavailable (CPU mode)"
    except ImportError:
        gpu_name = "PyTorch not installed locally (CPU baseline / Colab pairing mode)"
    print(f"[*] Hardware Compute:    {gpu_name}")
    
    # 3. Directory Structure Audit
    required_dirs = ['configs', 'data', 'notebooks', 'src', 'scripts', 'results', 'paper']
    missing_dirs = [d for d in required_dirs if not os.path.isdir(d)]
    if not missing_dirs:
        print("[+] Repository Tree:     All 7 required directories verified present.")
    else:
        print(f"[-] Repository Tree:     Missing directories: {missing_dirs}")
        
    # 4. Deterministic Random Seed Test
    random.seed(42)
    sample_seq = [round(random.random(), 4) for _ in range(3)]
    expected_seq = [0.6394, 0.025, 0.275]  # Standard Python 3.x Mersenne Twister sequence for seed 42
    seed_ok = (sample_seq == expected_seq)
    if seed_ok:
        print(f"[+] Random Seed Control: Verified deterministic (seed 42 -> {sample_seq})")
    else:
        print(f"[!] Random Seed Control: Deviation detected: {sample_seq} vs expected {expected_seq}")
        
    # 5. Core Package Availability Audit
    packages_to_check = ['numpy', 'pandas', 'sklearn', 'rank_bm25', 'tqdm', 'tabulate', 'transformers']
    status_dict = {}
    for pkg in packages_to_check:
        try:
            mod = __import__(pkg)
            version = getattr(mod, '__version__', 'Installed')
            status_dict[pkg] = f"Installed (v{version})"
        except ImportError:
            status_dict[pkg] = "Not installed (Run: python -m pip install -r requirements.txt)"
            
    print("\n--- Package Installation Audit ---")
    for pkg, status in status_dict.items():
        symbol = "[+]" if "Installed" in status else "[-]"
        print(f"  {symbol} {pkg:15s}: {status}")
        
    # Summary JSON output
    diagnostic_report = {
        "status": "PASSED" if not missing_dirs and seed_ok else "WARNING",
        "python_version": py_version,
        "platform": f"{os_name}-{arch}",
        "gpu_available": gpu_available,
        "directories_verified": len(missing_dirs) == 0,
        "seed_control_verified": seed_ok,
        "installed_packages": {k: v for k, v in status_dict.items() if "Installed" in v}
    }
    
    print("=" * 70)
    print(f"DIAGNOSTIC STATUS: {diagnostic_report['status']}")
    print("=" * 70)
    return diagnostic_report

if __name__ == "__main__":
    report = run_diagnostics()
    # Save diagnostic log to results
    os.makedirs("results", exist_ok=True)
    with open("results/env_diagnostic_log.json", "w") as f:
        json.dump(report, f, indent=2)
    print("[*] Diagnostic report logged to results/env_diagnostic_log.json")
