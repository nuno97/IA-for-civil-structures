
import csv
from abaqusConstants import *
from part import *
from material import *
from section import *
from assembly import *
from step import *
from interaction import *
from load import *
from mesh import *
from optimization import *
from job import *
from sketch import *
from visualization import *
from connectorBehavior import *
import visualization
import os
import datetime
import shutil
from odbAccess import *
import time
import numpy
import numpy as np
import re
import mesh


file_beams = open('reals.txt','r')
with open('reals.csv', mode='w') as file:
	writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
	n=0
	for beam in file_beams.readlines():
		print >> sys.__stdout__, n
		n+=1

		try:
			carga=beam.split('Job-')
			carga=carga[1].split('cargas')
			carga2=carga[1].split('-alpha')
			posicoes=carga2[0].split('-')	
			carga1=float(carga[0])
			carga2=carga2[1].split('-beta')
			carga3=float(carga2[0])*carga1
			carga2=float(carga2[1])*carga1
	
			
			print >> sys.__stdout__, beam, '\n'


			if len(beam.split('0.')) >=2:
				beam= beam.replace('0.','') 
			o2 = session.openOdb(name=str(beam)[0:-1]+'.odb')
			session.viewports['Viewport: 1'].setValues(displayedObject=o2)
    	
			odb = session.odbs['C:/SIMULIA/Abaqus/Commands/'+str(beam)[0:-1]+'.odb']
		


			LPF = session.XYDataFromHistory(name='LPF', odb=odb, 
			         outputVariableName='Load proportionality factor: LPF for Whole Model', 
			         steps=('Step-1', ), )
					 
			x0 = session.xyDataObjects['LPF']
			#print >> sys.__stdout__, x0[-1][1]
			LPF_val=x0[-1][1]
			#carga2=carga2*(x0[-1][1])
			#carga3=carga3*(x0[-1][1])
			
			posicoes.append(carga1)
			posicoes.append(carga2)
			posicoes.append(carga3)
			posicoes.append(LPF_val)
			posicoes.append(' ')


			frame = len(odb.steps['Step-1'].frames)-1
		
			session.writeFieldReport(fileName='abaqus.rpt', append=OFF, 
		sortItem='Element Label', odb=odb, step=0, frame=frame, 
		outputPosition=ELEMENT_NODAL, variable=(('SM', INTEGRATION_POINT),))

			info=[]

			elem=[]
			node=[]
			moment=[]

			info.append(elem)
			info.append(node)
			info.append(moment)


			f = open('abaqus.rpt', "r")
			copy=False
			for i in f.readlines():
				l=i.split(' ')
				if i=="\n":
					copy=False

				if copy:
					ww=0
					for j in l:
						if j != '':
							info[ww].append(float(j))
							ww+=1
				
				if i=='-------------------------------------------------\n':
					copy=True


			f.close()




			Node_label=[]
			Node_position=[]
			#get positions(coordinates) by label of each node 
			copy=False
			f = open(str(beam)[0:-1]+'.inp', "r")
			for i in f.readlines():
				l=i.split(',')

				if l[0]=="*Element":
					copy=False

				if copy:
					Node_label.append(l[0])
					Node_position.append(l[1])

				if i=='*Node\n':
					copy=True

			f.close()


		#from str to float
			for i in range(0,len(Node_position)):
				Node_position[i]=float(Node_position[i])
				Node_label[i]=float(Node_label[i])


			#place in dict to sort node labels by node positions
			Dict = {}
			for i in range(0,len(Node_label)):
				Dict[Node_label[i]]=Node_position[i]


			node_label_order= sorted(Dict, key=Dict.__getitem__)


			for i in range(0,len(node)):
				node[i]=Dict[float(node[i])]



			for i in range(1, len(node)):
				key_item = node[i]
				elem_item=elem[i]
				moment_item=moment[i]

				j = i - 1
				while j >= 0 and node[j] > key_item:

					elem[j + 1] = elem[j]
					node[j + 1] = node[j]
					moment[j + 1] = moment[j]

					j -= 1


				elem[j + 1] = elem_item
				node[j + 1] = key_item
				moment[j + 1] = moment_item



			#print >> sys.__stdout__, posicoes

			posicoes.extend(moment)
			writer.writerow(posicoes)
		except:
			pass


	writer.writerow(node)