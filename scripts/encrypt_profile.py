#!/usr/bin/env python3
"""
Encrypt Chrome profile for GitHub Secrets storage
Run this locally to prepare your profile for GitHub
"""
import os
import sys
import base64
import tarfile
import tempfile
from pathlib import Path

def compress_and_encode_profile(profile_path):
    """Compress Chrome profile and encode as base64"""
    
    if not os.path.exists(profile_path):
        print(f"❌ Profile not found at: {profile_path}")
        return None
    
    print(f"📦 Compressing Chrome profile...")
    print(f"   Source: {profile_path}")
    
    # Create temporary tar file
    with tempfile.NamedTemporaryFile(suffix='.tar.gz', delete=False) as tmp_file:
        tmp_path = tmp_file.name
    
    try:
        # Compress profile directory
        with tarfile.open(tmp_path, "w:gz") as tar:
            tar.add(profile_path, arcname=os.path.basename(profile_path))
        
        # Read and encode
        with open(tmp_path, 'rb') as f:
            compressed_data = f.read()
        
        encoded_data = base64.b64encode(compressed_data).decode('utf-8')
        
        # Get size info
        original_size = sum(
            os.path.getsize(os.path.join(dirpath, filename))
            for dirpath, _, filenames in os.walk(profile_path)
            for filename in filenames
        )
        compressed_size = len(compressed_data)
        encoded_size = len(encoded_data)
        
        print(f"✅ Compression complete!")
        print(f"   Original size: {original_size / 1024 / 1024:.2f} MB")
        print(f"   Compressed size: {compressed_size / 1024 / 1024:.2f} MB")
        print(f"   Encoded size: {encoded_size / 1024 / 1024:.2f} MB")
        print(f"   Compression ratio: {(1 - compressed_size/original_size)*100:.1f}%")
        
        # Cleanup
        os.unlink(tmp_path)
        
        return encoded_data
        
    except Exception as e:
        print(f"❌ Error: {e}")
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)
        return None


def main():
    print("=" * 60)
    print("🔐 Chrome Profile Encryption for GitHub Secrets")
    print("=" * 60)
    
    # Use the same profile path from config
    profile_path = os.path.join(os.path.expanduser("~"), ".gsc_chrome_profile")
    
    if not os.path.exists(profile_path):
        print(f"\n❌ Chrome profile not found!")
        print(f"   Expected location: {profile_path}")
        print(f"\n💡 Run first_time_gsc_login.py first to create the profile")
        sys.exit(1)
    
    print(f"\n📁 Profile location: {profile_path}")
    
    # Encrypt and encode
    encoded_profile = compress_and_encode_profile(profile_path)
    
    if not encoded_profile:
        sys.exit(1)
    
    # Save to file
    output_file = "chrome_profile_encoded.txt"
    with open(output_file, 'w') as f:
        f.write(encoded_profile)
    
    print(f"\n💾 Encoded profile saved to: {output_file}")
    print(f"\n" + "=" * 60)
    print("📋 NEXT STEPS:")
    print("=" * 60)
    print("1. Copy the contents of chrome_profile_encoded.txt")
    print("2. Go to GitHub → Settings → Secrets → Actions")
    print("3. Create new secret: GSC_CHROME_PROFILE")
    print("4. Paste the encoded profile as the value")
    print("5. Delete chrome_profile_encoded.txt (contains sensitive data)")
    print("=" * 60)
    print("\n⚠️  IMPORTANT: Delete chrome_profile_encoded.txt after uploading!")
    print("   This file contains your authentication credentials")
    print("=" * 60)


if __name__ == "__main__":
    main()
