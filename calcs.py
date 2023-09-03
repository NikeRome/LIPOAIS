from dicts import *
from scipy.interpolate import interp1d
import numpy as np
import math
#5.1

def CountW(Wvstatus,Wv,Ustatus,U,d0, Uzv, Type):
  S = np.pi * (d0/2)**2
  if Ustatus == 1:
    if Type == 1:
      Uout = 0.2 * Uzv
    else:
      Uout = 0.5 * Uzv
  else:
    Uout = float(U)
  if Wvstatus == 1:
    Wvout = 0.785 * Uout * S
  else:
    Wvout = float(Wv)
  return(round(Wvout,3),round(Uout+0.1,3))

#5.2

def CountPg(VolumeDict,Pgimport, Pginfo):
  Pj = [0]*len(VolumeDict)
  if Pginfo:
    DensitySum = 0
    n = 0
    for key in VolumeDict.keys():
      Pj[n] = round(VolumeDict.get(key) * Dictionaries.DensityDict.get(key),3)
      DensitySum = DensitySum + (VolumeDict.get(key) * Dictionaries.DensityDict.get(key))
      n = n + 1
    Pg = round(DensitySum,3)
  else:
    Pg = float(Pgimport)
  return  Pj, round(0.01 *Pg,3)


def CountWg(Wv,Pg):
  return(3600*Wv*Pg)

#5.3
def CountWpr(Wv, Vps, Tr):
  Wpr = Wv * Vps * ((273+Tr)/273)
  return(Wpr)


#6.1 Расчет физико-химических характеристик сжигаемого попутного нефтяного газа
#Расчет условной молекулярной массы ПНГ ug, кг/моль (п. 6.1.2)
def CountMassMol(VolumeDict):
  MassSum = 0
  uj = []
  for key in VolumeDict.keys():
    uj.append(round(0.01* VolumeDict.get(key) * Dictionaries.MassDict.get(key),3))
    MassSum = MassSum + VolumeDict.get(key) * Dictionaries.MassDict.get(key)
  ug = 0.01 * MassSum
  return(ug, uj)

#Расчет массового содержания химических элементов (% масс.)в ПНГ (формулы 3 и 4 Приложения А).
#подрядок элементов в массиве: C H N O S
def CountMassSoderj(VolumeDict,Pg):
  bj = [0, 0, 0, 0, 0]
  bi = [0]*len(VolumeDict.keys())
  n = 0
  for key in VolumeDict.keys():
    bi[n] = round(0.01 * VolumeDict.get(key) * (Dictionaries.DensityDict.get(key) / Pg),3)
    n+= 1
  for key in VolumeDict.keys(): 
    for j in range(len(bj)):
      bj[j] = round(bj[j] + (0.01 * VolumeDict.get(key) *
        (Dictionaries.DensityDict.get(key)/Pg)) * (Dictionaries.ComponentMassDict.get(key)[j]),3)
  return(bj)

#Расчет числа атомов элементов в условной молекулярной формуле ПНГ (формулы 5 и 6 Приложения А).
#подрядок элементов в массиве: C H N O S
def CountAtomNumbers(bj,ug,uj,AtomicMass):
  Katom = [0, 0, 0, 0, 0]
  Ugtochn = 0
  for j in range(len(Katom)):
    Katom[j] = round(0.01 * (bj[j] / AtomicMass[j]) * ug,3)# Кол-во атомов C H N O S
    Ugtochn += Katom[j] * uj[j] # Для прил. B2 - уточненная молекулярная масса
  return(Katom, Ugtochn)

#6.2 Расчет физико-химических характеристик влажного воздуха для заданных метеосуловий
# Определение массового влагосодержания d (кг/кг) влажного воздуха по номограмме (прил. Б1)

def CountDbyMeteo(t, fi):
  y = [-5,0,5,10,15,20,25,30,35,40]
  y8 = [-5,0,5,10,15,20,25,30,35]
  y10 = [-5,0,5,10,15,20,25,30,32.5]
  x2 = [0.00045,0.0007,0.001,0.00142,0.0021,0.0029,0.004,0.0055,0.0076,0.00985]
  x4 = [0.001,0.0016,0.0021,0.003,0.00405,0.00587,0.008,0.011,0.0145, 0.0192]
  x6 = [0.0017,0.0022,0.003,0.0042,0.0063,0.0087,0.0119,0.016,0.0218,0.02895]
  x8 = [0.00198,0.00308,0.0041,0.006,0.0085,0.01185,0.016,0.0215,0.029]
  x10 = [0.00292,0.004,0.00536,0.0079,0.0109,0.0149,0.02,0.027,0.031]

  functions_of_t = [None, None, 
  interp1d(y,x2, kind='linear', bounds_error=False,fill_value='extrapolate'), None,
  interp1d(y,x4, kind='linear', bounds_error=False,fill_value='extrapolate'), None,
  interp1d(y,x6, kind='linear', bounds_error=False,fill_value='extrapolate'), None,
  interp1d(y8,x8, kind='linear', bounds_error=False,fill_value='extrapolate'), None,
  interp1d(y10,x10, kind='linear', bounds_error=False,fill_value='extrapolate')]
  d = 0
  if fi == 20:
    d = functions_of_t[2](t)
  if fi == 40:
    d = functions_of_t[4](t)
  if fi == 60:
    d = functions_of_t[6](t)
  if fi == 80:
    d = functions_of_t[8](t)
  if fi == 100:
    d = functions_of_t[10](t)
  return(d)

#Расчет парциального давления водяного пара, мм. рт. ст. (Pp)
def CountPpbyD(d):
  base_d = [0,0.081,0.017,0.0259,0.035]
  base_Pp = [0,10,20,30,40.8]
  funcPp_d = interp1d(base_d,base_Pp, kind = 'linear')
  return(round(funcPp_d(d)+0.5,0),funcPp_d)


#Расчет количества атомов химических элементов в условной 
# молекулярной формуле влажного воздуха (табл.3.Приложения Б).

def CountAtomsinWetAir(d, t, P, Pp): #d 20 60 760
  AirElements = {'Воздух' : [23.27, 76.73, 0], 'Влага': [88.81, 0, 11.19]}
  ComponentMass = {'O': [AirElements.get('Воздух')[0]/(1+d),
                  AirElements.get('Влага')[0]*d/(1+d)],
                  'N': [AirElements.get('Воздух')[1]/(1+d),
                  AirElements.get('Влага')[1]*d/(1+d)],
                  'H': [AirElements.get('Воздух')[2]/(1+d),
                  AirElements.get('Влага')[2]*d/(1+d)],}
  for key in ComponentMass:
    ComponentMass[key].append(np.sum(ComponentMass.get(key)))
    
  Kj = np.round([(0.421+1.607*d)/(1+d), 1.586/(1+d), 3.215*d/(1+d)],3) #(O, N H)
  return ComponentMass, Kj
# Расчет плотности влажного воздуха Р в.в., кг/м3 (формула 5 Приложения Б).
def CountPvv(t,P,Pp):
  return(round(0.4648* (P - 0.3783 * Pp)/(273.2 + t),3))


#6.3. Расчет стехиометрической реакции горения попутного нефтяного газа в атмосфере влажного воздуха.

#Расчет мольного стехиометрического коэффициента М (формула 2 Приложения В).
def CountM(Katom,Kj):
  M = 0
  sub = 0
  valentnostKatom = [4, 1, 0, -2, -2] #Валентности веществ ПНГ C H N O S 
  valentnostKj = [-2, 0, 1] #Валентности веществ вл. воздуха O N H
  for j in range(len(Katom)):
    M += Katom[j] * -valentnostKatom[j]
  for j in range(len(valentnostKj)):
    sub += Kj[j] * valentnostKj[j]
  M = M/sub

  Vvv = M  # Кол-во влажного воздуха, необходимого для полного сгорания 1м3 ПНГ, м3
  return(round(M,3),round(Vvv,3))


#Расчет количества продуктов сгорания Vпc (м3/м3), образующихся при стехиометрическом
# сгорании 1 м3 ПНГ в атмосфере влажного воздуха (формула 3 Приложения В).
def CountVps(Katom, Kj, M):
  return(round(Katom[0] + Katom[4] + 0.5*(Katom[1] + Katom[2] + M * (Kj[2] + Kj[1])),3))


#6.4. Проверка выполнения условий бессажевого горения попутного 
# нефтяного газа на факельной установке.

#Расчет показателя адиабаты K для ПНГ и Расчет скорости распространения звука в 
# сжигаемой газовой смеси и Uzv (м/с) (формула 1 Приложения Г)
def CountK(VolumeDict,Ugtochn, t):
  AdiabatKi = {}
  for key in VolumeDict:
    AdiabatKi[key] = round(VolumeDict.get(key) * Dictionaries.AdiabatDict.get(key),4)

  AdiabatK = 0
  for key in Dictionaries.AdiabatDict:
    AdiabatK += AdiabatKi[key]
  AdiabatK = 0.01 * round(AdiabatK,4)
  Uzv = round(91.5 * ((AdiabatK * (t + 273)/Ugtochn))**0.5) # м/c
  return(Uzv, AdiabatK)


#Проверка выполнения условия бессажевого горения:
def CheckSoot(U, Uzv):
  if U >= 0.2*Uzv:
    return True
  else:
    return False

# 6.5. Определение удельных выбросов вредных веществ на единицу
# массы сжигаемого попутного нефтяного газа (кг/кг).
#Для оценок мощности выбросов, оксида углерода, оксидов
#азота (в пересчете на диоксид азота), а также сажи в случае невыполнения
#условия бессажевого сжигания используются опытные значения удельных
#выбросов на единицу массы сжигаемого газа [4], 
# представленные в таблице ниже:
#РАСЧЕТ МАКСИМАЛЬНЫХ И ВАЛОВЫХ ВЫБРОСОВ ВРЕДНЫХ ВЕЩЕСТВ
#7.1. Расчет максимальных выбросов вредных веществ в (г/сек):
# CO; NO; Сажа; бензапирен. - строки
# Бессаживое; с сажей. - столбцы
Ejection_table = [[0.02, 0.25],
                    [0.003, 0.002],
                    [0, 0.03],
                    [2*(10**-11), 8*(10**-11)]]
def CountEjectionMain(VolumeDict,uj,NoSoot,Wg, Katom, Ugtochn,nedojeg_var,nedojeg_value):
  
  if NoSoot:
    qCO = Ejection_table[0][0] #удельный выброс оксида углерода
    qNO = Ejection_table[1][0] #удельный выброс оксида азота
    qPetrol = Ejection_table[3][0] #удельный выброс бензапирена
    nedojeg = 0.0006 # коэффициент недожега
    qSaja = 0
  else:
    qCO = Ejection_table[0][1]
    qNO = Ejection_table[1][1]
    qPetrol = Ejection_table[3][1]
    nedojeg = 0.035
    qSaja = 0.03
  if nedojeg_var== 0:
    nedojeg = float(nedojeg_value)
  
  qH2S = round(0.01 * nedojeg * uj[-1]/Ugtochn * 100,6)
  massSO2 = 16*2+32.066
  qSO2 = round(massSO2*(Katom[4]/Ugtochn),6) #удельный выброс диоксида серы
  
  metanmass = 0 # удельный выброс углеводородов в пересчете на метан
  metan = Dictionaries.MassDict.get('Метан')* VolumeDict.get('Метан')
  for key in Dictionaries.MassDict:
    if Dictionaries.riDict.get(key) != None:
      if key != 'Метан':
        metanmass += Dictionaries.riDict.get(key)*Dictionaries.MassDict.get(key)

  qCH4 = round(metanmass/metan*100 * nedojeg * Wg * 0.01,6)
  qi = [qCO,qNO,qPetrol,qSaja,qSO2,qH2S,qCH4]
  #удельные выбросы в г/c
  return(qi,nedojeg)

#7.2. Расчет валовых выбросов вредных веществ за год (т/год)
def CountPolutionMax(qi,Wg):
  Wgi = []
  for i in range(len(qi)):
    if i == 6:
      Wgi.append(qi[i])
    else:
      Wgi.append(0.278*qi[i]*Wg)
  return Wgi
    
def CountPolutionPerYear(qi,Wg,time): 
  Wgit = []
  for i in range(len(qi)):
    Wgit.append(0.001 * qi[i] * Wg *time)
  return Wgit

#8 РАСЧЕТ ПАРАМЕТРОВ ФАКЕЛЬНОЙ УСТАНОВКИ КАК ПОТЕНЦИАЛЬНОГО 
# ИСТОЧНИКА ЗАГРЯЗНЕНИЯ АТМОСФЕРЫ
#8.1. Расчет высоты источника выброса загрязняющих веществ 
# в атмосферу над уровнем земли, Н (м)

# 8.3.1. Расчет удельных выбросов Н20, N2 и O2 на единицу массы
#сжигаемого ПНГ (кг/кг) (Приложение Е).
def CountEjectionSub(VolumeDict,AtomicMass,Katom,Ugtochn,qi,Wg,a,M,Kj,nedojeg,uj):
  #qi = [qCO,qNO,qPetrol,qSaja,qSO2,qH2S,qCH4]
  massCO = AtomicMass[0] + AtomicMass[3]
  #Удельный выброс диоксида углерода
  qCO2 = round(float(Dictionaries.MassDict.get('Диоксид'))*((Katom[0]/Ugtochn)-
        (qi[6]/Wg/float(Dictionaries.MassDict.get('Метан')))-(qi[0]/Wg/massCO)),6)

  massH2O = 2 * AtomicMass[1] + AtomicMass[3]  #(C H N O S)
  #порядок элементов для количества атомов Katom (O, N, H)
  #Удельный выброс водяного пара
  qH2O = 0.5 * massH2O * ((1/Ugtochn)*(Katom[1] + a * M * Kj[2])-qi[6]/Wg/float(Dictionaries.MassDict.get('Метан')))

  #Удельный выброс сероводорода
  qH2S = 0.01 * nedojeg * uj[-1]/Ugtochn * 100
  
  #Удельный выброс азота
  qN2 = float(Dictionaries.MassDict.get('Азот')) * (1/Ugtochn * (Katom[2] + a * M * Kj[1]) 
      - qi[1]/Wg/float(Dictionaries.MassDict.get('Азот')))

  massNO = AtomicMass[2] + AtomicMass[3]
  massSO2 = 16*2+32.066
  #Удельный выброс кислорода
  qO2 = 32 * (((1/Ugtochn) * (Katom[3] + a * M * Kj[0])) - 2 * (qCO2/float(Dictionaries.MassDict.get('Диоксид'))) -
        (qH2O/massH2O) - 2 * (qi[4]/massSO2) - (qi[0]/Wg/massCO) - (qi[1]/Wg/massNO))
  qi_larger = qi
  qi_larger.append(round(qCO2,6))
  qi_larger.append(round(qH2O,6))
  qi_larger.append(round(qH2S,6))
  qi_larger.append(round(qN2,6))
  qi_larger.append(round(qO2,6))
  return(qi_larger)

#8.3.2. Расчет низшей теплоты сгорания сжигаемого газа QH (Ккал/м3) (Приложение 3).
def CountQh(VolumeDict):
  Qh = (85.5* VolumeDict.get('Метан') + 152 * VolumeDict.get('Этан') + 218 * VolumeDict.get('Пропан') + 
        283 * VolumeDict.get('Бутан') + 349 * VolumeDict.get('Пентан') + 56 * VolumeDict.get('Сероводород'))
  return(Qh)

def CountDelta(Ugtochn):
  return(0.048*(Ugtochn**0.5))

#8.3.4. Расчет количества теплоты в продуктах сгорания попутного
# нефтяного газа для трех значений температуры горения Т “К (например,
# Т, = 1500°К; Т2 = 1900°К; Т3 = 2300°К) Qnc (Ккал)
def CountQpsTr(qi_larger,Qh,delta):
              #  0  1     2       3    4     5    6   7     8    9  10   11
  #qi_larger = [qCO,qNO,qPetrol,qSaja,qSO2,qH2S,qCH4,qCO2,qH20,qH2S,qN2,qO2]
  qi_8 = [qi_larger[7],qi_larger[8],qi_larger[0],qi_larger[1],
          qi_larger[10],qi_larger[11],qi_larger[6],qi_larger[9]]
  #Средние массовые изобарные теплоемкости составляющих продуктов
  #сгорания, определяемые в интервале от 293 °К до Т °К (Ккал/кг град).
  # 1100, 1500, 1900, 2300
  Heatvolume = [
    # CO2    H20     CO     NO     N2    O2     CH4    H2S
    [0.263, 0.500, 0.266, 0.254, 0.263, 0.244, 0.844, 0.280],
    [0.279, 0.543, 0.276, 0.263, 0.273, 0.252, 0.967, 0.302],
    [0.289, 0.563, 0.283, 0.269, 0.280, 0.258, 1.060, 0.323],
    [0.297, 0.589, 0.288, 0.274, 0.285, 0.263, 1.132, 0.345]]
  #Расчет кол-ва теплоты в продуктах сгорания ПНГ для 4 значений темпеатуры горения T в K
  # (T1 = 1100, T2 = 1500K, T3 = 1900K, T4 = 2300K) Qps (Ккал)
  Tmassive = [1100, 1500, 1900, 2300]
  Qps = [0, 0, 0, 0]
  for i in range(4):
    for j in range(len(qi_8)):
      if j == 0 or j == 1 or j == 4 or j == 5:
        Qps[i] += round(Heatvolume[i][j] * qi_8[j] * (Tmassive[i] - 293)/2)
  func_T_Qps = interp1d(Qps,Tmassive,kind='linear',bounds_error=False,fill_value='extrapolate')
  return(Qps,func_T_Qps(Qh*(1-delta))-273,func_T_Qps)


def CountFakelParameters(VolumeDict,Hb,d0,Tr,T0,Vvv,Pvv,Pg,hg,La,Type): #Tr - из прил. И
  uglesum = 0
  num = 1
  for key in VolumeDict:
    if key == 'Азот':
      break
    else:
      uglesum +=(num + (2 * num + 2)/4) * float(VolumeDict.get(key))
      num += 1
  
  V0 = 0.0476 * (1.5 * float(VolumeDict.get('Сероводород')) 
              + uglesum - float(VolumeDict.get('Диоксид'))) #Стехиометрическое 
  #кол-во сухого воздуха для сжигания 1м3 ПНГ.
  Lf = 5.3 * d0 * math.sqrt((Tr / T0) * math.sqrt((1 + V0) * (1 + Vvv * Pvv/Pg)))# Lf - длина факела (формула 1 прил. Ж)
  if Type == 1:
    Height = float(Hb) + Lf #Высота источника выброса загрязняющих веществ атмосферу над ур. земли, м
  else:
    Height = 0.707 * (Lf - float(La)) + float(hg)
  return(Height, Lf)

#8.2. Расчет расхода и средней скорости поступления в атмосферу
# газовой смеси (продуктов сгорания)

def CountWps(Wpr,Lf):
  Df = 0.189 * Lf
  Wps = (1.274*Wpr) / (Df**2)
  return round(Wps,3)