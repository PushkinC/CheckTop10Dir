import os


def human_read_format(size):
    if size >= 1024:
        size = size / 1024
        if size >= 1024:
            size /= 1024
            if size >= 1024:
                size /= 1024
                return f'{round(size, 2)}ГБ'
            return f'{round(size, 2)}МБ'
        return f'{round(size, 2)}КБ'
    return f'{round(size, 2)}Б'


def count_of_dir(name, count):
    try:
        for i in os.listdir(name):
            if os.path.isdir(name + '/' + i):
                count += 1
                a = count_of_dir(name + '/' + i, 0)
                if a is not None:
                    count += a

        return count
    except Exception as ex:
        print(f'Найдено: {count}, ', ex)


def size_of_dir(name, size):
    for i in os.listdir(name):
        if os.path.isfile(name + '/' + i):
            size += os.path.getsize(name + '/' + i)
        else:
            size += size_of_dir(name + '/' + i, 0)
    return size


a = 0


def go_to_dir(name, top={}):
    try:
        global a
        for i in os.listdir(name):
            if os.path.isdir(name + '/' + i):
                a += 1
                if name + '/' + i in top.keys():
                    top[name + '/' + i] += size_of_dir(name + '/' + i, 0)
                else:
                    top[name + '/' + i] = size_of_dir(name + '/' + i, 0)
                print(f'Проверено {a} из {count}')

                top.update(go_to_dir(name + '/' + i, top))
            else:
                if name in top.keys():
                    top[name] += os.path.getsize(name)
                else:
                    top[name] = os.path.getsize(name)
        return top
    except Exception as ex:
        print(ex)


name = input('Введите директорию: ')
if os.path.isdir(name):
    count = count_of_dir(name, 0)
    asd = input(f'Найдено {count} папок, продолжим?(y/n)')
    if asd.lower() == 'y':
        top = go_to_dir(name)

        if len(top) < 10:
            print()
            print('Упс... директорий меньше десяти!')
            top = sorted(top.items(), key=lambda i: i[1], reverse=True)
            for i, j in top:
                print(i + '\t' + human_read_format(j))
        else:
            print()
            top = sorted(top.items(), key=lambda i: i[1], reverse=True)[:10]
            for i, j in top:
                print(i + '\t' + human_read_format(j))

    else:
        print(':(')
else:
    print('Упс... Это неправильный путь!')
