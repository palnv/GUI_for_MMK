
import uncertainty_v_2_0_Pt as un
import os


if __name__ == '__main__':

    #a = un.mmk(r'{}'.format(os.getcwd() + '\Вводные данные.xlsx'))

    #a.choice()

    """
    отладка
    """
    im = un.data_load(r'{}'.format(os.getcwd() + '\Вводные данные.xlsx'))

    #print(im.import_liq_gso('Dy')['blank'])
    #print(im.import_tv_gso('Nb')['blank'].to_numpy()[0][0])

    #print('ok')
