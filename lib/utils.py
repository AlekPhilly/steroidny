from pathlib import Path


def remove_pics(folder):
    files = Path(folder).glob('*.png')
    for file in files:
        file.unlink()