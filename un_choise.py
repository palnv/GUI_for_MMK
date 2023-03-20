import pandas as pd
import numpy as np
import random
import sklearn.linear_model as lm
from sklearn.base import BaseEstimator
import xlwings as xw

import class_data_load as cdl
import class_monte_karlo as cmk

import matplotlib.backends.backend_pdf
import matplotlib.pyplot as plt



from tqdm import tqdm


# внести изменения в def choice(self) и отладить


class mmk(BaseEstimator):
    """
    Класс автоматического выбора расчета
    
    Пока что только для:
     - массвой доле в навеске при жидком ГСО
     - массвой доле в растворе при жидком ГСО
    
    path - путь к файлу c данными
    """
    
    def __init__(self, path):
        
        self.path = path
                
    def choice(self):
        
        wb = xw.Book(self.path)
        
        # открываем лист с вводанными
        data_list = wb.sheets['Вводные данные'] 

        # считываем табличку с элементом/типом измерения
        data_el = data_list.range('B5:D15').options(pd.DataFrame, index = 1).value

        # считываем табличку с вводными данными
        data_param = data_list.range('B24:C34').options(pd.DataFrame, index = 1).value

        # удаляем пустые строки
        data_el.dropna(axis=0, inplace = True) 

        g = 0 # для отображения прогресса в exel
        el_prob = 0 # сквозное кол-во проб для всех элементов

        data_itog = wb.sheets['Итог']

        data_itog.range('B{}'.format(3)).value = 'РАБОТАЕТ...'

        for s in data_el.index:

            g =+ 1

            # заполнение таблички выполнения (название элемента)
            data_itog.range('B{}'.format(4 + g)).value = 'Расчет для {}'.format(s)

            # массовая доля в навеске, жидкий ГСО
            if ((data_el.loc[s,:]['Тип расчета'] == 1) & (data_el.loc[s,:]['Тип ГСО'] == 2)):

                fit_int = bool(int(data_param.loc['fit_int']))
                blank_on_of = bool(int(data_param.loc['blank']))
                holost_on_of = bool(int(data_param.loc['holost']))

                # объявим класс импорта данных
                im = cdl.data_load(self.path)

                # загрузка данных
                prob_r_num = im.import_proba_mass_dol_tv(s)['prob'].to_numpy()
                hol_r_num = im.import_proba_mass_dol_tv(s)['hol'].to_numpy()

                data_blank_num = im.import_liq_gso(s)['blank'].to_numpy()
                gso_3 = im.import_liq_gso(s)['gso'].to_numpy()


                prob_r = im.import_proba_mass_dol_tv(s)['prob']

                # объявим класс расчета неопределенности
                mk = cmk.monte_carlo(
                                    u_m=float(data_param.loc['u_m']),  
                                    u_mk=float(data_param.loc['u_mk']), 
                                    u_gso_steel=float(data_param.loc['u_gso_steel']), 
                                    u_gso_liq=float(data_param.loc['u_gso_liq']), 
                                    u_razb=float(data_param.loc['u_razb']), 
                                    u_plt=float(data_param.loc['u_plt'])
                                    )

                # сбор массива данных и расчет неопределенности

                itog = pd.DataFrame()

                for j in tqdm(range(0, len(prob_r_num))):

                    # отображение прогресса
                    data_itog.range('D{}'.format(5)).value = 'расчет {} '.format(j + 1) + 'из {}'.format(len(prob_r_num))

                    i = int(data_param.loc['i']) # количество итерации

                    result = []
                    for n in range(0,i):   
                        result.append(mk.mass_dol(2, prob_r_num[j], data_blank_num, hol_r_num, gso_3,
                                                     fit_int, blank_on_of, holost_on_of)['sod'])


                    result = pd.Series(result)
                    mean = result.mean()
                    U_abs = (result.quantile(0.975)-result.quantile(0.025))/2
                    U_proc = U_abs/mean * 100

                    itog.loc[j,'Проба'] = prob_r.index[j]

                    itog.loc[j,'{}, %'.format(s)] = mean  

                    itog.loc[j,'U({}), %'.format(s)] = U_proc


                # копирование итоговой таблицы для элемента в лист ИТОГ

                data_itog['G{}'.format(5 + el_prob)].options(pd.DataFrame, header=1, index=True, expand='table').value = itog
                el_prob = el_prob + len(prob_r_num) + 2
                
                # получение картинки и сохранение в папку в виде pdf
                
                # fig = plt.figure()
                # ax=fig.add_subplot(111)
                #
                # cell_text = []
                #
                # for row in range(len(itog)):
                #     cell_text.append(itog.iloc[row])
                #
                # ax.table(cellText=cell_text, colLabels=itog.columns, loc='center')
                # ax.axis('off')
                #
                # pdf = matplotlib.backends.backend_pdf.PdfPages("Расшир_неопред_{}.pdf".format(s))
                # pdf.savefig(fig)
                # pdf.close()

            # массовая доля в растворе при жидком ГСО
            elif ((data_el.loc[s, :]['Тип расчета'] == 2) & (data_el.loc[s, :]['Тип ГСО'] == 2)):

                fit_int = bool(int(data_param.loc['fit_int']))
                blank_on_of = bool(int(data_param.loc['blank']))
                holost_on_of = bool(int(data_param.loc['holost']))

                # объявим класс импорта данных
                im = cdl.data_load(self.path)

                # загрузка данных
                prob_r_num = im.import_proba_mass_dol_r(s)['prob'].to_numpy()
                hol_r_num = im.import_proba_mass_dol_r(s)['hol'].to_numpy()

                data_blank_num = im.import_liq_gso(s)['blank'].to_numpy()
                gso_3 = im.import_liq_gso(s)['gso'].to_numpy()

                prob_r = im.import_proba_mass_dol_r(s)['prob']

                # объявим класс расчета неопределенности
                mk = cmk.monte_carlo(
                    u_m=float(data_param.loc['u_m']),
                    u_mk=float(data_param.loc['u_mk']),
                    u_gso_steel=float(data_param.loc['u_gso_steel']),
                    u_gso_liq=float(data_param.loc['u_gso_liq']),
                    u_razb=float(data_param.loc['u_razb']),
                    u_plt=float(data_param.loc['u_plt'])
                )

                # сбор массива данных и расчет неопределенности

                itog = pd.DataFrame()

                for j in tqdm(range(0, len(prob_r_num))):

                    # отображение прогресса
                    data_itog.range('D{}'.format(5)).value = 'расчет {} '.format(j + 1) + 'из {}'.format(
                        len(prob_r_num))

                    i = int(data_param.loc['i'])

                    result = []
                    for n in range(0, i):
                        result.append(mk.mass_dol_r(2, prob_r_num[j], data_blank_num, hol_r_num, gso_3, 1, fit_int, blank_on_of, holost_on_of)['sod'])

                    result = pd.Series(result)
                    mean = result.mean()
                    U_abs = (result.quantile(0.975) - result.quantile(0.025)) / 2
                    U_proc = U_abs / mean * 100

                    itog.loc[j, 'Проба'] = prob_r.index[j]

                    itog.loc[j, '{}, мкг/кг'.format(s)] = mean

                    itog.loc[j, 'U({}), %'.format(s)] = U_proc


                # копирование итоговой таблицы для элемента в лист ИТОГ

                data_itog['G{}'.format(5 + el_prob)].options(pd.DataFrame, header=1, index=True,
                                                             expand='table').value = itog
                el_prob = el_prob + len(prob_r_num) + 2


            # массовая доля в навеске, твердый ГСО
            elif ((data_el.loc[s,:]['Тип расчета'] == 1) & (data_el.loc[s,:]['Тип ГСО'] == 1)):

                fit_int = bool(int(data_param.loc['fit_int']))
                blank_on_of = bool(int(data_param.loc['blank']))
                holost_on_of = bool(int(data_param.loc['holost']))

                # объявим класс импорта данных
                im = cdl.data_load(self.path)

                # загрузка данных
                prob_r_num = im.import_proba_mass_dol_tv(s)['prob'].to_numpy()
                hol_r_num = im.import_proba_mass_dol_tv(s)['hol'].to_numpy()

                data_blank_num = im.import_tv_gso(s)['blank'].to_numpy()
                gso_3 = im.import_tv_gso(s)['gso'].to_numpy()


                prob_r = im.import_proba_mass_dol_tv(s)['prob']

                # объявим класс расчета неопределенности
                mk = cmk.monte_carlo(
                                    u_m=float(data_param.loc['u_m']),
                                    u_mk=float(data_param.loc['u_mk']),
                                    u_gso_steel=float(data_param.loc['u_gso_steel']),
                                    u_gso_liq=float(data_param.loc['u_gso_liq']),
                                    u_razb=float(data_param.loc['u_razb']),
                                    u_plt=float(data_param.loc['u_plt'])
                                    )

                # сбор массива данных и расчет неопределенности

                itog = pd.DataFrame()

                for j in tqdm(range(0, len(prob_r_num))):

                    # отображение прогресса
                    data_itog.range('D{}'.format(5)).value = 'расчет {} '.format(j + 1) + 'из {}'.format(len(prob_r_num))

                    i = int(data_param.loc['i']) # количество итерации

                    result = []
                    for n in range(0,i):
                        result.append(mk.mass_dol(1, prob_r_num[j], data_blank_num, hol_r_num, gso_3,
                                                     fit_int, blank_on_of, holost_on_of)['sod'])


                    result = pd.Series(result)
                    mean = result.mean()
                    U_abs = (result.quantile(0.975)-result.quantile(0.025))/2
                    U_proc = U_abs/mean * 100

                    itog.loc[j,'Проба'] = prob_r.index[j]

                    itog.loc[j,'{}, %'.format(s)] = mean

                    itog.loc[j,'U({}), %'.format(s)] = U_proc


                # копирование итоговой таблицы для элемента в лист ИТОГ

                data_itog['G{}'.format(5 + el_prob)].options(pd.DataFrame, header=1, index=True, expand='table').value = itog
                el_prob = el_prob + len(prob_r_num) + 2

            # массовая доля в растворе при твердом ГСО
            elif ((data_el.loc[s, :]['Тип расчета'] == 2) & (data_el.loc[s, :]['Тип ГСО'] == 1)):

                fit_int = bool(int(data_param.loc['fit_int']))
                blank_on_of = bool(int(data_param.loc['blank']))
                holost_on_of = bool(int(data_param.loc['holost']))

                # объявим класс импорта данных
                im = cdl.data_load(self.path)

                # загрузка данных
                prob_r_num = im.import_proba_mass_dol_r(s)['prob'].to_numpy()
                hol_r_num = im.import_proba_mass_dol_r(s)['hol'].to_numpy()

                data_blank_num = im.import_liq_gso(s)['blank'].to_numpy()
                gso_3 = im.import_liq_gso(s)['gso'].to_numpy()

                prob_r = im.import_proba_mass_dol_r(s)['prob']

                # объявим класс расчета неопределенности
                mk = cmk.monte_carlo(
                    u_m=float(data_param.loc['u_m']),
                    u_mk=float(data_param.loc['u_mk']),
                    u_gso_steel=float(data_param.loc['u_gso_steel']),
                    u_gso_liq=float(data_param.loc['u_gso_liq']),
                    u_razb=float(data_param.loc['u_razb']),
                    u_plt=float(data_param.loc['u_plt'])
                )

                # сбор массива данных и расчет неопределенности

                itog = pd.DataFrame()

                for j in tqdm(range(0, len(prob_r_num))):

                    # отображение прогресса
                    data_itog.range('D{}'.format(5)).value = 'расчет {} '.format(j + 1) + 'из {}'.format(
                        len(prob_r_num))

                    i = int(data_param.loc['i'])

                    result = []
                    for n in range(0, i):
                        result.append(mk.mass_dol_r(2, prob_r_num[j], data_blank_num, hol_r_num, gso_3, 1, fit_int, blank_on_of, holost_on_of)['sod'])

                    result = pd.Series(result)
                    mean = result.mean()
                    U_abs = (result.quantile(0.975) - result.quantile(0.025)) / 2
                    U_proc = U_abs / mean * 100

                    itog.loc[j, 'Проба'] = prob_r.index[j]

                    itog.loc[j, '{}, мкг/кг'.format(s)] = mean

                    itog.loc[j, 'U({}), %'.format(s)] = U_proc


                # копирование итоговой таблицы для элемента в лист ИТОГ

                data_itog['G{}'.format(5 + el_prob)].options(pd.DataFrame, header=1, index=True,
                                                             expand='table').value = itog
                el_prob = el_prob + len(prob_r_num) + 2








        data_itog.range('B{}'.format(3)).value = 'ВЫПОЛНЕНО'

        wb.save()
    

