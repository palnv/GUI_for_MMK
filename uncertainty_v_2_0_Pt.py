import pandas as pd
import numpy as np
import random
import sklearn.linear_model as lm
from sklearn.base import BaseEstimator
import xlwings as xw

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

            #data_itog = wb.sheets['Итог']

            # заполнение таблички выполнения (название элемента)
            data_itog.range('B{}'.format(4 + g)).value = 'Расчет для {}'.format(s)

            if ((data_el.loc[s,:]['Тип расчета'] == 1) & (data_el.loc[s,:]['Тип ГСО'] == 2)):

                # объявим класс импорта данных
                im = data_load(self.path)

                # загрузка данных
                prob_r_num = im.import_proba_mass_dol_tv(s)['prob'].to_numpy()
                hol_r_num = im.import_proba_mass_dol_tv(s)['hol'].to_numpy()
                gso_3 = im.import_liq_gso(s).to_numpy()

                prob_r = im.import_proba_mass_dol_tv(s)['prob']

                # объявим класс расчета неопределенности
                mk = monte_carlo(
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

                    i = int(data_param.loc['i'])

                    result = []
                    for n in range(0,i):   
                        result.append(mk.mass_dol(2, prob_r_num[j], hol_r_num, gso_3, fit_int=bool(int(data_param.loc['fit_int'])))['sod'])
                    result = pd.Series(result)
                    mean = result.mean()
                    U_abs = (result.quantile(0.975)-result.quantile(0.025))/2
                    U_proc = U_abs/mean * 100

                    itog.loc[j,'Проба'] = prob_r.index[j]

                    itog.loc[j,'{}, %'.format(s)] = mean  

                    itog.loc[j,'U({}), %'.format(s)] = U_proc

                print(itog)

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

            elif ((data_el.loc[s, :]['Тип расчета'] == 2) & (data_el.loc[s, :]['Тип ГСО'] == 2)):

                # объявим класс импорта данных
                im = data_load(self.path)

                # загрузка данных
                prob_r_num = im.import_proba_mass_dol_r(s)['prob'].to_numpy()
                hol_r_num = im.import_proba_mass_dol_r(s)['hol'].to_numpy()
                gso_3 = im.import_liq_gso(s).to_numpy()

                prob_r = im.import_proba_mass_dol_r(s)['prob']

                # объявим класс расчета неопределенности
                mk = monte_carlo(
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
                        result.append(mk.mass_dol_r(2, prob_r_num[j], hol_r_num, gso_3, fit_int=bool(int(data_param.loc['fit_int'])))['sod'])
                    result = pd.Series(result)
                    mean = result.mean()
                    U_abs = (result.quantile(0.975) - result.quantile(0.025)) / 2
                    U_proc = U_abs / mean * 100

                    itog.loc[j, 'Проба'] = prob_r.index[j]

                    itog.loc[j, '{}, мкг/кг'.format(s)] = mean

                    itog.loc[j, 'U({}), %'.format(s)] = U_proc

                print(itog)

                # копирование итоговой таблицы для элемента в лист ИТОГ

                data_itog['G{}'.format(5 + el_prob)].options(pd.DataFrame, header=1, index=True,
                                                             expand='table').value = itog
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

        data_itog.range('B{}'.format(3)).value = 'ВЫПОЛНЕНО'

        wb.save()
    




class monte_carlo(BaseEstimator):
    
    """
    Класс для расчета случайных значений:
    - массовой доли элемента в навесе
    - массовой доля элемента в растворе 
    
    Аргументы класса: 
    u_m = 0.0002          - неопределенность взвешивания на обычных весах, отн.ед.
    u_mk = 0.002          - неопределенность взвешивания на микровесах, отн.ед.
    u_gso_steel = 0.00001 - неопределенность стандартов ГСО металла, отн.ед. (изготовленно из осч. металла)
    u_gso_liq = 0.005     - неопределенность стандартов ГСО жидких р-ров, отн.ед.
    u_razb = 0.003        - неопределенность разбавления, отн.ед.
    u_plt = 0.002         - неопределенность определения плотности
    """
    
    def __init__(self, u_m=0.0002,  u_mk=0.002, u_gso_steel=0.00001, u_gso_liq=0.005, u_razb=0.003, u_plt=0.002):
        
        self.u_m = u_m
        self.u_mk = u_mk
        self.u_gso_steel = u_gso_steel
        self.u_gso_liq = u_gso_liq
        self.u_razb = u_razb
        self.u_plt = u_plt
        
        
      
    def kalibrovka_tv_rsd(self, data_kalibr_num, data_blank_num,  fit_int, blank_on_of):
        '''
        однократные значения коэффициентов линейной регрессии, твердые ГСО с учетом индивидуальных RSD и бланка
        
        data_kalibr_num - табличка со стандартами после gso(e) или gso_cor(e) в виде numpy
        data_blank_num - табличка с данными бланка в numpy

        fit_int - параметр лин.регрессии fit_intercept, False - график не идет через ноль, True - привязка к нулю,
                  по умолчанию False

        blank_on_of - учитываем бланк или нет
                  
        ны выход: словарь с параметрами калибровки - A, B, corr
        расчет производится в мкг/кг  
        
        '''
          
        kalibr = np.zeros((0, 2))    
        for i in range(0, len(data_kalibr_num)): 

                # найдем источники неопределенности для калибровки с учетом нормального распределения
                impuls_kal = random.normalvariate(data_kalibr_num[i][3], data_kalibr_num[i][3]*data_kalibr_num[i][4])
                m_naveska_kal = random.normalvariate(data_kalibr_num[i][0], data_kalibr_num[i][0]*self.u_mk)          
                m_probirk_kal = random.normalvariate(data_kalibr_num[i][1], data_kalibr_num[i][1]*self.u_m)          
                m_prob_r_kal = random.normalvariate(data_kalibr_num[i][2], data_kalibr_num[i][2]*self.u_m)    
                razbavlenie_1_kal = random.normalvariate(data_kalibr_num[i][6], data_kalibr_num[i][6]*self.u_razb)
                el_proc_kal = random.normalvariate(data_kalibr_num[i][5], data_kalibr_num[i][5]*self.u_gso_steel)

                impuls_blank_kal = random.normalvariate(data_blank_num[0][0], data_blank_num[0][0]*data_blank_num[0][1])

                concentrac_kal =  m_naveska_kal/(m_prob_r_kal - m_probirk_kal)*1000 / razbavlenie_1_kal * el_proc_kal/100 * 1000

                # добавим бланк
                if blank_on_of:

                    kalibr = np.append(kalibr, [[(impuls_kal - impuls_blank_kal), concentrac_kal]], axis=0)

                else:

                    kalibr = np.append(kalibr, [[impuls_kal,concentrac_kal]], axis = 0)

        # находим коэффициенты линейной регрессии

        x = (kalibr[:,1]).reshape(-1, 1)
        y = kalibr[:,0]

        skm = lm.LinearRegression(fit_intercept=fit_int)
        skm.fit(x, y)

        B =  skm.coef_   
        A = skm.intercept_

        kalibrov = {'A': A, 'B': B[0], 'corr': np.corrcoef(kalibr[:,1], kalibr[:,0])[0,1]}

        return kalibrov
       
        
        
    def kalibrovka_liq_rsd(self, data_kalibr_liq, data_blank_num,  fit_int, blank_on_of):
        '''
        однократные значения коэффициентов линейной регрессии, жидкие ГСО c учетом индивидуальных RSD
        
        data_kalibr_liq - табличка со стандартами после gso_liq в виде numpy
        data_blank_num - табличка с данными бланка
        fit_int - параметр лин.регрессии fit_intercept, False - график не идет через ноль, True - привязка к нулю,
                  по умолчанию False

        blank_on_of - учитываем бланк или нет

                  
        ны выход: словарь с параметрами калибровки - A, B, corr
        расчет производится в мкг/кг
        
        '''
           
        kalibr_liq = np.zeros((0, 2))    
        for i in range(0, len(data_kalibr_liq)): 

                # найдем источники неопределенности для калибровки с учетом нормального распределения
                impuls_kal_liq = random.normalvariate(data_kalibr_liq[i][3], data_kalibr_liq[i][3]*data_kalibr_liq[i][4])
                gso_kal_liq = random.normalvariate(data_kalibr_liq[i][0], (data_kalibr_liq[i][0])*(self.u_gso_liq))
                razbavlenie_kal_liq = random.normalvariate(data_kalibr_liq[i][2], data_kalibr_liq[i][2]*self.u_razb)
                plt_kal_liq = random.normalvariate(data_kalibr_liq[i][1], data_kalibr_liq[i][1]*self.u_plt)

                impuls_blank_kal_liq = random.normalvariate(data_blank_num[0][0], data_blank_num[0][0]*data_blank_num[0][1])

                concentrac_kal_liq =  gso_kal_liq*10**6/plt_kal_liq/razbavlenie_kal_liq

                if blank_on_of:
                    kalibr_liq = np.append(kalibr_liq, [[(impuls_kal_liq-impuls_blank_kal_liq),concentrac_kal_liq]], axis = 0)

                else:
                    kalibr_liq = np.append(kalibr_liq, [[impuls_kal_liq, concentrac_kal_liq]], axis=0)

        # находим коэффициенты линейной регрессии

        x = (kalibr_liq[:,1]).reshape(-1, 1)
        y = kalibr_liq[:,0]

        skm = lm.LinearRegression(fit_intercept = fit_int)
        skm.fit(x, y)

        B =  skm.coef_   
        A = skm.intercept_

        kalibrov_liq = {'A': A, 'B': B[0],  'corr': np.corrcoef(kalibr_liq[:,1], kalibr_liq[:,0])[0,1]}

        return kalibrov_liq


    
    def mass_dol(self, v, data_prob_num, data_blank_num, data_xol_num_i, data_kalibr, \
                 fit_int=False, blank_on_of=True, holost_on_of=False):
    
        '''
        Однократное случайное значение массовой доли элемента в навеске c учетом индивидуальных rsd проб
        data_prob_num  - таблица с данными по пробам (numpy)
        data_xol_num_i - таблица с данными по холостым (numpy)
        data_kalibr    - таблица с данными по калибровке (numpy)
        data_blank_num - таблица с данными по бланку (numpy)
        v - выбор варианта калибровки, если 1 - ГСО металла, 2 - ГСО жидкие
        
        fit_int - параметр лин.регрессии fit_intercept, False - график не идет через ноль, True - привязка к нулю,
                  по умолчанию False

        blank_on_of - учет бланка (True/False)
        holost_on_of - учет холостой (True/False)
                  
        на выход: словарь со значенями пробы в % и значение холостой в ppb
        
        промежуточные расчеты и калибровка в ppb
        расчет итогового значения производится в % 
        
        '''

        # калибровочные коэффициенты, ПЕРЕДЕЛАТЬ: ДВАЖДЫ ВЫЗЫВАЕТСЯ ФУНКЦИЯ РАСЧЕТА КАЛИБРОВКИ

        if v == 1:
            A = self.kalibrovka_tv_rsd(data_kalibr, data_blank_num, fit_int, blank_on_of)['A']
            B = self.kalibrovka_tv_rsd(data_kalibr, data_blank_num, fit_int, blank_on_of)['B']
        elif v == 2:
            A = self.kalibrovka_liq_rsd(data_kalibr, data_blank_num, fit_int, blank_on_of)['A']
            B = self.kalibrovka_liq_rsd(data_kalibr, data_blank_num, fit_int, blank_on_of)['B']

        #result = np.zeros(0)

        xolost = np.zeros(0)

        # находим содержание в холостой пробе

        for i in range(0, len(data_xol_num_i)):

            impuls_xol = random.normalvariate(data_xol_num_i[i][3], data_xol_num_i[i][3]*data_xol_num_i[i][4])
            razbavlenie_1_xol = random.normalvariate(data_xol_num_i[i][2], data_xol_num_i[i][2]*self.u_razb)
            m_r_xol = random.normalvariate(data_xol_num_i[i][1], data_xol_num_i[i][1]*self.u_m)
            m_prob_xol = random.normalvariate(data_xol_num_i[i][0], data_xol_num_i[i][0]*self.u_m)

            impuls_blank = random.normalvariate(data_blank_num[0][0],
                                                        data_blank_num[0][0] * data_blank_num[0][1])

            if blank_on_of:
                concentac_xol = ((impuls_xol-impuls_blank) - A) / B
            else:
                concentac_xol = (impuls_xol - A) / B

            soderganie_xol = concentac_xol*razbavlenie_1_xol/1000*(m_r_xol - m_prob_xol)

            if soderganie_xol > 0:                
                xolost = np.append(xolost, soderganie_xol)                
            else:
                xolost = np.append(xolost, 0)  

        # считаем содержание элемента в стали массовая доля %'

        impuls_prob = random.normalvariate(data_prob_num[4], data_prob_num[4]*data_prob_num[5])
        razbavlenie_1_prob = random.normalvariate(data_prob_num[3], data_prob_num[3]*self.u_razb)
        m_naveska_prob = random.normalvariate(data_prob_num[0], data_prob_num[0]*self.u_mk)
        m_prob_prob = random.normalvariate(data_prob_num[1], data_prob_num[1]*self.u_m)
        m_r_prob = random.normalvariate(data_prob_num[2], data_prob_num[2]*self.u_m)

        impuls_blank = random.normalvariate(data_blank_num[0][0],
                                                    data_blank_num[0][0] * data_blank_num[0][1])

        # учет бланка
        if blank_on_of:
            concentac_prob = ((impuls_prob-impuls_blank) - A) / B
        else:
            concentac_prob = (impuls_prob - A) / B

        # учет холостой
        if holost_on_of:
            soderganie_prob = ((concentac_prob*razbavlenie_1_prob/1000*(m_r_prob - m_prob_prob)) - np.mean(xolost))/ \
                            1000/m_naveska_prob*100
        else:
            soderganie_prob = (concentac_prob * razbavlenie_1_prob / 1000 * (m_r_prob - m_prob_prob)) / \
                            1000 / m_naveska_prob * 100
        
        itog = {'sod': soderganie_prob, 'hol': np.mean(xolost)}

        return itog


    def mass_dol_r(self, v, data_prob_num, data_blank_num, data_xol_num_i, data_kalibr, с = 1, \
                   fit_int=False, blank_on_of=True, holost_on_of=False):

        '''
        Однократное случайное значение массовой доли элемента в растворе в мг либо мкг/кг 
        v - выбор варианта калибровки, если 1 - ГСО металла, 2 - ГСО жидкие
        
        data_prob_num  - таблица с данными по пробам (numpy)
        data_xol_num_i - таблица с данными по холостым (numpy)
        data_kalibr    - таблица с данными по калибровке (numpy)
       
        с - 1000 - рез-ты в мг/кг, с = 1 рез-ты в мкг/кг
        
        fit_int - параметр лин.регрессии fit_intercept, False - график не идет через ноль, True - привязка к нулю,
                  по умолчанию False

        blank_on_of - учет бланка (True/False)
        holost_on_of - учет холостой (True/False)

        на выход: словарь со значенями пробы в ppb и значение холостой в ppb
        
        промежуточные расчеты и калибровка в ppb
        расчет итогового значения производится в ppb
        
        '''

        # калибровочные коэффициенты (расчет в мкг/кг)

        if v == 1:
            A = self.kalibrovka_tv_rsd(data_kalibr, data_blank_num, fit_int, blank_on_of)['A']
            B = self.kalibrovka_tv_rsd(data_kalibr, data_blank_num, fit_int, blank_on_of)['B']
        elif v == 2:
            A = self.kalibrovka_liq_rsd(data_kalibr, data_blank_num, fit_int, blank_on_of)['A']
            B = self.kalibrovka_liq_rsd(data_kalibr, data_blank_num, fit_int, blank_on_of)['B']

        #result = np.zeros(0)

        xolost = np.zeros(0)

        # находим содержание в холостой пробе

        for i in range(0, len(data_xol_num_i)):

            impuls_xol = random.normalvariate(data_xol_num_i[i][0], data_xol_num_i[i][0]*data_xol_num_i[i][3])
            plt_xol = random.normalvariate(data_xol_num_i[i][1], data_xol_num_i[i][1]*self.u_plt)
            razbavlenie_xol = random.normalvariate(data_xol_num_i[i][2], data_xol_num_i[i][2]*self.u_razb)

            impuls_blank = random.normalvariate(data_blank_num[0][0],
                                                data_blank_num[0][0] * data_blank_num[0][1])

            if blank_on_of:
                concentac_xol = ((impuls_xol-impuls_blank) - A) / B
            else:
                concentac_xol = (impuls_xol - A) / B

            soderganie_xol = concentac_xol*plt_xol*razbavlenie_xol

            if soderganie_xol > 0:                
                xolost = np.append(xolost, soderganie_xol)                
            else:
                xolost = np.append(xolost, 0)  

        # считаем содержание элемента в стали массовая доля %'

        impuls_prob = random.normalvariate(data_prob_num[0], data_prob_num[0]*data_prob_num[3])
        plt_prob = random.normalvariate(data_prob_num[1], data_prob_num[1]*self.u_plt)
        razbavlenie_prob = random.normalvariate(data_prob_num[2], data_prob_num[2]*self.u_razb)

        impuls_blank = random.normalvariate(data_blank_num[0][0],
                                            data_blank_num[0][0] * data_blank_num[0][1])

        # учет бланка
        if blank_on_of:
            concentac_prob = ((impuls_prob-impuls_blank) - A) / B
        else:
            concentac_prob = (impuls_prob - A) / B

        # учет холостой
        if holost_on_of:
            soderganie_prob = (concentac_prob * plt_prob * razbavlenie_prob - np.mean(xolost)) / с
        else:
            soderganie_prob = (concentac_prob * plt_prob * razbavlenie_prob) / с

        itog = {'sod': soderganie_prob, 'hol': np.mean(xolost)}

        return itog

    
    
    
    
    
    
    
    
    
    
    
class data_load(BaseEstimator):
    
    """
    Класс для: 
    - загрузки данных из excel
    - приведение данных по пробам в numpy
    - приведение данных по ГСО в numpy  
    
    path - путь к файлу
    
    """
    
    def __init__(self, path):
        
        self.wb = xw.Book(path)
         
    def import_liq_gso(
        self, 
        e, 
        name_list          = 'ГСО жидкие', 
        diap_std_liq_gso   = 'B10:G30', 
        diap_std_liq_plotn = 'I10:N30', 
        diap_std_liq_k     = 'P10:U30',
        diap_std_liq_imp   = 'W10:AB30',
        diap_std_liq_rsd   = 'AD10:AI30',
        diap_std_liq_blank_imp = 'AK10:AP11',
        diap_std_liq_blank_rsd = 'AK16:AP17'
                       ):
        
        """
        Функция загрузки и обработки данных по жидким ГСО: по умолчанию на 5 элементов по 4 град. р-ра
        + данные бланка
        
        e - элемент
        
        name_list          = 'ГСО жидкие' - название листа с данными по жидким ГСО
        diap_std_liq_gso   = 'B10:G30'    - диапазон считывания данных по содержанию элемента в ГСО мг/см.куб (г/литр) 
        diap_std_liq_plotn = 'I10:N30'    - диапазон считывания данных по плотности
        diap_std_liq_k     = 'P10:U30'    - диапазон считывания данных по степени разбавления k
        diap_std_liq_imp   = 'W10:AB30'   - диапазон считывания данных по значению импульсов
        diap_std_liq_rsd   = 'AD10:AI30'  - диапазон считывания данных по значению rsd
        diap_std_liq_blank_imp = 'AK10:AP11' - диапазон считывания данных по импульсам бланка
        diap_std_liq_blank_rsd = 'AK16:AP17' - диапазон считывания данных по rsd для бланка
        
        На выходе pandas табличка с данными по градуировке
        
        """
        
        # открываем лист с данными
        gso_liq = self.wb.sheets[name_list] 
        # считываем данные по содержанию элемента в ГСО мг/см.куб (г/литр)
        std_liq_gso = gso_liq.range(diap_std_liq_gso).options(pd.DataFrame, index = 1).value
        # считываем данные по плотности
        std_liq_plotn = gso_liq.range(diap_std_liq_plotn).options(pd.DataFrame, index = 1).value
        # степень разбавления k
        std_liq_k = gso_liq.range(diap_std_liq_k).options(pd.DataFrame, index = 1).value
        # значение импульсов
        std_liq_imp = gso_liq.range(diap_std_liq_imp).options(pd.DataFrame, index = 1).value
        # значения rsd 
        std_liq_rsd = gso_liq.range(diap_std_liq_rsd).options(pd.DataFrame, index = 1).value
        # значение импульсов по бланку
        std_liq_blank_imp = gso_liq.range(diap_std_liq_blank_imp).options(pd.DataFrame, index = 1).value
        # значение rsd по бланку
        std_liq_blank_rsd = gso_liq.range(diap_std_liq_blank_rsd).options(pd.DataFrame, index = 1).value
        
        pds = pd.DataFrame(index = std_liq_gso.index)
        gso_liq_el = pds.join(std_liq_gso[e]).join(std_liq_plotn['{}_plt'.format(e)]).join(std_liq_k['{}_k'.format(e)])    \
        .join(std_liq_imp['{}_imp'.format(e)]).join(std_liq_rsd['{}_rsd'.format(e)])

        gso_liq_el_bl = std_liq_blank_imp.filter(like=e).join(std_liq_blank_rsd.filter(like=e))

        gso_liq_el['soderg, ppb'] = gso_liq_el[e]*10**6/gso_liq_el['{}_plt'.format(e)]/gso_liq_el['{}_k'.format(e)]    

        gso_liq_el.dropna(axis=0, inplace = True)

        itog_liq_gso = {'gso': gso_liq_el, 'blank': gso_liq_el_bl}
        
        return itog_liq_gso
        
    
    def import_tv_gso  (
        
        self, 
        e, 
        name_list             = 'ГСО сталь', 
        diap_data_gso_conc    = 'C10:F14', 
        diap_data_gso_imp     = 'C19:F23', 
        diap_data_gso_rsd     = 'C27:F31',
        diap_data_gso_probirk = 'C36:L40',
        diap_data_gso_razbavl = 'C44:F48',
        diap_data_gso_bl_imp  = 'C54:F55',
        diap_data_gso_bl_rsd  = 'C59:E60'
                       ):
        
        """
        Функция загрузки и обработки данных по твердым ГСО: по умолчанию на 3 элемента и 4 град. р-ра
        + данные бланка
      
        e - элемент 
        
        name_list             = 'ГСО сталь' - название листа с данными по твердым ГСО
        diap_data_gso_conc    = 'C10:F14'   - диапазон считывания данных по массовой доле
        diap_data_gso_imp     = 'C19:F23'   - диапазон считывания данных по импульсам
        diap_data_gso_rsd     = 'C27:F31'   - диапазон считывания данных по rsd
        diap_data_gso_probirk = 'C36:L40'   - диапазон считывания данных по переводу в пробирку
        diap_data_gso_razbavl = 'C44:F48'   - диапазон считывания данных по разбавлению
        diap_data_gso_bl_imp  = 'C54:F55'   - диапазон считывания данных по импульсам бланка
        diap_data_gso_bl_rsd  = 'C59:E60'   - диапазон считывания данных по rsd бланка
        
        На выходе pandas табличка с данными по градуировке
        
        """
    
        # открываем лист с данными
        data_gso_steel = self.wb.sheets[name_list] # Читаем лист Данные
        # считываем данные по массовой доле 
        data_gso_conc = data_gso_steel.range(diap_data_gso_conc).options(pd.DataFrame, index = 1).value
        # считываем данные по импульсам
        data_gso_imp = data_gso_steel.range(diap_data_gso_imp).options(pd.DataFrame, index = 1).value
        # данные по rsd
        data_gso_rsd = data_gso_steel.range(diap_data_gso_rsd).options(pd.DataFrame, index = 1).value
        # перевод в пробирку
        data_gso_probirk = data_gso_steel.range(diap_data_gso_probirk).options(pd.DataFrame, index = 1).value
        # разбавление
        data_gso_razbavl = data_gso_steel.range(diap_data_gso_razbavl).options(pd.DataFrame, index = 1).value
        # импульсы бланка
        data_gso_bl_imp = data_gso_steel.range(diap_data_gso_bl_imp).options(pd.DataFrame, index = 1).value
        # rsd бланка
        data_gso_bl_rsd = data_gso_steel.range(diap_data_gso_bl_rsd).options(pd.DataFrame, index = 1).value

        
        gso_tabl_el = data_gso_probirk.filter(like=e).join(data_gso_imp['{}_imp'.format(e)]).join(data_gso_rsd['{}_rsd'.format(e)]).join(data_gso_conc[e]).join(data_gso_razbavl.filter(like=e), how = 'inner')

        data_gso_bl = data_gso_bl_imp.filter(like=e).join(data_gso_bl_rsd.filter(like=e))


        gso_tabl_el['soderg, ppb'] = (gso_tabl_el['м нав, мг {}'.format(e)]/(gso_tabl_el['м пр+р-р, г {}'.format(e)] - gso_tabl_el['м проб, г {}'.format(e)]))*1000 / \
        gso_tabl_el['разб {}'.format(e)] * gso_tabl_el[e]/100*1000    
    
        gso_tabl_el.dropna(axis=0, inplace = True)

        gso_tabl_itog = {'gso': gso_tabl_el, 'blank': data_gso_bl}
        
        return gso_tabl_itog
    
            
    
    def import_proba_mass_dol_r  (
        
        self, 
        e, 
        name_list             = 'Пробы_мд_раств', 
        diap_proba_r_imp    = 'C4:F12', 
        diap_proba_r_plt     = 'C16:F24', 
        diap_proba_r_k     = 'C28:F36',
        diap_proba_r_rsd = 'C40:F48',
        
        diap_proba_r_holost_imp = 'I4:L6',
        diap_proba_r_holost_plt = 'I16:L18',
        diap_proba_r_holost_k = 'I28:L30', 
        diap_proba_r_holost_rsd = 'I40:L42'
                                  ):
        
        """
        Функция загрузки и обработки данных по жидким пробам: по умолчанию на 3 элемента и 8 проб, 2 холостые
      
        e - элемент 
        
        name_list             = 'Пробы_мд_раств' - название листа с данными по пробам
        
        diap_proba_r_imp       = 'C4:F12'    - диапазон считывания данных по импульсам
        diap_proba_r_plt       = 'C16:F24'   - диапазон считывания данных по плотности
        diap_proba_r_k         = 'C28:F36'   - диапазон считывания данных по k разбавлению
        diap_proba_r_rsd       = 'C40:F48'   - диапазон считывания данных по rsd
        
        diap_proba_r_holost_imp  = 'I4:L6',   - диапазон считывания данных холостой по импульсам
        diap_proba_r_holost_plt  = 'I16:L18'  - диапазон считывания данных холостой по плотности
        diap_proba_r_holost_k    = 'I28:L30'  - диапазон считывания данных холостой по k разбавлению
        diap_proba_r_holost_rsd  = 'I40:L42'  - диапазон считывания данных холостой по rsd
              
        На выходе pandas табличка с данными с пробами и холостой
        
        """      
    
        # открываем лист с данными
        proba_r = self.wb.sheets[name_list] # Читаем лист Данные

        # данные по импульсам
        proba_r_imp = proba_r.range(diap_proba_r_imp).options(pd.DataFrame, index = 1).value

        # данные по плотности
        proba_r_plt = proba_r.range(diap_proba_r_plt).options(pd.DataFrame, index = 1).value

        # данные по разбавлению
        proba_r_k = proba_r.range(diap_proba_r_k).options(pd.DataFrame, index = 1).value

        # данные по rsd
        proba_r_rsd = proba_r.range(diap_proba_r_rsd).options(pd.DataFrame, index = 1).value


        # холостые данные по импульсам
        proba_r_holost_imp = proba_r.range(diap_proba_r_holost_imp).options(pd.DataFrame, index = 1).value

        # холостые данные по плотности
        proba_r_holost_plt = proba_r.range(diap_proba_r_holost_plt).options(pd.DataFrame, index = 1).value

        # холостые данные по разбавлению
        proba_r_holost_k = proba_r.range(diap_proba_r_holost_k).options(pd.DataFrame, index = 1).value

        # холостые данные по rsd
        proba_r_holost_rsd = proba_r.range(diap_proba_r_holost_rsd).options(pd.DataFrame, index = 1).value
    
    
        prob_r_all = proba_r_imp.join(proba_r_plt).join(proba_r_k).join(proba_r_rsd) 
        prob_r_el = prob_r_all[['{}_imp'.format(e),'{}_plt'.format(e),'{}_k'.format(e),'{}_rsd'.format(e)]]
        prob_r_el.dropna(axis=0, inplace=True)

        hol_r_all = proba_r_holost_imp.join(proba_r_holost_plt).join(proba_r_holost_k).join(proba_r_holost_rsd) 
        hol_r_el = hol_r_all[['{}_imp'.format(e),'{}_plt'.format(e),'{}_k'.format(e),'{}_rsd'.format(e)]]
        hol_r_el.dropna(axis=0, inplace=True)

        itog = {'prob': prob_r_el, 'hol': hol_r_el}

        return itog
    
    
    def import_proba_mass_dol_tv  (
        
        self, 
        e, 
        name_list                     = 'Пробы_мд_нав', 
        diap_data_proba_steel         = 'B2:F9', 
        diap_data_proba_steel_imp     = 'B13:E20', 
        diap_data_proba_steel_rsd     = 'B24:E31',
  
        diap_data_holost_stell        = 'B35:E38',
        diap_data_holost_stell_imp    = 'B41:E44',
        diap_data_holost_stell_rsd    = 'B47:E50',
                                   ):
        
        """
        Функция загрузки и обработки данных по твердым пробам: по умолчанию на 3 элемента и 7 проб, 3 холостые пробы
      
        e - элемент 
        
        name_list             = 'Пробы_мд_нав' - название листа с данными по пробам
        
        diap_data_proba_steel         = 'B2:F9'   -  диапазон считывания данных по переводу в пробирки и разбавлению
        diap_data_proba_steel_imp     = 'B13:E20' -  диапазон считывания данных по импульсам
        diap_data_proba_steel_rsd     = 'B24:E31' -  диапазон считывания данных по rsd проб
        
        diap_data_holost_stell        = 'B35:E38'    -  диапазон считывания данных холостой по переводу в пробирки и разбавлению
        diap_data_holost_stell_imp    = 'B41:E44'      -  диапазон считывания данных холостой по импульсам
        diap_data_holost_stell_rsd    = 'B47:E50'    -  диапазон считывания данных холостой по rsd проб
              
        На выходе pandas табличка с данными с пробами и холостой
        
        """      
    
        # открываем лист с данными
        proba_steel = self.wb.sheets[name_list] # Читаем лист Данные

        #данные по переводу в пробирки и разбавлению
        data_proba_steel = proba_steel.range(diap_data_proba_steel).options(pd.DataFrame, index = 1).value

        #данные для проб импульсы
        data_proba_steel_imp = proba_steel.range(diap_data_proba_steel_imp).options(pd.DataFrame, index = 1).value

        #данные для проб rsd
        data_proba_steel_rsd = proba_steel.range(diap_data_proba_steel_rsd).options(pd.DataFrame, index = 1).value

        #данные по холостой разбавление
        data_holost_stell = proba_steel.range(diap_data_holost_stell).options(pd.DataFrame, index = 1).value

        #данные холостой по переводу в пробирки и разбавлению
        data_holost_stell_imp = proba_steel.range(diap_data_holost_stell_imp).options(pd.DataFrame, index = 1).value

        #данные по холостой rsd
        data_holost_stell_rsd = proba_steel.range(diap_data_holost_stell_rsd).options(pd.DataFrame, index = 1).value
    
    
        data_prob = data_proba_steel.join(data_proba_steel_imp['{}_imp'.format(e)]).join(data_proba_steel_rsd['{}_rsd'.format(e)]).iloc[:, 0:7]
        data_prob.dropna(axis=0, inplace = True)  

        data_xol = data_holost_stell.join(data_holost_stell_imp['{}_imp'.format(e)]).join(data_holost_stell_rsd['{}_rsd'.format(e)]).iloc[:, 0:6]
        
        data_xol.dropna(axis=0, inplace = True)  
        
        itog = {'prob': data_prob, 'hol': data_xol}

        return itog    
    

    
    
    

    
    

    