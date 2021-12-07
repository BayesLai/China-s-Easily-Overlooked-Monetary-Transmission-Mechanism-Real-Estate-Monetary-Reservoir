import Main_DSGE
from csv import writer

Main_DSGE.Lambda=int(0)
filename='dsge_irf_s_varying_noadjust.csv'
with open(filename, 'a', newline='') as myfile:
    csvwriter = writer(myfile)
    to_list = [
        's-noadjust-consume',
        's-noadjust-investment',
        's-noadjust-Laobr',
    's-noadjust-houseprice',
    's-noadjust-Nonhouseprice',
    's-noadjust-GDP',
    's-noadjust-NonhouseProduction',
    's-noadjust-financegap',
    's-noadjust-homeleverage']

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
simulated_times=160+1

Initial_value=Main_DSGE.theta
Main_DSGE.theta+=0.0471
print("Finish")
while po<simulated_times:
    with open(filename, 'a',newline='') as myfile:
        q.simulation_bystep()
        Main_DSGE.theta=Initial_value
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
