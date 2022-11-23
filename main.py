from tkinter import *
from tkinter import ttk
from tkinter.ttk import Checkbutton

# начальное окно
window = Tk()
window.title("Рассчет неопределенности ММК")
window.geometry('800x500')


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
chk_state_3 = BooleanVar()
chk_state_4 = BooleanVar()
#начальное состояние
chk_state_1.set(False)
chk_state_2.set(False)
chk_state_3.set(False)
chk_state_4.set(False)
chk_1 = Checkbutton(tab1, text='Массовая доля в навеске', var=chk_state_1)
chk_2 = Checkbutton(tab1, text='Массовая доля в растворе', var=chk_state_2)
chk_3 = Checkbutton(tab1, text='Градуировка из навески', var=chk_state_3)
chk_4 = Checkbutton(tab1, text='Градуировка из раствора', var=chk_state_4)
chk_1.grid(column=0, row=1)
chk_2.grid(column=0, row=2)
chk_3.grid(column=1, row=1)
chk_4.grid(column=1, row=2)



# вторая вкладка ввод данных
tab2 = ttk.Frame(tab_control)
tab_control.add(tab2, text='Ввод данных')
# текст 2 вкладки
lbl = Label(tab2, text="Ввод первичных данных по пробам и градуировке", font=("Arial Bold", 15))
lbl.grid(column=0, row=0)

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