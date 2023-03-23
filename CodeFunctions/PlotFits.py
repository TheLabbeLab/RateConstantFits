import os
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from CodeFunctions import FittingFunctions
from CodeFunctions import ErrorFunctions

AvagadroNum = 6.0221408e+23 # For converting Bimolecular rates from cm3/s-molecules to cm3 / s-mol 

# Plotting Class
def PlotterFitter(Temp, Rates, RateName, Pressure, Bimolec, WeightsIndices=[]):
    # def __init__(self, Temp, Rates, RateName, Pressure, WeightsIndices=[] , Bimolec = False):
    #     self.Temp = Temp
    #     if Bimolec == True:
    #         self.Rates = Rates * Avagadro
    #     self.RateName = RateName
    #     self.Pressure = Pressure
    #     self.WeightsIndices = WeightsIndices

    if Bimolec == True:
        Rates = Rates * AvagadroNum
    # ------------------------------------------------------------------------------------------------------ Weighted --------------------------------------------------------------------------------------------------------------- #

    if len(WeightsIndices) != 0:
        fig, ax = plt.subplots(2, figsize=(25,25), dpi=300)# for fits at different pressures

        ax[0].plot(1000/Temp, Rates, 'b-', linewidth=5, label=f"MESS Rate")# Arrh fit

        # ------------------------------------------------------------------------------------------------------- Mod Arrh fit -------------------------------------------------------------------------------------------------------------- #
        try:
            ModArr_popt, ModArr_pcov = curve_fit(FittingFunctions.ModArrhenius, Temp, np.log(Rates), maxfev=500000)
            ax[0].plot(1000/Temp, np.exp(FittingFunctions.ModArrhenius(Temp, ModArr_popt[0], ModArr_popt[1], ModArr_popt[2])), 'g--', linewidth=5, label=f'Modified Arrhenius Fit')
            
            ModArrMeanError, ModArrError = ErrorFunctions.ErrorPercentage(Rates, np.exp(FittingFunctions.ModArrhenius(Temp, ModArr_popt[0], ModArr_popt[1], ModArr_popt[2])))

            TailoredModArrMeanError, TailoredModArrError = ErrorFunctions.ErrorPercentage(Rates[WeightsIndices[0] : WeightsIndices[1]],
                                                            np.exp(FittingFunctions.ModArrhenius(Temp[WeightsIndices[0] : WeightsIndices[1]], 
                                                                                                ModArr_popt[0], ModArr_popt[1], ModArr_popt[2])))
        except RuntimeError:
            # print("Got Runtime Error")
            ModArr_popt, ModArr_pcov, ModArrMeanError, ModArrError = [0,0,0], [0,0,0], np.inf, np.ones(len(Rates)) * np.inf
        
            TailoredModArrMeanError, TailoredModArrError = np.inf, np.ones(len(Rates[WeightsIndices[0] : WeightsIndices[1]])) * np.inf

        ax[1].plot(1000/Temp, ModArrError, 'g--', linewidth=5, label='Modified Arrhenius Fit Error')

        # ------------------------------------------------------------------------------------------------------ Double Arrh fit --------------------------------------------------------------------------------------------------------------- #
        try:
            half = int(len(Temp)/2)
            popt1 ,pcov1 = curve_fit(FittingFunctions.ModArrhenius, Temp[:half], np.log(Rates[:half]), maxfev=500000)
            popt2 ,pcov2 = curve_fit(FittingFunctions.ModArrhenius, Temp[half:], np.log(Rates[half:]), maxfev=500000)
            init_guess = [popt1[0], popt1[1], popt1[2], popt2[0], popt2[1], popt2[2]]
            DoubleArr_popt, DoubleArr_pcov = curve_fit(FittingFunctions.DoubArrhenius, Temp, np.log(Rates), p0=init_guess, maxfev=500000)

            ax[0].plot(1000/Temp, np.exp(FittingFunctions.DoubArrhenius(Temp, DoubleArr_popt[0], DoubleArr_popt[1], DoubleArr_popt[2], 
                                                                        DoubleArr_popt[3], DoubleArr_popt[4], DoubleArr_popt[5])), 'r--', linewidth=5, label=f'Double Arrhenius Fit')

            DoubleArrMeanError, DoubleError = ErrorFunctions.ErrorPercentage(Rates, np.exp(FittingFunctions.DoubArrhenius(Temp, DoubleArr_popt[0], DoubleArr_popt[1], DoubleArr_popt[2], 
                                                                                                            DoubleArr_popt[3], DoubleArr_popt[4], DoubleArr_popt[5])))

            TailoredDoubleArrMeanError, TailoredDoubleError = ErrorFunctions.ErrorPercentage(Rates[WeightsIndices[0] : WeightsIndices[1]],
                                                    np.exp(FittingFunctions.DoubArrhenius(Temp[WeightsIndices[0] : WeightsIndices[1]], DoubleArr_popt[0], DoubleArr_popt[1], 
                                                                                        DoubleArr_popt[2], DoubleArr_popt[3], DoubleArr_popt[4], DoubleArr_popt[5])))
        except RuntimeError:
            DoubleArr_popt, DoubleArr_pcov, DoubleArrMeanError, DoubleError = [0,0,0,0,0,0], [0,0,0,0,0,0], np.inf, np.ones(len(Rates)) * np.inf

            TailoredDoubleArrMeanError, TailoredDoubleError = np.inf, np.ones(len(Rates[WeightsIndices[0] : WeightsIndices[1]])) * np.inf

        ax[1].plot(1000/Temp, DoubleError, 'r--', linewidth=5, label='Double Arrhenius Fit Error')

        # ------------------------------------------------------------------------------------------------------ Plotting Parameters --------------------------------------------------------------------------------------------------------------- #

        ax[0].legend(fontsize=25)
        ax[0].set_title("Rates Vs 1000/Temperature", fontsize=25)
        ax[0].set_xlabel("1000/Temperature [K]", fontsize=25)
        ax[0].set_ylabel("k [1/s]", fontsize=25)
        ax[0].set_yscale("log")
        ax[0].tick_params(axis='both', labelsize=25)
        ax[0].grid()

        ax[1].legend(fontsize=25)
        ax[1].set_title("Percentage Error Vs 1000/Temperautre", fontsize=25)
        ax[1].set_xlabel("1000/Temperature [K]", fontsize=25)
        ax[1].set_ylabel("Error %", fontsize=25)
        ax[1].tick_params(axis='both', labelsize=25)
        ax[1].grid()

        fig.suptitle(f"""{RateName}
        Pressure = {Pressure}""" , fontsize=40)

        if len(WeightsIndices) != 0:
            ax[0].axvspan(1000/Temp[WeightsIndices[0]], 1000/Temp[WeightsIndices[1] - 1], color='yellow', alpha=0.5)
            ax[1].axvspan(1000/Temp[WeightsIndices[0]], 1000/Temp[WeightsIndices[1] - 1], color='yellow', alpha=0.5)
        
        plt.savefig(os.path.join("Plots",f'{RateName}_P={Pressure}.jpg'), facecolor='w', dpi=300)
        plt.close()

        return ((ModArr_popt, ModArr_pcov, ModArrMeanError, ModArrError,TailoredModArrMeanError, TailoredModArrError), 
                (DoubleArr_popt, DoubleArr_pcov, DoubleArrMeanError, DoubleError, TailoredDoubleArrMeanError, TailoredDoubleError))

    # ------------------------------------------------------------------------------------------------------ No Weights --------------------------------------------------------------------------------------------------------------- #

    else:
        fig, ax = plt.subplots(2, figsize=(25,25), dpi=300)# for fits at different pressures

        ax[0].plot(1000/Temp, Rates, 'b-', linewidth=5, label=f"MESS Rate")# Arrh fit

        # ------------------------------------------------------------------------------------------------------- Mod Arrh fit -------------------------------------------------------------------------------------------------------------- #
        try:
            
            ModArr_popt, ModArr_pcov = curve_fit(FittingFunctions.ModArrhenius, Temp, np.log(Rates), maxfev=500000)
            ax[0].plot(1000/Temp, np.exp(FittingFunctions.ModArrhenius(Temp, ModArr_popt[0], ModArr_popt[1], ModArr_popt[2])), 'g--', linewidth=5, label=f'Modified Arrhenius Fit')
            ModArrMeanError, ModArrError = ErrorFunctions.ErrorPercentage(Rates, np.exp(FittingFunctions.ModArrhenius(Temp, ModArr_popt[0], ModArr_popt[1], ModArr_popt[2])))

        except RuntimeError:
            ModArr_popt, ModArr_pcov, ModArrMeanError, ModArrError = [0,0,0], [0,0,0], np.inf, np.ones(len(Rates)) * np.inf
            

        ax[1].plot(1000/Temp, ModArrError, 'g--', linewidth=5, label='Modified Arrhenius Fit Error')

        # ------------------------------------------------------------------------------------------------------ Double Arrh fit --------------------------------------------------------------------------------------------------------------- #
        try:
            half = int(len(Temp)/2)
            popt1 ,pcov1 = curve_fit(FittingFunctions.ModArrhenius, Temp[:half], np.log(Rates[:half]), maxfev=500000)
            popt2 ,pcov2 = curve_fit(FittingFunctions.ModArrhenius, Temp[half:], np.log(Rates[half:]), maxfev=500000)
            init_guess = [popt1[0], popt1[1], popt1[2], popt2[0], popt2[1], popt2[2]]
            DoubleArr_popt, DoubleArr_pcov = curve_fit(FittingFunctions.DoubArrhenius, Temp, np.log(Rates), p0=init_guess, maxfev=500000)

            ax[0].plot(1000/Temp, np.exp(FittingFunctions.DoubArrhenius(Temp, DoubleArr_popt[0], DoubleArr_popt[1], DoubleArr_popt[2], 
                                                                        DoubleArr_popt[3], DoubleArr_popt[4], DoubleArr_popt[5])), 'r--', linewidth=5, label=f'Double Arrhenius Fit')

            DoubleArrMeanError, DoubleError = ErrorFunctions.ErrorPercentage(Rates, np.exp(FittingFunctions.DoubArrhenius(Temp, DoubleArr_popt[0], DoubleArr_popt[1], DoubleArr_popt[2], 
                                                                                                            DoubleArr_popt[3], DoubleArr_popt[4], DoubleArr_popt[5])))
        except RuntimeError:
            DoubleArr_popt, DoubleArr_pcov, DoubleArrMeanError, DoubleError = [0,0,0,0,0,0], [0,0,0,0,0,0], np.inf, np.ones(len(Rates)) * np.inf

        ax[1].plot(1000/Temp, DoubleError, 'r--', linewidth=5, label='Double Arrhenius Fit Error')

        # ------------------------------------------------------------------------------------------------------ Plotting Parameters --------------------------------------------------------------------------------------------------------------- #

        ax[0].legend(fontsize=25)
        ax[0].set_title("Rates Vs 1000/Temperature", fontsize=25)
        ax[0].set_xlabel("1000/Temperature [K]", fontsize=25)
        ax[0].set_ylabel("k [1/s]", fontsize=25)
        ax[0].set_yscale("log")
        ax[0].tick_params(axis='both', labelsize=25)
        ax[0].grid()

        ax[1].legend(fontsize=25)
        ax[1].set_title("Percentage Error Vs 1000/Temperautre", fontsize=25)
        ax[1].set_xlabel("1000/Temperature [K]", fontsize=25)
        ax[1].set_ylabel("Error %", fontsize=25)
        ax[1].tick_params(axis='both', labelsize=25)
        ax[1].grid()

        fig.suptitle(f"""{RateName}
        Pressure = {Pressure}""" , fontsize=40)

        plt.savefig(os.path.join("Plots",f'{RateName}_P={Pressure}.jpg'), facecolor='w', dpi=300)
        plt.close()
        return ((ModArr_popt, ModArr_pcov, ModArrMeanError, ModArrError), (DoubleArr_popt, DoubleArr_pcov, DoubleArrMeanError, DoubleError))