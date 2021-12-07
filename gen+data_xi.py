import Main_DSGE
from csv import writer

Main_DSGE.Lambda=int(0)
filename='dsge_irf_xi_varying_noadjust.csv'
with open(filename, 'a', newline='') as myfile:
    csvwriter = writer(myfile)
    to_list = [
        'xi-notadjust-consume',
        'xi-notadjust-investment',
        'xi-notadjust-Laobr',
    'xi-notadjust-houseprice',
    'xi-notadjust-Nonhouseprice',
    'xi-notadjust-GDP',
    'xi-notadjust-NonhouseProduction',
    'xi-notadjust-financegap',
    'xi-notadjust-homeleverage']

    csvwriter.writerow(to_list)
    to_list = [
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0
        ,0]
    csvwriter.writerow(to_list)

po=0
q = Main_DSGE.DSGE_Main()
q.simulation()
stable_C=q.C
stable_I=q.I
stable_n=q.n*2
stable_Ph=q.Ph
stable_Pf=q.Pf
stable_GDP=q.GDP
stable_Yf=q.Yf
stable_financegap=q.financegap
stable_homeleverage=q.Homeleverage
Initial_value=Main_DSGE.xi_home
simulated_times=160+1
Main_DSGE.xi_home+=0.0177
print("Finish")
while po<simulated_times:
    with open(filename, 'a',newline='') as myfile:
        q.simulation_bystep()
        Main_DSGE.xi_home=Initial_value
        csvwriter = writer(myfile)
        to_list =[
            q.C-stable_C ,
        q.I-stable_I  ,
        q.n  * 2 -stable_n,
        q.Ph-stable_Ph,
        q.Pf- stable_Pf ,
        q.GDP-stable_GDP ,
        q.Yf-stable_Yf ,
        q.financegap-stable_financegap,
            q.Homeleverage-stable_homeleverage
        ]
        to_write=[to_list[i] for i in range(len(to_list))]
        csvwriter.writerow(to_write)
    print("Simulation Period:", po)
    po+=1