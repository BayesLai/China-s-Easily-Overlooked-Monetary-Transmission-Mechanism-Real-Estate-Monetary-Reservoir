from csv import writer
from time import sleep
filename='StaticSimulation.csv'
with open(filename, 'a', newline='') as myfile:
    csvwriter = writer(myfile)
    to_list = [
        'Lambda',
    'Lambda',]
    csvwriter.writerow(to_list)
po=0
simulated_times=500
max_Lambda=1
po_alpha=0
max_alpha=1
import Main_DSGE
while po<simulated_times:
    Main_DSGE.Lambda = (0.2 + po) * max_Lambda / simulated_times
    print("-" * 100)
    print("Simulation :", po, po_alpha)
    while po_alpha <= simulated_times:
        Main_DSGE.alpha = (0 + po_alpha) * max_alpha / simulated_times
        q = Main_DSGE.DSGE_Main()
        q.simulation(True)
        with open(filename, 'a', newline='') as myfile:
            csvwriter = writer(myfile)
            to_list = [
                Main_DSGE.Lambda,
                Main_DSGE.alpha,
                q.externalities * q.omega]
            print(to_list)
            last_var = to_list
            csvwriter.writerow(to_list)
        po_alpha += 1
    po_alpha=0
    po += 1
