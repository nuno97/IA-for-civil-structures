# -*- coding: mbcs -*-
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
import random
import re
import mesh

session.journalOptions.setValues(replayGeometry=COORDINATE, recoverGeometry=COORDINATE)



def runJob(_load,_beta,_alpha,_Q1,_Q2,_Q3):
	E=210000000
	niu=0.0
	fy=355000
	fu=355000
	eps_u=0.1

	ar=0.1
	br=0.5
	L=12
	pc=-_load
	load=_Q1
	pc2=-(_beta*_load)
	load2=_Q2
	pc3=-(_alpha*_load)
	load3=_Q3

	session.viewports['Viewport: 1'].setValues(displayedObject=None)

	s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', 
	    sheetSize=200.0)
	g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
	s.setPrimaryObject(option=STANDALONE)
	s.Spot(point=(0.0, 0.0))
	s.Spot(point=(L, 0.0))
	s.Line(point1=(0.0, 0.0), point2=(L, 0.0))
	s.HorizontalConstraint(entity=g.findAt((L/2.0, 0.0)), addUndoState=False)



	p = mdb.models['Model-1'].Part(name='Part-1', dimensionality=TWO_D_PLANAR, 
	    type=DEFORMABLE_BODY)
	p = mdb.models['Model-1'].parts['Part-1']
	p.BaseWire(sketch=s)
	s.unsetPrimaryObject()
	p = mdb.models['Model-1'].parts['Part-1']

	p = mdb.models['Model-1'].parts['Part-1']
	e, v1, d1 = p.edges, p.vertices, p.datums
	p.PartitionEdgeByPoint(edge=e.findAt(coordinates=(L/4.0, 0.0, 0.0)), 
	    point=p.InterestingPoint(edge=e.findAt(coordinates=(L/4.0, 0.0, 0.0)), 
	    rule=MIDDLE))
	session.viewports['Viewport: 1'].partDisplay.setValues(sectionAssignments=ON, 
	    engineeringFeatures=ON)
	session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
	    referenceRepresentation=OFF)



	


	## MATERIAIS

	## ELASTICO
	mdb.models['Model-1'].Material(name='S355')
	mdb.models['Model-1'].materials['S355'].Elastic(table=((E, niu), ))

	## PLASTICO
	mdb.models['Model-1'].materials['S355'].Plastic(table=((fy, 0.0), (fu,
	    eps_u)))
		
	mdb.models['Model-1'].RectangularProfile(name='Profile-1', a=ar, b=br)
	mdb.models['Model-1'].BeamSection(name='Section-1', 
	    integration=DURING_ANALYSIS, poissonRatio=niu, profile='Profile-1', 
	    material='S355', temperatureVar=LINEAR, consistentMassMatrix=False)
		
	a = mdb.models['Model-1'].rootAssembly
	session.viewports['Viewport: 1'].setValues(displayedObject=a)
	p = mdb.models['Model-1'].parts['Part-1']
	session.viewports['Viewport: 1'].setValues(displayedObject=p)
	p = mdb.models['Model-1'].parts['Part-1']
	e = p.edges
	edges = e.findAt(((L/4.0, 0.0, 0.0), ), ((L-L/4.0, 0.0, 0.0), ))
	region = p.Set(edges=edges, name='Set-1')
	p = mdb.models['Model-1'].parts['Part-1']
	p.SectionAssignment(region=region, sectionName='Section-1', offset=0.0, 
	    offsetType=MIDDLE_SURFACE, offsetField='', 
	    thicknessAssignment=FROM_SECTION)
		
	
	p = mdb.models['Model-1'].parts['Part-1']
	e = p.edges
	edges = e.findAt(((L/4.0, 0.0, 0.0), ), ((L-L/4.0, 0.0, 0.0), ))
	region=p.Set(edges=edges, name='Set-4')
	p = mdb.models['Model-1'].parts['Part-1']
	p.assignBeamSectionOrientation(region=region, method=N1_COSINES, n1=(0.0, 0.0, 
	    -1.0))
	


	p = mdb.models['Model-1'].parts['Part-1']
	load_datum = p.DatumPointByCoordinate((load,0,0))
	e, v1, d1 = p.edges, p.vertices, p.datums
	load_point = p.PartitionEdgeByPoint(edge=e[0], point=d1[5])	


	p = mdb.models['Model-1'].parts['Part-1']
	load_datum2 = p.DatumPointByCoordinate((load2,0,0))
	e, v1, d1 = p.edges, p.vertices, p.datums
	load_point2 = p.PartitionEdgeByPoint(edge=e[1], point=d1[7])	

	p = mdb.models['Model-1'].parts['Part-1']
	load_datum3 = p.DatumPointByCoordinate((load3,0,0))
	e, v1, d1 = p.edges, p.vertices, p.datums
	#print(d1)
	load_point3 = p.PartitionEdgeByPoint(edge=e[3], point=d1[9])	


	#Assembly

	a = mdb.models['Model-1'].rootAssembly
	session.viewports['Viewport: 1'].setValues(displayedObject=a)
	a = mdb.models['Model-1'].rootAssembly
	a.DatumCsysByDefault(CARTESIAN)
	p = mdb.models['Model-1'].parts['Part-1']
	a.Instance(name='Part-1-1', part=p, dependent=ON)

	#Steps - Riks
		
	mdb.models['Model-1'].StaticRiksStep(initialArcInc=0.01, maxArcInc=0.1, name=
	    'Step-1', nlgeom=OFF, previous='Initial')
		

	#Carga concentrada


	a = mdb.models['Model-1'].rootAssembly
	v1 = a.instances['Part-1-1'].vertices
	verts1 = v1.findAt( ((load, 0.0, 0.0), ) )
	region = a.Set(vertices=verts1, name='Set-3')
	mdb.models['Model-1'].ConcentratedForce(name='Load-2', createStepName='Step-1', 
	    region=region, distributionType=UNIFORM, field='', cf2=pc)


	a = mdb.models['Model-1'].rootAssembly
	v1 = a.instances['Part-1-1'].vertices
	verts1 = v1.findAt( ((load2, 0.0, 0.0), ) )
	region = a.Set(vertices=verts1, name='Set-4')
	mdb.models['Model-1'].ConcentratedForce(name='Load-3', createStepName='Step-1', 
	    region=region, distributionType=UNIFORM, field='', cf2=pc2)



	a = mdb.models['Model-1'].rootAssembly
	v1 = a.instances['Part-1-1'].vertices
	verts1 = v1.findAt( ((load3, 0.0, 0.0), ) )
	region = a.Set(vertices=verts1, name='Set-5')
	mdb.models['Model-1'].ConcentratedForce(name='Load-4', createStepName='Step-1', 
	    region=region, distributionType=UNIFORM, field='', cf2=pc3)


	#Apoios


	a = mdb.models['Model-1'].rootAssembly
	v1 = a.instances['Part-1-1'].vertices
	verts1 = v1.findAt( ((0.0, 0.0, 0.0), ), ((L, 0.0, 0.0), ),  ((L/2.0, 0.0, 0.0),) )  
	region = a.Set(vertices=verts1, name='Set-2')
	mdb.models['Model-1'].PinnedBC(name='BC-1', createStepName='Step-1', 
	    region=region, localCsys=None)




	#Mesh

	p = mdb.models['Model-1'].parts['Part-1']
	session.viewports['Viewport: 1'].setValues(displayedObject=p)
	session.viewports['Viewport: 1'].partDisplay.setValues(sectionAssignments=OFF, 
	    engineeringFeatures=OFF)
	p = mdb.models['Model-1'].parts['Part-1']
	e = p.edges
	#edges = e.findAt(((L-L/4, 0.0, 0.0), ))
	#p.seedPart(size=1, deviationFactor=1, minSizeFactor=1)
	p.seedEdgeBySize(edges=(e[0],e[1],e[2],e[3],e[4]),size=1)
	#p.seedEdgeByNumber(edges=(e[0],),number=load)
	#p.seedEdgeByNumber(edges=(e[1],),number=(load2-load))
	#p.seedEdgeByNumber(edges=(e[2],),number=6-load2)
	#p.seedEdgeByNumber(edges=(e[3],),number=(load3-6))
	#p.seedEdgeByNumber(edges=(e[4],),number=12-load3)
	p = mdb.models['Model-1'].parts['Part-1']
	p.generateMesh()
	elemType1 = mesh.ElemType(elemCode=B22, elemLibrary=STANDARD)
	p = mdb.models['Model-1'].parts['Part-1']
	e = p.edges
	pickedRegions =(e[0],e[1],e[2],e[3],e[4])
	p.setElementType(regions=pickedRegions, elemTypes=(elemType1, ))

	#Job

	mdb.models['Model-1'].fieldOutputRequests['F-Output-1'].setValues(variables=('U','SF','UR','COORD','SE'))
	if _alpha==0.5:
		_alpha= 05

	if _beta==0.5:
		_beta=05
	mdb.Job(atTime=None, contactPrint=OFF, description='', echoPrint=OFF, 
	    explicitPrecision=SINGLE, getMemoryFromAnalysis=True, historyPrint=OFF, 
	    memory=90, memoryUnits=PERCENTAGE, model='Model-1', modelPrint=OFF, 
	    multiprocessingMode=DEFAULT, name='Job-'+str(_load)+'cargas'+str(Q1)+'-'+str(Q2)+'-'+str(Q3)+'-alpha'+str(_alpha)+'-beta'+str(_beta), nodalOutputPrecision=SINGLE, 
	    numCpus=1, numGPUs=0, queue=None, scratch='', type=ANALYSIS, 
	    userSubroutine='', waitHours=0, waitMinutes=0)



	mdb.jobs['Job-'+str(_load)+'cargas'+str(Q1)+'-'+str(Q2)+'-'+str(Q3)+'-alpha'+str(_alpha)+'-beta'+str(_beta)].submit(consistencyChecking=OFF)
	mdb.jobs['Job-'+str(_load)+'cargas'+str(Q1)+'-'+str(Q2)+'-'+str(Q3)+'-alpha'+str(_alpha)+'-beta'+str(_beta)].waitForCompletion()



f = open("4th-beams10.txt", "a")
for i in range(1,1000):
	carga = np.random.randint(400,800)
	alpha = random.choice([0.5,1,2])
	beta = random.choice([0.5,1,2])
	Q3 = np.random.randint(7,12)
	Q1 = np.random.randint(1,5)
	Q2 = np.random.randint(Q1+1,6)
	
	print >> sys.__stdout__, i 
	print >> sys.__stdout__, carga,beta,alpha,Q1,Q2,Q3
	try:
		runJob(carga,beta,alpha, Q1,Q2,Q3)
		f.write('Job-'+str(carga)+'cargas'+str(Q1)+'-'+str(Q2)+'-'+str(Q3)+'-alpha'+str(alpha)+'-beta'+str(beta)+'\n')
	except:
		pass
	

f.close
