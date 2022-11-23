
import uncertainty_v_2_0_Pt as un
import os


if __name__ == '__main__':

    a = un.mmk(r'{}'.format(os.getcwd() + '\Вводные данные.xlsx'))

    a.choice()


