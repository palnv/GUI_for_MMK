from tkinter import *
from tkinter import ttk

from tkinter.ttk import Checkbutton

"""
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
Label(tab2, text="Ввод первичных данных по градуировке", font=("Arial Bold", 15)).place(x=10, y=10)
Label(tab2, text="Введите количество анализируемых элементов", font=("Arial Bold", 10)).place(x=10, y=70)
Label(tab2, text="Введите количество градуировочных растворов", font=("Arial Bold", 10)).place(x=10, y=100)

# выпадающий список
number = [1,2,3,4,5,6,7,8,9,10]

combobox_1 = ttk.Combobox(tab2,  values=number)
combobox_1.place(x=340, y=70)
combobox_1.current(1)

combobox_2 = ttk.Combobox(tab2,  values=number)
combobox_2.place(x=340, y=100)
combobox_2.current(3)


# програмка для кол-ва полей n
def pole_n():

    """
    програмка для кол-ва полей (в разработке)
    """

    try:
        pole_n_del()

    except: pass

    num_el = int(combobox_1.get())
    num_std = int(combobox_2.get())

    """
    табличка добавления массовой доли
    """
    global name_table_mass_dol # создаем глобальную переменную для названия таблички массовой доли
    name_table_mass_dol = Label(tab2, text="Массовая доля (%)", font=("Arial Bold", 10))
    name_table_mass_dol.place(x=10, y=150)

    gap_0 = 0 # горизонтальный пропуск для таблички массовой доли

    for e in range(num_el):

        globals()['lbl_el_m_d' + str(e)] = Label(tab2, text=f'Элемент_{e + 1}', font=("Arial Bold", 8))
        globals()['lbl_el_m_d' + str(e)].place(x=180+gap_0, y=180)

        gap_0 += 130

        gap_1 = 0  # вертикальный пропуск для таблички массовой доли

        for i in range(num_std):

            # создание таблички со стандартами
            if 'lbl_std_m_d' + str(i) not in globals():
                globals()['lbl_std_m_d' + str(i)] = Label(tab2, text=f'Стандарт_{i+1}', font=("Arial Bold", 8))
                globals()['lbl_std_m_d' + str(i)].place(x=40, y=200+gap_1)

            if 'lbl_ent_m_d' + str(e) + str(i) not in globals():
                globals()['lbl_ent_m_d' + str(e) + str(i)] = ttk.Entry(tab2)
                globals()['lbl_ent_m_d' + str(e) + str(i)].place(x=10+gap_0, y=200+gap_1)

            gap_1 += 23


    gap_0_itog_md = gap_0  # запомним размеры таблички массовой доли по горизонтали
    gap_0 = 0  # обнулим

    gap_1_itog_md = gap_1  # запомним размеры таблички массовой доли по вертикали
    gap_1 = 0  # обнулим


    """
    табличка добавления импульсов
    """

    global name_table_impuls  # создаем глобальную переменную для названия таблички массовой доли
    name_table_impuls = Label(tab2, text="Импульсы (cps)", font=("Arial Bold", 10))
    name_table_impuls.place(x=10, y=gap_1_itog_md + 250) # отталкиваемся от размеров предыдущей таблички

    # for e in range(num_el):
    #
    #     globals()['lbl_el_imp' + str(e)] = Label(tab2, text=f'Элемент_{e + 1}', font=("Arial Bold", 8))
    #     globals()['lbl_el_imp' + str(e)].place(x=180+gap_0, y=gap_1_itog_md + 180)
    #
    #     gap_0 += 130
    #
    #     for i in range(num_std):
    #
    #         # создание таблички со стандартами
    #         if 'lbl_std' + str(i) not in globals():
    #             globals()['lbl_std_imp' + str(i)] = Label(tab2, text=f'Стандарт_{i+1}', font=("Arial Bold", 8))
    #             globals()['lbl_std_imp' + str(i)].place(x=40, y=gap_1_itog_md + 200+gap_1)
    #
    #         if 'lbl_ent' + str(e) + str(i) not in globals():
    #             globals()['lbl_ent_imp' + str(e) + str(i)] = ttk.Entry(tab2)
    #             globals()['lbl_ent_imp' + str(e) + str(i)].place(x=10+gap_0, y=gap_1_itog_md + 200+gap_1)
    #
    #         gap_1 += 23





def pole_n_del():

    """
    програмка для удаления  полей (в разработке)
    """

    #num_std = int(combobox_1.get())
    #num_el = int(combobox_2.get())

    # удаляем табличку массовой доли
    name_table_mass_dol.destroy()

    for e in range(10):

        if 'lbl_el_m_d' + str(e) in globals():
            globals()['lbl_el_m_d' + str(e)].destroy()
            try:
                del globals()['lbl_el_m_d' + str(i)] # неясно почему c "i" работает, а с "e" нет
            except: pass

        # if 'lbl_el_imp' + str(e) in globals():
        #     globals()['lbl_el_imp' + str(e)].destroy()
        #     try:
        #         del globals()['lbl_std_imp' + str(e)]
        #     except: pass

        for i in range(10):

            if 'lbl_std_m_d' + str(i) in globals():
                globals()['lbl_std_m_d' + str(i)].destroy()
                try:
                    del globals()['lbl_std_m_d' + str(i)]
                except: pass

            if 'lbl_ent_m_d' + str(e) + str(i) in globals():
                globals()['lbl_ent_m_d' + str(e) + str(i)].destroy()
                try:
                    del globals()['lbl_ent_m_d' + str(e) + str(i)]
                except: pass

    # удаляем табличку импульсов
    name_table_impuls.destroy()




# кнопка при нажатии которой вылазит таблица, которую надо заполнить
ttk.Button(tab2, text="Заполнить", command=pole_n).place(x=510, y=85)

# кнопка удалении таблицы
ttk.Button(tab2, text="Все удалить", command=pole_n_del).place(x=610, y=85)



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