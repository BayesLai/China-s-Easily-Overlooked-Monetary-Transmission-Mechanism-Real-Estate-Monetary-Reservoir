# -*- coding: utf-8
from math import exp,log,sqrt
from scipy.optimize import basinhopping
import sys
from sys import exc_info
from csv import writer
from copy import copy
from random import normalvariate
#校准参数
added_rate=int(0)
beta=0.98#居民主观贴现率
mu=0.03363861789360544#住房贷款比例
eta=0.03#住房交易成本
sigma=0.9
rho=1.5
perfer=0.05
chi=0.8
p_ir=1
j=0.2
delta_k=0.1
kappa=0.1
phi=1.2
xi=0.5
Tg=0.05
psi_f=0.06
phi_f=0.3
psi_h=0.3
phi_h=0.4
X=1.2
delta=0.05
theta=0.2833
Tq=0.05
gamma_d=0.9
omega=0.4
Omega_i=0.2
Omega_c=0.3
Gamma=0.5
rho_R= .992881
rho_gdp= .007119
Lambda=0.02
alpha=1
xi_home=Initial_xi_home=0.0322149083684202
R=InitialR=0.03199


class DSGE_Main(object):
    def __init__(self):
        #一阶段初始化
        self.reset()
    def reset(self):
        global R, xi_home
        R=InitialR
        xi_home=Initial_xi_home
        self.PL = 1
        self.omega =((1 - theta)* R) ** (-1/(1+xi_home))
        self.rh = R * (self.omega) ** (xi_home)
        lambda_t = -((chi / beta) * (1 + R) / (1 + self.rh))
        Lambda_t = chi * (1 + R) * (1 + 1 / (beta * (1 + self.rh)))
        self.C = (-lambda_t) ** (-1 / sigma)
        self.Wn = -j / (lambda_t * (1 + beta * theta * (delta - 1)) - mu * Lambda_t)
        self.PhYh = self.Wn * self.omega / (1 - psi_h - phi_h)
        self.n = sqrt(self.omega * (1 - Tg) * self.Wn * self.C ** (-sigma) / (2 * kappa))
        self.W = self.Wn / self.n
        self.Homeleverage = ((phi_h + psi_h) / self.omega + (self.omega) - 1) / (2 * (1 - Tg) * (1 - psi_h - phi_h))
        self.PfYf = self.PhYh / self.omega
        self.GDP = self.PhYh + self.PfYf
        self.initial_R = R
        self.Kh = self.PhYh * phi_h
        self.Kf = self.PfYf * phi_f
        self.Ih = self.PhYh * phi_h - (1 - delta_k) * self.Kh
        self.If = self.PfYf * phi_f - (1 - delta_k) * self.Kf
        self.I = self.Ih + self.If
        self.G_part = (psi_f + Tg) / (1 - psi_f - phi_f) + (psi_h + Tq) * self.omega / (1 - psi_h - phi_h) + 2 * Tg
        self.Pf = self.Wn * (1 / (1 - psi_f - phi_f) + ((1 - gamma_d) / (1 - psi_f - phi_f) - gamma_d) * self.G_part) / (
                    self.C + self.I)

        self.Ph = self.Pf * self.omega ** (1 - psi_h - phi_h) * \
                  (self.Wn * (1 + (1 - gamma_d) * self.G_part)) ** (psi_f + phi_f - phi_h - psi_h) * \
                  self.n ** (phi_h + psi_h - psi_f - phi_f) * \
                  self.PL ** (psi_h - psi_f) * \
                  (phi_f / (1 - psi_f - phi_f)) ** phi_f * \
                  (phi_f / (1 - psi_f - phi_f)) ** phi_f * \
                  (psi_f / (1 - psi_f - phi_f)) ** psi_f * (1 - psi_f - phi_f) / (
                              (phi_h / (1 - psi_h - phi_h)) ** phi_h * (phi_h / (1 - psi_h - phi_h)) ** phi_h * (
                                  psi_h / (1 - psi_h - phi_h)) ** psi_h * (1 - psi_h - phi_h))
        self.Yh = self.PhYh / self.Ph
        self.Yf = self.PfYf / self.Pf
        self.T = self.G_part * self.Wn
        self.Gt=self.T*gamma_d
        self.financegap = ((psi_f + Tg) / (1 - psi_f - phi_f) + (psi_h + Tq) * (self.omega - 1) / (
                    1 - psi_h - phi_h) + 2 * Tg) * self.Wn\
        # 需要用到的稳态值
        self.GDP = (self.PhYh + self.PfYf)
        self.stable_GDP = self.GDP
    def simulation_bystep(self,**randomshocks):
        global R
        self.omega =((1 - theta)* R) ** (-1/(1+xi_home))
        self.xi=xi_home
        self.rh =R * (self.omega) ** (xi_home)
        self.PL=1
        lambda_t = -((chi / beta) * (1 + R) / (1 + self.rh))
        Lambda_t = chi * (1 + R) * (1 + 1 / (beta * (1 + self.rh)))
        self.C = (-lambda_t) ** (-1 / sigma)

        self.Wn =-j / (lambda_t * (1 + beta * theta * (delta - 1)) - mu * Lambda_t)
        self.G_part = ((psi_f + Tg) / (1 - psi_f - phi_f) + (psi_h + Tq) * self.omega / (1 - psi_h - phi_h) + 2 * Tg)
        self.PhYh = self.Wn * self.omega / (1 - psi_h - phi_h)
        try:
            self.n = sqrt(self.omega * (1 - Tg) * self.Wn * self.C ** (-sigma) / (2 * kappa))
        except:
            print("sdfs")
        self.W = self.Wn / self.n
        self.Homeleverage = ((phi_h + psi_h) / self.omega + (self.omega) - 1) / (2 * (1 - Tg) * (1 - psi_h - phi_h))
        self.PfYf = self.PhYh / self.omega
        self.Kh = self.PhYh * phi_h
        self.Kf = self.PfYf * phi_f
        self.Ih = self.PhYh * phi_h - (1 - delta_k) * self.Kh
        self.If = self.PfYf * phi_f - (1 - delta_k) * self.Kf
        formalPh=self.Ph

        self.Pf =self.Wn*(1/(1-psi_f-phi_f)+((1-gamma_d)/(1-psi_f-phi_f)-gamma_d)*self.G_part)/(self.C+self.I)

        self.Ph = self.Pf*self.omega**(1-psi_h-phi_h)*\
                  (self.Wn*(1+(1-gamma_d)*self.G_part))**(psi_f+phi_f-phi_h-psi_h)*\
                  self.n**(phi_h+psi_h-psi_f-phi_f)*\
                  self.PL**(psi_h-psi_f)*\
                  (phi_f/(1-psi_f-phi_f))**phi_f*\
                  (phi_f/(1-psi_f-phi_f))**phi_f*\
        (psi_f / (1 - psi_f - phi_f)) ** psi_f*(1 - psi_f - phi_f)/((phi_h/(1-psi_h-phi_h))**phi_h*(phi_h/(1-psi_h-phi_h))**phi_h* (psi_h / (1 - psi_h - phi_h)) ** psi_h*(1 - psi_h - phi_h))
        self.Yh = self.PhYh / self.Ph
        self.Yf = self.PfYf / self.Pf
        self.K = self.Kh+self.Kf
        self.I=self.Ih+self.If
        former_Gt= self.Gt
        self.T = self.G_part*self.Wn
        self.Gt = self.T * gamma_d
        self.market_Pre=self.PhYh/self.PfYf
        self.Price_pre=self.Ph/self.Pf
        self.financegap = ((psi_f + Tg) / (1 - psi_f - phi_f) + (psi_h + Tq) * (self.omega -1)/ (1 - psi_h - phi_h) + 2 * Tg)*self.Wn

        if 'Culmulative_GovernmentInvest' in self.__dir__():
            self.Culmulative_GovernmentInvest+=(alpha*(self.Gt)-delta_k*self.Culmulative_GovernmentInvest)
        else:
            self.Culmulative_GovernmentInvest=alpha*self.Gt
        formalGDP=self.GDP
        self.externalities=exp(-Lambda*self.Culmulative_GovernmentInvest)
        self.GDP =( self.PhYh + self.PfYf)/self.externalities
        R=self.initial_R*(R/self.initial_R)**rho_R*(self.GDP/(formalGDP))**rho_gdp
        print(R)
    def simulation(self,finance_self_adjust=True,error=1e-10):
        formalPh=self.Ph/2
        i=0
        while abs(log(self.Ph/formalPh))>error:
            #print("迭代中,现在收敛为",abs(log(self.Ph/formalPh)))
            formalPh=self.Ph
            self.simulation_bystep(finance_self_adjust=finance_self_adjust)
            i+=1
        print("达到稳态,迭代次数%d"%i)

a=DSGE_Main()

print("*"*100)
a.simulation()
for k in a.__dir__():
    print(k,":",a.__getattribute__(k))
print("sdg")





