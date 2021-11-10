from dcv import utils


def test_file_is_renamed_including_suffix(tempfile):
    new_filename = 'foo.dat'
    renamed_file = utils.rename_newest_file(tempfile.parent, new_filename)
    assert renamed_file.name == new_filename
    renamed_file.unlink()


def test_file_is_renamed_with_existing_suffix(tempfile):
    new_filename = 'foo'
    tempfile_suffix = tempfile.suffix
    renamed_file = utils.rename_newest_file(
        tempfile.parent, new_filename, keep_existing_suffix=True
    )
    assert renamed_file.name == new_filename + tempfile_suffix
    renamed_file.unlink()
