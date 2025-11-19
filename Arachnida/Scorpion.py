from PIL import Image, ExifTags
import argparse
import json

def get_exif(image_path):
    image = Image.open(image_path)
    exif_data = image._getexif()
    if not exif_data:
        return {}
    exif = {}
    for tag_id, value in exif_data.items():
        tag = ExifTags.TAGS.get(tag_id, tag_id)
        exif[tag] = value
    return exif

def get_metadata(image_path):
    try:
        image = Image.open(image_path)
        metadata = {
            "Filename": os.path.basename(image_path),
            "Format": image.format,
            "Mode": image.mode,
            "Size": image.size,
        }
        return metadata
    except Exception as e:
        print(f"Error while reading metadatas: {e}")
        return {}

def main():
    parser = argparse.ArgumentParser(description="Process one or more image files.")
    parser.add_argument("files", nargs="+", help="One or more image files")
    args = parser.parse_args()

    metadata = get_metadata(args.files)
    print("\n=== Metadata ===\n")
    for key, val in metadata.items():
        print(f"{key:15} : {val}")

    for image_path in args.files:
        print(f"\n=== EXIF ===\n")
        exif = get_exif(image_path)

        for key, val in exif.items():
            print(f"{key:30} : {val}")


        

if __name__ == "__main__":
    main()