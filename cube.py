import traceback

__author__ = 'duzhengjie'


def get_cube_collections(cube_column):
    try:
        count = len(cube_column)
        unique_columns_all = []
        for i in range(0, 2 ** count):
            if i == 5 or i == 1 or i == 7 or i == 6:
                continue
            unique_columns = []
            tempstr = bin(i)
            count_temp = len(tempstr)
            for j in range(count_temp):
                if tempstr[count_temp - j - 1] == '1':
                    unique_columns.append(cube_column[count - j - 1])
                if tempstr[count_temp - j - 1] == 'b':
                    break
            unique_columns_all.append(unique_columns)
        return unique_columns_all
    except:
        print traceback.print_exc()


def test():
    cube = get_cube_collections(['server', 'ch', 'pt'])
    print cube


