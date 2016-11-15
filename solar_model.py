# coding: utf-8
# license: GPLv3

gravitational_constant = 6.67408E-11
"""Гравитационная постоянная Ньютона G"""


def calculate_force(body, space_objects):
    """Вычисляет силу, действующую на тело.
    Параметры:
    **body** — тело, для которого нужно вычислить дейстующую силу.
    **space_objects** — список объектов, которые воздействуют на тело.
    """

    body.Fx = body.Fy = 0
    for obj in space_objects:
        if body == obj:
            continue  # тело не действует гравитационной силой на само себя!
        delta_x = obj.x - body.x # расстояние по оси х
        delta_y = obj.y - body.y # расстояние по оси y
        radius = (delta_x**2 + delta_y**2)**0.5 # радиус
        # модуль сислы гравитации для двух объектов
        F_grav = gravitational_constant * (body.m * obj.m) / (radius ** 2)
        sin_Fi = delta_y / radius  # синус угла для вычисления проекции силы
        cos_Fi = delta_x / radius  # косинус угла для вычисления проекции силы
        body.Fx += F_grav * cos_Fi
        body.Fy += F_grav * sin_Fi
        print('body.Fx=', body.Fx,'body.Fy=',body.Fy,
        'модуль F',  F_grav, 'объект ',body.type)

def move_space_object(body, dt):
    """Перемещает тело в соответствии с действующей на него силой.
    Параметры:
    **body** — тело, которое нужно переместить.
    """

    ax = body.Fx/body.m
    body.Vx += ax*dt
    body.x += body.Vx * dt
    ay = body.Fy/body.m
    body.Vy += ay*dt
    body.y += body.Vy * dt
    print('body.x=', body.x,'body.y=',body.y, 'объект ',body.type)
    print('A.x=', ax,'A.y=', ay,'объект ',body.type)

    print('body.Vx',body.Vx,'body.Vy', body.Vy, 'объект ',body.type)

def recalculate_space_objects_positions(space_objects, dt):
    """Пересчитывает координаты объектов.
    Параметры:
    **space_objects** — список оьъектов, для которых нужно пересчитать координаты.
    **dt** — шаг по времени
    """

    for body in space_objects:
        calculate_force(body, space_objects)
    for body in space_objects:
        move_space_object(body, dt)


if __name__ == "__main__":
    print("This module is not for direct call!")