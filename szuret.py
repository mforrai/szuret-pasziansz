# -*- coding: utf-8 -*-

from random import shuffle
import copy
import os
import platform
import sys
import shutil
import time
import pymysql
import requests
import urllib.parse

#print(os.name)
# print(platform.system())
# print(platform.release())
#print(platform.platform())

#############################################!
#### MAC address lementése ##################
#############################################
from uuid import getnode as get_mac
try:
	mc = get_mac()
	mac=hex(mc)
except:
	print('Nincs Internet kapcsolat!')

############################
#### Milyen op.rendszer??###
############################
def oprendszer():
	if os.name == 'nt':
		return 'win'
	if os.name == 'posix':
		if platform.platform() in ['Darwin-18.2.0-iPhone10,6-64bit','Darwin-18.2.0-iPad7,3-64bit']:
			return 'ios'
		else:
			return 'mac'

###################################################
###### KÉPERNYŐ TÖRLÉS - iOS, Linux/OSX, Windows###
###################################################
def kepernyo_torles():
	if oprendszer() == 'nt':
		os.system('cls')
	if oprendszer()=='ios':
		import console
		console.clear()
	if oprendszer() == 'mac':
		os.system('clear')
############################################
# TERMINAL BEÁLLÍTÁSAI
############################################
print('                                                                  \n' * 200)

if oprendszer() == 'mac':
	kepernyo_torles()
	sys.stdout.write("\x1b[8;{rows};{cols}t".format(rows=63, cols=72))
if oprendszer() == 'ios':
	kepernyo_torles()
	import console
	console.set_font("Menlo-Regular", 8)
if oprendszer() == 'win':
	kepernyo_torles()
	os.system('mode con: cols=72 lines=63')
kepernyo_torles()

###########################
#EMAIL
###########################
level_tartalma = '111'
def send_email_results(level_tartalma):
	import smtplib
	server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
	server.login("xxx", "xxx123")
	server.sendmail(
	  "xxx@gmail.com", 
	  "xxx@gmail.com", 
	  level_tartalma)
	server.quit()
# send_email_results(level_tartalma)


#################################
#### Lenyomott gomb érzékelése ##
#################################
def getchar():
	if oprendszer() == 'mac':
		# Returns a single character from standard input
		import os
		ch = ''
		if os.name == 'nt': # how it works on windows
			import msvcrt
			ch = msvcrt.getch()
		else:
			import tty, termios, sys
			fd = sys.stdin.fileno()
			old_settings = termios.tcgetattr(fd)
			try:
				tty.setraw(sys.stdin.fileno())
				ch = sys.stdin.read(1)
			finally:
				termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
		if ord(ch) == 3: quit() # handle ctrl+C
		return ch
	else:
		pass
# while 1:  # ha ki kellene próbálni, hogy mik az egyes key code-ok
# 	ch = getchar()
# 	print('You pressed %c (%i)' % (ch, ord(ch)))

###########################################################
# FELKÜLDÉS A SZERVERNEK ##################################
###########################################################
def send_results_net(birtok1, result_1, birtok2, result_2, birtok3, result_3, birtok4, result_4, birtok5, result_5, pirosvar, zoldvar, nullasok, total, kerekitett_ido, kor1_ido, kor2_ido, kor3_ido, kor4_ido, kor5_ido, hossz1, hossz2, hossz3, hossz4, hossz5, hossz_zold, hossz_piros, mac, matrix):

	url = ("http://mforrai.mooo.com:1213/szuret/insert_new.php?birtok1="+birtok1+"&result1="+str(result_1)+"&birtok2="+birtok2+"&result2="+str(result_2)+"&birtok3="+birtok3+"&result3="+str(result_3)+"&birtok4="+birtok4+"&result4="+str(result_4)+"&birtok5="+birtok5+"&result5="+str(result_5)+"&pirosvar="+str(pirosvar)+"&zoldvar="+str(zoldvar)+"&nullasok="+str(nullasok)+"&total="+str(total)+"&kerekitett_ido="+str(kerekitett_ido)+"&kor1_ido="+str(kor1_ido)+"&kor2_ido="+str(kor2_ido)+"&kor3_ido="+str(kor3_ido)+"&kor4_ido="+str(kor4_ido)+"&kor5_ido="+str(kor5_ido)+"&hossz1="+str(hossz1)+"&hossz2="+str(hossz2)+"&hossz3="+str(hossz3)+"&hossz4="+str(hossz4)+"&hossz5="+str(hossz5)+"&hossz_zold="+str(hossz_zold)+"&hossz_piros="+str(hossz_piros)+"&macaddress="+str(mac)+"&matrix="+str(matrix))
	r = requests.get(url)



###########################################################
# KORÁBBI LEGNAGYOBB EREDMÉNYEM ###########################
###########################################################
def legmagasabb_pont():
	url = ("http://mforrai.mooo.com:1213/szuret/sajat_eredmenyek_lekerdezese.php?mac="+mac)
	try:
		r = requests.get(url)
		pontszam = str(r.content.decode("utf-8"))	
	except:
		pontszam = '-999'
	if pontszam == '':
		pontszam = '-999'
	return pontszam

######################################
#### ZENE + SZÍNEK ###################
######################################
if oprendszer() == 'mac':
	import wget
	while True:
		print('                                                                  \n' * 100)
		print('Szeretnél háttér zenét? (i/n)')
		print('A lejátszáshoz Internet kapcsolatra van szükség!')
		ch_zene = ord(getchar())
		if ch_zene in [105,73]: # kér zenét
			zene = 'i'
			kepernyo_torles()
			break
		if ch_zene in [110,78]: # nem kér zenét
			zene = 'n'
			kepernyo_torles()
			break
		else:
			kepernyo_torles()

	while True:
		print('                                                                  \n' * 100)
		print('Szeretnél színeket? (i/n)')
		print('Egyes terminal alkalmazásokban nem jelennek meg helyesen.')
		ch_szin = ord(getchar())
		if ch_szin in [105,73]: # kér zenét
			szinek = 'i'
			kepernyo_torles()
			break
		if ch_szin in [110,78]: # nem kér zenét
			szinek = 'n'
			kepernyo_torles()
			break
		else:
			kepernyo_torles()
	
	if zene == 'i':
		import contextlib
		with contextlib.redirect_stdout(None):
			import pygame,os
			import pygame.midi
		pygame.midi.init()
		dir = os.path.dirname(__file__)
		pygame.mixer.init()
	
		url = 'http://www.curtisclark.org/emusic/midi/agrivenb.mid'
		wget.download(url, 'ambient3.mid')

		pygame.mixer.music.load(os.path.join(dir,'ambient3.mid'))
		pygame.mixer.music.play(loops = -1)
	else:
		pass
else:
	pass

#######################################################
## AZ ADOTT IRÁNYBA FOLYTATÓDIK-E AZ ÚT ###############
#######################################################
def fel(matrix,sor,oszlop):
	if sor==0:
		return 0
	if matrix[sor][oszlop][0] + matrix[sor-1][oszlop][2] == 2:
		return 1
	else:
		return 0

def jobbra(matrix,sor,oszlop):
	if oszlop ==5:
		return 0
	if matrix[sor][oszlop][1] + matrix[sor][oszlop+1][3] == 2:
		return 1
	else:
		return 0
		
def le(matrix,sor,oszlop):
	if sor==6:
		return 0
	if matrix[sor][oszlop][2] + matrix[sor+1][oszlop][0] == 2:
		return 1
	else:
		return 0

def balra(matrix,sor,oszlop):
	if oszlop==0:
		return 0
	if matrix[sor][oszlop][3] + matrix[sor][oszlop-1][1] == 2:
		return 1
	else:
		return 0

###############################################
############# Szőlők mennyisége adott mezőn ###
###############################################
def zold(matrix,sor,oszlop):
	zold = 0
	if (matrix[sor][oszlop][4] not in ['A','B','C','D','E','F','Z','P']) == True:
		zold +=	matrix[sor][oszlop][4]
	return zold
	
def piros(matrix,sor,oszlop):
	piros = 0
	if (matrix[sor][oszlop][5] not in ['A','B','C','D','E','F','Z','P']) == True:
		piros += matrix[sor][oszlop][5]
	return piros
	
###############################################
##### MELYEK A SZOMSZÉDOS MEZŐK ###############
###############################################
def szomszedos(matrix,sor,oszlop):
	szomszedos_mezok = []
	if fel(matrix,sor,oszlop)==1:
		szomszedos_mezok.append([sor-1,oszlop])
	if jobbra(matrix,sor,oszlop)==1:
		szomszedos_mezok.append([sor,oszlop+1])
	if le(matrix,sor,oszlop)==1:
		szomszedos_mezok.append([sor+1,oszlop])
	if balra(matrix,sor,oszlop)==1:
		szomszedos_mezok.append([sor,oszlop-1])
	return szomszedos_mezok

#####################################
#####################################
#####################################
###############  RAJZ  ##############
#####################################
def rajz(imp_matrix,n1,n2):
	if ((oprendszer() in ['ios','win'] or szinek == 'n')):
		mtrx = copy.deepcopy(imp_matrix)
		for x in range(sor):
			for y in range(oszlop):
				if mtrx[x][y][:4] == [0,0,0,0] and (mtrx[x][y][4] in ['A','B','C','D','E','F'] or mtrx[x][y][5] in ['P','Z']):
					mtrx[x][y][:4] = kiemelt['[0,0,0,0]']
					mtrx[x][y][1] = mtrx[x][y][1][:2] + str(mtrx[x][y][5]) + mtrx[x][y][1][3:7] + str(mtrx[x][y][6]) + mtrx[x][y][1][-3:]
				if mtrx[x][y][:4] == [0,0,0,0]:
					mtrx[x][y][:4] = d['[0,0,0,0]']
					mtrx[x][y][1] = mtrx[x][y][1][:2] + str(mtrx[x][y][5]) + mtrx[x][y][1][3:7] + str(mtrx[x][y][6]) + mtrx[x][y][1][-3:]				
				if mtrx[x][y][:4] == [1,1,0,0] and (mtrx[x][y][4] in ['A','B','C','D','E','F'] or mtrx[x][y][5] in ['P','Z']):
					mtrx[x][y][:4] = kiemelt['[1,1,0,0]']
					mtrx[x][y][1] = mtrx[x][y][1][:2] + str(mtrx[x][y][5]) +  mtrx[x][y][1][3:7] + str(mtrx[x][y][6]) + mtrx[x][y][1][-3:]				
				if mtrx[x][y][:4] == [1,1,0,0]:
					mtrx[x][y][:4] = d['[1,1,0,0]']
					mtrx[x][y][1] = mtrx[x][y][1][:2] + str(mtrx[x][y][5]) +  mtrx[x][y][1][3:7] + str(mtrx[x][y][6]) + mtrx[x][y][1][-3:]				
				if mtrx[x][y][:4] == [1,0,1,0] and (mtrx[x][y][4] in ['A','B','C','D','E','F'] or mtrx[x][y][5] in ['P','Z']):
					mtrx[x][y][:4] = kiemelt['[1,0,1,0]']
					mtrx[x][y][1] = mtrx[x][y][1][:2] + str(mtrx[x][y][5]) +  mtrx[x][y][1][3:7] + str(mtrx[x][y][6]) + mtrx[x][y][1][-3:]				
				if mtrx[x][y][:4] == [1,0,1,0]:
					mtrx[x][y][:4] = d['[1,0,1,0]']
					mtrx[x][y][1] = mtrx[x][y][1][:2] + str(mtrx[x][y][5]) +  mtrx[x][y][1][3:7] + str(mtrx[x][y][6]) + mtrx[x][y][1][-3:]				
				if mtrx[x][y][:4] == [1,0,0,1] and (mtrx[x][y][4] in ['A','B','C','D','E','F'] or mtrx[x][y][5] in ['P','Z']):
					mtrx[x][y][:4] = kiemelt['[1,0,0,1]']
					mtrx[x][y][1] = mtrx[x][y][1][:2] + str(mtrx[x][y][5]) +  mtrx[x][y][1][3:7] + str(mtrx[x][y][6]) + mtrx[x][y][1][-3:]				
				if mtrx[x][y][:4] == [1,0,0,1]:
					mtrx[x][y][:4] = d['[1,0,0,1]']
					mtrx[x][y][1] = mtrx[x][y][1][:2] + str(mtrx[x][y][5]) +  mtrx[x][y][1][3:7] + str(mtrx[x][y][6]) + mtrx[x][y][1][-3:]			
				if mtrx[x][y][:4] == [0,1,1,0] and (mtrx[x][y][4] in ['A','B','C','D','E','F'] or mtrx[x][y][5] in ['P','Z']):
					mtrx[x][y][:4] = kiemelt['[0,1,1,0]']
					mtrx[x][y][1] = mtrx[x][y][1][:2] + str(mtrx[x][y][5]) +  mtrx[x][y][1][3:7] + str(mtrx[x][y][6]) + mtrx[x][y][1][-3:]				
				if mtrx[x][y][:4] == [0,1,1,0]:
					mtrx[x][y][:4] = d['[0,1,1,0]']
					mtrx[x][y][1] = mtrx[x][y][1][:2] + str(mtrx[x][y][5]) +  mtrx[x][y][1][3:7] + str(mtrx[x][y][6]) + mtrx[x][y][1][-3:]				
				if mtrx[x][y][:4] == [0,1,0,1] and (mtrx[x][y][4] in ['A','B','C','D','E','F'] or mtrx[x][y][5] in ['P','Z']):
					mtrx[x][y][:4] = kiemelt['[0,1,0,1]']
					mtrx[x][y][1] = mtrx[x][y][1][:2] + str(mtrx[x][y][5]) +  mtrx[x][y][1][3:7] + str(mtrx[x][y][6]) + mtrx[x][y][1][-3:]				
				if mtrx[x][y][:4] == [0,1,0,1]:
					mtrx[x][y][:4] = d['[0,1,0,1]']
					mtrx[x][y][1] = mtrx[x][y][1][:2] + str(mtrx[x][y][5]) +  mtrx[x][y][1][3:7] + str(mtrx[x][y][6]) + mtrx[x][y][1][-3:]				
				if mtrx[x][y][:4] == [0,0,1,1] and (mtrx[x][y][4] in ['A','B','C','D','E','F'] or mtrx[x][y][5] in ['P','Z']):
					mtrx[x][y][:4] = kiemelt['[0,0,1,1]']
					mtrx[x][y][1] = mtrx[x][y][1][:2] + str(mtrx[x][y][5]) +  mtrx[x][y][1][3:7] + str(mtrx[x][y][6]) + mtrx[x][y][1][-3:]				
				if mtrx[x][y][:4] == [0,0,1,1]:
					mtrx[x][y][:4] = d['[0,0,1,1]']
					mtrx[x][y][1] = mtrx[x][y][1][:2] + str(mtrx[x][y][5]) +  mtrx[x][y][1][3:7] + str(mtrx[x][y][6]) + mtrx[x][y][1][-3:]

		print('                                                         © 2019 mforraix')
		print('────────────────────────────────────────────────────────────────────────')
		print('        A          B          C          D          E          F     ')
		print('  ┌──────────────────────────────────────────────────────────────────┐')
		j=0
		while j < n2:
			z = 0
			while z < 5:
				i = 0
				if z ==2:
					print(str(j+1)+' │', sep='', end='')
				else:
					print('  │', sep='', end='')
				while i < n1:
					print(mtrx[j][i][z].replace('0',' '), sep='', end='')
					i += 1
				if z ==2:
					print('│ '+ str(j+1), sep='', end='')
				else:
					print('│  ', sep='', end='')
				print('')
				z += 1
			j += 1
		print('  └──────────────────────────────────────────────────────────────────┘')
		print('        A          B          C          D          E          F     ')
		print('────────────────────────────────────────────────────────────────────────')


	else:
		mtrx = copy.deepcopy(imp_matrix)
		for x in range(sor):
			for y in range(oszlop):
				if mtrx[x][y][:4] == [0,0,0,0] and (mtrx[x][y][4] in ['A','B','C','D','E','F'] or mtrx[x][y][5] in ['P','Z']):
					mtrx[x][y][:4] = kiemelt['[0,0,0,0]']
					mtrx[x][y][1] = mtrx[x][y][1][:2] + '\033[1;32m' + str(mtrx[x][y][5]) + '\033[1;m' +  mtrx[x][y][1][3:7] + '\033[1;31m' + str(mtrx[x][y][6]) + '\033[1;m' + mtrx[x][y][1][-3:]
				if mtrx[x][y][:4] == [0,0,0,0]:
					mtrx[x][y][:4] = d['[0,0,0,0]']
					mtrx[x][y][1] = mtrx[x][y][1][:2] + '\033[1;32m' + str(mtrx[x][y][5]) + '\033[1;m' +  mtrx[x][y][1][3:7] + '\033[1;31m' + str(mtrx[x][y][6]) + '\033[1;m' + mtrx[x][y][1][-3:]

				if mtrx[x][y][:4] == [1,1,0,0] and (mtrx[x][y][4] in ['A','B','C','D','E','F'] or mtrx[x][y][5] in ['P','Z']):
					mtrx[x][y][:4] = kiemelt['[1,1,0,0]']
					mtrx[x][y][1] = mtrx[x][y][1][:2] + '\033[1;32m' + str(mtrx[x][y][5]) + '\033[1;m' +  mtrx[x][y][1][3:7] + '\033[1;31m' + str(mtrx[x][y][6]) + '\033[1;m' + mtrx[x][y][1][-3:]
				if mtrx[x][y][:4] == [1,1,0,0]:
					mtrx[x][y][:4] = d['[1,1,0,0]']
					mtrx[x][y][1] = mtrx[x][y][1][:2] + '\033[1;32m' + str(mtrx[x][y][5]) + '\033[1;m' +  mtrx[x][y][1][3:7] + '\033[1;31m' + str(mtrx[x][y][6]) + '\033[1;m' + mtrx[x][y][1][-3:]

				if mtrx[x][y][:4] == [1,0,1,0] and (mtrx[x][y][4] in ['A','B','C','D','E','F'] or mtrx[x][y][5] in ['P','Z']):
					mtrx[x][y][:4] = kiemelt['[1,0,1,0]']
					mtrx[x][y][1] = mtrx[x][y][1][:2] + '\033[1;32m' + str(mtrx[x][y][5]) + '\033[1;m' +  mtrx[x][y][1][3:7] + '\033[1;31m' + str(mtrx[x][y][6]) + '\033[1;m' + mtrx[x][y][1][-3:]
				if mtrx[x][y][:4] == [1,0,1,0]:
					mtrx[x][y][:4] = d['[1,0,1,0]']
					mtrx[x][y][1] = mtrx[x][y][1][:2] + '\033[1;32m' + str(mtrx[x][y][5]) + '\033[1;m' +  mtrx[x][y][1][3:7] + '\033[1;31m' + str(mtrx[x][y][6]) + '\033[1;m' + mtrx[x][y][1][-3:]


				if mtrx[x][y][:4] == [1,0,0,1] and (mtrx[x][y][4] in ['A','B','C','D','E','F'] or mtrx[x][y][5] in ['P','Z']):
					mtrx[x][y][:4] = kiemelt['[1,0,0,1]']
					mtrx[x][y][1] = mtrx[x][y][1][:2] + '\033[1;32m' + str(mtrx[x][y][5]) + '\033[1;m' +  mtrx[x][y][1][3:7] + '\033[1;31m' + str(mtrx[x][y][6]) + '\033[1;m' + mtrx[x][y][1][-3:]
				if mtrx[x][y][:4] == [1,0,0,1]:
					mtrx[x][y][:4] = d['[1,0,0,1]']
					mtrx[x][y][1] = mtrx[x][y][1][:2] + '\033[1;32m' + str(mtrx[x][y][5]) + '\033[1;m' +  mtrx[x][y][1][3:7] + '\033[1;31m' + str(mtrx[x][y][6]) + '\033[1;m' + mtrx[x][y][1][-3:]


				if mtrx[x][y][:4] == [0,1,1,0] and (mtrx[x][y][4] in ['A','B','C','D','E','F'] or mtrx[x][y][5] in ['P','Z']):
					mtrx[x][y][:4] = kiemelt['[0,1,1,0]']
					mtrx[x][y][1] = mtrx[x][y][1][:2] + '\033[1;32m' + str(mtrx[x][y][5]) + '\033[1;m' +  mtrx[x][y][1][3:7] + '\033[1;31m' + str(mtrx[x][y][6]) + '\033[1;m' + mtrx[x][y][1][-3:]
				if mtrx[x][y][:4] == [0,1,1,0]:
					mtrx[x][y][:4] = d['[0,1,1,0]']
					mtrx[x][y][1] = mtrx[x][y][1][:2] + '\033[1;32m' + str(mtrx[x][y][5]) + '\033[1;m' +  mtrx[x][y][1][3:7] + '\033[1;31m' + str(mtrx[x][y][6]) + '\033[1;m' + mtrx[x][y][1][-3:]


				if mtrx[x][y][:4] == [0,1,0,1] and (mtrx[x][y][4] in ['A','B','C','D','E','F'] or mtrx[x][y][5] in ['P','Z']):
					mtrx[x][y][:4] = kiemelt['[0,1,0,1]']
					mtrx[x][y][1] = mtrx[x][y][1][:2] + '\033[1;32m' + str(mtrx[x][y][5]) + '\033[1;m' +  mtrx[x][y][1][3:7] + '\033[1;31m' + str(mtrx[x][y][6]) + '\033[1;m' + mtrx[x][y][1][-3:]
				if mtrx[x][y][:4] == [0,1,0,1]:
					mtrx[x][y][:4] = d['[0,1,0,1]']
					mtrx[x][y][1] = mtrx[x][y][1][:2] + '\033[1;32m' + str(mtrx[x][y][5]) + '\033[1;m' +  mtrx[x][y][1][3:7] + '\033[1;31m' + str(mtrx[x][y][6]) + '\033[1;m' + mtrx[x][y][1][-3:]


				if mtrx[x][y][:4] == [0,0,1,1] and (mtrx[x][y][4] in ['A','B','C','D','E','F'] or mtrx[x][y][5] in ['P','Z']):
					mtrx[x][y][:4] = kiemelt['[0,0,1,1]']
					mtrx[x][y][1] = mtrx[x][y][1][:2] + '\033[1;32m' + str(mtrx[x][y][5]) + '\033[1;m' +  mtrx[x][y][1][3:7] + '\033[1;31m' + str(mtrx[x][y][6]) + '\033[1;m' + mtrx[x][y][1][-3:]
				if mtrx[x][y][:4] == [0,0,1,1]:
					mtrx[x][y][:4] = d['[0,0,1,1]']
					mtrx[x][y][1] = mtrx[x][y][1][:2] + '\033[1;32m' + str(mtrx[x][y][5]) + '\033[1;m' +  mtrx[x][y][1][3:7] + '\033[1;31m' + str(mtrx[x][y][6]) + '\033[1;m' + mtrx[x][y][1][-3:]


		print('                                                         © 2019 mforraix')
		print('────────────────────────────────────────────────────────────────────────')
		print('        A          B          C          D          E          F     ')
		print('  ┌──────────────────────────────────────────────────────────────────┐')
		j=0
		while j < n2:
			z = 0
			while z < 5:
				i = 0
				if z ==2:
					print(str(j+1)+' │', sep='', end='')
				else:
					print('  │', sep='', end='')
				while i < n1:
					print(mtrx[j][i][z].replace('0',' '), sep='', end='')
					i += 1
				if z ==2:
					print('│ '+ str(j+1), sep='', end='')
				else:
					print('│  ', sep='', end='')
				print('')
				z += 1
			j += 1
		print('  └──────────────────────────────────────────────────────────────────┘')
		print('        A          B          C          D          E          F     ')
		print('────────────────────────────────────────────────────────────────────────')

#############################################
######## Kihúzott lap rajza #################
#############################################
def laprajz(matrix,sor):
	for i in range(sor):
		print(matrix[i])
		
#############################################
######## Kihúzott lap rajza - SÁRGA #########
#############################################
def laprajz_sarga(matrix,sor):
	if oprendszer() == 'mac' and szinek in ['I','i']:
		for i in range(sor):
			print('\033[0;33m',matrix[i],'\033[1;m')
	else:
		for i in range(sor):
			print(matrix[i])
			
#############################################
######## Kihúzott birtok rajza #################
#############################################
def birtokrajz(birtok):
	print('                                                                  \n' * 10)
	
	if birtok=='A':	
		print(
		'''
				
				
			                                 
			                                 
			               AAA               
			              A:::A              
			             A:::::A             
			            A:::::::A            
			           A:::::::::A           
			          A:::::A:::::A          
			         A:::::A A:::::A         
			        A:::::A   A:::::A        
			       A:::::A     A:::::A       
			      A:::::AAAAAAAAA:::::A      
			     A:::::::::::::::::::::A     
			    A:::::AAAAAAAAAAAAA:::::A    
			   A:::::A             A:::::A   
			  A:::::A               A:::::A  
			 A:::::A                 A:::::A 
			AAAAAAA                   AAAAAAA
			                                 
			                                 
			                                 
			                                 
			                                 
			                                 
		'''
		)                                 
	
	if birtok=='B':
		print(
		'''
			
			                    
			                    
			BBBBBBBBBBBBBBBBB   
			B::::::::::::::::B  
			B::::::BBBBBB:::::B 
			BB:::::B     B:::::B
			  B::::B     B:::::B
			  B::::B     B:::::B
			  B::::BBBBBB:::::B 
			  B:::::::::::::BB  
			  B::::BBBBBB:::::B 
			  B::::B     B:::::B
			  B::::B     B:::::B
			  B::::B     B:::::B
			BB:::::BBBBBB::::::B
			B:::::::::::::::::B 
			B::::::::::::::::B  
			BBBBBBBBBBBBBBBBB   
			                    
			                    
			                    
			                    
			                    
			                    
			                    
		'''
		) 
	
	if birtok=='C':
		print(
		'''
			
			                     
			                     
			        CCCCCCCCCCCCC
			     CCC::::::::::::C
			   CC:::::::::::::::C
			  C:::::CCCCCCCC::::C
			 C:::::C       CCCCCC
			C:::::C              
			C:::::C              
			C:::::C              
			C:::::C              
			C:::::C              
			C:::::C              
			 C:::::C       CCCCCC
			  C:::::CCCCCCCC::::C
			   CC:::::::::::::::C
			     CCC::::::::::::C
			        CCCCCCCCCCCCC
			                     
			                     
			                     
			                     
			                     
			                     
			                     
		'''
		) 
	
	if birtok=='D':
		print(
		'''
			
			                     
			                     
			DDDDDDDDDDDDD        
			D::::::::::::DDD     
			D:::::::::::::::DD   
			DDD:::::DDDDD:::::D  
			  D:::::D    D:::::D 
			  D:::::D     D:::::D
			  D:::::D     D:::::D
			  D:::::D     D:::::D
			  D:::::D     D:::::D
			  D:::::D     D:::::D
			  D:::::D     D:::::D
			  D:::::D    D:::::D 
			DDD:::::DDDDD:::::D  
			D:::::::::::::::DD   
			D::::::::::::DDD     
			DDDDDDDDDDDDD        
			                     
			                     
			                     
			                     
			                     
			                     
			                     
		'''
		) 
	
	
	if birtok=='E':
		print(
		'''
			
			                      
			                      
			EEEEEEEEEEEEEEEEEEEEEE
			E::::::::::::::::::::E
			E::::::::::::::::::::E
			EE::::::EEEEEEEEE::::E
			  E:::::E       EEEEEE
			  E:::::E             
			  E::::::EEEEEEEEEE   
			  E:::::::::::::::E   
			  E:::::::::::::::E   
			  E::::::EEEEEEEEEE   
			  E:::::E             
			  E:::::E       EEEEEE
			EE::::::EEEEEEEE:::::E
			E::::::::::::::::::::E
			E::::::::::::::::::::E
			EEEEEEEEEEEEEEEEEEEEEE
			                      
			                      
			                      
			                      
			                      
			                      
			                      
		'''
		) 
	
	if birtok=='F':
		print(
		'''
			
			                      
			                      
			FFFFFFFFFFFFFFFFFFFFFF
			F::::::::::::::::::::F
			F::::::::::::::::::::F
			FF::::::FFFFFFFFF::::F
			  F:::::F       FFFFFF
			  F:::::F             
			  F::::::FFFFFFFFFF   
			  F:::::::::::::::F   
			  F:::::::::::::::F   
			  F::::::FFFFFFFFFF   
			  F:::::F             
			  F:::::F             
			FF:::::::FF           
			F::::::::FF           
			F::::::::FF           
			FFFFFFFFFFF           
			                      
			                      
			                      
			                      
			                      
			                      
			                      
		'''
		) 
	print('                                                                  \n' * 8)
	print('────────────────────────────────────────────────────────────────────────')



	
	
	
	print('Nyomj ENTER-t a folytatáshoz!')
	input('')
	kepernyo_torles()
	
#######################################
######## KOORDINÁTA ELLENŐRZÉS ########
#######################################
def check(valasz):
	if len(valasz) > 2:
		return 0
	y_szam = valasz[:1].upper()
	x_szam = valasz[-1:]	
	if y_szam in ['A','B','C','D','E','F'] and x_szam in ['1','2','3','4','5','6','7']:
		return 1
	else:
		return 0

##################################
######## KÉPERNYŐK, FEJLÉCEK  ####
##################################		
def cim():

	print('────────────────────────────────────────────────────────────────────────')
	print('                                                         © 2019 mforraix')
	print('                                                                  \n' * 3)
	print(
	'''
			 _____     _   _          _   
			/  ___|   (_) (_)        | |  
			\ `--. _____   _ _ __ ___| |_ 
			 `--. \_  / | | | '__/ _ \ __|
			/\__/ // /| |_| | | |  __/ |_ 
			\____//___|\__,_|_|  \___|\__|
	                 --- p a s z i á n s z ---
				         __            
				     __ {_/
				     \_}\\ _
				        _\(_)_
				       (_)_)(_)_
				      (_)(_)_)(_)
				       (_)(_))_)
				        (_(_(_)
				         (_)_)
				          (_)              
	'''
	)

def help():
	kepernyo_torles()
	print('                                                                  \n' * 9)
	print(
	'''
────────────────────────────────────────────────────────────────────────
 Szüret: A játék célja                                              1/5
────────────────────────────────────────────────────────────────────────

A játék során dűlőutakat (útvonalakat) kell berajzolni a térképre,
miközben a szőlőket szőlőbirtokokkal és a várkastélyokkal kell
összekötni.
Minden forduló végén össze kell számolni az adott birtok után járó
pontokat. Pontot akkor kap egy játékos, ha több pontot érnek a
dűlőútépítéssel elért új szőlők, mint amennyit az előző birtok
után kapott.
Minden olyan birtok után, amelyért a játékosnak nem járt pont, a
játék végén 5 pontot le kell vonni.

A játék célja: minél több pont elérése.










────────────────────────────────────────────────────────────────────────
                                                 ENTER: következő
────────────────────────────────────────────────────────────────────────
		'''
	
	)
	input('')
	
	kepernyo_torles()
	print('                                                                  \n' * 9)
	print(
	'''
────────────────────────────────────────────────────────────────────────
 Szüret: A játék menete                                             2/5
────────────────────────────────────────────────────────────────────────

A játék 5 körből áll.
Minden kör elején felfedésre kerül egy birtok.
                 Pl. Első birtok: E
Ezt követően felfedésre kerül egy útvonal az alábbiak közül:
┌────┬────┐┌────┬────┐┌─────────┐┌─────────┐┌─────────┐┌────┬────┐
│    │    ││    │    ││         ││         ││         ││    │    │
├────┘    ││    └────┤│    ┌────┤├────┐    │├─────────┤│    │    │
│         ││         ││    │    ││    │    ││         ││    │    │
└─────────┘└─────────┘└────┴────┘└────┴────┘└─────────┘└────┴────┘
Az útvonal színe lehet fehér vagy sárga. Minden lehetséges elemből
3 db fehér és 4 db sárga áll rendelkezésre.

A játékos két lehetőség közül választhat:
    1. Berajzolja az adott útvonalat a játékmezőre (térképre)
       Ehhez meg kell adni a térkép egy koordinátáját, pl. C3
       
    2. Megnézi, hogy melyik birtok lesz a következő.
       Ehhez a BIRTOK parancsot kell megadni.
       (Fordulónként csak egy alkalommal lehetséges.)

És így tovább a forduló végéig...
────────────────────────────────────────────────────────────────────────
                                                 ENTER: következő
────────────────────────────────────────────────────────────────────────
		'''
	
	)
	input('')

	kepernyo_torles()
	print('                                                                  \n' * 9)
	print(
	'''
────────────────────────────────────────────────────────────────────────
 Szüret: Útvonalrajzolás és pontozás                                3/5
────────────────────────────────────────────────────────────────────────

A játékosnak a térkép egy szabadon választott úres mezőjébe kell
elhelyeznie az útvonalat.
Szabad zsákutcákat és a birtokok határához érő útvonalakat
képezni.
Az újonnan elhelyezett útvonalaknak nem kell amár meglévőket
folytatniuk.


Folyamatosan látható a képernyőn, hogy az adott fordulóban hány 
sárga útvonal került felfedésre.
Ha az adott fordulóban a 4. sárga útvonal is felfedésre került,
vége a fordulónak, és megtörténik a pontozás.

Minden fehér (zöld) és piros szőlőért, amelyhez bármilyen irányban út 
vezet az adott forduló birtokáról, 1 pont jár.






────────────────────────────────────────────────────────────────────────
                                                 ENTER: következő
────────────────────────────────────────────────────────────────────────
		'''
	
	)	
	input('')

	kepernyo_torles()
	print('                                                                  \n' * 9)
	print(
	'''
────────────────────────────────────────────────────────────────────────
 Szüret: Térkép magyarázata                                         4/5
────────────────────────────────────────────────────────────────────────


                      ┌─────────┐
       zöld szőlő --> │ 3    1  │ <-- piros szőlő
                      │         │
                      │         │
                      └─────────┘
                      
                      ╔═════════╗
       "A" birtok --> ║ A       ║
                      ║         ║
                      ║         ║
                      ╚═════════╝
                      
                      ╔═════════╗ 
                      ║      Z  ║ <-- Zöld kastély
                      ║         ║ 
                      ║         ║ 
                      ╚═════════╝ 



────────────────────────────────────────────────────────────────────────
                                                 ENTER: következő
────────────────────────────────────────────────────────────────────────
		'''
	
	)	
	input('')

	kepernyo_torles()
	print('                                                                  \n' * 9)
	print(
	'''
────────────────────────────────────────────────────────────────────────
 Szüret: A végeredmény kiszámítása                                  5/5
────────────────────────────────────────────────────────────────────────

Az ötödik birtok után járó pontok kiszámítása utána a játék véget ér.

   - "1 pont" jár minden piros szőlőért, ami a piros kastéllyal
	  van összekötve

   - "1 pont" jár minden fehér (zöld) szőlőért, ami a zöld kastéllyal
	  van összekötve

   - "- 5 pont" pont jár minden 0 pontos birtokért (fordulóért)












────────────────────────────────────────────────────────────────────────
                                         ENTER: vissza a főmenübe
────────────────────────────────────────────────────────────────────────
		'''
	
	)	
	input('')
	intro()
	
def magamrol():
	kepernyo_torles()
	print('Feltöltés alatt...')
	print('')
	print('https://github.com/mforrai/szuret-pasziansz')
	input('')
	intro()

def szoveges_ertekeles(pont):
	try:
		if pont == -999:
			return 'Nincs korábbi eredmény.'
		
		if -50 <= pont <= 20:
			return 'lőre'
		
		if 20 <= pont <= 39:
			return 'kocsisbor'
	
		if 40 <= pont <= 59:
			return 'fröccsnek megteszi'
	
		if 60 <= pont <= 79:
			return 'asztali bor'
			
		if 80 <= pont <= 99:
			return 'tájbor'
	
		if 100 <= pont <= 119:
			return 'minőségi bor'
			
		if 120 <= pont <= 149:
			return 'Grand Cru'
	
		if 150 <= pont <= 500:
			return 'Grand Cru Reserve'
	except:
		return '-'

def eredmeny(kor):
	print('──────────────────────────────────────────────────────────────── v0.93.1')
	if kor == 1:
		print('........................................................................')

	if kor == 2:
		print(kihuzott_birtokok[1] + ': ' + str(resultkor[1]) + ' pont')
	
	if kor == 3:
		print(kihuzott_birtokok[1] + ': ' + str(resultkor[1]) + ' pont, ' + kihuzott_birtokok[2] + ': ' + str(resultkor[2]) + ' pont')

	if kor == 4:
		print(kihuzott_birtokok[1] + ': ' + str(resultkor[1]) + ' pont, ' + kihuzott_birtokok[2] + ': ' + str(resultkor[2]) + ' pont, ' + kihuzott_birtokok[3] + ': ' + str(resultkor[3]) + ' pont')

	if kor == 5:
		print(kihuzott_birtokok[1] + ': ' + str(resultkor[1]) + ' pont, ' + kihuzott_birtokok[2] + ': ' + str(resultkor[2]) + ' pont, ' + kihuzott_birtokok[3] + ': ' + str(resultkor[3]) + ' pont, ' + kihuzott_birtokok[4] + ': ' + str(resultkor[4]) + ' pont')
	print('────────────────────────────────────────────────────────────────────────')
#####################################
###### PÁLYA BETÖLTÉSE ####
#####################################

def alaphelyzet(sor,oszlop):	
	Matrix = [[[0,0,0,0,0,0] for i in range(oszlop)] for j in range(sor)]
	Matrix[0][0][4] = 3		#zöld
	Matrix[0][0][5] = 1		#piros
	Matrix[0][1][4] = 0		#zöld
	Matrix[0][1][5] = 1		#piros
	Matrix[0][2][4] = 'A'
	Matrix[0][2][5] = 0
	Matrix[0][3][4] = 2		#zöld
	Matrix[0][3][5] = 0		#piros
	Matrix[0][4][4] = 0		#zöld
	Matrix[0][4][5] = 0		#piros		
	Matrix[0][5][4] = 0		#zöld
	Matrix[0][5][5] = 'Z'	#piros

	Matrix[1][0][4] = 0		#zöld
	Matrix[1][0][5] = 1		#piros
	Matrix[1][1][4] = 2		#zöld
	Matrix[1][1][5] = 0		#piros
	Matrix[1][2][4] = 1
	Matrix[1][2][5] = 0
	Matrix[1][3][4] = 0		#zöld
	Matrix[1][3][5] = 1		#piros
	Matrix[1][4][4] = 2		#zöld
	Matrix[1][4][5] = 1		#piros		
	Matrix[1][5][4] = 0		#zöld
	Matrix[1][5][5] = 0		#piros	

	Matrix[2][0][4] = 1		#zöld
	Matrix[2][0][5] = 0		#piros
	Matrix[2][1][4] = 0		#zöld
	Matrix[2][1][5] = 0		#piros
	Matrix[2][2][4] = 1		#zöld
	Matrix[2][2][5] = 2		#piros
	Matrix[2][3][4] = 'B'
	Matrix[2][3][5] = 0
	Matrix[2][4][4] = 1		#zöld
	Matrix[2][4][5] = 0		#piros		
	Matrix[2][5][4] = 2		#zöld
	Matrix[2][5][5] = 0		#piros	
		
	Matrix[3][0][4] = 'C'
	Matrix[3][0][5] = 0
	Matrix[3][1][4] = 0		#zöld
	Matrix[3][1][5] = 2		#piros
	Matrix[3][2][4] = 2		#zöld
	Matrix[3][2][5] = 0		#piros
	Matrix[3][3][4] = 0		#zöld
	Matrix[3][3][5] = 0		#piros
	Matrix[3][4][4] = 0		#zöld
	Matrix[3][4][5] = 2		#piros		
	Matrix[3][5][4] = 'D'	
	Matrix[3][5][5] = 0		
	
	Matrix[4][0][4] = 0		#zöld
	Matrix[4][0][5] = 2		#piros
	Matrix[4][1][4] = 0		#zöld
	Matrix[4][1][5] = 0		#piros
	Matrix[4][2][4] = 'E'
	Matrix[4][2][5] = 0
	Matrix[4][3][4] = 0		#zöld
	Matrix[4][3][5] = 1		#piros
	Matrix[4][4][4] = 2		#zöld
	Matrix[4][4][5] = 1		#piros		
	Matrix[4][5][4] = 0		#zöld	
	Matrix[4][5][5] = 1		#piros
	
	Matrix[5][0][4] = 0		#zöld
	Matrix[5][0][5] = 0		#piros
	Matrix[5][1][4] = 1		#zöld
	Matrix[5][1][5] = 2		#piros
	Matrix[5][2][4] = 1		#zöld
	Matrix[5][2][5] = 0		#piros
	Matrix[5][3][4] = 0		#zöld
	Matrix[5][3][5] = 2		#piros
	Matrix[5][4][4] = 1		#zöld
	Matrix[5][4][5] = 0		#piros		
	Matrix[5][5][4] = 0		#zöld	
	Matrix[5][5][5] = 0		#piros												
																												
	Matrix[6][0][4] = 0
	Matrix[6][0][5] = 'P'
	Matrix[6][1][4] = 1		#zöld
	Matrix[6][1][5] = 0		#piros
	Matrix[6][2][4] = 0		#zöld
	Matrix[6][2][5] = 1		#piros
	Matrix[6][3][4] = 'F'
	Matrix[6][3][5] = 0
	Matrix[6][4][4] = 0		#zöld
	Matrix[6][4][5] = 0		#piros		
	Matrix[6][5][4] = 1		#zöld	
	Matrix[6][5][5] = 3		#piros
	
	return Matrix
													

########################################
######## ZÖLDEK ÖSSZEADÁSA #############
########################################
def zold_lanc(matrix,i,j):
	i=i
	j=j

	osszes_zold = 0
	ellenorizendo_mezok = []

	szomszedos_mezok = szomszedos(matrix,i,j) # a kiindulásival szomszédos mezők
	for i in range(len(szomszedos_mezok)):
		if szomszedos_mezok[i] not in ellenorizendo_mezok:
			ellenorizendo_mezok.append(szomszedos_mezok[i])	#hozzá kell adni az ellenőrizendő mezők listájához a szomszédosakat
	count = 0
	while count < sor*oszlop+1:
		for i in range(len(ellenorizendo_mezok)):
			x = ellenorizendo_mezok[i][0]
			y = ellenorizendo_mezok[i][1]
			szomszedos_mezok = szomszedos(matrix,x,y)
			for i in range(len(szomszedos_mezok)):
				if szomszedos_mezok[i] not in ellenorizendo_mezok:
					ellenorizendo_mezok.append(szomszedos_mezok[i])	#hozzá kell adni az ellenőrizendő mezők listájához a szomszédosakat
		count += 1
	for i in range(len(ellenorizendo_mezok)):
		osszes_zold += zold(matrix,ellenorizendo_mezok[i][0],ellenorizendo_mezok[i][1])
	return osszes_zold

#########################################
######## PIROSAK ÖSSZEADÁSA #############
#########################################
def piros_lanc(matrix,i,j):
	i=i
	j=j

	osszes_piros = 0
	ellenorizendo_mezok = []

	szomszedos_mezok = szomszedos(matrix,i,j) # a kiindulásival szomszédos mezők
	for i in range(len(szomszedos_mezok)):
		if szomszedos_mezok[i] not in ellenorizendo_mezok:
			ellenorizendo_mezok.append(szomszedos_mezok[i])	#hozzá kell adni az ellenőrizendő mezők listájához a szomszédosakat
	count = 0
	while count < sor*oszlop+1:
		for i in range(len(ellenorizendo_mezok)):
			x = ellenorizendo_mezok[i][0]
			y = ellenorizendo_mezok[i][1]
			szomszedos_mezok = szomszedos(matrix,x,y)
			for i in range(len(szomszedos_mezok)):
				if szomszedos_mezok[i] not in ellenorizendo_mezok:
					ellenorizendo_mezok.append(szomszedos_mezok[i])	#hozzá kell adni az ellenőrizendő mezők listájához a szomszédosakat
		count += 1
	for i in range(len(ellenorizendo_mezok)):
		osszes_piros += piros(matrix,ellenorizendo_mezok[i][0],ellenorizendo_mezok[i][1])
	return osszes_piros

#########################################
######## ÖSSZEFÜGGŐ LÁNC ################
#########################################
def lanc(matrix,i,j):
	i=i
	j=j

	ellenorizendo_mezok = [[i,j]]

# while az ellenorizendo_mezok üres nem lesz
# osszes_zold += zold(Matrix,i,j)	# a kiindulási mező
	szomszedos_mezok = szomszedos(matrix,i,j) # a kiindulásival szomszédos mezők
	for i in range(len(szomszedos_mezok)):
		if szomszedos_mezok[i] not in ellenorizendo_mezok:
			ellenorizendo_mezok.append(szomszedos_mezok[i])	#hozzá kell adni az ellenőrizendő mezők listájához a szomszédosakat
	count = 0
	while count < sor*oszlop+1:
		for i in range(len(ellenorizendo_mezok)):
			x = ellenorizendo_mezok[i][0]
			y = ellenorizendo_mezok[i][1]
			szomszedos_mezok = szomszedos(matrix,x,y)
			for i in range(len(szomszedos_mezok)):
				if szomszedos_mezok[i] not in ellenorizendo_mezok:
					ellenorizendo_mezok.append(szomszedos_mezok[i])	#hozzá kell adni az ellenőrizendő mezők listájához a szomszédosakat
		count += 1
	return ellenorizendo_mezok
	
#####################################
######## ALAKZAT SZÓTÁR #############
#####################################
d = {
	'[0,0,0,0]' : ['┌─────────┐','│         │','│         │','│         │','└─────────┘'],
	'[1,1,0,0]' : ['┌────┬────┐','│    │    │','│    └────┤','│         │','└─────────┘'],
	'[1,0,1,0]' : ['┌────┬────┐','│    │    │','│    │    │','│    │    │','└────┴────┘'],
	'[1,0,0,1]' : ['┌────┬────┐','│    │    │','├────┘    │','│         │','└─────────┘'],
	'[0,1,1,0]' : ['┌─────────┐','│         │','│    ┌────┤','│    │    │','└────┴────┘'],
	'[0,1,0,1]' : ['┌─────────┐','│         │','├─────────┤','│         │','└─────────┘'],
	'[0,0,1,1]' : ['┌─────────┐','│         │','├────┐    │','│    │    │','└────┴────┘']	
}

kiemelt = {
	'[0,0,0,0]' : ['╔═════════╗','║         ║','║         ║','║         ║','╚═════════╝'],
	'[1,1,0,0]' : ['╔════╤════╗','║    │    ║','║    └────╢','║         ║','╚═════════╝'],
	'[1,0,1,0]' : ['╔════╤════╗','║    │    ║','║    │    ║','║    │    ║','╚════╧════╝'],
	'[1,0,0,1]' : ['╔════╤════╗','║    │    ║','╟────┘    ║','║         ║','╚═════════╝'],
	'[0,1,1,0]' : ['╔═════════╗','║         ║','║    ┌────╢','║    │    ║','╚════╧════╝'],
	'[0,1,0,1]' : ['╔═════════╗','║         ║','╟─────────╢','║         ║','╚═════════╝'],
	'[0,0,1,1]' : ['╔═════════╗','║         ║','╟────┐    ║','║    │    ║','╚════╧════╝']
}

#####################################
################? ? ? ? ?############
#####################################
elem1 = [1,0,0,1]
elem2 = [1,1,0,0]
elem3 = [0,1,1,0]
elem4 = [0,0,1,1]
elem5 = [0,1,0,1]
elem6 = [1,0,1,0] 

#####################################
######### PAKLI #####################
#####################################
deck1 = [1,0,0,1,11] # 11 = szürke kártya
deck2 = [1,1,0,0,11]
deck3 = [0,1,1,0,11]
deck4 = [0,0,1,1,11]
deck5 = [0,1,0,1,11]
deck6 = [1,0,1,0,11]

deck1s = [1,0,0,1,99] # 99 = SÁRGA kártya
deck2s = [1,1,0,0,99]
deck3s = [0,1,1,0,99]
deck4s = [0,0,1,1,99]
deck5s = [0,1,0,1,99]
deck6s = [1,0,1,0,99]

oszlopok = ['A','B','C','D','E','F']
birtok_poziciok = {
	'A' : [0,2],
	'B' : [2,3],
	'C' : [3,0],
	'D' : [3,5],
	'E' : [4,2],
	'F' : [6,3]
}

#####################################
#########JÁTÉKMEZŐ###################
#####################################

oszlop = 6
sor = 7

#######################################
############ INTRO ####################
#######################################

def intro():
	if oprendszer() == 'mac':	
		kepernyo_torles()
		print('                                                                  \n' * 9)
		cim()
		print('                                                                  \n' * 3)
		print('Legjobb eredményed: '+legmagasabb_pont()+' pont - '+szoveges_ertekeles(int(legmagasabb_pont())))
		print('────────────────────────────────────────────────────────────────────────')
		print(' (H)elp                        (Ú)j játék                    (M)agamról ')
		print('────────────────────────────────────────────────────────────────────────')
		print('                                                                v0.93.1 ')
		print('')
	#########################################
	# h: 104	H:72
	# ú: 250	Ú:218
	# i: 105	m:109	M:77
	# n: 110
	#########################################
		while True:
			ch = ord(getchar())
			if ch in [250,218]: # új játék
				jatek()
			if ch in [104,72]:	# help
				help()
			if ch in [109,77]:	# magamról
				magamrol()
			else:
				pass
	else: #iOS miatt butított a menü
		kepernyo_torles()
		print('                                                                  \n' * 9)
		cim()
		print('                                                                  \n' * 3)
		print('Legjobb eredményed: '+legmagasabb_pont()+' pont')
		print('────────────────────────────────────────────────────────────────────────')
		print('                            ENTER: Új játék                             ')
		print('────────────────────────────────────────────────────────────────────────')
		print('                                                                v0.93.1 ')
		input('')
		jatek()

def jatek():
	birtokok = ['A','B','C','D','E','F']
	shuffle(birtokok)
	
	deck = 3*[deck1] + 3*[deck2] + 3*[deck3] + 3*[deck4] + 4*[deck5] + 4*[deck6]
	deck += 4*[deck1s] + 4*[deck2s] + 4*[deck3s] + 4*[deck4s] + 3*[deck5s] + 3*[deck6s]
	shuffle(deck) #Keverés
	
	global kihuzott_birtokok
	kihuzott_birtokok = [None, None, None, None, None, None]
	global resultkor
	resultkor = [None, None, None, None, None, None]
	koridok = [None, None, None, None, None, None]
	korstart = [None, None, None, None, None, None]
	korvege = [None, None, None, None, None, None]
	kukk = [None, None, None, None, None, None]
	hosszkor = [None, None, None, None, None, None]
	
	Matrix = alaphelyzet(sor,oszlop)
	start = time.time()	# idő mérés indul
	########################################
	######### FORDULÓK ##################
	########################################
	kor=1
	while kor < 6:
	# KÖVETKEZŐ BIRTOK MEGTEKINTÉSE
		kepernyo_torles()
		eredmeny(kor)
		if kihuzott_birtokok[kor] is not None:
			birtok = kihuzott_birtokok[kor]
		else:
			birtok = birtokok.pop()
		print(str(kor)+'. birtok: ' + birtok)
		birtokrajz(birtok)
	
	# INDUL A KÖR
		korstart[kor] = time.time()
		kepernyo_torles()
		eredmeny(kor)
		print(str(kor)+'. birtok: ' + birtok)
		rajz(Matrix,oszlop,sor)
		kukk[kor] = 0
		i=0
		while i < 4: #számolja a sárgákat
			kihuzott_kartya = deck.pop()
			lap_rajz = copy.deepcopy(kihuzott_kartya)
			if lap_rajz[:4] == [0,0,0,0]:
				lap_rajz = d['[0,0,0,0]']
			if lap_rajz[:4] == [1,1,0,0]:
				lap_rajz = d['[1,1,0,0]']
			if lap_rajz[:4] == [1,0,1,0]:
				lap_rajz = d['[1,0,1,0]']
			if lap_rajz[:4] == [1,0,0,1]:
				lap_rajz = d['[1,0,0,1]']
			if lap_rajz[:4] == [0,1,1,0]:
				lap_rajz = d['[0,1,1,0]']
			if lap_rajz[:4] == [0,1,0,1]:
				lap_rajz = d['[0,1,0,1]']
			if lap_rajz[:4] == [0,0,1,1]:
				lap_rajz = d['[0,0,1,1]']
			if kihuzott_kartya[4] == 99:
				i +=1
				laprajz_sarga(lap_rajz,5)
			else:
				laprajz(lap_rajz,5)	
			print('Kihúzott sárga utak száma: ' + str(i))
			x=birtok_poziciok[birtok][0]
			y=birtok_poziciok[birtok][1]
			aktualis = zold_lanc(Matrix,x,y) + piros_lanc(Matrix,x,y)
			print('Várható pontok száma a körben:',aktualis)
			while True:
				valasz = input('Hová helyezi az utat?')
				if check(valasz) == 1:
					y_szam = valasz[:1].upper()
					x_szam = int(valasz[-1:])
					y = oszlopok.index(y_szam)
					x = x_szam-1
					if Matrix[x][y][:4] == [0,0,0,0]:
						kepernyo_torles()
						break
					else:
						print('A megadott mezőn már van út!')
				
				else:
					# KÖVETKEZŐ BIRTOK MEGTEKINTÉSE
					if valasz in ['BIRTOK','birtok'] and kukk[kor] == 0 and i < 4 and kor < 5:
						kihuzott_birtokok[kor+1] = birtokok.pop()
						kepernyo_torles()
						eredmeny(kor)
						print(str(kor)+'. birtok: ' + birtok)
						birtokrajz(kihuzott_birtokok[kor+1])
						kukk[kor] = 1
						
						# VISSZA AZ ADOTT KÖRBE
						eredmeny(kor)
						print(str(kor) + '. birtok: ' + birtok)
						rajz(Matrix,oszlop,sor)

						kihuzott_kartya = deck.pop()
						lap_rajz = copy.deepcopy(kihuzott_kartya)
						if lap_rajz[:4] == [0,0,0,0]:
							lap_rajz = d['[0,0,0,0]']
						if lap_rajz[:4] == [1,1,0,0]:
							lap_rajz = d['[1,1,0,0]']
						if lap_rajz[:4] == [1,0,1,0]:
							lap_rajz = d['[1,0,1,0]']
						if lap_rajz[:4] == [1,0,0,1]:
							lap_rajz = d['[1,0,0,1]']
						if lap_rajz[:4] == [0,1,1,0]:
							lap_rajz = d['[0,1,1,0]']
						if lap_rajz[:4] == [0,1,0,1]:
							lap_rajz = d['[0,1,0,1]']
						if lap_rajz[:4] == [0,0,1,1]:
							lap_rajz = d['[0,0,1,1]']
						if kihuzott_kartya[4] == 99:
							i +=1
							laprajz_sarga(lap_rajz,5)
						else:
							laprajz(lap_rajz,5)
						print('Kihúzott sárga utak száma: ' + str(i))
						print('Várható pontok száma a körben:',aktualis)
					else:
						if kukk[kor] == 1 and valasz in ['BIRTOK','birtok']:
							print('Ebben a körben már megtekintette a következő birtokot!')
						else:
							if kor == 5:
								print('Ez az utolsó kör!')
							else:	
								print('Nem létező parancs! Helyes formátum pl.: A1, D4 stb. vagy BIRTOK')
			
			# ÚT ELHELYEZÉSE A MEGADOTT KOORDINÁTÁKRA
			Matrix[x][y][:4] = kihuzott_kartya[:4]
			eredmeny(kor)
			print(str(kor) + '. birtok: ' + birtok)
			rajz(Matrix,oszlop,sor)
	
		
		# EREDMÉNY MEGHATÁROZÁSA
		x=birtok_poziciok[birtok][0]
		y=birtok_poziciok[birtok][1]
		resultkor[kor] = int(zold_lanc(Matrix,x,y))+int(piros_lanc(Matrix,x,y))
		#print(result_1)
		
		if resultkor[kor-1] is not None:
			if (resultkor[kor] <= resultkor[kor-1]) is True:
				print('Sajnos nem haladta meg az előző birtok pontszámát. (' + str(resultkor[kor-1]) + ')')
				resultkor[kor] = 0
				print(birtok + ' birtok pontszáma: ' + str(resultkor[kor]))
			else:
				print(birtok + ' birtok pontszáma: ' + str(resultkor[kor]))
		else:		
			print(birtok + ' birtok pontszáma: ' + str(resultkor[kor]))

		hosszkor[kor] = copy.deepcopy(len(lanc(Matrix,x,y)))
		kihuzott_birtokok[kor] = birtok
		korvege[kor] = time.time()
		if kor == 5:
			print('────────────────────────────────────────────────────────────────────────')
			print('────────────────────────────── V É G E ─────────────────────────────────')
			print('────────────────── Nyomj ENTER-t a végeredményhez... ───────────────────')
			print('────────────────────────────────────────────────────────────────────────')
			input('')
			kepernyo_torles()
		else:
			input("Nyomj ENTER-t a folytatáshoz...")
			kepernyo_torles()
		kor += 1
	end = time.time()

	#######################################################################
	#######################################################################
	koridok[1] = round(korvege[1]-korstart[1],2)
	koridok[2] = round(korvege[2]-korstart[2],2)
	koridok[3] = round(korvege[3]-korstart[3],2)
	koridok[4] = round(korvege[4]-korstart[4],2)
	koridok[5] = round(korvege[5]-korstart[5],2)

	eltelt_ido = end - start
	kerekitett_ido = round(eltelt_ido,2)
	kerekitett_ido_szoveg = str(kerekitett_ido)
	hossz = len(kerekitett_ido_szoveg)+ (8-len((kerekitett_ido_szoveg)))
	kerekitett_ido_vezeto = kerekitett_ido_szoveg.rjust(hossz)
	
	matrix_up = str(Matrix)
	matrix_up = matrix_up.replace("'","vesszo")
	#######################################################################
	#######################################################################

	########################################
	######### ÖSSZEGZÉS ####################
	########################################
	rajz(Matrix,oszlop,sor)
	print('══════════════════════════════════════════════════════════════'+kerekitett_ido_vezeto+' s')
	print('──────────────────────── V É G E R E D M É N Y ─────────────────────────')
	print('════════════════════════════════════════════════════════════════════════')
	print(kihuzott_birtokok[1] + ' birtok:                       ' + str(resultkor[1]).zfill(2) + ' pont')
	print(kihuzott_birtokok[2] + ' birtok:                       ' + str(resultkor[2]).zfill(2) + ' pont')
	print(kihuzott_birtokok[3] + ' birtok:                       ' + str(resultkor[3]).zfill(2) + ' pont')
	print(kihuzott_birtokok[4] + ' birtok:                       ' + str(resultkor[4]).zfill(2) + ' pont')
	print(kihuzott_birtokok[5] + ' birtok:                       ' + str(resultkor[5]).zfill(2) + ' pont')
	print('────────────────────────────────────────────────────────────────────────')
	osszes_birtok = resultkor[1]+resultkor[2]+resultkor[3]+resultkor[4]+resultkor[5]
	print('Összes birtok:                 ' + str(osszes_birtok).zfill(3) + ' pont')#Összesen
	print('────────────────────────────────────────────────────────────────────────')
	zold_var = zold_lanc(Matrix,0,5)
	hossz_zold = len(lanc(Matrix,0,5))
	print('Zöld vár:                       ' + str(zold_var).zfill(2) + ' pont')# plusz a zöld vár
	piros_var = piros_lanc(Matrix,6,0)
	hossz_piros = len(lanc(Matrix,6,0))
	print('Piros vár:                      ' + str(piros_var).zfill(2) + ' pont')# plusz a piros vár
	print('────────────────────────────────────────────────────────────────────────')
	nullasok = [resultkor[1],resultkor[2],resultkor[3],resultkor[4],resultkor[5]].count(0)*(-5)
	print('Nulla pontos körök (' + str([resultkor[1],resultkor[2],resultkor[3],resultkor[4],resultkor[5]].count(0))+ ' db):     ' + str(nullasok).zfill(2) + ' pont')# mínusz 5*(nullás várak)
	print('════════════════════════════════════════════════════════════════════════')
	grand_total = osszes_birtok + zold_var + piros_var + nullasok # grant total
	print('ÖSSZESEN:                      ' + str(grand_total).zfill(3) + ' pont - ' + szoveges_ertekeles(grand_total))
	print('════════════════════════════════════════════════════════════════════════')
	send_results_net(kihuzott_birtokok[1], resultkor[1], kihuzott_birtokok[2], resultkor[2], kihuzott_birtokok[3], resultkor[3], kihuzott_birtokok[4], resultkor[4], kihuzott_birtokok[5], resultkor[5], piros_var, zold_var, nullasok, grand_total, kerekitett_ido, koridok[1], koridok[2], koridok[3], koridok[4], koridok[5], hosszkor[1], hosszkor[2], hosszkor[3], hosszkor[4], hosszkor[5], hossz_zold, hossz_piros, mac, matrix_up)
	print('Nyomj ENTER-t...')
	input('')
	intro()

##############################################################################
##### START 
##############################################################################

kihuzott_birtokok = [None, None, None, None, None, None]
resultkor = [None, None, None, None, None, None]
intro()

