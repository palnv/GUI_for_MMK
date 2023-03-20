import numpy as np
import random
import sklearn.linear_model as lm
from sklearn.base import BaseEstimator



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

    def __init__(self, u_m=0.0002, u_mk=0.002, u_gso_steel=0.00001, u_gso_liq=0.005, u_razb=0.003, u_plt=0.002):

        self.u_m = u_m
        self.u_mk = u_mk
        self.u_gso_steel = u_gso_steel
        self.u_gso_liq = u_gso_liq
        self.u_razb = u_razb
        self.u_plt = u_plt

    def kalibrovka_tv_rsd(self, data_kalibr_num, data_blank_num, fit_int, blank_on_of):
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
            impuls_kal = random.normalvariate(data_kalibr_num[i][3], data_kalibr_num[i][3] * data_kalibr_num[i][4])
            m_naveska_kal = random.normalvariate(data_kalibr_num[i][0], data_kalibr_num[i][0] * self.u_mk)
            m_probirk_kal = random.normalvariate(data_kalibr_num[i][1], data_kalibr_num[i][1] * self.u_m)
            m_prob_r_kal = random.normalvariate(data_kalibr_num[i][2], data_kalibr_num[i][2] * self.u_m)
            razbavlenie_1_kal = random.normalvariate(data_kalibr_num[i][6], data_kalibr_num[i][6] * self.u_razb)
            el_proc_kal = random.normalvariate(data_kalibr_num[i][5], data_kalibr_num[i][5] * self.u_gso_steel)

            impuls_blank_kal = random.normalvariate(data_blank_num[0][0], data_blank_num[0][0] * data_blank_num[0][1])

            concentrac_kal = m_naveska_kal / (
                        m_prob_r_kal - m_probirk_kal) * 1000 / razbavlenie_1_kal * el_proc_kal / 100 * 1000

            # добавим бланк
            if blank_on_of:

                kalibr = np.append(kalibr, [[(impuls_kal - impuls_blank_kal), concentrac_kal]], axis=0)

            else:

                kalibr = np.append(kalibr, [[impuls_kal, concentrac_kal]], axis=0)

        # находим коэффициенты линейной регрессии

        x = (kalibr[:, 1]).reshape(-1, 1)
        y = kalibr[:, 0]

        skm = lm.LinearRegression(fit_intercept=fit_int)
        skm.fit(x, y)

        B = skm.coef_
        A = skm.intercept_

        kalibrov = {'A': A, 'B': B[0], 'corr': np.corrcoef(kalibr[:, 1], kalibr[:, 0])[0, 1]}

        return kalibrov

    def kalibrovka_liq_rsd(self, data_kalibr_liq, data_blank_num, fit_int, blank_on_of):
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
            impuls_kal_liq = random.normalvariate(data_kalibr_liq[i][3], data_kalibr_liq[i][3] * data_kalibr_liq[i][4])
            gso_kal_liq = random.normalvariate(data_kalibr_liq[i][0], (data_kalibr_liq[i][0]) * (self.u_gso_liq))
            razbavlenie_kal_liq = random.normalvariate(data_kalibr_liq[i][2], data_kalibr_liq[i][2] * self.u_razb)
            plt_kal_liq = random.normalvariate(data_kalibr_liq[i][1], data_kalibr_liq[i][1] * self.u_plt)

            impuls_blank_kal_liq = random.normalvariate(data_blank_num[0][0],
                                                        data_blank_num[0][0] * data_blank_num[0][1])

            concentrac_kal_liq = gso_kal_liq * 10 ** 6 / plt_kal_liq / razbavlenie_kal_liq

            if blank_on_of:
                kalibr_liq = np.append(kalibr_liq, [[(impuls_kal_liq - impuls_blank_kal_liq), concentrac_kal_liq]],
                                       axis=0)

            else:
                kalibr_liq = np.append(kalibr_liq, [[impuls_kal_liq, concentrac_kal_liq]], axis=0)

        # находим коэффициенты линейной регрессии

        x = (kalibr_liq[:, 1]).reshape(-1, 1)
        y = kalibr_liq[:, 0]

        skm = lm.LinearRegression(fit_intercept=fit_int)
        skm.fit(x, y)

        B = skm.coef_
        A = skm.intercept_

        kalibrov_liq = {'A': A, 'B': B[0], 'corr': np.corrcoef(kalibr_liq[:, 1], kalibr_liq[:, 0])[0, 1]}

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

        # result = np.zeros(0)





                # считаем содержание элемента в стали массовая доля %'

        impuls_prob = random.normalvariate(data_prob_num[4], data_prob_num[4] * data_prob_num[5])
        razbavlenie_1_prob = random.normalvariate(data_prob_num[3], data_prob_num[3] * self.u_razb)
        m_naveska_prob = random.normalvariate(data_prob_num[0], data_prob_num[0] * self.u_mk)
        m_prob_prob = random.normalvariate(data_prob_num[1], data_prob_num[1] * self.u_m)
        m_r_prob = random.normalvariate(data_prob_num[2], data_prob_num[2] * self.u_m)

        impuls_blank = random.normalvariate(data_blank_num[0][0],
                                            data_blank_num[0][0] * data_blank_num[0][1])

        # учет бланка
        if blank_on_of:
            concentac_prob = ((impuls_prob - impuls_blank) - A) / B
        else:
            concentac_prob = (impuls_prob - A) / B

        # учет холостой
        if holost_on_of:

            # находим содержание в холостой пробе

            xolost = np.zeros(0)

            for i in range(0, len(data_xol_num_i)):

                impuls_xol = random.normalvariate(data_xol_num_i[i][3], data_xol_num_i[i][3] * data_xol_num_i[i][4])
                razbavlenie_1_xol = random.normalvariate(data_xol_num_i[i][2], data_xol_num_i[i][2] * self.u_razb)
                m_r_xol = random.normalvariate(data_xol_num_i[i][1], data_xol_num_i[i][1] * self.u_m)
                m_prob_xol = random.normalvariate(data_xol_num_i[i][0], data_xol_num_i[i][0] * self.u_m)

                impuls_blank = random.normalvariate(data_blank_num[0][0],
                                                    data_blank_num[0][0] * data_blank_num[0][1])

                if blank_on_of:
                    concentac_xol = ((impuls_xol - impuls_blank) - A) / B
                else:
                    concentac_xol = (impuls_xol - A) / B

                soderganie_xol = concentac_xol * razbavlenie_1_xol / 1000 * (m_r_xol - m_prob_xol)

                if soderganie_xol > 0:
                    xolost = np.append(xolost, soderganie_xol)
                else:
                    xolost = np.append(xolost, 0)

            soderganie_prob = ((concentac_prob * razbavlenie_1_prob / 1000 * (m_r_prob - m_prob_prob)) - np.mean(
                xolost)) / \
                              1000 / m_naveska_prob * 100
        else:
            soderganie_prob = (concentac_prob * razbavlenie_1_prob / 1000 * (m_r_prob - m_prob_prob)) / \
                              1000 / m_naveska_prob * 100


        if holost_on_of:
            itog = {'sod': soderganie_prob, 'hol': np.mean(xolost)}
        else:
            itog = {'sod': soderganie_prob}

        return itog

    def mass_dol_r(self, v, data_prob_num, data_blank_num, data_xol_num_i, data_kalibr, c=1, \
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

        # result = np.zeros(0)



                # считаем содержание элемента в стали массовая доля %'

        impuls_prob = random.normalvariate(data_prob_num[0], data_prob_num[0] * data_prob_num[3])
        plt_prob = random.normalvariate(data_prob_num[1], data_prob_num[1] * self.u_plt)
        razbavlenie_prob = random.normalvariate(data_prob_num[2], data_prob_num[2] * self.u_razb)

        impuls_blank = random.normalvariate(data_blank_num[0][0],
                                            data_blank_num[0][0] * data_blank_num[0][1])

        # учет бланка
        if blank_on_of:
            concentac_prob = ((impuls_prob - impuls_blank) - A) / B
        else:
            concentac_prob = (impuls_prob - A) / B

        # учет холостой
        if holost_on_of:

            xolost = np.zeros(0)

            # находим содержание в холостой пробе

            for i in range(0, len(data_xol_num_i)):

                impuls_xol = random.normalvariate(data_xol_num_i[i][0], data_xol_num_i[i][0] * data_xol_num_i[i][3])
                plt_xol = random.normalvariate(data_xol_num_i[i][1], data_xol_num_i[i][1] * self.u_plt)
                razbavlenie_xol = random.normalvariate(data_xol_num_i[i][2], data_xol_num_i[i][2] * self.u_razb)

                impuls_blank = random.normalvariate(data_blank_num[0][0],
                                                    data_blank_num[0][0] * data_blank_num[0][1])

                if blank_on_of:
                    concentac_xol = ((impuls_xol - impuls_blank) - A) / B
                else:
                    concentac_xol = (impuls_xol - A) / B

                soderganie_xol = concentac_xol * plt_xol * razbavlenie_xol

                if soderganie_xol > 0:
                    xolost = np.append(xolost, soderganie_xol)
                else:
                    xolost = np.append(xolost, 0)

            soderganie_prob = (concentac_prob * plt_prob * razbavlenie_prob - np.mean(xolost)) / c
        else:
            soderganie_prob = (concentac_prob * plt_prob * razbavlenie_prob) / c

        if holost_on_of:
            itog = {'sod': soderganie_prob, 'hol': np.mean(xolost)}
        else:
            itog = {'sod': soderganie_prob}

        return itog