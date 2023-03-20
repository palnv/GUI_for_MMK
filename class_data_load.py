import pandas as pd
from sklearn.base import BaseEstimator
import xlwings as xw


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
            name_list='ГСО жидкие',
            diap_std_liq_gso='B10:G30',
            diap_std_liq_plotn='I10:N30',
            diap_std_liq_k='P10:U30',
            diap_std_liq_imp='W10:AB30',
            diap_std_liq_rsd='AD10:AI30',
            diap_std_liq_blank_imp='AK10:AP11',
            diap_std_liq_blank_rsd='AK16:AP17'
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
        std_liq_gso = gso_liq.range(diap_std_liq_gso).options(pd.DataFrame, index=1).value
        # считываем данные по плотности
        std_liq_plotn = gso_liq.range(diap_std_liq_plotn).options(pd.DataFrame, index=1).value
        # степень разбавления k
        std_liq_k = gso_liq.range(diap_std_liq_k).options(pd.DataFrame, index=1).value
        # значение импульсов
        std_liq_imp = gso_liq.range(diap_std_liq_imp).options(pd.DataFrame, index=1).value
        # значения rsd
        std_liq_rsd = gso_liq.range(diap_std_liq_rsd).options(pd.DataFrame, index=1).value
        # значение импульсов по бланку
        std_liq_blank_imp = gso_liq.range(diap_std_liq_blank_imp).options(pd.DataFrame, index=1).value
        # значение rsd по бланку
        std_liq_blank_rsd = gso_liq.range(diap_std_liq_blank_rsd).options(pd.DataFrame, index=1).value

        pds = pd.DataFrame(index=std_liq_gso.index)
        gso_liq_el = pds.join(std_liq_gso[e]).join(std_liq_plotn['{}_plt'.format(e)]).join(std_liq_k['{}_k'.format(e)]) \
            .join(std_liq_imp['{}_imp'.format(e)]).join(std_liq_rsd['{}_rsd'.format(e)])

        gso_liq_el_bl = std_liq_blank_imp.filter(like=e).join(std_liq_blank_rsd.filter(like=e))

        gso_liq_el['soderg, ppb'] = gso_liq_el[e] * 10 ** 6 / gso_liq_el['{}_plt'.format(e)] / gso_liq_el[
            '{}_k'.format(e)]

        gso_liq_el.dropna(axis=0, inplace=True)

        itog_liq_gso = {'gso': gso_liq_el, 'blank': gso_liq_el_bl}

        return itog_liq_gso

    def import_tv_gso(

            self,
            e,
            name_list='ГСО сталь',
            diap_data_gso_conc='C10:F14',
            diap_data_gso_imp='C19:F23',
            diap_data_gso_rsd='C27:F31',
            diap_data_gso_probirk='C36:L40',
            diap_data_gso_razbavl='C44:F48',
            diap_data_gso_bl_imp='C54:F55',
            diap_data_gso_bl_rsd='C59:E60'
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
        data_gso_steel = self.wb.sheets[name_list]  # Читаем лист Данные
        # считываем данные по массовой доле
        data_gso_conc = data_gso_steel.range(diap_data_gso_conc).options(pd.DataFrame, index=1).value
        # считываем данные по импульсам
        data_gso_imp = data_gso_steel.range(diap_data_gso_imp).options(pd.DataFrame, index=1).value
        # данные по rsd
        data_gso_rsd = data_gso_steel.range(diap_data_gso_rsd).options(pd.DataFrame, index=1).value
        # перевод в пробирку
        data_gso_probirk = data_gso_steel.range(diap_data_gso_probirk).options(pd.DataFrame, index=1).value
        # разбавление
        data_gso_razbavl = data_gso_steel.range(diap_data_gso_razbavl).options(pd.DataFrame, index=1).value
        # импульсы бланка
        data_gso_bl_imp = data_gso_steel.range(diap_data_gso_bl_imp).options(pd.DataFrame, index=1).value
        # rsd бланка
        data_gso_bl_rsd = data_gso_steel.range(diap_data_gso_bl_rsd).options(pd.DataFrame, index=1).value

        gso_tabl_el = data_gso_probirk.filter(like=e).join(data_gso_imp['{}_imp'.format(e)]).join(
            data_gso_rsd['{}_rsd'.format(e)]).join(data_gso_conc[e]).join(data_gso_razbavl.filter(like=e), how='inner')

        data_gso_bl = data_gso_bl_imp.filter(like=e).join(data_gso_bl_rsd.filter(like=e))

        gso_tabl_el['soderg, ppb'] = (gso_tabl_el['м нав, мг {}'.format(e)] / (
                    gso_tabl_el['м пр+р-р, г {}'.format(e)] - gso_tabl_el['м проб, г {}'.format(e)])) * 1000 / \
                                     gso_tabl_el['разб {}'.format(e)] * gso_tabl_el[e] / 100 * 1000

        gso_tabl_el.dropna(axis=0, inplace=True)

        gso_tabl_itog = {'gso': gso_tabl_el, 'blank': data_gso_bl}

        return gso_tabl_itog

    def import_proba_mass_dol_r(

            self,
            e,
            name_list='Пробы_мд_раств',
            diap_proba_r_imp='C4:F12',
            diap_proba_r_plt='C16:F24',
            diap_proba_r_k='C28:F36',
            diap_proba_r_rsd='C40:F48',

            diap_proba_r_holost_imp='I4:L6',
            diap_proba_r_holost_plt='I16:L18',
            diap_proba_r_holost_k='I28:L30',
            diap_proba_r_holost_rsd='I40:L42'
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
        proba_r = self.wb.sheets[name_list]  # Читаем лист Данные

        # данные по импульсам
        proba_r_imp = proba_r.range(diap_proba_r_imp).options(pd.DataFrame, index=1).value

        # данные по плотности
        proba_r_plt = proba_r.range(diap_proba_r_plt).options(pd.DataFrame, index=1).value

        # данные по разбавлению
        proba_r_k = proba_r.range(diap_proba_r_k).options(pd.DataFrame, index=1).value

        # данные по rsd
        proba_r_rsd = proba_r.range(diap_proba_r_rsd).options(pd.DataFrame, index=1).value

        # холостые данные по импульсам
        proba_r_holost_imp = proba_r.range(diap_proba_r_holost_imp).options(pd.DataFrame, index=1).value

        # холостые данные по плотности
        proba_r_holost_plt = proba_r.range(diap_proba_r_holost_plt).options(pd.DataFrame, index=1).value

        # холостые данные по разбавлению
        proba_r_holost_k = proba_r.range(diap_proba_r_holost_k).options(pd.DataFrame, index=1).value

        # холостые данные по rsd
        proba_r_holost_rsd = proba_r.range(diap_proba_r_holost_rsd).options(pd.DataFrame, index=1).value

        prob_r_all = proba_r_imp.join(proba_r_plt).join(proba_r_k).join(proba_r_rsd)
        prob_r_el = prob_r_all[['{}_imp'.format(e), '{}_plt'.format(e), '{}_k'.format(e), '{}_rsd'.format(e)]]
        prob_r_el.dropna(axis=0, inplace=True)

        hol_r_all = proba_r_holost_imp.join(proba_r_holost_plt).join(proba_r_holost_k).join(proba_r_holost_rsd)
        hol_r_el = hol_r_all[['{}_imp'.format(e), '{}_plt'.format(e), '{}_k'.format(e), '{}_rsd'.format(e)]]
        hol_r_el.dropna(axis=0, inplace=True)

        itog = {'prob': prob_r_el, 'hol': hol_r_el}

        return itog

    def import_proba_mass_dol_tv(

            self,
            e,
            name_list='Пробы_мд_нав',
            diap_data_proba_steel='B2:F9',
            diap_data_proba_steel_imp='B13:E20',
            diap_data_proba_steel_rsd='B24:E31',

            diap_data_holost_stell='B35:E38',
            diap_data_holost_stell_imp='B41:E44',
            diap_data_holost_stell_rsd='B47:E50',
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
        proba_steel = self.wb.sheets[name_list]  # Читаем лист Данные

        # данные по переводу в пробирки и разбавлению
        data_proba_steel = proba_steel.range(diap_data_proba_steel).options(pd.DataFrame, index=1).value

        # данные для проб импульсы
        data_proba_steel_imp = proba_steel.range(diap_data_proba_steel_imp).options(pd.DataFrame, index=1).value

        # данные для проб rsd
        data_proba_steel_rsd = proba_steel.range(diap_data_proba_steel_rsd).options(pd.DataFrame, index=1).value

        # данные по холостой разбавление
        data_holost_stell = proba_steel.range(diap_data_holost_stell).options(pd.DataFrame, index=1).value

        # данные холостой по переводу в пробирки и разбавлению
        data_holost_stell_imp = proba_steel.range(diap_data_holost_stell_imp).options(pd.DataFrame, index=1).value

        # данные по холостой rsd
        data_holost_stell_rsd = proba_steel.range(diap_data_holost_stell_rsd).options(pd.DataFrame, index=1).value

        data_prob = data_proba_steel.join(data_proba_steel_imp['{}_imp'.format(e)]).join(
            data_proba_steel_rsd['{}_rsd'.format(e)]).iloc[:, 0:7]
        data_prob.dropna(axis=0, inplace=True)

        data_xol = data_holost_stell.join(data_holost_stell_imp['{}_imp'.format(e)]).join(
            data_holost_stell_rsd['{}_rsd'.format(e)]).iloc[:, 0:6]

        data_xol.dropna(axis=0, inplace=True)

        itog = {'prob': data_prob, 'hol': data_xol}

        return itog