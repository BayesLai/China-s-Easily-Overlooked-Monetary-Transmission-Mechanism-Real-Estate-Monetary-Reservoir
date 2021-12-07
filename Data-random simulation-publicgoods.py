from random import betavariate,gammavariate,seed
from time import sleep,time
from csv import writer
from sys import exc_info
from copy import copy
Consumption=[]
Investment=[]
HousePrice=[]
HeavyPrice=[]
NonheavyPrice=[]
ProductionValue=[]
Production=[]
sample_size=100
i_index=0
R_mean=0.0320
R_std=0.01092
mu_mean=0.0357
mu_std=0.0123
s_mean=0.2833
s_std=0.0471
xi_mean=0.0322
xi_std=0.0177
alpha_for_Beta=lambda mu,sigma:mu*(mu*(1-mu)/(sigma**2)-1)
beta_for_Beta=lambda mu,sigma:(1-mu)*(mu*(1-mu)/(sigma**2)-1)
beta_for_gamma=lambda mu,sigma:(sigma**2)/mu
alpha_for_gamma=lambda mu,sigma:mu/beta_for_gamma(mu,sigma)
Consumption_T = []
Investment_T = []
HousePrice_T = []
HeavyPrice_T = []
NonheavyPrice_T = []
Production_T = []
ProductionValue_T = []

Consumption_T_1 = []
Investment_T_1 = []
HousePrice_T_1 = []
HeavyPrice_T_1 = []
NonheavyPrice_T_1 = []
Production_T_1 = []
ProductionValue_T_1 = []

random_shock_R = []
ramdom_sock_mu=[]
random_shock_chi_c = []
random_shock_chi_i = []
random_shock_xi_home_c = []
random_shock_xi_home_i=[]
import Main_DSGE
q = Main_DSGE.DSGE_Main()
b=Main_DSGE.DSGE_Main()
q.simulation()
temp_lambda = Main_DSGE.Lambda
Main_DSGE.Lambda = 0
b.simulation()
Main_DSGE.Lambda= temp_lambda
stable_R=Main_DSGE.R
stable_mu=Main_DSGE.mu
stable_xi=Main_DSGE.xi_home
stable_theta=Main_DSGE.theta
filename="random_simulation-publicgoods.csv"
temp_lambda=Main_DSGE.Lambda
Data_to_write=[]

for i in    [
        'time',
            'externalities-lambda='+str(Main_DSGE.Lambda),
            'omega-lambda='+str(Main_DSGE.Lambda),
    'Tf-lambda='+str(Main_DSGE.Lambda),
    'omega-Tf-lambda='+str(Main_DSGE.Lambda),
    'omega-Tf-externalities-lambda='+str(Main_DSGE.Lambda),
'externalities-lambda='+str(0),
            'omega-lambda='+str(0),
    'Tf-lambda='+str(0),
    'omega-Tf-lambda='+str(0),
    'omega-Tf-externalities-lambda='+str(0),

    ]:
            Data_to_write.append(i)
with open(filename, 'a') as myfile:
    csvwriter = writer(myfile)
    csvwriter.writerow(Data_to_write)
save_Model=copy(q)
def sampling():
    global i_index,save_Model,q,save_bModel,b
    seed(int(time()*16000))
    R_shocks = betavariate(alpha_for_Beta(R_mean, R_std), beta_for_Beta(R_mean, R_std))
    mu_shocks = betavariate(alpha_for_Beta(mu_mean, mu_std), beta_for_Beta(mu_mean, mu_std))
    theta_shocks = betavariate(alpha_for_Beta(s_mean, s_std), beta_for_Beta(s_mean, s_std))
    xi_home_shocks = gammavariate(alpha_for_gamma(xi_mean, xi_std), beta_for_gamma(xi_mean, xi_std))


    try:
        print("-" * 50, i_index, "-" * 50)
        print("R shocks", R_shocks)
        print("mu shocks", mu_shocks)
        print("theta_shocks", theta_shocks)
        print("xi_shocks", xi_home_shocks)
        Main_DSGE.R = R_shocks  # if R_shocks>R_mean-1.5*R_std else R_mean
        Main_DSGE.mu = mu_shocks  # if mu_shocks>mu_mean-1.5*mu_std else mu_mean
        Main_DSGE.theta = theta_shocks  # if chi_c_shocks>chic_mean-1.5*chic_std else chic_mean
        Main_DSGE.xi_home = xi_home_shocks  # if xi_home_i_shocks>xi_investhome_mean-1.5*xi_investehome_std else xi_investhome_mean
        Data_to_write = []
        q.simulation_bystep()

        for i in [
            i_index+1,
           1/q.externalities,
            q.omega,
            ((1 - Main_DSGE.gamma_d) * q.G_part),
            (q.omega-1)*(Main_DSGE.psi_h+Main_DSGE.Tg) /(1-Main_DSGE.psi_h-Main_DSGE.phi_h)-(1+(1-Main_DSGE.gamma_d)*q.G_part),
            (q.omega - 1) * (Main_DSGE.psi_h+Main_DSGE.Tg) / (1 - Main_DSGE.psi_h - Main_DSGE.phi_h) -(1 + (1 - Main_DSGE.gamma_d) * q.G_part)/q.externalities,
        ]:
            Data_to_write.append(i)
        temp_lambda = Main_DSGE.Lambda
        Main_DSGE.Lambda = 0
        b.simulation_bystep()
        for i in [
           1/b.externalities,
            b.omega,
            ((1 - Main_DSGE.gamma_d) * b.G_part),
            (b.omega-1)*Main_DSGE.psi_h/(1-Main_DSGE.psi_h-Main_DSGE.phi_h)-(1+(1-Main_DSGE.gamma_d)*b.G_part),
            (b.omega - 1) * Main_DSGE.psi_h / (1 - Main_DSGE.psi_h - Main_DSGE.phi_h) -(1 + (1 - Main_DSGE.gamma_d) * b.G_part)/b.externalities,

        ]:
            Data_to_write.append(i)
        Main_DSGE.Lambda = temp_lambda
        with open(filename, 'a') as myfile:
            csvwriter = writer(myfile)
            csvwriter.writerow(Data_to_write)
        i_index += 1
        save_Model=copy(q)
    except:
        sleep(0.005)
        q=copy(save_Model)
        print(exc_info())

while i_index<=sample_size:
    sleep(0.005)
    sampling()