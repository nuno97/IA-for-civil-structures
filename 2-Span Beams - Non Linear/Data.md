The MOMENT2.xlsx and ROTATION2.xlsx have the same structure and were used to train the network to predict the moment and rotation respectively as well as the 
moment x rotation graphs. The structure of the data includes in the first 3 columns the P1, P2 and P3 that correspond to an integer from 1 to 11 excluding 6 (support)
these integers correspond to a concentrated load position on the beam. The next 3 columns L1, L2, L3 have the value of load given as input to Abaqus for each one of the
loads. Then we have the 7th column with the value of LPF at the end of the Abaqus simulations. The next 3 columns L1_real, L2_real and L3_real, have the values of the 
loads in L1, L2 and L3 multiplied by the LPF to give the real load at the end of Abaqus simulation. Finally we got from r0 to r35 (in the case of the MOMENT2.xlsx) or r24
(in the case of ROTATION2.xlsx) the values of moment or rotation in each node of the beam.

The SK.csv was used to train the NN to predict the section curvature. It has a similar structure, with the first 3 columns representing the position of the loads, the
following 3 representing the loads given as input to Abaqus and then the 7th column having the LPF. Next we have an empty column, before having the results with values
of SK in each node of the beam.

The rest of the csv files have the same structure as SK.csv and represent real values of examples that were used to compare with predictions in the notebooks tests.
