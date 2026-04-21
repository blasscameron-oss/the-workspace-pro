#!/usr/bin/env python3
import requests
import os
import sys

def upload_to_fileio(filepath):
    """Upload file to file.io and return download link"""
    print(f"Uploading {filepath} to file.io...")
    
    with open(filepath, 'rb') as f:
        files = {'file': (os.path.basename(filepath), f)}
        
        try:
            # Upload with 1-week expiration
            response = requests.post(
                'https://file.io',
                files=files,
                params={'expires': '1w'}
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    print(f"✅ Upload successful!")
                    print(f"📥 Download link: {data['link']}")
                    print(f"🗑️  File will expire in 1 week")
                    print(f"🔑 Key: {data.get('key', 'N/A')}")
                    return data['link']
                else:
                    print(f"❌ Upload failed: {data}")
            else:
                print(f"❌ HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            print(f"❌ Error uploading: {e}")
            
    return None

def upload_to_transfer_sh(filepath):
    """Upload file to transfer.sh (alternative)"""
    print(f"Uploading {filepath} to transfer.sh...")
    
    try:
        with open(filepath, 'rb') as f:
            response = requests.put(
                f'https://transfer.sh/{os.path.basename(filepath)}',
                data=f
            )
            
        if response.status_code == 200:
            download_url = response.text.strip()
            print(f"✅ Upload successful!")
            print(f"📥 Download link: {download_url}")
            print(f"🗑️  File will expire in 14 days")
            return download_url
        else:
            print(f"❌ HTTP {response.status_code}: {response.text}")
            
    except Exception as e:
        print(f"❌ Error uploading: {e}")
        
    return None

if __name__ == '__main__':
    zip_file = 'workspace-pro-deploy-2026-04-18.zip'
    
    if not os.path.exists(zip_file):
        print(f"❌ File not found: {zip_file}")
        sys.exit(1)
    
    print(f"File: {zip_file}")
    print(f"Size: {os.path.getsize(zip_file) / (1024*1024):.1f} MB")
    
    # Try file.io first
    print("\n" + "="*50)
    url = upload_to_fileio(zip_file)
    
    if not url:
        # Fall back to transfer.sh
        print("\n" + "="*50)
        print("Trying transfer.sh as fallback...")
        url = upload_to_transfer_sh(zip_file)
    
    if url:
        print("\n" + "="*50)
        print(f"✅ SUCCESS! Share this link:")
        print(f"🔗 {url}")
    else:
        print("\n❌ All upload attempts failed.")
        sys.exit(1)