import ConfigParser
import traceback


def read_ini(file_name):
    try:
        cf = ConfigParser.ConfigParser()
        cf.read(file_name)
        return cf
    except:
        traceback.print_exc()
        return None


def write_ini(file_name, section, item, value):
    try:
        cf = ConfigParser.ConfigParser()
        cf.read(file_name)
        cf.set(section, item, value)
        cf.write(open(file_name, 'w'))
        return True
    except:
        traceback.print_exc()
        return False

