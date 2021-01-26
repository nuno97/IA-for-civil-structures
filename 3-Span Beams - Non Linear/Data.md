The 3span-beams-MOM.xlsx, 3span-beams-ROT.xlsx and 3span-beams-SK.xlsx, were used to train the NN to predict the moment, rotation and section curvature respectively.
The structure of the data is the same, with the first 3 columns P1, P2 and P3 representing the load magnitudes given as input to abaqus on each span of the beam, 
the 4th column has the value of LPF, then the next 3 columns L1, L2 and L3 have the size in meters of each span and the 8th column "unipos" represents if the position
os the uniform load is on the middle span or the edge span. The rest of the columns represent the values of either moment, rotation os section curvature in each node of
the beam
