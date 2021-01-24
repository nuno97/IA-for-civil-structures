import numpy as np
import tensorflow as tf

def BeamDeflectorCalculator():
    
    
      
    X=np.zeros((3,10000))
    Y=np.zeros((10000,11))
    for i in range(0,10000):

    	
    	X[0][i]=np.random.random()*10 +1
    	X[0][i]= round(X[0][i],2)
    	X[1][i]= 1
    	X[2][i]=(np.random.randint(9)+1)/10

    	#print(X[2][i], " a/l")
    	part = X[0][i]/10    # L/10   --> tamanho de cada divisao 

    	a = X[0][i]*(X[2][i])  # a
    	#print(a, " a")
    	b = X[0][i]-a        # b
    	#print(b, " b")
    	
    	for j in range(0,11):
    		
    		x=part*j             # x
    		#print(x, " x",j)
    		if j==10:
    			Y[i][j]=0
    		
    		elif x < a:
    			#print("before")
                # deflection = P*b*x / 6*L  *  L^2 - X^2 - b^2
    			Y[i][j] = (( (X[1][i] * b * x) / (6* X[0][i]) )   *   ( X[0][i]**2 - x**2 - b**2 ) )
  
    		else:
    			#print("after")
    			Y[i][j] = (( (X[1][i] * a * (X[0][i]-x) ) / (6* X[0][i]) )   *   ( X[0][i]**2 - (X[0][i]-x)**2 - a**2 ) )
    		

    		#print(Y[i][j], " deflection")
    			
        
    return X,Y


def BeamDeflectorUniformDist():
    
    X=np.zeros((2,10000))
    Y=np.zeros((10000,11))
    
    for i in range(0,10000):

    	X[0][i]=np.random.random()*100 +1
    	X[0][i]= round(X[0][i],2)
    	X[1][i]= 1

    	part = X[0][i]/10    # L/10   --> tamanho de cada divisao



    	for j in range(0,10):

            
    		x=part*j             # x

    		Y[i][j]= (x/24)  *  (X[0][i]**3  - (2 * X[0][i] * x**2)  +  x**3)         #      = (w*x/24)  *  (l^3 - 2lx^2 + x^3)
           
            
    return X,Y



def BeamDeflectorCalcConstantL():

      
    X=np.zeros((3,10000))
    Y=np.zeros((10000,11))
    for i in range(0,10000):

    	
    	X[0][i]=5
    	X[1][i]= 1
    	X[2][i]=(np.random.randint(9)+1)/10

    	part = X[0][i]/10    # L/10   --> tamanho de cada divisao 

    	a = X[0][i]*(X[2][i])  # a
    	#print(a, " a")
    	b = X[0][i]-a        # b
    	#print(b, " b")
    	
    	for j in range(0,11):
    		
    		x=part*j             # x
    		#print(x, " x",j)
    		if j==10:
    			Y[i][j]=0
    		
    		elif x < a:
    			#print("before")
                # deflection = P*b*x / 6*L  *  L^2 - X^2 - b^2
    			Y[i][j] = (( (X[1][i] * b * x) / (6* X[0][i]) )   *   ( X[0][i]**2 - x**2 - b**2 ) )
  
    		else:
    			#print("after")
    			Y[i][j] = (( (X[1][i] * a * (X[0][i]-x) ) / (6* X[0][i]) )   *   ( X[0][i]**2 - (X[0][i]-x)**2 - a**2 ) )
    		

    		#print(Y[i][j], " deflection")
    			
        
    return X,Y



def BeamMomentumCalc():

    X=np.zeros((3,10000))
    Y=np.zeros((10000,11))
    for i in range(0,10000):

    	
    	X[0][i]=np.random.random()*10 +1
    	X[0][i]= round(X[0][i],2)
    	X[1][i]= 1
    	X[2][i]=(np.random.randint(9)+1)/10

    	#print(X[2][i], " a/l")
    	part = X[0][i]/10    # L/10   --> tamanho de cada divisao 

    	a = X[0][i]*(X[2][i])  # a
    	#print(a, " a")
    	b = X[0][i]-a        # b
    	#print(b, " b")
    	
    	for j in range(0,11):
    		
    		x=part*j             # x
    	
    		if j==10:
    			Y[i][j]=0
    		
    		elif x < a:
    		
    			Y[i][j] =(X[1][i] * b * x) / X[0][i]
  
    		else:
    		
    			Y[i][j] = (X[1][i] * a * (X[0][i]-x) ) /  X[0][i]    		

    		print(Y[i][j])
    		
    			
        
    return X,Y


BeamMomentumCalc()