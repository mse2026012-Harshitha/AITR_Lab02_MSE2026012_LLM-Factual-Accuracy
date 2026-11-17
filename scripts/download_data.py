#!/usr/bin/env python3
"""
Official SciFact Data Downloader and Extractor
Author: Penumala Harshitha (M.Tech, IIIT Allahabad)
Source: Allen Institute for AI (Wadden et al., 2020)
URL: https://scifact.s3-us-west-2.amazonaws.com/release/latest/data.tar.gz
"""

import os
import sys
import tarfile
import urllib.request
import shutil

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
TAR_URL = "https://scifact.s3-us-west-2.amazonaws.com/release/latest/data.tar.gz"

def download_and_extract():
    os.makedirs(DATA_DIR, exist_ok=True)
    tar_path = os.path.join(DATA_DIR, "data.tar.gz")
    
    print("=" * 60)
    print("SCIFACT OFFICIAL ARCHIVE ACQUISITION")
    print("=" * 60)
    print(f"[*] Downloading {TAR_URL}...")
    
    req = urllib.request.Request(TAR_URL, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as response, open(tar_path, "wb") as out_file:
        shutil.copyfileobj(response, out_file)
        
    print(f"[+] Download complete: {tar_path} ({os.path.getsize(tar_path):,} bytes)")
    
    print("[*] Extracting files into data directory...")
    with tarfile.open(tar_path, "r:gz") as tar:
        # Inspect members
        members = tar.getmembers()
        print(f"[*] Archive contains {len(members)} entries:")
        for m in members:
            if m.isfile():
                print(f"    - {m.name} ({m.size:,} bytes)")
        tar.extractall(path=DATA_DIR)
        
    # Clean up archive tar.gz
    if os.path.exists(tar_path):
        os.remove(tar_path)
        
    print("=" * 60)
    print("[+] SciFact dataset extracted successfully.")
    print("=" * 60)

if __name__ == "__main__":
    download_and_extract()
