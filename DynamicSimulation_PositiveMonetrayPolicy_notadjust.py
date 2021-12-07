import Main_DSGE
from csv import writer
from random import betavariate,gammavariate,seed
from time import time
seed(int(time()*10))
alpha_for_Beta=lambda mu,sigma:mu*(mu*(1-mu)/(sigma**2)-1)
beta_for_Beta=lambda mu,sigma:(1-mu)*(mu*(1-mu)/(sigma**2)-1)
beta_for_gamma=lambda mu,sigma:(sigma**2)/mu
alpha_for_gamma=lambda mu,sigma:mu/beta_for_gamma(mu,sigma)
filename='DynamicSimulation_PositiveMonetrayPolicy-notadjust.csv'
simulatetimes=80
Vary_Times=6
with open(filename, 'a', newline='') as myfile:
    csvwriter = writer(myfile)
    to_list = [
        'time',
         'P-notadjust-consume',
        'P-notadjust-investment',
        'P-notadjust-Laobr',
    'P-notadjust-houseprice',
    'P-notadjust-Nonhouseprice',
    'P-notadjust-GDP',
    'P-notadjust-NonhouseProduction',
    'P-notadjust-financegap',
    'P-notadjust-homeleverage',
        'P-notadjust-pricepremium',
    'R randomshock',
    'Mu randomshock',
        'Xi randomshocks'
    ]
    csvwriter.writerow(to_list)
po=0
q = Main_DSGE.DSGE_Main(Taylor_monetary_policy=True)
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
stable_R=Main_DSGE.R
stable_mu=Main_DSGE.mu
stable_xi=Main_DSGE.xi_home
while po<simulatetimes:
    with open(filename, 'a',newline='') as myfile:
        q.simulation_bystep()
        csvwriter = writer(myfile)
        to_list =[
            po,
            q.C - stable_C,
            q.I - stable_I,
            q.n * 2 - stable_n,
            q.Ph - stable_Ph,
            q.Pf - stable_Pf,
            q.GDP - stable_GDP,
            q.Yf - stable_Yf,
            q.financegap - stable_financegap,
            q.Homeleverage - stable_homeleverage,
            q.PricePremium,
            Main_DSGE.R-stable_R,
            Main_DSGE.mu-stable_mu,
            Main_DSGE.xi_home-stable_xi
        ]
        to_write=[to_list[i] for i in range(len(to_list))]
        last_var=to_list
        csvwriter.writerow(to_write)
    print("Simulation Period:", po)
    if po < Vary_Times:
        Main_DSGE.R *= 0.99
        Main_DSGE.mu /= 0.99
        Main_DSGE.xi_home *= 0.99

    po+=1