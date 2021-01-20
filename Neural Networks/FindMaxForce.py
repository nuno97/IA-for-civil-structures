import os
import sys
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
stderr = sys.stderr
sys.stderr = open(os.devnull,'w')
from keras.models import load_model
sys.stderr=stderr
import numpy as np
import matplotlib.pyplot as plt
import time


def __main__():
	#print("Do you wish to design a single setting or give multiple settings? (type s for single or m for multiple)")
	#number_of_settings=input()
	number_of_settings='s'
	if number_of_settings == 's':
		setting, alpha, beta = getSingleSetting()
		begin=time.time()
		pos, pesos = create_incrementedLoads(setting,alpha,beta)
		cur_pesos,cur_pos = create_cur_input(alpha,beta,pos)
		rot1, rot2 = findRotula(cur_pos,cur_pesos,True)  
	else:
		getMultipleSettings()

	
	findLastForces([pos,pesos[:,:,0]],rot1,rot2)



	end=time.time()
	print(end-begin)
	
	print("Type q to quit, r to rerun.")
	ans=input()

	if ans=='r':
		plt.clf() 
		__main__()


def create_cur_input(_alpha,_beta,_pos):
	cur_pos=np.zeros((1,13,1))
	cur_pesos = np.zeros((1,3,1))

	cur_pos[0,:,0] = _pos[0,:,0]
	cur_pesos[0,0,0]=400*0.01
	cur_pesos[0,1,0]=400*0.01*_alpha
	cur_pesos[0,2,0]=400*0.01*_beta


	return cur_pesos, cur_pos



def create_incrementedLoads(_setting,_alpha,_beta):
	pos = np.zeros((3200,13,1))
	pesos = np.zeros((3200,3,1))

	for i in range(0,3200):
	    pos[i,:,0] = _setting[0,:,0]

	    pesos[i,0,0] = (i+800)*0.01    
	    pesos[i,1,0] = (i+800)*0.01*_alpha       
	    pesos[i,2,0] = (i+800)*0.01*_beta
	    
	return pos,pesos





def findRotula(_pos,_cur_pesos,_single):
	model = load_model('SKmodel.h5')
	prediction = model.predict([_pos,_cur_pesos[:,:,0]])[0]
	
	rotula1=np.where(prediction == min(prediction))[0][0]
	plt.ion()
	plt.title('Section Curvature')
	plt.plot([0,1,2,3,4,5,6,7,8,9,10,11,12],prediction)

	rotula2=6

	print("\nPLASTIC HINGES IN POSITIONS",rotula1, "and", rotula2,"\n")

	return rotula1,rotula2




def findLastForces(_setting,_rot1,_rot2):
	m_model=load_model('MOMENTmodel.h5')
	#r_model=load_model('ROTATIONmodel.h5')

	m_prediction = m_model.predict(_setting)
	#r_prediction = r_model.predict(_setting)

	#print(_setting)
	
	momento_rot1=[]
	momento_rot2=[]

	for i in range(0,3200):
		print(m_prediction[i-1][_rot1])
		print(m_prediction[i][_rot1])
		if np.abs(m_prediction[i][_rot1]) < np.abs(m_prediction[i-1][_rot1]):
			carga_max=i
			break
	print('Carga para a rotula no ponto ',_rot1,':',(carga_max+800))	

	for i in range(1,4000):
		if np.abs(m_prediction[i][_rot2]) < np.abs(m_prediction[i-1][_rot2]):
			carga_max=i
			break
	print('Carga para a rotula no ponto ',_rot2,':',(carga_max+800))
	print()




	#plt.plot(rotacao_rot1,momento_rot1)
	#plt.show()

	#plt.plot(rotacao_rot2,momento_rot2)
	#plt.show()

	#print(max(momento))
	#print(rotacao[ponto_max])


def getMultipleSettings():
	print("Insert File Name:")
	filename=input()
	sets_file = open(filename+'.txt','r')
	sets_file=open('settings.txt','r')
	for sett in sets_file.readlines():

		info=sett.split(',')
		posicao1=int(info[0])
		posicao2=int(info[1])
		posicao3=int(info[2])
		forca1=int(info[3])
		forca2=int(info[4])
		forca3=int(info[5])

		Pos = np.zeros((1,13,1))
		Pesos = np.zeros((1,3,1))

		Pos[0,posicao1,0] = 1
		Pos[0,posicao2,0] = 1
		Pos[0,posicao3,0] = 1
		Pesos[0,0,0]=forca1*0.01
		Pesos[0,1,0]=forca2*0.01
		Pesos[0,2,0]=forca3*0.01

		findRotula([Pos,Pesos[:,:,0]],False)
		

def getSingleSetting():
	cenario = True
	while (cenario):
		plt.ion()
		AllPoints=[0,1,2,3,4,5,6,7,8,9,10,11,12]
		plt.plot([0,0,0,0,0,0,0,0,0,0,0,0,0],'k-')
		plt.plot([0,6,12],[0,0,0],'^k')
		plt.plot([1,2,3,4,5,7,8,9,10,11],[0,0,0,0,0,0,0,0,0,0],'bo')
		for i in range(0,13):
			plt.annotate(AllPoints[i], # this is the text
			(AllPoints[i],0), # this is the point to label
			textcoords="offset points", # how to position the text
			xytext=(0,-15), # distance from text to points (x,y)
			ha='center') # horizontal alignment can be left, right or center

		
		Carga1Opcoes='(1, 2, 3, 4 or 5)'
		print("Type the desired 1st and 2nd load positions "+Carga1Opcoes+":")
		posicao1 = int(input('1st:'))
		posicao2 = int(input('2nd:'))
		while (posicao1 == posicao2):
			print("ERROR! Load positions must be diferent.")
			print("\n")
			print("Type the desired 1st and 2nd load positions"+Carga1Opcoes+":")
			posicao1 = int(input('1st:'))
			posicao2 = int(input('2nd:'))
		
		while ((posicao1>5) or (posicao1<1) or (posicao2>5) or (posicao2<1)):
			print("ERROR! 1st and 2nd load positions must be in the first span. (positions 1, 2, 3, 4 or 5)")
			print("\n")
			print("Type the desired 1st and 2nd load positions"+Carga1Opcoes+":")
			posicao1 = int(input('1st:'))
			posicao2 = int(input('2nd:'))
		


		Carga3Opcoes='(7, 8, 9, 10 ou 11)'
		print("Type the desired 3rd load position "+Carga3Opcoes+":")
		posicao3 = int(input('3rd:'))

		while ((posicao3>11) or (posicao3<7)):
			print("ERROR! 3rd load position must be in the 2nd span. (positions 7, 8, 9, 10 or 11)")
			print("\n")
			print("Type the desired 3rd load position "+Carga3Opcoes+":")
			posicao3 = int(input('3rd:'))
			

		factorOpcoes='(0.5, 1, 2)'
		print("Type the desired multiplying factor for the 2nd and 3rd load forces"+factorOpcoes+":")
		alpha=float(input('2nd:'))
		beta=float(input('3rd:'))
		while((alpha not in (0.5,1,2)) and (beta not in (0.5,1,2))):
			print("ERROR! Multiplying factors must be 0.5, 1 or 2")
			print()
			print("Type the desired multiplying factor for the 2nd and 3rd load forces"+factorOpcoes+":")
			alpha=float(input('2nd:'))
			beta=float(input('3rd:'))
		

		posicoes = [posicao1,posicao2,posicao3]
		factor=['',alpha, beta]
		plt.plot([posicao1,posicao2,posicao3],[0,0,0],'ro')
		for i in range(0,3):
			plt.annotate(str(factor[i])+'X',#str(forcas[i])+'kN', # this is the text
			(posicoes[i],0), # this is the point to label
			textcoords="offset points", # how to position the text
			xytext=(0,10), # distance from text to points (x,y)
			ha='center') # horizontal alignment can be left, right or center



		print("Is this your desired setting? (type y if yes, n if no)")
		answer = input()

		if answer=='y': 
			cenario=False	
		else:
			cenario=True
			plt.clf() 
		



	Pos = np.zeros((1,13,1))

	Pos[0,posicao1,0] = 1
	Pos[0,posicao2,0] = 1
	Pos[0,posicao3,0] = 1
	


	return Pos,alpha,beta
	



__main__()






















'''for i in range(50,200):
		abs_media=sum(abs(prediction[i]))/len(prediction[i])
		rotula1=None
		if(abs(min(prediction[i]))) > 4*abs_media:
			rotula1=(np.where(prediction[i] == min(prediction[i]))[0][0])
			print(prediction[i])
			plt.ion()
			plt.title('Section Curvature')
			plt.plot([0,1,2,3,4,5,6,7,8,9,10,11,12],prediction[i])

			break

	if rotula1==None:
		rotula1=(np.where(prediction[100] == min(prediction[100]))[0][0])
		print(prediction[i])
		plt.ion()
		plt.title('Section Curvature')
		plt.plot([0,1,2,3,4,5,6,7,8,9,10,11,12],prediction[100])
'''