from math import *
import numpy as np
from datetime import datetime
import pyorbital
from pyorbital.orbital import Orbital

gela=(24.5730, 41.6500015, 1463)    # Coordinates of Gela, Bulgaria 
lon, lat, ao = gela #ao is observer altitude above sea level
sat = Orbital("QMR-KWT")
satlon,satlat, asat = sat.get_lonlatalt(datetime.utcnow()) #altitude of satellite
el = sat.get_observer_look(datetime.utcnow(),lon, lat, ao) # elevation angle towards sat

def getSatVelocity(sat, utcTime): #sat = Orbital('QMR-KWT') or sth
	Vvector = sat.get_position(utcTime,0)[1] #velocity vector
	Vs = sqrt(np.sum(np.square(np.multiply(Vvector,1e3))))
	return Vs

def calcReAtLat(lat): # the earth is a potato  
	r1 = 6378.14e3 #earth equatorial radius
	r2 = 6356.75e3 #earth polar radius
	#(values from https://calgary.rasc.ca/latlong.htm)
	lat = radians(lat)
	Re=sqrt(((r1**2*cos(lat))**2+(r2**2*sin(lat))**2)/((r1*cos(lat))**2+(r2*sin(lat))**2)) # (formula from https://rechneronline.de/earth-radius/ )
	return Re/1e3

def calcAngleToObserver(Re,ao,asat,el): #potato radius, observer altitude, satellite altitude, elevation from horizon
	cosElPN = cos(radians(el+90)) # cos(el+90deg)
	x = (Re+ao)*cosElPN+sqrt((Re+ao)**2*(cosElPN**2)+(Re+asat)**2) #distance between sat and observer
	cosGamma = ((Re+asat)**2+(Re+ao)**2-x**2)/(2*(Re+asat)*(Re+ao)) #calculate cosine of gamma (using cosine theorem) where gamma is the angle between the observer and the satellite from the center of the earth
	gamma = acos(cosGamma) # get the angle (in radians)
	return gamma 

def calcDopplerShift(f,Vsx,Vo=0): #difference in frequencies (in KHz) for stationary observer
	#frequency in MHz, 1d velocity of satellite, 1d velocity of observer 
	c=299792458#speed of light in meters
	df=f*((c+Vo)/(c+Vsx)-1)
	return df*1e3

print(calcDopplerShift(436.5,getSatVelocity(sat,datetime.utcnow())),'KHz')