"""
    табличка rsd
    """
    global name_table_rsd_proba  #  название таблички
    name_table_rsd_proba = Label(tab3, text="Неопределенность сигнала прибора (RSD)", font=("Arial Bold", 10))
    name_table_rsd_proba.place(x=gap_0_itog_md+170, y=gap_1_itog_md + 210)  # отталкиваемся от размеров предыдущей таблички

    for e in range(num_el):

        globals()['lbl_el_rsd_proba' + str(e)] = Label(tab3, text=f'Проба_{e + 1}', font=("Arial Bold", 8))
        globals()['lbl_el_rsd_proba' + str(e)].place(x=gap_0_itog_md+v.gap_250_add + gap_0, y=gap_1_itog_md + 230)

        gap_0 += v.gap_gor_add

        gap_3 = 0  # вертикальный пропуск для таблички массовой доли

        for i in range(num_std):

            if 'lbl_std_rsd_proba' + str(i) not in globals():
                globals()['lbl_std_rsd_proba' + str(i)] = Label(tab3, text=f'Проба_{i + 1}', font=("Arial Bold", 8))
                globals()['lbl_std_rsd_proba' + str(i)].place(x=gap_0_itog_md+170, y=gap_1_itog_md + 250 + gap_3)

            if 'lbl_ent_rsd_proba' + str(e) + str(i) not in globals():
                globals()['lbl_ent_rsd_proba' + str(e) + str(i)] = ttk.Entry(tab3, width = 10)
                globals()['lbl_ent_rsd_proba' + str(e) + str(i)].place(x=gap_0_itog_md+180 + gap_0, y=gap_1_itog_md + 250 + gap_3)

            gap_3 += v.gap_vert_add
