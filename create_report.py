import os
import pandas as pd
from matplotlib import pyplot as plt

from paths_filenames import path_report, report_file, need_files, sample_directory

all_files = True

for file in need_files:
    if not os.path.exists(f'{path_report}\\{file}'):
        print(f'Отсутствует требуемый для генерации отчёта файл: {file}')
        all_files = False

if all_files:

    html = ('<h1 align="center" style="color: blue">Сравнительный анализ эффективности использования методов<br>'
            'мультипоточного, мультипроцессного и асинхронного программирования<br>'
            'применительно к задачам загрузки изображений из Интернета и их преобразования</h1>')

    html += '<h2 align="center" style="color: magenta">Этап I. Загрузка изображений из Интернета</h2>'

    html += '<h2 align="center" style="color: darkgreen">1. Последовательная реализация</h2>'

    filename = f'{path_report}\\{need_files[0]}'
    with open(filename, mode='r') as data_file:
        content = data_file.read()
    time_request_sequence_value = float(content)

    html += '<h3 align="center">Общее время загрузки изображений:</h3>'
    html += f'<h2 align="center" style="color: red">{content} сек</h2>'

    html += '<h2 align="center" style="color: darkgreen">2. Мультипоточная реализация</h2>'

    filename = f'{path_report}\\{need_files[1]}'
    with open(filename, mode='r') as data_file:
        content = data_file.read()
    lines = content.split('\n')
    index_list = [int(value) for value in lines[0].strip().split(' ')]
    time_list = [round(float(value), 2) for value in lines[1].strip().split(' ')]
    min_time_value_for_thread = min(time_list)
    acceleration_for_thread = time_request_sequence_value / min_time_value_for_thread

    data = {'Количество потоков': index_list,
            'Время загрузки, сек': time_list}

    table = pd.DataFrame.from_dict(data).to_html(index=False, col_space=200)
    html += f'<p align="center">{table}</p>'

    html += '<h3 align="center">Минимальное время загрузки изображений:</h3>'
    html += f'<h2 align="center" style="color: red">{min_time_value_for_thread} сек</h2>'

    html += '<h3 align="center">Достигнутое ускорение:</h3>'
    html += f'<h2 align="center" style="color: red">{acceleration_for_thread: .1f}</h2>'

    fig, ax = plt.subplots(figsize=(10, 5))
    bars = plt.barh(index_list, time_list)
    ax.bar_label(bars, padding=2, color='blue', fontweight='bold')
    plt.xlabel('Время загрузки, сек')
    plt.ylabel('Количество потоков')
    plt.xticks([i for i in range(int(max(time_list)) + 1)])
    plt.yticks(index_list)
    plt.title('Зависимость времени загрузки от количества используемых потоков')
    plt.savefig(f'{path_report}\\figure_1.jpg')

    html += f'<center><img src="figure_1.jpg" border="1"/></center>'

    html += '<h2 align="center" style="color: darkgreen">3. Мультипроцессная реализация</h2>'

    filename = f'{path_report}\\{need_files[2]}'
    with open(filename, mode='r') as data_file:
        content = data_file.read()
    lines = content.split('\n')
    index_list = [int(value) for value in lines[0].strip().split(' ')]
    time_list = [round(float(value), 2) for value in lines[1].strip().split(' ')]
    min_time_value_for_process = min(time_list)
    acceleration_for_process = time_request_sequence_value / min_time_value_for_process

    data = {'Количество процессов': index_list,
            'Время загрузки, сек': time_list}

    table = pd.DataFrame.from_dict(data).to_html(index=False, col_space=200)
    html += f'<p align="center">{table}</p>'

    html += '<h3 align="center">Минимальное время загрузки изображений:</h3>'
    html += f'<h2 align="center" style="color: red">{min_time_value_for_process} сек</h2>'

    html += '<h3 align="center">Достигнутое ускорение:</h3>'
    html += f'<h2 align="center" style="color: red">{acceleration_for_process: .1f}</h2>'

    fig, ax = plt.subplots(figsize=(10, 5))
    bars = plt.barh(index_list, time_list)
    ax.bar_label(bars, padding=2, color='blue', fontweight='bold')
    plt.xlabel('Время загрузки, сек')
    plt.ylabel('Количество процессов')
    plt.xticks([i for i in range(int(max(time_list)) + 1)])
    plt.yticks(index_list)
    plt.title('Зависимость времени загрузки от количества используемых процессов')
    plt.savefig(f'{path_report}\\figure_2.jpg')

    html += f'<center><img src="figure_2.jpg" border="1"/></center>'

    html += '<h2 align="center" style="color: darkgreen">4. Асинхронная реализация</h2>'

    filename = f'{path_report}\\{need_files[3]}'
    with open(filename, mode='r') as data_file:
        content = data_file.read()
    time_request_async_value = float(content)
    acceleration_for_async = time_request_sequence_value / time_request_async_value

    html += '<h3 align="center">Общее время загрузки изображений:</h3>'
    html += f'<h2 align="center" style="color: red">{content} сек</h2>'

    html += '<h3 align="center">Достигнутое ускорение:</h3>'
    html += f'<h2 align="center" style="color: red">{acceleration_for_async: .1f}</h2>'

    index_list = [i + 1 for i in range(4)]
    acceleration_list = [1.00,
                         round(acceleration_for_thread, 1),
                         round(acceleration_for_process, 1),
                         round(acceleration_for_async, 1)]

    fig, ax = plt.subplots(figsize=(10, 7))
    colors = ['gray', 'red', 'green', 'blue']
    legend = ['Последовательная реализация',
              'Мультипоточная реализация',
              'Мультипроцессная реализация',
              'Асинхронная реализация']
    bar1 = plt.bar(index_list[0], acceleration_list[0], color=colors[0], width=0.5, label=legend[0])
    ax.bar_label(bar1, padding=2, color=colors[0], fontweight='bold')
    bar2 = plt.bar(index_list[1], acceleration_list[1], color=colors[1], width=0.5, label=legend[1])
    ax.bar_label(bar2, padding=2, color=colors[1], fontweight='bold')
    bar3 = plt.bar(index_list[2], acceleration_list[2], color=colors[2], width=0.5, label=legend[2])
    ax.bar_label(bar3, padding=2, color=colors[2], fontweight='bold')
    bar4 = plt.bar(index_list[3], acceleration_list[3], color=colors[3], width=0.5, label=legend[3])
    ax.bar_label(bar4, padding=2, color=colors[3], fontweight='bold')
    plt.legend()
    plt.xlabel('Способ реализации')
    plt.ylabel('Достигнутое ускорение')
    plt.xticks(index_list)
    plt.ylim(0, (int(max(acceleration_list) / 0.5) + 2) / 2)
    plt.title('Достигнутое ускорение при различных способах реализации')
    plt.savefig(f'{path_report}\\figure_3.jpg')

    html += f'<center><img src="figure_3.jpg" border="1"/></center>'

    html += '<h2 align="center" style="color: magenta">Этап II. Обработка изображений</h2>'

    html += '<h2 align="center" style="color: darkgreen">О важности использования оптимизированных операций</h2>'

    html += '<h3 align="center" style="color: orange">Пример изображения до инверсии цветов:</h3>'

    html += f'<center><img src="..\\{sample_directory}\\sample_for_inverse_from.jpg" border="1"/></center>'

    html += '<h3 align="center" style="color: orange">То же изображение после инверсии цветов:</h3>'

    html += f'<center><img src="..\\{sample_directory}\\sample_for_inverse_to.jpg" border="1"/></center>'

    filename = f'{path_report}\\{need_files[9]}'
    with open(filename, mode='r') as data_file:
        content = data_file.read()
    time_image_by_matrix_value = float(content)

    html += '<h3 align="center">Общее время инвертирования цветов для всех изображений ("матричный" способ):</h3>'
    html += f'<h2 align="center" style="color: red">{content} сек</h2>'

    filename = f'{path_report}\\{need_files[8]}'
    with open(filename, mode='r') as data_file:
        content = data_file.read()
    time_image_by_iter_value = float(content)
    deceleration = time_image_by_matrix_value / time_image_by_iter_value

    html += '<h3 align="center">Общее время инвертирования цветов для всех изображений ("пиксельный" способ):</h3>'
    html += f'<h2 align="center" style="color: red">{content} сек</h2>'

    html += '<h3 align="center">Полученное замедление:</h3>'
    html += f'<h2 align="center" style="color: red">{deceleration: .3f}</h2>'

    index_list = [1, 2]
    deceleration_list = [1.00, round(deceleration, 3)]

    fig, ax = plt.subplots(figsize=(6, 4))
    colors = ['green', 'red']
    legend = ['Оптимизированное инвертирование',
              'Неоптимизированное инвертирование']
    bar1 = plt.bar(index_list[0], deceleration_list[0], color=colors[0], width=0.25, label=legend[0])
    bar2 = plt.bar(index_list[1], deceleration_list[1], color=colors[1], width=0.25, label=legend[1])
    ax.bar_label(bar2, padding=2, color=colors[1], fontweight='bold')
    plt.legend()
    plt.xlabel('Способ инвертирования')
    plt.ylabel('Полученное замедление')
    plt.xticks(index_list)
    plt.ylim(0, 1)
    plt.title('"Эффект" неоптимизированного метода преобразования')
    plt.savefig(f'{path_report}\\figure_4.jpg')

    html += f'<center><img src="figure_4.jpg" border="1"/></center>'

    html += '<h2 align="center" style="color: darkgreen">Базовое преобразование для исследования</h2>'

    html += '<h3 align="center" style="color: orange">Изображение после "обнуления" канала красного цвета:</h3>'

    html += f'<center><img src="..\\{sample_directory}\\sample_for_no_red.jpg" border="1"/></center>'

    html += '<h2 align="center" style="color: darkgreen">1. Последовательная реализация</h2>'

    filename = f'{path_report}\\{need_files[4]}'
    with open(filename, mode='r') as data_file:
        content = data_file.read()
    time_sequence_value = float(content)

    html += '<h3 align="center">Общее время преобразования изображений:</h3>'
    html += f'<h2 align="center" style="color: red">{content} сек</h2>'

    html += '<h2 align="center" style="color: darkgreen">2. Мультипоточная реализация</h2>'

    filename = f'{path_report}\\{need_files[5]}'
    with open(filename, mode='r') as data_file:
        content = data_file.read()
    lines = content.split('\n')
    index_list = [int(value) for value in lines[0].strip().split(' ')]
    time_list = [round(float(value), 2) for value in lines[1].strip().split(' ')]
    min_time_value_for_thread = min(time_list)
    acceleration_for_thread = time_sequence_value / min_time_value_for_thread

    data = {'Количество потоков': index_list,
            'Время преобразования, сек': time_list}

    table = pd.DataFrame.from_dict(data).to_html(index=False, col_space=250)
    html += f'<p align="center">{table}</p>'

    html += '<h3 align="center">Минимальное время преобразования изображений:</h3>'
    html += f'<h2 align="center" style="color: red">{min_time_value_for_thread} сек</h2>'

    html += '<h3 align="center">Достигнутое ускорение:</h3>'
    html += f'<h2 align="center" style="color: red">{acceleration_for_thread: .1f}</h2>'

    fig, ax = plt.subplots(figsize=(10, 5))
    bars = plt.barh(index_list, time_list)
    ax.bar_label(bars, padding=2, color='blue', fontweight='bold')
    plt.xlabel('Время преобразования, сек')
    plt.ylabel('Количество потоков')
    plt.xticks([i for i in range(int(max(time_list)) + 1)])
    plt.yticks(index_list)
    plt.title('Зависимость времени преобразования от количества используемых потоков')
    plt.savefig(f'{path_report}\\figure_5.jpg')

    html += f'<center><img src="figure_5.jpg" border="1"/></center>'

    html += '<h2 align="center" style="color: darkgreen">3. Мультипроцессная реализация</h2>'

    filename = f'{path_report}\\{need_files[6]}'
    with open(filename, mode='r') as data_file:
        content = data_file.read()
    lines = content.split('\n')
    index_list = [int(value) for value in lines[0].strip().split(' ')]
    time_list = [round(float(value), 2) for value in lines[1].strip().split(' ')]
    min_time_value_for_process = min(time_list)
    acceleration_for_process = time_sequence_value / min_time_value_for_process

    data = {'Количество процессов': index_list,
            'Время преобразования, сек': time_list}

    table = pd.DataFrame.from_dict(data).to_html(index=False, col_space=250)
    html += f'<p align="center">{table}</p>'

    html += '<h3 align="center">Минимальное время преобразования изображений:</h3>'
    html += f'<h2 align="center" style="color: red">{min_time_value_for_process} сек</h2>'

    html += '<h3 align="center">Достигнутое ускорение:</h3>'
    html += f'<h2 align="center" style="color: red">{acceleration_for_process: .1f}</h2>'

    fig, ax = plt.subplots(figsize=(10, 5))
    bars = plt.barh(index_list, time_list)
    ax.bar_label(bars, padding=2, color='blue', fontweight='bold')
    plt.xlabel('Время преобразования, сек')
    plt.ylabel('Количество процессов')
    plt.xticks([i for i in range(int(max(time_list)) + 1)])
    plt.yticks(index_list)
    plt.title('Зависимость времени преобразования от количества используемых процессов')
    plt.savefig(f'{path_report}\\figure_6.jpg')

    html += f'<center><img src="figure_6.jpg" border="1"/></center>'

    html += '<h2 align="center" style="color: darkgreen">4. Асинхронная реализация</h2>'

    filename = f'{path_report}\\{need_files[7]}'
    with open(filename, mode='r') as data_file:
        content = data_file.read()
    time_async_value = float(content)
    acceleration_for_async = time_sequence_value / time_async_value

    html += '<h3 align="center">Общее время загрузки изображений:</h3>'
    html += f'<h2 align="center" style="color: red">{content} сек</h2>'

    html += '<h3 align="center">Достигнутое ускорение:</h3>'
    html += f'<h2 align="center" style="color: red">{acceleration_for_async: .1f}</h2>'

    html += '<h2 align="center" style="color: darkgreen">5. Асинхронно-Мультипоточная реализация</h2>'

    filename = f'{path_report}\\{need_files[10]}'
    with open(filename, mode='r') as data_file:
        content = data_file.read()
    lines = content.split('\n')
    index_list = [int(value) for value in lines[0].strip().split(' ')]
    time_list = [round(float(value), 2) for value in lines[1].strip().split(' ')]
    min_time_value_for_async_thread = min(time_list)
    acceleration_for_async_thread = time_sequence_value / min_time_value_for_async_thread

    data = {'Количество потоков': index_list,
            'Время преобразования, сек': time_list}

    table = pd.DataFrame.from_dict(data).to_html(index=False, col_space=250)
    html += f'<p align="center">{table}</p>'

    html += '<h3 align="center">Минимальное время преобразования изображений:</h3>'
    html += f'<h2 align="center" style="color: red">{min_time_value_for_async_thread} сек</h2>'

    html += '<h3 align="center">Достигнутое ускорение:</h3>'
    html += f'<h2 align="center" style="color: red">{acceleration_for_async_thread: .1f}</h2>'

    fig, ax = plt.subplots(figsize=(10, 5))
    bars = plt.barh(index_list, time_list)
    ax.bar_label(bars, padding=2, color='blue', fontweight='bold')
    plt.xlabel('Время преобразования, сек')
    plt.ylabel('Количество потоков')
    plt.xticks([i for i in range(int(max(time_list)) + 1)])
    plt.yticks(index_list)
    plt.title('Зависимость времени преобразования от количества используемых потоков')
    plt.savefig(f'{path_report}\\figure_7.jpg')

    html += f'<center><img src="figure_7.jpg" border="1"/></center>'

    html += '<h2 align="center" style="color: darkgreen">6. Асинхронно-Мультипроцессная реализация</h2>'

    filename = f'{path_report}\\{need_files[11]}'
    with open(filename, mode='r') as data_file:
        content = data_file.read()
    lines = content.split('\n')
    index_list = [int(value) for value in lines[0].strip().split(' ')]
    time_list = [round(float(value), 2) for value in lines[1].strip().split(' ')]
    min_time_value_for_async_process = min(time_list)
    acceleration_for_async_process = time_sequence_value / min_time_value_for_async_process

    data = {'Количество процессов': index_list,
            'Время преобразования, сек': time_list}

    table = pd.DataFrame.from_dict(data).to_html(index=False, col_space=250)
    html += f'<p align="center">{table}</p>'

    html += '<h3 align="center">Минимальное время преобразования изображений:</h3>'
    html += f'<h2 align="center" style="color: red">{min_time_value_for_async_process} сек</h2>'

    html += '<h3 align="center">Достигнутое ускорение:</h3>'
    html += f'<h2 align="center" style="color: red">{acceleration_for_async_process: .1f}</h2>'

    fig, ax = plt.subplots(figsize=(10, 5))
    bars = plt.barh(index_list, time_list)
    ax.bar_label(bars, padding=2, color='blue', fontweight='bold')
    plt.xlabel('Время преобразования, сек')
    plt.ylabel('Количество процессов')
    plt.xticks([i for i in range(int(max(time_list)) + 1)])
    plt.yticks(index_list)
    plt.title('Зависимость времени преобразования от количества используемых процессов')
    plt.savefig(f'{path_report}\\figure_8.jpg')

    html += f'<center><img src="figure_8.jpg" border="1"/></center>'

    index_list = [i + 1 for i in range(6)]
    acceleration_list = [1.00,
                         round(acceleration_for_thread, 1),
                         round(acceleration_for_process, 1),
                         round(acceleration_for_async, 1),
                         round(acceleration_for_async_thread, 1),
                         round(acceleration_for_async_process, 1)]

    fig, ax = plt.subplots(figsize=(10, 7))
    colors = ['gray', 'red', 'green', 'blue', 'magenta', 'purple']
    legend = ['Последовательная реализация',
              'Мультипоточная реализация',
              'Мультипроцессная реализация',
              'Асинхронная реализация',
              'Асинхронно-мультипоточная реализация',
              'Асинхронно-мультипроцессная реализация']
    bar1 = plt.bar(index_list[0], acceleration_list[0], color=colors[0], width=0.5, label=legend[0])
    ax.bar_label(bar1, padding=2, color=colors[0], fontweight='bold')
    bar2 = plt.bar(index_list[1], acceleration_list[1], color=colors[1], width=0.5, label=legend[1])
    ax.bar_label(bar2, padding=2, color=colors[1], fontweight='bold')
    bar3 = plt.bar(index_list[2], acceleration_list[2], color=colors[2], width=0.5, label=legend[2])
    ax.bar_label(bar3, padding=2, color=colors[2], fontweight='bold')
    bar4 = plt.bar(index_list[3], acceleration_list[3], color=colors[3], width=0.5, label=legend[3])
    ax.bar_label(bar4, padding=2, color=colors[3], fontweight='bold')
    bar5 = plt.bar(index_list[4], acceleration_list[4], color=colors[4], width=0.5, label=legend[4])
    ax.bar_label(bar5, padding=2, color=colors[4], fontweight='bold')
    bar6 = plt.bar(index_list[5], acceleration_list[5], color=colors[5], width=0.5, label=legend[5])
    ax.bar_label(bar6, padding=2, color=colors[5], fontweight='bold')
    plt.legend()
    plt.xlabel('Способ реализации')
    plt.ylabel('Достигнутое ускорение')
    plt.xticks(index_list)
    plt.ylim(0, (int(max(acceleration_list) / 0.5) + 3) / 2)
    plt.title('Достигнутое ускорение при различных способах реализации')
    plt.savefig(f'{path_report}\\figure_9.jpg')

    html += f'<center><img src="figure_9.jpg" border="1" vspace="25"/></center>'

    with open(f'{path_report}\\{report_file}', mode='w') as html_file:
        html_file.write(html)

    print('Report generated successfully.')
