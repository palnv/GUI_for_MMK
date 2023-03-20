
import un_choise as un
import class_data_load as cdl
import class_monte_karlo as cmk

import random

import os


if __name__ == '__main__':

    a = un.mmk(r'{}'.format(os.getcwd() + '\Вводные данные.xlsx'))

    a.choice()

    """
    отладка
    

    im = cdl.data_load(r'{}'.format(os.getcwd() + '\Вводные данные.xlsx'))

    s = 'Tb'

    mk = cmk.monte_carlo()

    data_prob_num = im.import_proba_mass_dol_r(s)['prob'].to_numpy()
    data_xol_num_i = im.import_proba_mass_dol_r(s)['hol'].to_numpy()
    data_blank_num = im.import_liq_gso(s)['blank'].to_numpy()
    data_kalibr_liq = im.import_liq_gso(s)['gso'].to_numpy()

    print(mk.mass_dol_r(2, data_prob_num[1], data_blank_num, data_xol_num_i, data_kalibr_liq)['sod'])

    """
