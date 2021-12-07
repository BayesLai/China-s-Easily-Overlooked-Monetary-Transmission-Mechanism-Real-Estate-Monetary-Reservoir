# -*- coding: utf-8
from scipy.fftpack import fft
from csv import reader
from numpy import angle,corrcoef,std,mean
from math import pi,log
filename='Americadata.csv'
#filename='Chinesedata.csv'
def FourierAndRank(x):
    fft_x=fft(x)
    Angle_x=angle(fft_x)/(2*pi)
    Abs_X=abs(fft_x)
    Phase=[]
    Rank=[]
    for i in sorted(list(Abs_X[:int(len(Abs_X)/2)]),reverse=True):
        Phase.append(abs(Angle_x[list(Abs_X).index(i)]))
    a=sorted(Phase,reverse=True)
    for i in sorted(Phase,reverse=True):
        Rank.append(Phase.index(i)+1)
    return Angle_x,Abs_X,Rank
CUL_CPI=1
CUL_PPI=1
if filename=='Chinesedata.csv':
    with open(filename,'r') as myfile:
        filereader=list(reader(myfile))
        M2=[]
        CPI=[]
        PPI=[]
        SZindex=[]
        Phindex=[]
        Premium=[0]
        Premium_PPI=[0]
        Premium_CPI = [0]
        for i in filereader[2:]:
            M2.append(float(i[1]))
            CPI .append(float(i[2])/100)
            PPI .append(float(i[3])/100)
            SZindex .append(float(i[4]))
            Phindex.append(float(i[5]))
            if len(M2)>1:
                Premium.append(float(i[5])-float(i[4]))
                Premium_PPI.append(float(i[5])-float(i[3])/100)
                Premium_CPI.append(float(i[5])-float(i[2])/100)
                CUL_PPI*=(1+float(i[5])-float(i[3])/100)
                CUL_CPI*=(1+float(i[5])-float(i[2])/100)
                print("Premium CPI",float(i[5]) - float(i[2]) / 100)
                print("Premium PPI",float(i[5]) - float(i[3]) / 100)
    M2F=FourierAndRank(M2)
    CPIF=FourierAndRank(CPI)
    PPIF=FourierAndRank(PPI)
    SZindexF=FourierAndRank(SZindex)
    PhindexF=FourierAndRank(Phindex)
    PremiumF=FourierAndRank(Premium)
    Premium_PPIF=FourierAndRank(Premium_PPI)
    Premium_CPIF=FourierAndRank(Premium_CPI)
    COV=corrcoef([M2,CPI,PPI,SZindex,Phindex,Premium,Premium_PPI,Premium_CPI])
    COVF=corrcoef([M2F[2],CPIF[2],PPIF[2],SZindexF[2],PhindexF[2],PremiumF[2],Premium_PPIF[2],Premium_CPIF[2]])
    print("CPI",CUL_CPI)
    print("PPI",CUL_PPI)
    print("df")
else:
    with open(filename,'r') as myfile:
        filereader=list(reader(myfile))
        D_Ph=[]
        InterestRate=[]
        CPI=[]
        PPI=[]
        D_Dowjones=[]
        Premium_CPI=[0]
        Premium_PPI=[0]
        GDP=[]
        UnEm=[]
        for i in filereader[1:]:
            GDP.append(float(i[6])/100)
            UnEm.append(float(i[7])/100)
            D_Ph.append(float(i[5])/100)
            InterestRate.append(float(i[1]))
            CPI.append(float(i[2])/100)
            PPI.append(float(i[4])/100)
            D_Dowjones .append(float(i[3]))
            if len(CPI)>1:
                Premium_CPI.append(D_Dowjones[-1]-CPI[-1])
                Premium_PPI.append(D_Dowjones[-1]-PPI[-1])
                CUL_PPI *= (1 + Premium_PPI[-1])
                CUL_CPI *= (1 + Premium_CPI[-1])
                print("Premium_CPI:",Premium_PPI[-1])
                print("Premium PPI:",Premium_PPI[-1])
    GDPF=FourierAndRank(GDP)
    UnEmF=FourierAndRank(UnEm)
    InterestrateF=FourierAndRank(InterestRate)
    CPIF=FourierAndRank(CPI)
    DjonesF=FourierAndRank(D_Dowjones)
    PPIF=FourierAndRank(PPI)
    PhF=FourierAndRank(D_Ph)
    Premium_PPIF = FourierAndRank(Premium_PPI)
    Premium_CPIF = FourierAndRank(Premium_CPI)
    COV = corrcoef([InterestRate, UnEm, GDP, CPI, PPI,D_Dowjones, D_Ph,Premium_PPI,Premium_CPI])
    COVM=corrcoef([InterestrateF[2],UnEmF[2],GDPF[2],CPIF[2],PPIF[2],DjonesF[2],PhF[2],Premium_PPIF[2],Premium_CPIF[2]])
    print("CPI", CUL_CPI)
    print("PPI", CUL_PPI)
    print("df")
