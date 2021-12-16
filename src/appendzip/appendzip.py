import pathlib
import shutil
import tempfile


def appendzip(dest: pathlib.Path, file_to_include: pathlib.Path, arcname: str):
    if file_to_include.exists() is False:
        raise Exception("file to include does not exist")

    if dest.exists() is False:
        raise Exception("destination zip does not exist")

    if isinstance(arcname, str) is False:
        raise Exception("arcname should be a string")

    place_to_unpack = tempfile.TemporaryDirectory()

    shutil.unpack_archive(dest, place_to_unpack.name)

    copy2_path = pathlib.Path(place_to_unpack.name).joinpath(arcname)

    shutil.copy2(file_to_include, copy2_path)

    shutil.make_archive(
        dest.parent.joinpath(dest.stem),
        "zip",
        root_dir=place_to_unpack.name
    )

    place_to_unpack.cleanup()
