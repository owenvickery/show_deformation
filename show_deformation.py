import os, sys 
import numpy as np
from pylab import *
from matplotlib.font_manager import FontProperties
import argparse
from subprocess import Popen, PIPE
import subprocess, shlex
from time import gmtime, strftime
from shutil import copyfile
from pathlib import Path
from collections import Counter  
import re
import time


def read_deformation(frame, leaflet):
	x,y,bfac=[],[],[]
	# print('z'+str(leaflet)+'xyzi_'+str(frame)+'.pdb')
	if Path('z'+str(leaflet)+'xyzi_'+str(frame)+'.pdb').exists():
		# print('z'+str(leaflet)+'xyzi_'+str(frame)+'.pdb')
		for line in open('z'+str(leaflet)+'xyzi_'+str(frame)+'.pdb', 'r').readlines():
			# print(1)
			if len(line.split()) > 1: 
				if line.split()[0] == 'ATOM':
					x.append(float(line.split()[5]))
					y.append(float(line.split()[6]))
					bfac.append(float(line.split()[9]))
	return np.array(x),np.array(y),np.array(bfac)


# deformation_x, deformation_y, deformation_bfac = read_deformation(1000, 0)
# minima=np.where((deformation_x >= float(1)-0.5 ) & (deformation_x <= float(1)+0.5 ) & (deformation_y >= float(7)-0.5 ) & (deformation_y <= float(7)+0.5 ))

# print(deformation_x[minima], deformation_y[minima], deformation_bfac[minima])

def write_pdb():
	with open('conf.pdb', 'w') as pdb:
		initial = 'ATOM     01  SS  SUR     1     '	
		for frame in range(0, 25000, 500):
			deformation_x, deformation_y, deformation_bfac = read_deformation(frame, 0)	
			pdb.write('MODEL        '+str(frame)+'\n')
			for grid_line_x in range(-99,99):
				x_offset=' '
				if grid_line_x < 0:
					x_offset=''
				for grid_line_y in range(-99,99):
					y_offset=' '
					if grid_line_y < 0:
						y_offset=''
					coord=np.where((deformation_x >= float(grid_line_x)-0.5 ) & (deformation_x <= float(grid_line_x)+0.5 ) & (deformation_y >= float(grid_line_y)-0.5 ) & (deformation_y <= float(grid_line_y)+0.5 ))
					if len(deformation_x[coord]) ==0:
						pdb.write(initial+x_offset+str(grid_line_x)+'.000 '+y_offset+str(grid_line_y)+'.000 '+str(0)+'.000\n')
					else:
						bfac_offset=' '
						if np.mean(deformation_bfac[coord]) < 0:
							bfac_offset=''
						pdb.write(initial+x_offset+str(grid_line_x)+'.000 '+y_offset+str(grid_line_y)+'.000 '+bfac_offset+str(np.mean(deformation_bfac[coord]))+'\n')
			pdb.write('TER\nENDMOL\n')

write_pdb()