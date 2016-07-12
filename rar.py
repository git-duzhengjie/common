import os
import tarfile
import zipfile
import gzip
import shutil
# from unrar import rarfile
import traceback


def win_rar(src, dst):
    if not os.path.exists('temp_dir'):
        os.mkdir('temp_dir')
    rar_command = '"C:\\Program Files\\WinRAR\\rar.exe" x -o+ -idq %s %s' \
                  % (src, 'temp_dir')
    if os.system(rar_command) == 0:
        files = os.listdir('temp_dir')
        os.chdir('temp_dir')
        for f in files:
            if f.__contains__('.gz'):
                un_gz(f)
                shutil.copy(f.replace('.gz', ''), "../" + dst)
        os.chdir('..')
        return True
    else:
        return False


def un_gz(file_name):
    try:
        f_name = file_name.replace(".gz", "")
        g_file = gzip.GzipFile(file_name)
        open(f_name, "w+").write(g_file.read())
        g_file.close()
        return True
    except:
        traceback.print_exc()
        return False


def un_tar(file_name, dst):
    try:
        tar = tarfile.open(file_name)
        names = tar.getnames()
        if os.path.isdir(dst):
            pass
        else:
            os.mkdir(dst)
        for name in names:
            tar.extract(name, dst)
        tar.close()
        return True
    except:
        traceback.print_exc()
        return False


def un_zip(file_name, dst):
    try:
        zip_file = zipfile.ZipFile(file_name)
        if os.path.isdir(dst):
            pass
        else:
            os.mkdir(dst)
        for names in zip_file.namelist():
            zip_file.extract(names, file_name + "_files/")
        zip_file.close()
        return True
    except:
        traceback.print_exc()
        return False


# def un_rar(file_name, dst):
#     try:
#         rar = rarfile.RarFile(file_name)
#         if os.path.isdir(dst):
#             pass
#         else:
#             os.mkdir(dst)
#         os.chdir(dst)
#         rar.extractall()
#         rar.close()
#         return True
#     except:
#         traceback.print_exc()
#         return False


def to_gz(file_name):
    g = gzip.GzipFile(filename="", mode='wb', compresslevel=9, fileobj=open(file_name + '.gz', 'wb'))
    g.write(open(file_name).read())
    g.close()

