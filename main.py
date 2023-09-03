import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter.messagebox import showerror, showwarning
import webbrowser
import matplotlib.pyplot as plt
from  matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np
import calcs
import os
import sys


class Interface:
  def __init__(self):
    self.VolumeDict = {'Метан' : 0, 'Этан' : 0, 'Пропан' : 0, 'Бутан' : 0, 'Пентан' : 0,
            'Гексан' : 0, 'Гептан' : 0, 'Азот' : 0, 'Диоксид' : 0, 'Сероводород' : 0}
    
  def changeVolume(self):
    self.VolumeDict = {'Метан' : 0, 'Этан' : 0, 'Пропан' : 0, 'Бутан' : 0, 'Пентан' : 0,
            'Гексан' : 0, 'Гептан' : 0, 'Азот' : 0, 'Диоксид' : 0, 'Сероводород' : 0}
    i = 0
    for key in self.VolumeDict:
      if self.CheckFloat((self.EntryMassive[i].get(),)):
        self.VolumeDict[key] = round(float(self.EntryMassive[i].get()),3)
        i += 1
      else:
        return
      
  def createform(self):
    self.menu = Tk()
    width = 800
    height = 600
    self.menu.geometry("{}x{}+650+280".format(width, height))
    self.menu.minsize(int(width), int(height))
    self.menu.maxsize(int(width), int(height))
    self.menu.title('Расчет выбросов на факельных установках')
    filepath = os.getcwd()
    self.menu.iconbitmap(default=('./gas.ico'))
    
    self.notebook = ttk.Notebook()
    self.notebook.pack(expand=True,fill=BOTH)
    self.frame1 = tk.Frame(self.notebook)
    
    #Создание полей ввода для объемных долей ПНГ
    self.Volumelabel = tk.Label(self.frame1, text='Объемные доли веществ в ПНГ', font=('Arial',13))
    self.Volumelabel.place(relx = 0.02, rely = 0.01)
    
    self.EntryMassive = []
    for i in range(10):
      self.EntryMassive.append(tk.Entry(self.frame1, validate='all', validatecommand=self.countsumvolumes))
    for i in range(10):
      self.EntryMassive[i].config(width = 10)
      self.EntryMassive[i].place(relx = 0.05, rely = (i+1)/20)
    LabelMassive = []
    for i in range(10):
      LabelMassive.append(tk.Label(self.frame1))
    k = 0
    for key in self.VolumeDict:
      LabelMassive[k]['text'] = key
      LabelMassive[k].place(x=70, relx = 0.05, rely = (k+1)/20)
      k += 1

    self.sumvolumes = StringVar(value='Σ =')
    self.Sumlabel = tk.Label(self.frame1,textvariable=self.sumvolumes,font=('Arial',12))
    self.Sumlabel.place( relx=0.05, rely= 0.55)
    
    self.countsumbutton = tk.Button(self.frame1,text='Проверить',command=self.sumcheck)
    self.countsumbutton.place(x=75,relx=0.05,rely=0.55)
    
    
    self.createmenu()
  
  def countsumvolumes(self):
    self.tempsum = 0
    for i in range(len(self.EntryMassive)):
      if self.CheckFloat((self.EntryMassive[i].get())):
        self.tempsum += float(self.EntryMassive[i].get())
    self.sumvolumes.set(value='Σ = {0}'.format(str(round(self.tempsum,1))))
    return True
  
  def sumcheck(self):
    self.countsumvolumes()
    if float(self.tempsum > 100.0):
      showwarning('Ошибка', 'Сумма объемных долей не может превышать 100!\nпроверьте объемные доли!')
      
    
  def createmenu(self):
    self.mainmenu = Menu(self.menu)
    self.filemenu = Menu(self.mainmenu, tearoff=0)
    self.filemenu.add_command(label="Импорт объемных долей", command=self.importVolumes)
    self.filemenu.add_command(label="Импорт входных параметров",command=self.importParameters)
    self.filemenu.add_command(label="Выход", command=self.on_closing)
    
    self.helpmenu = Menu(self.mainmenu, tearoff=0)
    self.helpmenu.add_command(label="Методика расчётов",command=self.openmethod)
    self.menu.config(menu=self.mainmenu)
    
    self.mainmenu.add_cascade(label="Файл",
                     menu=self.filemenu)
    self.mainmenu.add_cascade(label="Справка",
                        menu=self.helpmenu)
    
    self.additionalmenu()
  
  def openmethod(self):
    webbrowser.open_new('https://files.stroyinf.ru/Data1/7/7512/index.htm')
    
  def changetype(self): #Смена типа установки
    if self.CheckState.get():
      self.hblabel.configure(state=NORMAL)
      self.hrlabel.configure(state=DISABLED)
      self.lalabel.configure(state=DISABLED)
      self.tubeheight.configure(state=NORMAL)
      self.soploheight.configure(state=DISABLED)
      self.soploambar.configure(state=DISABLED)
    else:
      self.hblabel.configure(state=DISABLED)
      self.hrlabel.configure(state=NORMAL)
      self.lalabel.configure(state=NORMAL)
      self.tubeheight.configure(state=DISABLED)
      self.soploheight.configure(state=NORMAL)
      self.soploambar.configure(state=NORMAL)
    
  def additionalmenu(self):
    self.Ustanovkalabel = tk.Label(self.frame1,text='Тип установки',font=('Arial',13))
    self.Ustanovkalabel.place(relx=0.02, rely= 0.62)
    #Выбор типа установки
    self.CheckState = BooleanVar()
    self.CheckState.set(1)
    self.UstanovkaVCheck = tk.Radiobutton(self.frame1, text='Вертикальная установка', variable= self.CheckState, value=1, command=self.changetype)
    self.UstanovkaVCheck.place(relx = 0.02, rely = 0.68)
    self.UstanovkaHCheck = tk.Radiobutton(self.frame1, text='Горизонтальная установка', variable= self.CheckState, value=0, command=self.changetype)
    self.UstanovkaHCheck.place(relx = 0.02, rely = 0.78)
    
    #Высота трубы
    self.tubeheight = tk.Entry(self.frame1, width=8)
    self.tubeheight.place(y=4,x=180, relx = 0.02, rely = 0.68)
    self.hblabel = tk.Label(self.frame1, text='Высота трубы')
    self.hblabel.place(y=-20,x=160, relx = 0.02, rely = 0.68)
    
    #Высота сопла и Расстояние от сопла до другого края амбара
    self.soploheight = tk.Entry(self.frame1, width=8)
    self.soploheight.place(y=4,x=180, relx = 0.02, rely = 0.78)
    self.soploambar = tk.Entry(self.frame1, width=8)
    self.soploambar.place(y=4,x=260, relx = 0.02, rely = 0.78)
    self.hrlabel = tk.Label(self.frame1, text='Высота сопла;')
    self.hrlabel.place(y=-20,x=160, relx = 0.02, rely = 0.78)
    self.lalabel = tk.Label(self.frame1, text='Расстояние до края амбара')
    self.lalabel.place(y=-20,x=242, relx = 0.02, rely = 0.78)
    self.changetype()
    self.interwidgets()
    
  def interwidgets(self):
    self.Paramsalbel = tk.Label(self.frame1, text=('Исходные данные'),font=('Arial',13))
    self.Paramsalbel.place(relx=0.58,rely= 0.01)
    #Диаметр выходного сопла
    self.d0entry = tk.Entry(self.frame1, width=8)
    self.d0entry.place(relx=0.6,rely=0.1)
    self.d0label = tk.Label(self.frame1, text='Диаметр выходного сопла')
    self.d0label.place(y= -22,relx=0.6,rely=0.1)
    self.d0label1 = tk.Label(self.frame1, text='м')
    self.d0label1.place(x= 52,relx=0.6,rely=0.1)
    
    #Объемный расход сжигаемого ПНГ и Скорость истечения ПНГ
    self.Wventry = tk.Entry(self.frame1, width=8)
    self.Wventry.place(y=4,relx=0.6,rely=0.18)
    self.Uentry = tk.Entry(self.frame1, width=8)
    self.Uentry.place(y=4,relx=0.6,rely=0.26)
    
    self.Wvlabel = tk.Label(self.frame1, text='Объемный расход сжигаемого ПНГ')
    self.Wvlabel.place(y=-20,relx=0.6,rely=0.18)
    self.Wvlabel1 = tk.Label(self.frame1, text='м3/с')
    self.Wvlabel1.place(x=52,y=5,relx=0.6,rely=0.18)
    self.Ulabel = tk.Label(self.frame1, text='Скорость истечения ПНГ')
    self.Ulabel.place(y=-20,relx=0.6,rely=0.26)
    self.Ulabel1 = tk.Label(self.frame1, text='м/с')
    self.Ulabel1.place(x=52,y=5,relx=0.6,rely=0.26)
  
    self.Wvstatus = IntVar()
    self.Ustatus = IntVar()
    self.Wvcheck = tk.Checkbutton(self.frame1, text= 'Нет измерений', variable=self.Wvstatus,command=self.hideWv)
    self.Wvcheck.place(x = 92, relx=0.6,rely= 0.18)
    self.Ucheck = tk.Checkbutton(self.frame1, text= 'Нет измерений', variable=self.Ustatus, command=self.addU)
    self.Ucheck.place(x = 92, relx=0.6,rely= 0.26)
    
    self.Utake = BooleanVar()
    self.Utake.set(1)
    self.Uconst = tk.Radiobutton(self.frame1, text='Постоянный сброс', variable= self.Utake, value=1, command=self.addU)
    self.Uperiod = tk.Radiobutton(self.frame1, text='Периодический сброс', variable= self.Utake, value=0, command=self.addU)
    
    #Плотность ПНГ
    self.Pgentry = tk.Entry(self.frame1, width=8)
    self.Pgentry.place(y=4,relx=0.6,rely=0.38)
    self.Pglabel = tk.Label(self.frame1, text='Плотность ПНГ')
    self.Pglabel.place(y=-20,relx=0.6,rely=0.38)
    self.Pglabel1 = tk.Label(self.frame1, text='кг/м3')
    self.Pglabel1.place(x=52,y=5,relx=0.6,rely=0.38)
    self.Pginfo = IntVar()
    self.Pgcheck = tk.Checkbutton(self.frame1, text= 'Расчёт по объемным долям', variable=self.Pginfo, command=self.hidePg, wraplength='100p', justify=LEFT)
    self.Pgcheck.place(x= 92,y= -5, relx=0.6,rely= 0.38)
    #Температура ПНГ
    self.Tempentry = tk.Entry(self.frame1, width=8)
    self.Tempentry.place(y=4,relx=0.6,rely=0.46)
    self.Templabel = tk.Label(self.frame1, text='Температура ПНГ')
    self.Templabel.place(y=-20,relx=0.6,rely=0.46)
    self.Templabel1 = tk.Label(self.frame1, text='°С')
    self.Templabel1.place(x=52,y=5,relx=0.6,rely=0.46)
    
    #Атмосферное давление
    self.Pressurevariants = []
    for i in range(745, 761):
      self.Pressurevariants.append(i)
    self.Pressure_var = StringVar(value=self.Pressurevariants[-1])
    self.Pressurecombobox = ttk.Combobox(self.frame1,textvariable= self.Pressure_var,values=self.Pressurevariants, width=5, state='readonly')
    self.Pressurecombobox.place(y=4,relx=0.6,rely=0.54)
    self.Pressurelabel = tk.Label(self.frame1, text='Атмосферное давление')
    self.Pressurelabel.place(y=-20,relx=0.6,rely=0.54)
    self.Pressurelabel1 = tk.Label(self.frame1, text='мм. рт. ст.')
    self.Pressurelabel1.place(x=53,y=5,relx=0.6,rely=0.54)
    
    #Относительная влажность
    self.FIvariants = ["20", "40", "60", "80", "100"]
    self.Fi_var = StringVar(value=self.FIvariants[0]) 
    self.FIcombobox = ttk.Combobox(self.frame1,textvariable= self.Fi_var,values=self.FIvariants, width=5, state='readonly')
    self.FIcombobox.place(y=4,relx=0.6,rely=0.62)
    self.FIlabel = tk.Label(self.frame1, text='Относительная влажность')
    self.FIlabel.place(y=-20,relx=0.6,rely=0.62)
    self.FIlabel1 = tk.Label(self.frame1, text='%')
    self.FIlabel1.place(x=53,y=5,relx=0.6,rely=0.62)
    
    #Недожег
    self.nedojegentry = tk.Entry(self.frame1, width=8)
    self.nedojegentry.place(y=4,relx=0.6,rely=0.70)
    self.nedojeglabel = tk.Label(self.frame1, text='Коэффициент недожога')
    self.nedojeglabel.place(y=-20,relx=0.6,rely=0.70)
    self.nedojeginfo = IntVar()
    self.nedojeginfo.set(0)
    self.nedojegcheck = tk.Checkbutton(self.frame1, text= 'Нет данных', variable=self.nedojeginfo, command=self.hidenedojeg,)
    self.nedojegcheck.place(x= 92, relx=0.6,rely= 0.70)
    
    #Коэффициент избытка влажного воздуха
    self.Izbentry = tk.Entry(self.frame1, width=8)
    self.Izbentry.place(y=4,relx=0.6,rely=0.78)
    self.Izblabel = tk.Label(self.frame1, text='Коэффициент избытка влажного воздуха')
    self.Izblabel.place(y=-20,relx=0.6,rely=0.78)
    
    self.calcbutton = tk.Button(self.frame1,text='Рассчитать',font=('Arial',15),command=self.calc)
    self.calcbutton.place(relx=0.45,rely=0.9,anchor=NW)
    
    self.countsumvolumes()
    self.countnumbers = 0 #Количество нажатий на кнопку calc
    
    self.frame1.pack(anchor=NW, fill=BOTH, expand=True)
    self.notebook.add(self.frame1, text = 'Ввод параметров')
    
    
    self.menu.protocol("WM_DELETE_WINDOW", self.on_closing)
    self.menu.mainloop()

  '''
    self.Wvstatus = IntVar()
    self.Ustatus = IntVar()
    self.Wvcheck = tk.Checkbutton(self.frame1, text= 'Нет измерений', variable=self.Wvstatus,command=self.hideWv)
    self.Wvcheck.place(x = 92, relx=0.6,rely= 0.12)
    self.Ucheck = tk.Checkbutton(self.frame1, text= 'Нет измерений', variable=self.Ustatus, command=self.addU)
    self.Ucheck.place(x = 92, relx=0.6,rely= 0.2)
  '''
  def checkzeros(self):
    if float(self.Wventry.get()) == 0:
      self.Wvstatus.set(1)
      self.hideWv()
    if float(self.Uentry.get()) == 0:
      self.Ustatus.set(1)
      self.addU()
    if float(self.Pgentry.get()) == 0:
      self.Pginfo.set(1)
      self.hidePg()
    if float(self.nedojegentry.get()) == 0:
      self.nedojeginfo.set(1)
      self.hidenedojeg()
      
      
  
  def on_closing(self):
    sys.exit()
    
  def hidePg(self):
    if self.Pginfo.get():
      self.Pgentry.configure(state=DISABLED)
    else:
      self.Pgentry.configure(state=NORMAL)
  
  def hidenedojeg(self):
    if self.nedojeginfo.get():
      self.nedojegentry.configure(state=DISABLED)
    else:
      self.nedojegentry.configure(state=NORMAL)
  
  def hideWv(self):
    if self.Wvstatus.get():
      self.Wventry.configure(state=DISABLED)
    else:
      self.Wventry.configure(state=NORMAL)
      
  def hideU(self):
    if self.Ustatus.get():
      self.Uentry.configure(state=DISABLED)
    else:
      self.Uentry.configure(state=NORMAL)
      
  def addU(self):
    self.hideU()
    if self.Ustatus.get():
      self.Uconst.place(x= -20,y= 25, relx = 0.6, rely = 0.26)
      self.Uperiod.place(x= 110,y= 25, relx = 0.6, rely = 0.26)
    else:
      self.Uconst.place_forget()
      self.Uperiod.place_forget()
  
  def outputs(self):
    self.AtomicMass = [12.011, 1.008, 14.008, 16.000, 32.006] #Атомные массы элем-в C H N O S
    #2
    if (self.CheckFloat((self.Pgentry.get(),)) and self.Pginfo.get() == 0) or (self.Pginfo.get() == 1):
      self.Pj,self.Pg = calcs.CountPg(self.VolumeDict,self.Pgentry.get(), self.Pginfo.get())
    else:
      return
    
    self.ug, self.uj = calcs.CountMassMol(self.VolumeDict)
    #5
    self.MassSoderj = calcs.CountMassSoderj(self.VolumeDict,self.Pg)
    #6
    self.Katom,self.Ugtochn = calcs.CountAtomNumbers(self.MassSoderj,self.ug,self.uj,self.AtomicMass)
    #7
    if self.CheckFloat((self.Tempentry.get(),)):
      self.d = calcs.CountDbyMeteo(self.Tempentry.get(),int(self.Fi_var.get()))
    else:
      return
    
    #8
    self.Pp,self.func_Pp_d = calcs.CountPpbyD(self.d)
    #9
    if self.CheckFloat((self.Pressure_var.get())):
      self.HumidComponentMass, self.Kj = calcs.CountAtomsinWetAir(self.d, float(self.Tempentry.get()), float(self.Pressure_var.get()),self.Pp)
    
      self.Pvv = calcs.CountPvv(float(self.Tempentry.get()),float(self.Pressure_var.get()), self.Pp)
    else:
      return
    
    #11
    self.M,self.Vvv = calcs.CountM(self.Katom,self.Kj)
    #12
    self.Vps = calcs.CountVps(self.Katom, self.Kj, self.M)
    #13
    self.Uzv,self.AdiabatK = calcs.CountK(self.VolumeDict,self.Ugtochn, float(self.Tempentry.get()))
    #1
    if (self.CheckFloat((self.Wventry.get(),)) and self.Wvstatus.get() == 0) or (self.Wvstatus.get() == 1):
      if (self.CheckFloat((self.Uentry.get(),)) and self.Ustatus.get() == 0) or (self.Ustatus.get() == 1):
        if (self.CheckFloat((self.d0entry.get(),))):
          self.Wv,self.U = (calcs.CountW(self.Wvstatus.get(),self.Wventry.get(),
                            self.Ustatus.get(),self.Uentry.get(),float(self.d0entry.get()),self.Uzv,self.Utake.get()))
    else:
      return
    #3
    self.Wg = calcs.CountWg(self.Wv, self.Pg)

    #15
    self.NoSoot = calcs.CheckSoot(self.U, self.Uzv)
    if (self.CheckFloat((self.nedojegentry.get(),)) and self.nedojeginfo.get() == 0) or (self.nedojeginfo.get() == 1):
      self.qi, self.nedojeg = calcs.CountEjectionMain(self.VolumeDict,self.uj,self.NoSoot,self.Wg, self.Katom, self.Ugtochn,self.nedojeginfo.get(),self.nedojegentry.get())
    else:
      return
    if (self.CheckFloat((self.Izbentry.get(),))):
      self.qi_larger = calcs.CountEjectionSub(self.VolumeDict,self.AtomicMass,self.Katom,
                                              self.Ugtochn,self.qi,self.Wg,float(self.Izbentry.get()),
                                              self.M,self.Kj,self.nedojeg,self.uj)
    else:
      return
    
    self. Wgi = calcs.CountPolutionMax(self.qi,self.Wg)
    
    self.Qh = calcs.CountQh(self.VolumeDict)
    
    self.delta = calcs.CountDelta(self.Ugtochn)
    
    self.Qps,self.Tr,self.QpsFunction = calcs.CountQpsTr(self.qi_larger,self.Qh,self.delta)
    
    self.Wpr = calcs.CountWpr(self.Wv, self.Vps, self.Tr)
    if self.CheckState.get():
      if (self.CheckFloat((self.tubeheight.get(),))):
          self.Height, self.Lf = calcs.CountFakelParameters(self.VolumeDict,self.tubeheight.get(),float(self.d0entry.get()),
                                                  self.Tr,float(self.Tempentry.get()),self.Vvv,self.Pvv,self.Pg,
                                                  self.soploheight.get(),self.soploambar.get(),self.CheckState.get())
      else:
        return
    else:
      if (self.CheckFloat((self.soploheight.get(),))) and (self.CheckFloat((self.soploambar.get(),))):
        self.Height, self.Lf = calcs.CountFakelParameters(self.VolumeDict,self.tubeheight.get(),float(self.d0entry.get()),
                                        self.Tr,float(self.Tempentry.get()),self.Vvv,self.Pvv,self.Pg,
                                        self.soploheight.get(),self.soploambar.get(),self.CheckState.get())
      else:
        return
    
    self.Wps = calcs.CountWps(self.Wpr,self.Lf)
    
    self.createOutputPlots()
  
  def calc(self):
    self.changeVolume()
    self.outputs()
  
  def CheckFloat(self, entriesInput):
    for i in range(len(entriesInput)):
      if entriesInput[i] == '':
        showwarning('Ошибка', 'Введены не все значения\nпроверьте правильность ввода')
        return False
      try:
        float(entriesInput[i])
        return True
      except ValueError:
        showwarning('Ошибка', 'Невозможно преобразовать к числу значение {0}'.format(entriesInput[i]) + "\nпроверьте правильность ввода")
        return False
  
  def importVolumes(self):
    filepath = filedialog.askopenfilename()
    if filepath != "":
      file = open(filepath,'r')
      i = 0
      for line in file:
        t = line.split('= ')[-1]
        if self.CheckFloat((t,)):
          self.EntryMassive[i].delete(0,END)
          self.EntryMassive[i].insert(0,t)
          i += 1
        else:
          return showerror('Ошибка в файле', 'Некорректные данные в вводимом файле')
    self.countsumvolumes()
        
  def importParameters(self):
    self.Parameters = [self.d0entry,self.Wventry,self.Uentry,self.Utake,self.Pgentry,
                      self.Tempentry,self.Pressure_var,self.Fi_var,self.nedojegentry,
                      self.Izbentry,self.CheckState,self.tubeheight,self.soploheight,self.soploambar]
    filepath = filedialog.askopenfilename()
    if filepath != "":
      file = open(filepath,'r')
      i = 0
      for line in file:
        t = line.split('= ')[-1]
        t = t.split('\n')[0]
        if self.CheckFloat((t,)):
          if i == 3:
            if t == '1' or t == '0':
              self.Parameters[i].set(int(t))
              i+=1
            else:
              return showerror('Ошибка в файле', 'Некорректный ввод параметра Sbros\n Параметр может принимать значения 0 или 1')
          elif i == 10:
            if t == '1' or t == '0':
              self.Parameters[i].set(t)
              self.changetype()
              i+=1
            else:
              return showerror('Ошибка в файле', 'Некорректный ввод параметра type\n Параметр может принимать значения от 0 или 1')
          elif i == 6:
            if int(t) in self.Pressurevariants:
              self.Parameters[i].set(t)
              i+=1
            else:
              return showerror('Ошибка в файле', 'Некорректный ввод параметра P\n Параметр может принимать значения от 745 до 760')
          elif i == 7:
            if t in self.FIvariants:
              self.Parameters[i].set(t)
              i+=1
            else:
              return showerror('Ошибка в файле', 'Некорректный ввод параметра fi\n Параметр может принимать значения от 20:40:60:80:100')
          elif i == 9:
            if float(t) <= 1 and float(t) >= 0:
              self.Parameters[i].delete(0,END)
              self.Parameters[i].insert(0,t)
              i+=1
            else:
              return showerror('Ошибка в файле', 'Некорректный ввод параметра a\n Параметр может принимать значения от 0 до 1')
          
          else:
            self.Parameters[i].delete(0,END)
            self.Parameters[i].insert(0,t)
            i+=1
        else:
          return showerror('Ошибка в файле', 'Некорректный ввод значения {}'.format(t))
      self.checkzeros()
        
  def createOutputPlots(self):
    self.countnumbers+= 1
    if self.countnumbers > 1:
      self.notebook.forget(self.frame2)
      self.notebook.forget(self.frame3)
      self.notebook.forget(self.frame4)
      self.frame2.destroy()
      self.frame3.destroy()
      self.frame4.destroy()
      
    self.frame2 = tk.Frame(self.notebook,bg='white')
    self.frame2.pack(fill=BOTH, expand=True)
    self.frame3 = tk.Frame(self.notebook,bg='white')
    self.frame3.pack(fill=BOTH, expand=True)
    self.frame4 = tk.Frame(self.notebook)
    
    self.notebook.add(self.frame2, text = 'Номограмма')
    self.notebook.add(self.frame3, text = 'Температура')
    
    Qnew_x = np.linspace(self.Qps[0],self.Qps[-1],1000)
    Qnew_y = self.QpsFunction(Qnew_x)
    fig1 = plt.figure(figsize=(8, 8))
    ax1 = fig1.add_subplot(111)
    ax1.plot(Qnew_x, Qnew_y)
    ax1.grid()
    ax1.set_xlabel('Q, ккал')
    ax1.set_ylabel('T, °K')
    canvas = FigureCanvasTkAgg(fig1, self.frame3)
    TLabel = tk.Label(self.frame3,text='График для визуального определения температуры продуктов сгорания T по количеству теплоты в подуктах сгорания Q',
                      font=('Arial',14),justify=LEFT,wraplength=770,bg='white')
    TLabel.pack(side='top',anchor=NW)
    toolbar1 = NavigationToolbar2Tk(canvas, self.frame3)
    toolbar1.update()
    canvas.get_tk_widget().pack(side='bottom',fill=BOTH,expand=1)
  
    graf_d = np.linspace(0,0.035,1000)
    graf_Pp = self.func_Pp_d(graf_d)
    fig2 = plt.figure(figsize=(8,8))
    ax2 = fig2.add_subplot(111)
    ax2.plot(graf_d,graf_Pp)
    ax2.grid()
    ax2.set_xlabel('d, кг/кг')
    ax2.set_ylabel('Pп, мм. рт. ст.')
    ax2.set_xlim(0)
    ax2.set_ylim(0)
    canvas = FigureCanvasTkAgg(fig2,self.frame2)
    dLabel = tk.Label(self.frame2,text='График для визуального определения парциального давления водяного пара Pп по влагосодержанию d',
                      font=('Arial',14),justify=LEFT,wraplength=770,bg='white')
    dLabel.pack(side='top',anchor=NW)
    toolbar2 = NavigationToolbar2Tk(canvas, self.frame2)
    toolbar2.update()
    canvas.get_tk_widget().pack(side='bottom',fill=BOTH,expand=1)
    
    self.createOutputParameters()
    
  def export41(self):
    file_path = filedialog.askopenfilename(initialdir="/", title="Выберите файл для экспорта", filetypes=(("Текстовые файлы", "*.txt"), ("Все файлы", "*.*")))
    if file_path:
      with open(file_path, 'w') as file:
        label_value = self.fr41label['text']
        file.write(f"{label_value}\n")
        value = self.WvOut.get()
        label_value = self.WvlabelOut['text']
        file.write(f"{label_value}: {value}\n")
        value = self.UOut.get()
        label_value = self.UlabelOut['text']
        file.write(f"{label_value}: {value}\n")
        value = self.WgOut.get()
        label_value = self.WglabelOut['text']
        file.write(f"{label_value}: {value}\n")
        value = self.WprOut.get()
        label_value = self.WprlabelOut['text']
        file.write(f"{label_value}: {value}\n")
        
  def export42(self):
    file_path = filedialog.askopenfilename(initialdir="/", title="Выберите файл для экспорта", filetypes=(("Текстовые файлы", "*.txt"), ("Все файлы", "*.*")))
    if file_path:
      with open(file_path, 'w') as file:
        label_value = self.fr42label['text']
        file.write(f"{label_value}\n")
        value = self.Pgout.get()
        label_value = self.PglabelOut['text']
        file.write(f"{label_value}: {value}\n")
        value = self.Ugout.get()
        label_value = self.UglabelOut['text']
        file.write(f"{label_value}: {value}\n")
        value = self.dout.get()
        label_value = self.doutlabel['text']
        file.write(f"{label_value}: {value}\n")
        value = self.Pvvout.get()
        label_value = self.PvvlabelOut['text']
        file.write(f"{label_value}: {value}\n")
        value = self.Uzvout.get()
        label_value = self.UzvlabelOut['text']
        file.write(f"{label_value}: {value}\n")
        headers = '      '.join(map(str, self.colsuj))  # Объединяем элементы массива в строку с пробелами в качестве разделителя
        file.write(headers+'\n')
        values = '     '.join(map(str,self.uj))
        file.write(values+'\n')
        columnq = []
        for i in range(6):
          columnq.append(self.qi[i])
        headers = '      '.join(map(str,self.colsq))
        file.write(headers+'\n')
        values = '    '.join(map(str,columnq))
        file.write(values+'\n')
    
  def export44(self):
    file_path = filedialog.askopenfilename(initialdir="./", title="Выберите файл для экспорта", filetypes=(("Текстовые файлы", "*.txt"), ("Все файлы", "*.*")))
    if file_path:
      with open(file_path, 'w') as file:
        label_value = self.fr44label['text']
        file.write(f"{label_value}\n")
        headers = '      '.join(map(str, self.colsWgi))
        file.write(headers+'\n')
        values = '     '.join(map(str,self.Wgi))
        file.write(values+'\n')
        headers = '      '.join(map(str, self.colsWgit))
        file.write(headers+'\n')
        values = '    '.join(map(str,self.Wgit))
        file.write(values+'\n')
  
  def export43(self):
    file_path = filedialog.askopenfilename(initialdir="./", title="Выберите файл для экспорта", filetypes=(("Текстовые файлы", "*.txt"), ("Все файлы", "*.*")))
    if file_path:
      with open(file_path, 'w') as file:
        label_value = self.fr43label['text']
        file.write(f"{label_value}\n")
        value = self.HeightOut.get()
        label_value = self.HeightlabelOut['text']
        file.write(f"{label_value}: {value}\n")
        value = self.LfOut.get()
        label_value = self.LflabelOut['text']
        file.write(f"{label_value}: {value}\n")
        value = self.WpsOut.get()
        label_value = self.WpslabelOut['text']
        file.write(f"{label_value}: {value}\n")
        value = self.QhOut.get()
        label_value = self.QhlabelOut['text']
        file.write(f"{label_value}: {value}\n")
        value = self.deltaOut.get()
        label_value = self.deltalabelOut['text']
        file.write(f"{label_value}: {value}\n")
        value = self.QpsOut1.get()
        label_value = 'Количество теплоты в продуктах сгорания'
        file.write(label_value+'\n')
        label_value = 'T = 1100 K'
        file.write(f"{label_value}: {value}\n")
        value = self.QpsOut2.get()
        label_value = 'T = 1500 K'
        file.write(f"{label_value}: {value}\n")
        value = self.QpsOut3.get()
        label_value = 'T = 1900 K'
        file.write(f"{label_value}: {value}\n")
        value = self.QpsOut4.get()
        label_value = 'T = 2300 K'
        file.write(f"{label_value}: {value}\n")
        value = self.TrOut.get()
        label_value = self.TrlabelOut['text']
        file.write(f"{label_value}: {value}\n")
        
  def createOutputParameters(self):
    self.frame41 = tk.Frame(self.frame4,borderwidth=1, relief="sunken")
    self.frame41.place(relwidth=0.5, relheight=0.4,anchor=NW)
    self.frame42 = tk.Frame(self.frame4,borderwidth=1, relief="sunken")
    self.frame42.place(relwidth=0.5, relheight=0.75,anchor=NW, relx=0.5)
    self.frame43 = tk.Frame(self.frame4,borderwidth=1, relief="sunken")
    self.frame43.place(relwidth=0.5, relheight=0.6,anchor=NW, rely=0.4)
    self.frame44 = tk.Frame(self.frame4,borderwidth=1, relief="sunken")
    self.frame44.place(relwidth=0.5, relheight=0.25,anchor=NW,relx=0.5,rely=0.75)
    
    self.frame4.pack(fill=BOTH, expand=True)
    self.notebook.add(self.frame4, text= 'Выходные данные')
    
    #frame 4.1 
    self.fr41label = tk.Label(self.frame41,text='Оценка производительности факельной установки',font=('Arial',12))
    self.fr41label.place(relx=0.005,rely=0.01)
    
    self.WvOut = tk.Entry(self.frame41, width=8)
    self.WvOut.place(y=4,relx=0.02,rely=0.2)
    self.WvOut.insert(0,self.Wv)
    self.UOut = tk.Entry(self.frame41, width=8)
    self.UOut.place(y=4,relx=0.02,rely=0.4)
    self.UOut.insert(0,self.U)
    self.WvlabelOut = tk.Label(self.frame41, text='Объемный расход сжигаемого ПНГ')
    self.WvlabelOut.place(y=-20,relx=0.02,rely=0.2)
    self.WvlabelOut1 = tk.Label(self.frame41, text='м3/с')
    self.WvlabelOut1.place(x=52,y=5,relx=0.02,rely=0.2)
    self.UlabelOut = tk.Label(self.frame41, text='Скорость истечения ПНГ')
    self.UlabelOut.place(y=-20,relx=0.02,rely=0.4)
    self.UlabelOut1 = tk.Label(self.frame41, text='м/с')
    self.UlabelOut1.place(x=52,y=5,relx=0.02,rely=0.4)

    self.WgOut = tk.Entry(self.frame41, width=8)
    self.WgOut.place(y=4,relx=0.02,rely=0.6)
    self.WgOut.insert(0,self.Wg)
    self.WglabelOut = tk.Label(self.frame41, text='Массовый расход сбрасываемого газа')
    self.WglabelOut.place(y=-20,relx=0.02,rely=0.6)
    self.WglabelOut1 = tk.Label(self.frame41, text='кг/ч')
    self.WglabelOut1.place(x=52,y=5,relx=0.02,rely=0.6)
    
    self.WprOut = tk.Entry(self.frame41, width=8)
    self.WprOut.place(y=4,relx=0.02,rely=0.8)
    self.WprlabelOut = tk.Label(self.frame41, text='Объемный расход продуктов сгорания')
    self.WprlabelOut.place(y=-20,relx=0.02,rely=0.8)
    self.WprlabelOut1 = tk.Label(self.frame41, text='м3/c')
    self.WprlabelOut1.place(x=52,y=5,relx=0.02,rely=0.8)
    self.WprOut.insert(0,round(self.Wpr,3))
    
    self.Export41Button = tk.Button(self.frame41,text='Экспорт в файл',command=self.export41)
    self.Export41Button.place(relx=0.76,rely=0.9)
    #frame 4.2
    self.fr42label = tk.Label(self.frame42,text='Мощности выбросов вредных веществ',font=('Arial',12))
    self.fr42label.place(relx=0.005,rely=0.01)
    
    self.Pgout = tk.Entry(self.frame42, width=8)
    self.Pgout.place(y=4,relx=0.02,rely=0.1)
    self.Pgout.insert(0,self.Pg)
    self.PglabelOut = tk.Label(self.frame42, text='Плотность ПНГ')
    self.PglabelOut.place(y=-20,relx=0.02,rely=0.1)
    self.PglabelOut1 = tk.Label(self.frame42, text='кг/м3')
    self.PglabelOut1.place(x=52,y=5,relx=0.02,rely=0.1)
    
    self.Ugout = tk.Entry(self.frame42, width=8)
    self.Ugout.place(x=180,y=4,relx=0.02,rely=0.1)
    self.Ugout.insert(0,round(self.Ugtochn,3))
    self.UglabelOut = tk.Label(self.frame42, text='Условная молекулярная масса')
    self.UglabelOut.place(x=180,y=-20,relx=0.02,rely=0.1)
    self.UglabelOut1 = tk.Label(self.frame42, text='кг/моль')
    self.UglabelOut1.place(x=232,y=5,relx=0.02,rely=0.1)
    
    self.ViewUjButton = tk.Button(self.frame42,text='Посмотреть массовое содержание веществ в ПНГ',command=self.createujtable)
    self.ViewUjButton.place(relx=0.02,rely=0.17)
    
    self.Katomlabel = tk.Label(self.frame42,text='Условная молекулярная формула ПНГ')
    self.Katomlabel.place(relx=0.02,rely=0.23)
    self.Clabel = tk.Label(self.frame42, text='C')
    self.Clabel.place(relx=0.02,rely=0.28)
    self.Hlabel = tk.Label(self.frame42, text='H')
    self.Hlabel.place(x=40,relx=0.02,rely=0.28)
    self.Nlabel = tk.Label(self.frame42, text='N')
    self.Nlabel.place(x=80,relx=0.02,rely=0.28)
    self.Olabel = tk.Label(self.frame42, text='O')
    self.Olabel.place(x=120,relx=0.02,rely=0.28)
    self.Slabel = tk.Label(self.frame42, text='S')
    self.Slabel.place(x=160,relx=0.02,rely=0.28)
    
    self.c = StringVar()
    self.h = StringVar()
    self.n = StringVar()
    self.o = StringVar()
    self.s = StringVar()
    self.c.set(str(self.Katom[0]))
    self.h.set(str(self.Katom[1]))
    self.n.set(str(self.Katom[2]))
    self.o.set(str(self.Katom[3]))
    self.s.set(str(self.Katom[4]))
    self.clabel = tk.Label(self.frame42, textvariable=self.c,font=('Arial',6))
    self.clabel.place(x=12,y=6,relx=0.02,rely=0.28)
    self.hlabel = tk.Label(self.frame42, textvariable=self.h,font=('Arial',6))
    self.hlabel.place(x=52,y=6,relx=0.02,rely=0.28)
    self.nlabel = tk.Label(self.frame42, textvariable=self.n,font=('Arial',6))
    self.nlabel.place(x=92,y=6,relx=0.02,rely=0.28)
    self.olabel = tk.Label(self.frame42, textvariable=self.o,font=('Arial',6))
    self.olabel.place(x=132,y=6,relx=0.02,rely=0.28)
    self.slabel = tk.Label(self.frame42, textvariable=self.s,font=('Arial',6))
    self.slabel.place(x=172,y=6,relx=0.02,rely=0.28)
    
    self.doutlabel = tk.Label(self.frame42,text='Массовое влагосодержание d')
    self.doutlabel.place(relx=0.02,rely=0.38)
    self.dout = tk.Entry(self.frame42, width=8)
    self.dout.place(x=180,relx=0.02,rely=0.38)
    self.dout.insert(0,self.d)
    self.dlabelOut1 = tk.Label(self.frame42, text='кг/кг')
    self.dlabelOut1.place(x=232,relx=0.02,rely=0.38)
    
    self.o1 = StringVar()
    self.n1 = StringVar()
    self.h1 = StringVar()
    self.h1.set(str(self.Kj[2]))
    self.n1.set(str(self.Kj[1]))
    self.o1.set(str(self.Kj[0]))
    
    self.Kjlabel = tk.Label(self.frame42,text='Условная молекулярная формула влажного воздуха',justify='left',wraplength=180)
    self.Kjlabel.place(relx=0.02,rely=0.45)
    self.Olabel = tk.Label(self.frame42, text='O')
    self.Olabel.place(relx=0.02,rely=0.55)
    self.Nlabel = tk.Label(self.frame42, text='N')
    self.Nlabel.place(x=40,relx=0.02,rely=0.55)
    self.Hlabel = tk.Label(self.frame42, text='H')
    self.Hlabel.place(x=80,relx=0.02,rely=0.55)
    
    self.o1label = tk.Label(self.frame42, textvariable=self.o,font=('Arial',6))
    self.o1label.place(x=12,y=6,relx=0.02,rely=0.55)
    self.n1label = tk.Label(self.frame42, textvariable=self.n,font=('Arial',6))
    self.n1label.place(x=52,y=6,relx=0.02,rely=0.55)
    self.h1label = tk.Label(self.frame42, textvariable=self.h,font=('Arial',6))
    self.h1label.place(x=92,y=6,relx=0.02,rely=0.55)
    
    self.Pvvout = tk.Entry(self.frame42, width=8)
    self.Pvvout.place(x=180,y=4,relx=0.02,rely=0.53)
    self.Pvvout.insert(0,round(self.Pvv,3))
    self.PvvlabelOut = tk.Label(self.frame42, text='Плотность влажного воздуха')
    self.PvvlabelOut.place(x=180,y=-20,relx=0.02,rely=0.53)
    self.PvvlabelOut1 = tk.Label(self.frame42, text='кг/м3')
    self.PvvlabelOut1.place(x=234,y=5,relx=0.02,rely=0.53)
    
    self.Uzvout = tk.Entry(self.frame42, width=8)
    self.Uzvout.place(y=4,relx=0.02,rely=0.7)
    self.Uzvout.insert(0,self.Uzv)
    self.UzvlabelOut = tk.Label(self.frame42, text='Скорость распространения звука в ПНГ')
    self.UzvlabelOut.place(y=-20,relx=0.02,rely=0.7)
    self.UzvlabelOut1 = tk.Label(self.frame42, text='м/с')
    self.UzvlabelOut1.place(x=52,y=5,relx=0.02,rely=0.7)
    
    self.saja = StringVar()
    if self.NoSoot:
      self.saja.set(value='(Горение бессажевое)')
    else:
      self.saja.set(value='(Горение с сажей)')
    self.Bessaja = tk.Label(self.frame42, textvariable=self.saja)
    self.Bessaja.place(x=80,y=2,relx= 0.02, rely = 0.8)
    
    self.ViewqButton = tk.Button(self.frame42,text='Посмотреть удельные выбросы веществ ПНГ',command=self.createqtable)
    self.ViewqButton.place(relx=0.02,rely=0.8)
    
    self.Export42Button = tk.Button(self.frame42,text='Экспорт в файл',command=self.export42)
    self.Export42Button.place(relx=0.76,rely=0.94)

    #frame4.4
    self.fr44label = tk.Label(self.frame44,text='Максимальные и валовые выбросы',font=('Arial',12))
    self.fr44label.place(relx=0.005,rely=0.01)
    
    self.ViewWgiButton = tk.Button(self.frame44,text='Посмотреть максимальные выбросы вредных веществ г/с',command=self.createWgitable)
    self.ViewWgiButton.place(relx=0.02,rely=0.18)
    
    self.Timelabel = tk.Label(self.frame44, text = 'Введите время работы установки в течение года в часах:')
    self.Timelabel.place(y=2,relx= 0.02, rely = 0.45)
    
    self.TimeEntry = tk.Entry(self.frame44, width=8)
    self.TimeEntry.place(x=320,y=4,relx=0.02,rely=0.45)
    
    self.ViewWgitButton = tk.Button(self.frame44,text='Рассчитать валовые выбросы вредных веществ т/год',command=self.createWgittable)
    self.ViewWgitButton.place(relx=0.02,rely=0.63)
    
    self.TimeEntry.insert(0,1000)
    self.Export44Button = tk.Button(self.frame44,text='Экспорт в файл',command=self.export44)
    self.Export44Button.place(relx=0.76,rely=0.83)
    #frame4.3
    self.fr43label = tk.Label(self.frame43,text='Параметры факельной установки',font=('Arial',12))
    self.fr43label.place(relx=0.002,rely=0.01)
    
    self.HeightOut = tk.Entry(self.frame43, width=8)
    self.HeightOut.place(y=4,relx=0.02,rely=0.12)
    self.HeightOut.insert(0,round(self.Height,3))

    self.LfOut = tk.Entry(self.frame43, width=8)
    self.LfOut.place(x=180,y=4,relx=0.02,rely=0.12)
    self.LfOut.insert(0,round(self.Lf,3))
    
    self.HeightlabelOut = tk.Label(self.frame43, text='Высота трубы')
    self.HeightlabelOut.place(y=-20,relx=0.02,rely=0.12)
    self.HeightlabelOut1 = tk.Label(self.frame43, text='м')
    self.HeightlabelOut1.place(x=54,y=5,relx=0.02,rely=0.12)
    
    self.LflabelOut = tk.Label(self.frame43, text='Длина факела')
    self.LflabelOut.place(x=180,y=-20,relx=0.02,rely=0.12)
    self.LflabelOut1 = tk.Label(self.frame43, text='м')
    self.LflabelOut1.place(x=234,y=5,relx=0.02,rely=0.12)

    self.WgOut = tk.Entry(self.frame43, width=8)
    self.WgOut.place(y=4,relx=0.02,rely=0.24)
    self.WgOut.insert(0,round(self.Wg,3))
    self.WglabelOut = tk.Label(self.frame43, text='Массовый расход сбрасываемого газа')
    self.WglabelOut.place(y=-20,relx=0.02,rely=0.24)
    self.WglabelOut1 = tk.Label(self.frame43, text='кг/ч')
    self.WglabelOut1.place(x=52,y=5,relx=0.02,rely=0.24)
    
    self.WpsOut = tk.Entry(self.frame43, width=8)
    self.WpsOut.place(y=4,relx=0.02,rely=0.36)
    self.WpslabelOut = tk.Label(self.frame43, text='Средняя скорость поступления в атмосферу веществ:')
    self.WpslabelOut.place(y=-20,relx=0.02,rely=0.36)
    self.WpslabelOut1 = tk.Label(self.frame43, text='м3/c')
    self.WpslabelOut1.place(x=52,y=5,relx=0.02,rely=0.36)
    self.WpsOut.insert(0,round(self.Wps,3))
    
    self.QhOut = tk.Entry(self.frame43, width=8)
    self.QhOut.place(y=4,relx=0.02,rely=0.48)
    self.QhlabelOut = tk.Label(self.frame43, text='Низшая теплота сгорания газа')
    self.QhlabelOut.place(y=-20,relx=0.02,rely=0.48)
    self.QhlabelOut1 = tk.Label(self.frame43, text='Ккал/м3')
    self.QhlabelOut1.place(x=52,y=5,relx=0.02,rely=0.48)
    self.QhOut.insert(0,round(self.Qh,3))
    
    self.deltaOut = tk.Entry(self.frame43, width=8)
    self.deltaOut.place(y=4,relx=0.02,rely=0.6)
    self.deltalabelOut = tk.Label(self.frame43, text='Доля энергии, теряемой за счет радиации факела')
    self.deltalabelOut.place(y=-20,relx=0.02,rely=0.6)
    self.deltaOut.insert(0,round(self.delta,3))
    
    self.QpsOut1 = tk.Entry(self.frame43, width=8)
    self.QpsOut1.place(y=4,relx=0.02,rely=0.72)
    self.QpsOut2 = tk.Entry(self.frame43, width=8)
    self.QpsOut2.place(x=50,y=4,relx=0.02,rely=0.72)
    self.QpsOut3 = tk.Entry(self.frame43, width=8)
    self.QpsOut3.place(x=100,y=4,relx=0.02,rely=0.72)
    self.QpsOut4 = tk.Entry(self.frame43, width=8)
    self.QpsOut4.place(x=150,y=4,relx=0.02,rely=0.72)
    self.QpslabelOut = tk.Label(self.frame43, text='Кол-во теплоты в продуктах сгорания (T=1100,1500,1900,2300)')
    self.QpslabelOut.place(y=-20,relx=0.02,rely=0.72)
    self.QpslabelOut1 = tk.Label(self.frame43, text='Ккал')
    self.QpslabelOut1.place(x=200,y=5,relx=0.02,rely=0.72)
    self.QpsOut1.insert(0,round(self.Qps[0],3))
    self.QpsOut2.insert(0,round(self.Qps[1],3))
    self.QpsOut3.insert(0,round(self.Qps[2],3))
    self.QpsOut4.insert(0,round(self.Qps[3],3))
    
    self.TrOut = tk.Entry(self.frame43, width=8)
    self.TrOut.place(y=4,relx=0.02,rely=0.84)
    self.TrlabelOut = tk.Label(self.frame43, text='Температура выбрасываемой смеси')
    self.TrlabelOut.place(y=-20,relx=0.02,rely=0.84)
    self.TrlabelOut1 = tk.Label(self.frame43, text='°C')
    self.TrlabelOut1.place(x=52,y=5,relx=0.02,rely=0.84)
    self.TrOut.insert(0,round(self.Tr,3))
    
    self.Export43Button = tk.Button(self.frame43,text='Экспорт в файл',command=self.export43)
    self.Export43Button.place(relx=0.76,rely=0.93)
    
  def createujtable(self):
    ujwindow= Tk()
    ujwindow.title("Массовое содержание веществ в ПНГ")
    ujwindow.geometry("500x60+650+250")
    self.colsuj = ['CH4','C2H6','C3H8','C4H10','C5H12','C6H14','C7H16','N2','CO2','H2S']
    tree = ttk.Treeview(ujwindow,columns=self.colsuj,show='headings')
   
    for i in range(len(self.uj)):
      tree.heading(self.colsuj[i],text=self.colsuj[i],anchor=NW)
      tree.column('#{0}'.format(i+1),stretch=NO,width=50)
    
    tree.insert("",END, values=self.uj)
    
    tree.pack(fill=BOTH)
    ujwindow.mainloop()

  def createqtable(self):
    qi = [self.qi[0], self.qi[1], self.qi[2],self.qi[3], self.qi[4], self.qi[5]]
    qwindow= Tk()
    qwindow.title("Удельные выбросы вредных веществ ПНГ кг/кг")
    qwindow.geometry("360x60+650+250")
    self.colsq = ['CO','NO','Бензапирен','Сажа','SO2','H2S']
    tree = ttk.Treeview(qwindow,columns=self.colsq,show='headings')
    
    for i in range(6):
      tree.heading(self.colsq[i],text=self.colsq[i],anchor=NW)
      tree.column('#{0}'.format(i+1),stretch=NO,width=60)
    
    tree.insert("",END, values=qi)
    #qi = [qCO,qNO,qPetrol,qSaja,qSO2,qH2S,qCH4]
    tree.pack(fill=BOTH)
    qwindow.mainloop()

  def createWgitable(self):
    Wgiwindow= Tk()
    Wgiwindow.title("Максимальные выбросы вредных веществ")
    Wgiwindow.geometry("500x60+650+250")
    self.colsWgi = ['CO','NO','Бензапирен','Сажа','SO2','H2S','CH4']
    tree = ttk.Treeview(Wgiwindow,columns=self.colsWgi,show='headings')
    
    for i in range(7):
      tree.heading(self.colsWgi[i],text=self.colsWgi[i],anchor=NW)
      tree.column('#{0}'.format(i+1),stretch=NO,width=80)
    tree.insert("",END, values=self.Wgi)
    #qi = [qCO,qNO,qPetrol,qSaja,qSO2,qH2S,qCH4]
    tree.pack(fill=BOTH)
    Wgiwindow.mainloop()
    
  def createWgittable(self):
    if self.CheckFloat((self.TimeEntry.get(),)):
      self.Wgit = calcs.CountPolutionPerYear(self.qi,self.Wg,float(self.TimeEntry.get()))
    else:
      return showerror('Ошибка', 'Некорректные данные времени')
    Wgitwindow= Tk()
    Wgitwindow.title("Валовые выбросы вредных веществ в год")
    Wgitwindow.geometry("700x60+650+250")
    self.colsWgit = ['CO','NO','Бензапирен','Сажа','SO2','H2S','CH4']
    tree = ttk.Treeview(Wgitwindow,columns=self.colsWgit,show='headings')
    
    for i in range(7):
      tree.heading(self.colsWgit[i],text=self.colsWgit[i],anchor=NW)
      tree.column('#{0}'.format(i+1),stretch=NO,width=100)
    tree.insert("",END, values=self.Wgit)
    #qi = [qCO,qNO,qPetrol,qSaja,qSO2,qH2S,qCH4]
    tree.pack(fill=BOTH)
    Wgitwindow.mainloop()

startwindow = Interface()
startwindow.createform()