
def tables (name_p, text_name_table, text_name_str,\
            gap_b_v, gap_b_g, gap_gor_add, gap_vert_add, gap_dop_v, gap_dop_g,
            tab_n):
    """
    name_p - начало названия переменных (напр rsd)
    text_name_table - название таблички (напр "Неопределенность сигнала прибора (RSD)")
    text_name_str - название строк ("Стандарт" или "Проба")
    gap_b_v - вертикальный пробел м/у таблицами
    gap_b_g - горизонтальный пробел м/у таблицами
    gap_gor_add - маленький горизонтальный пробел м/у строками (gap_gor_add = 70)
    gap_vert_add - маленький вертикальный пробел м/у строками (gap_vert_add = 23)
    gap_dop_v - дополнительный вертикальный пробел (gap_170_add = 170)
    gap_dop_g - дополнительный горизонтальный пробел (gap_170_add = 170)
    tab_n - номер вкладки куда вставляется элемент (gap_210_add = 210)
    """

    gap_0 = 0

    num_el = int(combobox_3.get())
    num_std = int(combobox_4.get())

    #  название таблички
    globals()[name_p+'name_table'] = Label(tab_n, text=text_name_table, font=("Arial Bold", 10))
    globals()[name_p+'name_table'].place(x=gap_b_g+gap_dop_g, y=gap_b_v+gap_dop_v)  # отталкиваемся от размеров предыдущей таблички

        for e in range(num_el):

            globals()[name_p+'lbl_el' + str(e)] = Label(tab_n, text=text_name_str+f'_{e + 1}', font=("Arial Bold", 8))
            globals()[name_p+'lbl_el' + str(e)].place(x=gap_b_g+gap_dop_g+80+gap_0, y=gap_b_v+gap_dop_v + 20)

            gap_0 += gap_gor_add

            gap_3 = 0  # вертикальный пропуск для таблички массовой доли

            for i in range(num_std):

                if name_p+'lbl_std' + str(i) not in globals():
                    globals()[name_p+'lbl_std' + str(i)] = Label(tab_n, text=f'Стандарт_{i + 1}', font=("Arial Bold", 8))
                    globals()[name_p+'lbl_std' + str(i)].place(x=gap_b_g+gap_dop_g, y=gap_b_v+gap_dop_v + 40 + gap_3)

                if name_p+'lbl_ent' + str(e) + str(i) not in globals():
                    globals()[name_p+'lbl_ent' + str(e) + str(i)] = ttk.Entry(tab_n, width = 10)
                    globals()[name_p+'lbl_ent' + str(e) + str(i)].place(x=gap_b_g+gap_dop_g+10+gap_0, y=gap_b_v+gap_dop_v+40+gap_3)

                gap_3 += gap_vert_add
