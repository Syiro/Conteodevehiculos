import os
import time
import progressbar

list_name = os.listdir(\\wsl.localhost\Ubuntu\home\ruben-laptop\Tesis\Videotoframe\Modelo2.0\dataset\dataset)
list_name_lenght = len(list_name)
new_list = []
new_list_updated = []

def _create_list():
    global list_name_lenght, list_name, new_list
    print('Creando listas...')
    for i in progressbar.progressbar(range(list_name_lenght)):
        if old_name in list_name[i]:
            new_list.append(list_name[i])
        time.sleep(0.02)

def _create_list_updated():
    print('Creando nueva lista de cambio de nombre...')
    global new_list, new_list_updated
    new_list_updated = [name.replace(old_name, new_name) for name in new_list]


def _change_filename():
    print('Cambiando los nombres de los archivos...')
    global new_list, new_list_updated
    for i in progressbar.progressbar(range(len(new_list))):
        os.rename(new_list[i], new_list_updated[i])
        time.sleep(0.02)


if __name__ == '__main__':
    old_name = input('Valor a Buscar: ')
    new_name = input('Reemplazarlo por: ')
    _create_list()
    _create_list_updated()
    _change_filename()
    print('**PROCESO TERMINADO**')