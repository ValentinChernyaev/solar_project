# coding: utf-8
# license: GPLv3

from solar_objects import Star, Planet


def read_space_objects_data_from_file(input_filename):
    """Cчитывает данные о космических объектах из файла, создаёт сами объекты
    и вызывает создание их графических образов

    Параметры:

    **input_filename** — имя входного файла
    """

    objects = []
    with open(input_filename) as input_file:
        for line in input_file:
            if len(line.strip()) == 0 or line[0] == '#':
                continue  # пустые строки и строки-комментарии пропускаем
            object_type = line.split()[0].lower()
            if object_type == "star":  # FIXME: do the same for planet
                star = Star()
                parse_star_parameters(line, star)
                objects.append(star)
            else:
                print("Unknown space object")

    return objects


def parse_star_parameters(line, star):

    lines = line.split()
    star.R = float(lines[1])
    star.color = lines[2]
    star.m = float(lines[3])
    star.x = float(lines[4])
    star.y = float(lines[5])
    star.Vx = float(lines[6])
    star.Vy = float(lines[7])


def parse_planet_parameters(line, planet):

    lines = line.split()
    planet.R = float(lines[1])
    planet.color = lines[2]
    planet.m = float(lines[3])
    planet.x = float(lines[4])
    planet.y = float(lines[5])
    planet.Vx = float(lines[6])
    planet.Vy = float(lines[7])


def write_space_objects_data_to_file(output_filename, space_objects):

    with open(output_filename, 'w') as out_file:
        for obj in space_objects:
         line='{0:6s} | {1:3.0f} | {2:6s} | {3:6.3e} | {4:6.3e} | {5:6.3e} | {6:6.3e} | {7:6.3e} '.\
         format(obj.type, obj.R,
         obj.color, obj.m, obj.x, obj.y, obj.Vx, obj.Vy)
         print (line, file=out_file)
    out_file.close

if __name__ == "__main__":
    print("This module is not for direct call!")
