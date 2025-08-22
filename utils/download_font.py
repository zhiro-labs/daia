import requests
import os
import zipfile
from pathlib import Path

def check_font_exists():
    """Check if Noto CJK font already exists."""
    current_dir = Path(__file__).parent
    project_root = current_dir.parent
    fonts_dir = project_root / "assets" / "fonts"
    
    zip_file = fonts_dir / "03_NotoSansCJK-OTC.zip"
    
    # Check for zip file first
    if zip_file.exists():
        print(f"✓ ZIP file found: {zip_file}")
        print(f"  Size: {zip_file.stat().st_size / (1024*1024):.1f} MB")
        return True
    
    # Check for extracted fonts in subdirectory
    zip_extract_dir = fonts_dir / "03_NotoSansCJK-OTC"
    if zip_extract_dir.exists():
        ttc_files = list(zip_extract_dir.glob("*.ttc"))
        if ttc_files:
            print(f"✓ TTC font files found in {zip_extract_dir}:")
            for ttc in ttc_files:
                print(f"  - {ttc.name} ({ttc.stat().st_size / (1024*1024):.1f} MB)")
            return True
    
    # Check for fonts in root fonts directory (backward compatibility)
    ttc_files = list(fonts_dir.glob("*.ttc"))
    if ttc_files:
        print(f"✓ TTC font files found in {fonts_dir}:")
        for ttc in ttc_files:
            print(f"  - {ttc.name} ({ttc.stat().st_size / (1024*1024):.1f} MB)")
        return True
    
    print("✗ No Noto CJK font files found")
    return False

def download_noto_font(force=False):
    """
    Download and extract Noto CJK font to assets/fonts/ directory.
    
    Args:
        force (bool): If True, download even if file exists
    """
    # Get the project root directory (assuming this script is in util/)
    current_dir = Path(__file__).parent
    project_root = current_dir.parent
    fonts_dir = project_root / "assets" / "fonts"
    
    # Create the directory if it doesn't exist
    fonts_dir.mkdir(parents=True, exist_ok=True)
    
    url = "https://github.com/googlefonts/noto-cjk/releases/download/Sans2.004/03_NotoSansCJK-OTC.zip"
    zip_filename = fonts_dir / "03_NotoSansCJK-OTC.zip"
    
    # Check if TTC font files already exist (in subdirectory or root)
    zip_extract_dir = fonts_dir / "03_NotoSansCJK-OTC"
    existing_ttc_fonts = []
    
    if zip_extract_dir.exists():
        existing_ttc_fonts = list(zip_extract_dir.glob("*.ttc"))
    
    if not existing_ttc_fonts:
        existing_ttc_fonts = list(fonts_dir.glob("*.ttc"))
    
    if not force and existing_ttc_fonts:
        print("TTC font files already exist:")
        for font in existing_ttc_fonts:
            print(f"  - {font.name} ({font.stat().st_size / (1024*1024):.1f} MB)")
        print("Use force=True to re-download")
        return
    
    print("Downloading Noto CJK font...")
    print(f"URL: {url}")
    print(f"Destination: {zip_filename}")
    
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        with open(zip_filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"✓ Font downloaded successfully to {zip_filename}")
        print(f"✓ File size: {zip_filename.stat().st_size / (1024*1024):.1f} MB")
        
        # Extract the zip file into a folder with the same name as the zip file
        zip_extract_dir = fonts_dir / zip_filename.stem  # Remove .zip extension
        zip_extract_dir.mkdir(exist_ok=True)
        
        print(f"Extracting font file to {zip_extract_dir}...")
        with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
            zip_ref.extractall(zip_extract_dir)
        
        print(f"✓ Font extracted successfully to {zip_extract_dir}")
        
        # Delete the zip file
        zip_filename.unlink()
        print("✓ Zip file deleted")
        
        # Show final extracted TTC files in the new directory
        extracted_ttc_fonts = list(zip_extract_dir.glob("*.ttc"))
        if extracted_ttc_fonts:
            print("✓ Extracted TTC font files:")
            for font in extracted_ttc_fonts:
                print(f"  - {font.name} ({font.stat().st_size / (1024*1024):.1f} MB)")
        
    except requests.exceptions.RequestException as e:
        print(f"✗ Error downloading font: {e}")
        # Clean up partial download
        if zip_filename.exists():
            zip_filename.unlink()
    except zipfile.BadZipFile as e:
        print(f"✗ Error extracting zip file: {e}")
        # Clean up bad zip file
        if zip_filename.exists():
            zip_filename.unlink()
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        # Clean up partial download
        if zip_filename.exists():
            zip_filename.unlink()

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "check":
            check_font_exists()
        elif sys.argv[1] == "force":
            download_noto_font(force=True)
        else:
            print("Usage: python download_font.py [check|force]")
    else:
        # Default behavior: check first, then download if needed
        if not check_font_exists():
            print("\nDownloading font...")
            download_noto_font()
        else:
            print("\nFont already available. Use 'force' to re-download.")