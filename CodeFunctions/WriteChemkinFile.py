import numpy as np
import datetime
from CodeFunctions import PlotFits

def WriteFile(file, RatePlotDict, HighPIndex, PlottingPressure, SpeciesIndex, HighPressureRates, TempSpeciesRates, Tolerance, Bimolec, WeightStartEndTemps):

    def __CheckTemps(Temp):
        try:
            WeightsIndices = np.array([np.where(Temp == WeightStartEndTemps[0])[0][0], np.where(Temp == WeightStartEndTemps[1])[0][-1] + 1])
        except IndexError:
            WeightsIndices = np.array([np.where(Temp == WeightStartEndTemps[0])[0][0], -1])
                    
        return WeightsIndices

    # ------------------------------------------------------------------------------------------------------ Weighted --------------------------------------------------------------------------------------------------------------- #

    if len(WeightStartEndTemps) != 0:
        SpeciesNumber = HighPressureRates.shape[0]
        PressureNumber = int(TempSpeciesRates.shape[0] / SpeciesNumber)

        PressureShift = PressureNumber*HighPIndex

        for RateIndex in SpeciesIndex:
            
            # High Pressure:
            # if all data set are NaN then prints 0 0 0.
            if len(np.where(np.isnan ( HighPressureRates [HighPIndex] [RateIndex + 1]) == True)[0]) == len(HighPressureRates [HighPIndex] [RateIndex + 1]):
                file[0].write(f"{RatePlotDict[RateIndex]} 1.0 1.0 1.0\n")
                file[1].write(f"{RatePlotDict[RateIndex]} 1.0 1.0 1.0\n")
                file[2].write(f"{RatePlotDict[RateIndex]} 1.0 1.0 1.0\n")

            # elif checks where NaN begins in data set and terminates data when the NaN begins. 
            elif len(np.where(np.isnan(HighPressureRates[HighPIndex][RateIndex + 1]) == True)[0]) != 0:
                Rates = HighPressureRates [HighPIndex] [RateIndex]    [:np.where(np.isnan( HighPressureRates [HighPIndex] [RateIndex + 1] ) == True)[0][0]]
                Temp  = HighPressureRates     [0]          [0]        [:np.where(np.isnan( HighPressureRates [HighPIndex] [RateIndex + 1] ) == True)[0][0]]
                WeightsIndices = __CheckTemps(Temp)
                ModArr, DoubleArr = PlotFits.PlotterFitter(Temp, Rates, RatePlotDict[RateIndex], 'High', Bimolec, WeightsIndices)
                file[0].write(f"{RatePlotDict[RateIndex]} {ModArr[0][0]} {ModArr[0][1]} {ModArr[0][2]}\n")
                file[1].write(f"{RatePlotDict[RateIndex]} {ModArr[0][0]} {ModArr[0][1]} {ModArr[0][2]}\n")
                file[2].write(f"{RatePlotDict[RateIndex]} {ModArr[0][0]} {ModArr[0][1]} {ModArr[0][2]}\n")
            
            # else considers whole data.
            else:
                Rates = HighPressureRates[HighPIndex][RateIndex + 1]
                Temp  = HighPressureRates    [0]            [0]
                WeightsIndices = __CheckTemps(Temp)
                ModArr, DoubleArr = PlotFits.PlotterFitter(Temp, Rates, RatePlotDict[RateIndex], 'High', Bimolec, WeightsIndices)
                file[0].write(f"{RatePlotDict[RateIndex]} {ModArr[0][0]} {ModArr[0][1]} {ModArr[0][2]}\n")
                file[1].write(f"{RatePlotDict[RateIndex]} {ModArr[0][0]} {ModArr[0][1]} {ModArr[0][2]}\n")    
                file[2].write(f"{RatePlotDict[RateIndex]} {ModArr[0][0]} {ModArr[0][1]} {ModArr[0][2]}\n")  
                
            # All pressrues:
            for PressureIndex in range(PressureShift, PlottingPressure.shape[0] + PressureShift):
                
                if len(np.where(np.isnan( TempSpeciesRates [PressureIndex] [RateIndex]) == True)[0]) != 0:
                    Rates = TempSpeciesRates[PressureIndex][RateIndex]    [:np.where(np.isnan(TempSpeciesRates [PressureIndex] [RateIndex]) == True)[0][0]]
                    Temp  = TempSpeciesRates     [0]           [0]        [:np.where(np.isnan(TempSpeciesRates [PressureIndex] [RateIndex]) == True)[0][0]]
                else:
                    Rates = TempSpeciesRates [PressureIndex] [RateIndex]
                    Temp  = TempSpeciesRates     [0]            [0]
                
                WeightsIndices = __CheckTemps(Temp)
                ModArr, DoubleArr = PlotFits.PlotterFitter(Temp, Rates, RatePlotDict[RateIndex], PlottingPressure[PressureIndex - PressureShift], Bimolec, WeightsIndices)
                
                if WeightsIndices[1] != -1:
                    WeightsIndices[1] -= 1

                file[0].write("{:<60}".format(f"PLOG/ {PlottingPressure[PressureIndex - PressureShift]} {ModArr[0][0]} {ModArr[0][1]} {ModArr[0][2]}/") + 
                                            f"!Labbe Lab {datetime.datetime.now().strftime('%B %d, %Y')}." + 
                                            f" Fit tailored for {Temp[WeightsIndices[0]]}K - {Temp[WeightsIndices[1]]}K MAPE={ModArr[4]}% Max={np.max(ModArr[5])}%." + 
                                            f" Total data range {np.min(Temp)}K - {np.max(Temp)}K MAPE={ModArr[2]}% Max={np.max(ModArr[3])}%.\n")

                file[1].write("{:<60}".format(f"PLOG/ {PlottingPressure[PressureIndex - PressureShift]} {DoubleArr[0][0]} {DoubleArr[0][1]} {DoubleArr[0][2]}/")+
                                            f"!Labbe Lab {datetime.datetime.now().strftime('%B %d, %Y')}." +
                                            f" Fit tailored for {Temp[WeightsIndices[0]]}K - {Temp[WeightsIndices[1]]}K MAPE={DoubleArr[4]}% Max={np.max(DoubleArr[5])}%." +
                                            f" Total data range {np.min(Temp)}K - {np.max(Temp)}K MAPE={DoubleArr[2]}% Max={np.max(DoubleArr[3])}%." +
                                            f"\nPLOG/ {PlottingPressure[PressureIndex - PressureShift]} {DoubleArr[0][3]} {DoubleArr[0][4]} {DoubleArr[0][5]}/\n")  
                
                if (np.max(ModArr[5]) < Tolerance) or (np.max(ModArr[5]) < np.max(DoubleArr[5])):
                    file[2].write("{:<60}".format(f"PLOG/ {PlottingPressure[PressureIndex - PressureShift]} {ModArr[0][0]} {ModArr[0][1]} {ModArr[0][2]}/") + 
                                                f"!Labbe Lab {datetime.datetime.now().strftime('%B %d, %Y')}." + 
                                                f" Fit tailored for {Temp[WeightsIndices[0]]}K - {Temp[WeightsIndices[1]]}K MAPE={ModArr[4]}% Max={np.max(ModArr[5])}%." + 
                                                f" Total data range {np.min(Temp)}K - {np.max(Temp)}K MAPE={ModArr[2]}% Max={np.max(ModArr[3])}%.\n")  
                else:
                    file[2].write("{:<60}".format(f"PLOG/ {PlottingPressure[PressureIndex - PressureShift]} {DoubleArr[0][0]} {DoubleArr[0][1]} {DoubleArr[0][2]}/")+
                                        f"!Labbe Lab {datetime.datetime.now().strftime('%B %d, %Y')}." +
                                        f" Fit tailored for {Temp[WeightsIndices[0]]}K - {Temp[WeightsIndices[1]]}K MAPE={DoubleArr[4]}% Max={np.max(DoubleArr[5])}%." +
                                        f" Total data range {np.min(Temp)}K - {np.max(Temp)}K MAPE={DoubleArr[2]}% Max={np.max(DoubleArr[3])}%." +
                                        f"\nPLOG/ {PlottingPressure[PressureIndex - PressureShift]} {DoubleArr[0][3]} {DoubleArr[0][4]} {DoubleArr[0][5]}/\n")

            file[0].write('\n')
            file[1].write('\n')
            file[2].write('\n')

    # ------------------------------------------------------------------------------------------------------ No Weights --------------------------------------------------------------------------------------------------------------- #
           
    else:    
        SpeciesNumber = HighPressureRates.shape[0]
        PressureNumber = int(TempSpeciesRates.shape[0] / SpeciesNumber)

        PressureShift = PressureNumber*HighPIndex

        for RateIndex in SpeciesIndex:
            
            # High Pressure:
            # if all data set are NaN then prints 0 0 0.
            if len(np.where(np.isnan ( HighPressureRates [HighPIndex] [RateIndex + 1]) == True)[0]) == len(HighPressureRates [HighPIndex] [RateIndex + 1]):
                file[0].write(f"{RatePlotDict[RateIndex]} 1.0 1.0 1.0\n")
                file[1].write(f"{RatePlotDict[RateIndex]} 1.0 1.0 1.0\n")
                file[2].write(f"{RatePlotDict[RateIndex]} 1.0 1.0 1.0\n")

            # elif checks where NaN begins in data set and terminates data when the NaN begins. 
            elif len(np.where(np.isnan(HighPressureRates[HighPIndex][RateIndex + 1]) == True)[0]) != 0:
                Rates = HighPressureRates [HighPIndex] [RateIndex]    [:np.where(np.isnan( HighPressureRates [HighPIndex] [RateIndex + 1] ) == True)[0][0]]
                Temp  = HighPressureRates     [0]          [0]        [:np.where(np.isnan( HighPressureRates [HighPIndex] [RateIndex + 1] ) == True)[0][0]]
                ModArr, DoubleArr = PlotFits.PlotterFitter(Temp, Rates, RatePlotDict[RateIndex], 'High', Bimolec)
                
                file[0].write(f"{RatePlotDict[RateIndex]} {ModArr[0][0]} {ModArr[0][1]} {ModArr[0][2]}\n"), 
                file[1].write(f"{RatePlotDict[RateIndex]} {ModArr[0][0]} {ModArr[0][1]} {ModArr[0][2]}\n")
                file[2].write(f"{RatePlotDict[RateIndex]} {ModArr[0][0]} {ModArr[0][1]} {ModArr[0][2]}\n")

            # else considers whole data.
            else:
                Rates = HighPressureRates[HighPIndex][RateIndex + 1]
                Temp  = HighPressureRates    [0]            [0]
                ModArr, DoubleArr = PlotFits.PlotterFitter(Temp, Rates, RatePlotDict[RateIndex], 'High', Bimolec)
                
                file[0].write(f"{RatePlotDict[RateIndex]} {ModArr[0][0]} {ModArr[0][1]} {ModArr[0][2]}\n"), 
                file[1].write(f"{RatePlotDict[RateIndex]} {ModArr[0][0]} {ModArr[0][1]} {ModArr[0][2]}\n")      
                file[2].write(f"{RatePlotDict[RateIndex]} {ModArr[0][0]} {ModArr[0][1]} {ModArr[0][2]}\n")

            # All pressrues:
            for PressureIndex in range(PressureShift, PlottingPressure.shape[0] + PressureShift):
                
                if len(np.where(np.isnan( TempSpeciesRates [PressureIndex] [RateIndex]) == True)[0]) != 0:
                    Rates = TempSpeciesRates[PressureIndex][RateIndex]    [:np.where(np.isnan(TempSpeciesRates [PressureIndex] [RateIndex]) == True)[0][0]]
                    Temp  = TempSpeciesRates     [0]           [0]        [:np.where(np.isnan(TempSpeciesRates [PressureIndex] [RateIndex]) == True)[0][0]]
                else:
                    Rates = TempSpeciesRates [PressureIndex] [RateIndex]
                    Temp  = TempSpeciesRates     [0]            [0]

                ModArr, DoubleArr = PlotFits.PlotterFitter(Temp, Rates, RatePlotDict[RateIndex], PlottingPressure[PressureIndex - PressureShift], Bimolec)

                file[0].write("{:<60}".format(f"PLOG/ {PlottingPressure[PressureIndex - PressureShift]} {ModArr[0][0]} {ModArr[0][1]} {ModArr[0][2]}/") + 
                                            f"!Labbe Lab {datetime.datetime.now().strftime('%B %d, %Y')}." + 
                                            f" Total data range {np.min(Temp)}K - {np.max(Temp)}K MAPE={ModArr[2]}% Max={np.max(ModArr[3])}%.\n")

                file[1].write("{:<60}".format(f"PLOG/ {PlottingPressure[PressureIndex - PressureShift]} {DoubleArr[0][0]} {DoubleArr[0][1]} {DoubleArr[0][2]}/")+
                                            f"!Labbe Lab {datetime.datetime.now().strftime('%B %d, %Y')}." +
                                            f" Total data range {np.min(Temp)}K - {np.max(Temp)}K MAPE={DoubleArr[2]}% Max={np.max(DoubleArr[3])}%." +
                                            f"\nPLOG/ {PlottingPressure[PressureIndex - PressureShift]} {DoubleArr[0][3]} {DoubleArr[0][4]} {DoubleArr[0][5]}/\n")  
                
                if (np.max(ModArr[3]) < Tolerance) or (np.max(ModArr[3]) < np.max(DoubleArr[3])):
                    file[2].write("{:<60}".format(f"PLOG/ {PlottingPressure[PressureIndex - PressureShift]} {ModArr[0][0]} {ModArr[0][1]} {ModArr[0][2]}/") + 
                                                f"!Labbe Lab {datetime.datetime.now().strftime('%B %d, %Y')}." + 
                                                f" Total data range {np.min(Temp)}K - {np.max(Temp)}K MAPE={ModArr[2]}% Max={np.max(ModArr[3])}%.\n") 
                else:
                    file[2].write("{:<60}".format(f"PLOG/ {PlottingPressure[PressureIndex - PressureShift]} {DoubleArr[0][0]} {DoubleArr[0][1]} {DoubleArr[0][2]}/")+
                                        f"!Labbe Lab {datetime.datetime.now().strftime('%B %d, %Y')}." +
                                        f" Total data range {np.min(Temp)}K - {np.max(Temp)}K MAPE={DoubleArr[2]}% Max={np.max(DoubleArr[3])}%." +
                                        f"\nPLOG/ {PlottingPressure[PressureIndex - PressureShift]} {DoubleArr[0][3]} {DoubleArr[0][4]} {DoubleArr[0][5]}/\n")

            file[0].write('\n')
            file[1].write('\n')
            file[2].write('\n')


