import os
import traceback
import zipfile
import sys


def un_zip(file_name, dst):
    try:
        zip_fi = zipfile.ZipFile(file_name)
        if os.path.isdir(dst):
            pass
        else:
            os.mkdir(dst)
        for names in zip_fi.namelist():
            zip_fi.extract(names, dst)
        zip_fi.close()
        return True
    except:
        traceback.print_exc()
        return False


def add_zip(file_name, dst):
    f = zipfile.ZipFile(dst, 'a', zipfile.ZIP_DEFLATED)
    f.write(file_name)
    f.close()


def mg_zip(src, dst, mg):
    f = zipfile.ZipFile(dst)
    zi_fi = zipfile.ZipFile(src)
    tm = zipfile.ZipFile(mg, 'a', zipfile.ZIP_DEFLATED)
    for names in f.namelist():
        if names not in zi_fi.namelist():
            tm.writestr(f.getinfo(names), f.read(names))
    for names in zi_fi.namelist():
        tm.writestr(zi_fi.getinfo(names), zi_fi.read(names))
    tm.close()


def zip_file(start_dir, zip_name):
    f = zipfile.ZipFile(zip_name, 'a', zipfile.ZIP_DEFLATED)
    for dir_path, dir_names, file_names in os.walk(start_dir):
        for filename in file_names:
            f.write(os.path.join(dir_path, filename))
    f.close()


# mg_zip(sys.argv[0], sys.argv[1], sys.argv[2])
