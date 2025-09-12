import os
import argparse
from PIL import Image
from PIL.ExifTags import TAGS

def analyze_image(filepath):
    """Analyzes a single image file and prints its metadata."""
    if not os.path.exists(filepath):
        print(f"Error: File not found at '{filepath}'.")
        return

    try:
        image = Image.open(filepath)
    except Exception as e:
        print(f"Error: Could not open or process file '{filepath}'. - {e}")
        return

    print(f"\n--- Metadata Analysis: {os.path.basename(filepath)} ---")
    
    print(f"  Format: {image.format}")
    print(f"  Size: {image.size[0]}x{image.size[1]}")
    print(f"  Mode: {image.mode}")

    exif_data = image.getexif()

    if not exif_data:
        print(" No EXIF data found in this file.")
    else:
        print("  --- EXIF Data ---")
        for tag_id, value in exif_data.items():
            tag_name = TAGS.get(tag_id, tag_id)
            
            if isinstance(value, bytes):
                try:
                    value = value.decode('utf-8', errors='ignore').strip('\x00')
                except:
                    pass

            print(f"    {tag_name}: {value}")


def main():
    """Main function, gets file paths and runs the analyzer."""
    parser = argparse.ArgumentParser(description="Parses and displays metadata for image files.")
    parser.add_argument("files", nargs='+', help="One or more image files to analyze.")
    args = parser.parse_args()

    for filepath in args.files:
        analyze_image(filepath)

if __name__ == "__main__":
    main()