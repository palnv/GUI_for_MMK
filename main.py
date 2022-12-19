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
#начальное состояние
chk_state_1.set(False)
chk_state_2.set(False)

# галочки (тут не подходят)
# chk_1 = Checkbutton(tab1, text='Массовая доля в навеске', var=chk_state_1)
# chk_2 = Checkbutton(tab1, text='Массовая доля в растворе', var=chk_state_2)
# chk_3 = Checkbutton(tab1, text='Градуировка из навески', var=chk_state_3)
# chk_4 = Checkbutton(tab1, text='Градуировка из раствора', var=chk_state_4)

# создаем радиокнопки и сразу вставляем в вкладку
Radiobutton(tab1, text='Массовая доля в навеске', var=chk_state_1, value=0).grid(column=0, row=1)
Radiobutton(tab1, text='Массовая доля в растворе', var=chk_state_1, value=1).grid(column=0, row=2)
Radiobutton(tab1, text='Градуировка из навески', var=chk_state_2, value=0).grid(column=1, row=1)
Radiobutton(tab1, text='Градуировка из раствора', var=chk_state_2, value=1).grid(column=1, row=2)

# вторая вкладка ввод данных
tab2 = ttk.Frame(tab_control)
tab_control.add(tab2, text='Ввод данных градуировка')

# текст 2 вкладки
Label(tab2, text="Ввод первичных данных по градуировке", font=("Arial Bold", 15)).place(relx=0.05, rely=0.05)
Label(tab2, text="Введите количество анализируемых элементов", font=("Arial Bold", 10)).place(relx=0.05, rely=0.15)
Label(tab2, text="Введите количество градуировочных растворов", font=("Arial Bold", 10)).place(relx=0.05, rely=0.21)

# програмка для кол-ва полей n
def pole_n(event):

    n_pole = int(combobox.get())
    for i in range(n_pole):
        ttk.Entry().pack()

# выпадающий список
number = [1,2,3,4,5,6,7,8,9,10]

combobox_1 = ttk.Combobox(tab2,  values=number)
combobox_1.place(relx=0.45, rely=0.15)

combobox_2 = ttk.Combobox(tab2,  values=number)
combobox_2.place(relx=0.45, rely=0.22)

combobox_1.bind("<<ComboboxSelected>>", pole_n)

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