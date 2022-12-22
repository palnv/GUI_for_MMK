from tkinter import *
from tkinter import ttk


from tkinter.ttk import Checkbutton

"""
- решить проблему рамок
- добавить возможность построения графиков с расчетом корелляции
"""


# начальное окно
window = Tk()
window.title("Рассчет неопределенности ММК")
window.geometry('1000x500')
#window.geometry("%dx%d" % (500, 300))

tab_control = ttk.Notebook(window)

# первая вкладка тип анализа
tab1 = ttk.Frame(tab_control)
tab_control.add(tab1, text='Тип расчета')

# текст 1 вкладки
lbl_1 = Label(tab1, text="Тип анализа", font=("Arial Bold", 15), padx=5, pady=5)
lbl_2 = Label(tab1, text="Тип градуировки", font=("Arial Bold", 15), padx=5, pady=5)
lbl_1.grid(column=0, row=0)
lbl_2.grid(column=1, row=0)

# чеккнопки
# переменная Tkinter
chk_state_1 = BooleanVar()
chk_state_2 = BooleanVar()
#начальное состояние
chk_state_1.set(False)
chk_state_2.set(False)

# галочки (тут не подходят)
# chk_1 = Checkbutton(tab1, text='Массовая доля в навеске', var=chk_state_1)
# chk_2 = Checkbutton(tab1, text='Массовая доля в растворе', var=chk_state_2)
# chk_3 = Checkbutton(tab1, text='Градуировка из навески', var=chk_state_3)
# chk_4 = Checkbutton(tab1, text='Градуировка из раствора', var=chk_state_4)

# создаем радиокнопки и сразу вставляем в вкладку
Radiobutton(tab1, text='Массовая доля в навеске', var=chk_state_1, value=0).grid(column=0, row=1)
Radiobutton(tab1, text='Массовая доля в растворе', var=chk_state_1, value=1).grid(column=0, row=2)
Radiobutton(tab1, text='Градуировка из навески', var=chk_state_2, value=0).grid(column=1, row=1)
Radiobutton(tab1, text='Градуировка из раствора', var=chk_state_2, value=1).grid(column=1, row=2)




# вторая вкладка ввод данных
tab2 = ttk.Frame(tab_control)
tab_control.add(tab2, text='Ввод данных градуировка')

# текст 2 вкладки
Label(tab2, text="Ввод первичных данных по градуировке", font=("Arial Bold", 15)).place(relx=0.05, rely=0.05)
Label(tab2, text="Введите количество анализируемых элементов", font=("Arial Bold", 10)).place(relx=0.05, rely=0.15)
Label(tab2, text="Введите количество градуировочных растворов", font=("Arial Bold", 10)).place(relx=0.05, rely=0.21)


# програмка для кол-ва полей n
def pole_n():

    """
    програмка для кол-ва полей (в разработке)
    """

    try:
        pole_n_del()

    except: pass

    global name_table # создаем глобальную переменную для названия таблички массовой доли
    name_table = Label(tab2, text="Массовая доля", font=("Arial Bold", 10))
    name_table.place(relx=0.05, rely=0.31)

    num_el = int(combobox_1.get())
    num_std = int(combobox_2.get())

    dob_0 = 0 # горизонтальный пропуск


    for e in range(num_el):

        globals()['lbl_el' + str(e)] = Label(tab2, text=f'Элемент_{e + 1}', font=("Arial Bold", 8))
        globals()['lbl_el' + str(e)].place(relx=0.25+dob_0, rely=0.33)

        dob_0 += 0.16

        dob_1 = 0  # вертикальный пропуск между строк надписей
        dob_2 = 0  # вертикальный пропуск между полями ввода

        for i in range(num_std):

            if 'lbl_std' + str(i) not in globals():
                globals()['lbl_std' + str(i)] = Label(tab2, text=f'Стандарт_{i+1}', font=("Arial Bold", 8))
                globals()['lbl_std' + str(i)].place(relx=0.05, rely=0.375+dob_1)

            if 'lbl_ent' + str(e) + str(i) not in globals():
                globals()['lbl_ent' + str(e) + str(i)] = ttk.Entry(tab2)
                globals()['lbl_ent' + str(e) + str(i)].place(relx=0.05+dob_0, rely=0.40+dob_2)

            dob_1 += 0.045
            dob_2 += 0.043

def pole_n_del():

    """
    програмка для удаления  полей (в разработке)
    """

    num_std = int(combobox_1.get())
    num_el = int(combobox_2.get())

    name_table.destroy()

    for e in range(10):

        if 'lbl_el' + str(e) in globals():

            globals()['lbl_el' + str(e)].destroy()
            try:
                del globals()['lbl_std' + str(i)]
            except: pass

        for i in range(10):

            if 'lbl_std' + str(i) in globals():
                globals()['lbl_std' + str(i)].destroy()
                try:
                    del globals()['lbl_std' + str(i)]
                except: pass

            if 'lbl_ent' + str(e) + str(i) in globals():
                globals()['lbl_ent' + str(e) + str(i)].destroy()
                try:
                    del globals()['lbl_ent' + str(e) + str(i)]
                except: pass



# кнопка при нажатии которой вылазит таблица, которую надо заполнить
ttk.Button(tab2, text="Заполнить", command=pole_n).place(relx=0.67, rely=0.18)

# кнопка удалении таблицы
ttk.Button(tab2, text="Все удалить", command=pole_n_del).place(relx=0.80, rely=0.18)

# выпадающий список
number = [1,2,3,4,5,6,7,8,9,10]

combobox_1 = ttk.Combobox(tab2,  values=number)
combobox_1.place(relx=0.45, rely=0.15)

combobox_2 = ttk.Combobox(tab2,  values=number)
combobox_2.place(relx=0.45, rely=0.22)





#combobox_1.bind("<<ComboboxSelected>>", pole_n)

# третья вкладка настройки
tab3 = ttk.Frame(tab_control)
tab_control.add(tab3, text='Параметры')
# текст 3 вкладки
lbl = Label(tab3, text="Параметры рассчета", font=("Arial Bold", 15))
lbl.grid(column=0, row=0)

# четвертая вкладка вывод результата
tab3 = ttk.Frame(tab_control)
tab_control.add(tab3, text='Результаты')
# текст 4 вкладки
lbl = Label(tab3, text="Результаты рассчета неопределенности", font=("Arial Bold", 15))
lbl.grid(column=0, row=0)

tab_control.pack(expand=1, fill='both')
window.mainloop()