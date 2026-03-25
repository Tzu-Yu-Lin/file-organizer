
from pathlib import Path
import shutil

FILE_CATEGORIES = {
    "images": [".jpg", ".jpeg", ".png", ".gif"],
    "pdfs": [".pdf"],
    "texts": [".txt"],
    "documents": [".doc", ".docx"],
    "spreadsheets": [".xls", ".xlsx", ".csv"],
    "archives": [".zip", ".rar"],
}

def get_category(file_suffix:str) -> str:
    file_suffix = file_suffix.lower()
    for c, e in FILE_CATEGORIES.items():
        if file_suffix in e:
            return c

    return "others"

def organize (folder_path: Path, preview: bool) -> None:
    if not folder_path.exists():
        print("not exist")
        return
    if not folder_path.is_dir():
        print("The path is not a folder.")
        return
    summary = {}

    for item in folder_path.iterdir():
        if item.is_file():
            category = get_category(item.suffix)
            target_folder = folder_path / category
            if preview:
                target_folder.mkdir(exist_ok=True)
            target_file = target_folder / item.name

            c = 1
            while target_file.exists():
                target_file = target_folder/f"{item.stem}_{c}{item.suffix}"
                c += 1
            if preview:
                print(f"[preview]move{item.name} -> {category}/")
            else:
                shutil.move(str(item), str(target_file))
                print(f"Moved: {item.name} -> {category}/")
            summary[category] = summary.get(category, 0) + 1
    for ca, count in summary.items():
        print(f"{ca}: {count}")

def main():
    folder_input = input("Enter folder path: ").strip()
    folder_path = Path(folder_input)
    print("\nPreview:")
    organize(folder_path, True)

    confirm = input("\nDo you want to organize these files? (y/n): ").strip().lower()

    if confirm == "y":
        print("\nOrganizing files...")
        organize(folder_path, False)
    else:
        print("\nOperation cancelled.")

if __name__ == "__main__":
    main()
