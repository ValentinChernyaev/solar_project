# coding: utf-8
# license: GPLv3

import tkinter
from tkinter.filedialog import *
from solar_vis import *
from solar_model import *
from solar_input import *

perform_execution = False
"""Флаг цикличности выполнения расчёта"""



"""Заголовок по умолчанию"""
physical_time = 0
"""Физическое время от начала расчёта.
Тип: float"""

displayed_time = None
"""Отображаемое на экране время.
Тип: переменная tkinter"""

time_step = None
"""Шаг по времени при моделировании.
Тип: float"""

space_objects = []
"""Список космических объектов."""


def execution():
    """Функция исполнения -- выполняется циклически, вызывая обработку всех небесных тел,
    а также обновляя их положение на экране.
    Цикличность выполнения зависит от значения глобальной переменной perform_execution.
    При perform_execution == True функция запрашивает вызов самой себя по таймеру через от 1 мс до 100 мс.
    """
    global physical_time
    global displayed_time
    recalculate_space_objects_positions(space_objects, time_step.get())
    for body in space_objects:
        update_object_position(space, body)
    physical_time += time_step.get()
    displayed_time.set("%.1f" % physical_time + " прошло секунд")

    if perform_execution:
        space.after(101 - int(time_speed.get()), execution)


def start_execution():
    """Обработчик события нажатия на кнопку Start.
    Запускает циклическое исполнение функции execution.
    """
    global perform_execution
    perform_execution = True
    start_button['text'] = "Пауза"
    start_button['command'] = stop_execution

    execution()
    print('Программа запущена..')


def stop_execution():
    """Обработчик события нажатия на кнопку Start.
    Останавливает циклическое исполнение функции execution.
    """
    global perform_execution
    perform_execution = False
    start_button['text'] = "Пуск"
    start_button['command'] = start_execution
    print('Выполнение приостановлено')


def open_file_dialog():
    """Открывает диалоговое окно выбора имени файла и вызывает
    функцию считывания параметров системы небесных тел из данного файла.
    Считанные объекты сохраняются в глобальный список space_objects
    """
    global title_hider
    global space_objects
    global perform_execution
    perform_execution = False
    for obj in space_objects:
        space.delete(obj.image)  # удаление старых изображений планет
    in_filename = askopenfilename(filetypes=(("Text file", ".txt"),))
    space_objects = read_space_objects_data_from_file(in_filename)
    max_distance = max([max(abs(obj.x), abs(obj.y)) for obj in space_objects])
    # вычмсление масштаба отображения для первода в экранные координаты
    calculate_scale_factor(max_distance)
     #  Подпись на холсте
    update_system_name(space, title_header.title)



    for obj in space_objects:
        if obj.type == 'star':
            create_star_image(space, obj)
        elif obj.type == 'planet':
            create_planet_image(space, obj)
        else:
            raise AssertionError()


def save_file_dialog():
    """Открывает диалоговое окно выбора имени файла и вызывает
    функцию считывания параметров системы небесных тел из данного файла.
    Считанные объекты сохраняются в глобальный список space_objects
    """
    out_filename = asksaveasfilename(title = "Введите название файла отчёта",
    initialfile='Report.txt',filetypes=(("Text file", ".txt"),))
    write_space_objects_data_to_file(out_filename, space_objects)



    """Главная функция главного модуля.
    Создаёт объекты графического дизайна библиотеки tkinter: окно, холст, фрейм с кнопками, кнопки.
    """
global physical_time
global displayed_time
global time_step
global time_speed
global space
global start_button

print('Моделирование запущено..')
physical_time = 0

root = tkinter.Tk()
    # космическое пространство отображается на холсте типа Canvas
    # ЛУЧШЕ ЗАДАТЬ ЯВНО РАЗМЕР ПОЛОТНА ИНАЧЕ НЕ ОТОБРАЖАЕТСЯ НИЖНИЙ ФРЕЙМ
space = tkinter.Canvas(root, width=800, height=600, bg="black")
space.pack(side=tkinter.TOP)
    # нижняя панель с кнопками
frame = tkinter.Frame(root)
frame.pack(side=tkinter.BOTTOM)

start_button = tkinter.Button(frame, text="Пуск", command=start_execution, width=6)
start_button.pack(side=tkinter.LEFT)
lab = Label(frame, text="Множитель времени")
lab.pack(side=tkinter.LEFT)
# Поле ввода шага времени чтобы работало нужно минимум 100 000
time_step = tkinter.DoubleVar()
time_step.set(100000)
time_step_entry = tkinter.Entry(frame, width=8, bd=3, textvariable=time_step)
time_step_entry.pack(side=tkinter.LEFT)

time_speed = tkinter.DoubleVar()
scale = tkinter.Scale(frame, variable=time_speed, length=100,
from_=0,to=100,resolution=1,
orient=HORIZONTAL)


scale.pack(side=tkinter.LEFT, fill="y")


load_file_button = tkinter.Button(frame, text="Открыть файл..", command=open_file_dialog)
load_file_button.pack(side=tkinter.LEFT)
save_file_button = tkinter.Button(frame, text="Сохранить в файл...", command=save_file_dialog)
save_file_button.pack(side=tkinter.LEFT)

displayed_time = tkinter.StringVar()
displayed_time.set(str(physical_time) + " секунд с момента запуска")
time_label = tkinter.Label(frame, textvariable=displayed_time, width=30)
time_label.pack(side=tkinter.RIGHT)

root.mainloop()
print('Моделирование завершено...')


