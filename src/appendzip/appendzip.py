import zipfile
import pathlib
import shutil

def appendzip(dest: pathlib.Path, file_to_include: pathlib.Path, arcname: str):
    if pathlib.Path("temp").exists():
        shutil.rmtree("temp")

    if file_to_include.exists() == False:
        raise Exception("file to include does not exist")

    if dest.exists() == False:
        raise Exception("destination zip does not exist")

    shutil.unpack_archive(dest, "temp")

    copy2_path = pathlib.Path("temp").joinpath(arcname)

    shutil.copy2(file_to_include, copy2_path)

    shutil.make_archive(dest.stem, "zip", root_dir="temp")

    shutil.rmtree("temp")