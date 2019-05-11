# -*- coding: utf-8 -*-

# modulok importálása
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
import random
import secrets

# print(os.name)
# print(platform.system())
# print(platform.release())
# print(platform.platform())
# input()

# paraméterek
version = 'v1.3'
nyelv = 'hun'
ydim=72
xdim=63
host_address = 'http://mforrai.mooo.com:1213/szuret/'

# MAC address lementése
from uuid import getnode as get_mac
try:
	mc = get_mac()
	mac=hex(mc)
except:
	print('Nincs Internet kapcsolat!')

###################################################
# FÜGGVÉNYEK
###################################################

# oprendszer lekérdezése
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

#####################################
#### KÉPERNYŐ ELEMEK ################
#####################################
def teljessor(stilus,db=1):
	if stilus == 'ures':
		print((' ' *ydim)* db)

	if stilus == 'szimpla':
		print(('─' *ydim)* db)

	if stilus == 'dupla':
		print(('═' *ydim)* db)

	if stilus == 'pottyos':
		print(('.' *ydim)* db)
############################################
############################################
def teljessorszoveggel(stilus,szoveg,pozicio='kozep',extra_space=''):

	stilusok = {
		'ures': ' ',
		'szimpla': '─',
		'dupla' : '═',
		'pottyos': '.'
	}

	if extra_space == 1:
		szoveg = szoveg.replace("", " ")[1: -1]

	eleje_hossz = int((ydim-len(szoveg)-2)/2)
	vege_hossz = ydim-eleje_hossz-len(szoveg)-2
	karakter = stilusok[stilus]

	if pozicio == 'kozep':
		print((karakter* eleje_hossz + ' ' + szoveg+ ' ' +karakter * vege_hossz))

	if pozicio == 'bal':
		vege_hossz = ydim-len(szoveg)-1
		print((szoveg+ ' ' +karakter * vege_hossz))

	if pozicio == 'jobb':
		eleje_hossz=ydim-len(szoveg)-1
		print((karakter* eleje_hossz + ' ' + szoveg))

############################################
# TERMINAL BEÁLLÍTÁSAI
############################################
teljessor('ures')

if oprendszer() == 'mac':
	kepernyo_torles()
	sys.stdout.write("\x1b[8;{rows};{cols}t".format(rows=xdim, cols=ydim))
if oprendszer() == 'ios':
	kepernyo_torles()
	import console
	console.set_font("Menlo-Regular", 8)
if oprendszer() == 'win':
	kepernyo_torles()
	os.system('mode con: cols='+str(ydim)+' lines='+str(xdim))
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

#####################################
######## SZÓTÁR #############
#####################################
txt = {
	'legjobb_eredmeny' : {
		'hun' : 'Legjobb eredményed: ',
		'eng' : 'High Score: '
		},

	'szeretnel_zenet' : {
		'hun' : 'Szeretnél háttér zenét? (i/n)',
		'eng' : 'Turn on background music? (y/n)'
		},

	'szeretnel_zenet_internet' : {
		'hun' : 'A lejátszáshoz Internet kapcsolatra van szükség!',
		'eng' : 'Internet connection needed.'
		},

	'szeretnel_szineket' : {
		'hun' : 'Szeretnél színeket? (i/n)',
		'eng' : 'Color mode? (y/n)'
		},

	'szeretnel_szineket_warning' : {
		'hun' : 'Egyes terminal alkalmazásokban nem jelennek meg helyesen.',
		'eng' : 'Not supported by every terminal emulator.'
		},

	'pont' : {
		'hun' : ' pont',
		'eng' : ' point(s)'
		},

	'fomenu' : {
		'hun' : ' (H)elp                        (Ú)j játék                    (M)agamról ',
		'hun' : ' (H)elp         (Ú)j játék         (T)öbb játékos            (M)agamról ',
		'eng' : ' (H)elp         (N)ew game         (T)wo players             (A)bout    '
		},

	'fomenu_ios' : {
		'hun' : '                            ENTER: Új játék                             ',
		'eng' : '                            ENTER: New game                             '
		},

	'kihuzott_sarga' : {
		'hun' : 'Kihúzott sárga utak száma: ',
		'eng' : 'Yellow roads in current round: '
		},

	'birtok' : {
		'hun' : 'birtok',
		'eng' : 'Farm'
		},

	'every_birtok' : {
		'hun' : 'Összes birtok:',
		'eng' : 'Sum  of farms:'
		},

	'green_castle' : {
		'hun' : 'Zöld kastély:',
		'eng' : 'Green castle:'
		},

	'red_castle' : {
		'hun' : 'Piros kastély:',
		'eng' : 'Red castle   :'
		},

	'zero_point_rounds' : {
		'hun' : 'Nulla pontos körök',
		'eng' : 'Zero  point rounds'
		},

	'hit_enter' : {
		'hun' : 'Nyomj ENTER-t a folytatáshoz...',
		'eng' : 'Press ENTER to continue...'
		},

	'db' : {
		'hun' : ' db',
		'eng' : '   '
		},

	'under_contstruction' : {
		'hun' : 'Feltöltés alatt...',
		'eng' : 'Under construction...'
		},

	'under_contstruction' : {
		'hun' : 'Feltöltés alatt...',
		'eng' : 'Under construction...'
		},

	'points_expected' : {
		'hun' : 'Várható pontok a körben:',
		'eng' : 'Points in current round:'
		},

	'total' : {
		'hun' : 'ÖSSZESEN:',
		'eng' : 'TOTAL    '
		},

	'where_road' : {
		'hun' : 'Hová helyezi az utat?',
		'eng' : 'Where do you place the road?'
		},

	'field_used' : {
		'hun' : 'A megadott mezőn már van út!',
		'eng' : 'You already used this field.'
		},

	'kukk_happened' : {
		'hun' : 'Ebben a körben már megtekintette a következő birtokot!',
		'eng' : 'Next farm was already shown in this round.'
		},

	'last_round' : {
		'hun' : 'Ez az utolsó kör!',
		'eng' : 'Last round.'
		},

	'not_valid_command' : {
		'hun' : 'Nem létező parancs! Helyes formátum pl.: A1, D4 stb. vagy BIRTOK',
		'eng' : 'Not valid command. Valid format: A1, D4 etc. or FARM'
		},

	'points_cur_round' : {
		'hun' : ' birtok pontszáma: ',
		'eng' : ' Farm: '
		},

	'not_more' : {
		'hun' : 'Sajnos nem haladta meg az előző birtok pontszámát.',
		'eng' : 'Less or equal points than last round.'
		},

	'enter_results' : {
		'hun' : 'Nyomj ENTER-t a végeredményhez...',
		'eng' : 'Hit ENTER for final results...'
		},

	'end' : {
		'hun' : 'VÉGE',
		'eng' : 'THE END'
		},

	'results' : {
		'hun' : 'VÉGEREDMÉNY',
		'eng' : 'RESULTS'
		},

	'add_nick' : {
		'hun' : 'Add meg a neved, majd nyomj ENTER-t!',
		'eng' : 'Give a nick name and hit ENTER...'
		}


}

#################################
#### Lenyomott gomb érzékelése ##
#################################
def getchar():
	if oprendszer() == 'mac':
		# visszaadja a leütött karaktert
		import os
		ch = ''
		if os.name == 'nt': # Windows
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
		if ord(ch) == 3: quit() # ctrl+C
		return ch
	else:
		pass
# while 1:  # ha ki kellene próbálni, hogy mik az egyes key code-ok
# 	ch = getchar()
# 	print('Lenyomott gomb %c (%i)' % (ch, ord(ch)))

###########################################################
# FELKÜLDÉS A SZERVERNEK ##################################
###########################################################
# def send_results_net(birtok1, result_1, birtok2, result_2, birtok3, result_3, birtok4, result_4, birtok5, result_5, pirosvar, zoldvar, nullasok, total, kerekitett_ido, kor1_ido, kor2_ido, kor3_ido, kor4_ido, kor5_ido, hossz1, hossz2, hossz3, hossz4, hossz5, hossz_zold, hossz_piros, mac, matrix):
#
# 	url = (host_address+"insert_new.php?birtok1="+birtok1+"&result1="+str(result_1)+"&birtok2="+birtok2+"&result2="+str(result_2)+"&birtok3="+birtok3+"&result3="+str(result_3)+"&birtok4="+birtok4+"&result4="+str(result_4)+"&birtok5="+birtok5+"&result5="+str(result_5)+"&pirosvar="+str(pirosvar)+"&zoldvar="+str(zoldvar)+"&nullasok="+str(nullasok)+"&total="+str(total)+"&kerekitett_ido="+str(kerekitett_ido)+"&kor1_ido="+str(kor1_ido)+"&kor2_ido="+str(kor2_ido)+"&kor3_ido="+str(kor3_ido)+"&kor4_ido="+str(kor4_ido)+"&kor5_ido="+str(kor5_ido)+"&hossz1="+str(hossz1)+"&hossz2="+str(hossz2)+"&hossz3="+str(hossz3)+"&hossz4="+str(hossz4)+"&hossz5="+str(hossz5)+"&hossz_zold="+str(hossz_zold)+"&hossz_piros="+str(hossz_piros)+"&macaddress="+str(mac)+"&matrix="+str(matrix))
# 	try:
# 		r = retry_db().get(url,)
# 	except:
# 		pass

def send_results_net(birtok1, result_1, birtok2, result_2, birtok3, result_3, birtok4, result_4, birtok5, result_5, pirosvar, zoldvar, nullasok, total, kerekitett_ido, kor1_ido, kor2_ido, kor3_ido, kor4_ido, kor5_ido, hossz1, hossz2, hossz3, hossz4, hossz5, hossz_zold, hossz_piros, mac, matrix, multiplayer_hash=0):

	url = (host_address+"insert_new.php?birtok1="+birtok1+"&result1="+str(result_1)+"&birtok2="+birtok2+"&result2="+str(result_2)+"&birtok3="+birtok3+"&result3="+str(result_3)+"&birtok4="+birtok4+"&result4="+str(result_4)+"&birtok5="+birtok5+"&result5="+str(result_5)+"&pirosvar="+str(pirosvar)+"&zoldvar="+str(zoldvar)+"&nullasok="+str(nullasok)+"&total="+str(total)+"&kerekitett_ido="+str(kerekitett_ido)+"&kor1_ido="+str(kor1_ido)+"&kor2_ido="+str(kor2_ido)+"&kor3_ido="+str(kor3_ido)+"&kor4_ido="+str(kor4_ido)+"&kor5_ido="+str(kor5_ido)+"&hossz1="+str(hossz1)+"&hossz2="+str(hossz2)+"&hossz3="+str(hossz3)+"&hossz4="+str(hossz4)+"&hossz5="+str(hossz5)+"&hossz_zold="+str(hossz_zold)+"&hossz_piros="+str(hossz_piros)+"&macaddress="+str(mac)+"&matrix="+str(matrix)+"&multiplayer_hash="+str(multiplayer_hash))
	try:
		r = retry_db().get(url,)
	except:
		pass



###########################################################
# BEÁLLÍTÁSOK LEKÉRDEZÉSE    ###########################
###########################################################
def query_settings():
	global mac
	url = (host_address+"query_settings.php?mac="+mac)
	try:
		while 1:
			r = retry_db().get(url,)
			settings = str(r.content.decode("utf-8"))
			if settings != '':
				global beallitasok
				beallitasok = {
					'nyelv' : settings[0],
					'zene'  : settings[1],
					'szin'  : settings[2]
				}
				break
			else:
				time.sleep(1)
			return 1

	except:
		settings = ''
		return 0

def send_settings(mac,nyelv,zene,szin):
	url = (host_address+"add_settings.php?mac="+mac+"&nyelv="+nyelv+"&zene="+zene+"&szin="+szin)
	try:
		r = retry_db().get(url,)
	except:
		pass

###########################################################
# NICK LEKÉRDEZÉS ÉS FELKÜLDÉSE SZERVERRE ###########################
###########################################################
def query_nick(mac):
	url = (host_address+"query_nick.php?mac="+mac)
	try:
		r = retry_db().get(url,)
		nick = str(r.content.decode("utf-8"))
		return nick
	except:
		nick = ''
		return nick

def send_nick(mac,nick):
	url = (host_address+"add_nick.php?mac="+mac+"&nev="+nick)
	try:
		r = retry_db().get(url,)
	except:
		pass
###########################################################
# KORÁBBI LEGNAGYOBB EREDMÉNYEM ###########################
###########################################################
def legmagasabb_pont():
	url = (host_address+"sajat_eredmenyek_lekerdezese.php?mac="+mac)
	try:
		r = retry_db().get(url,)
		pontszam = str(r.content.decode("utf-8"))
	except:
		pontszam = '-999'
	if pontszam == '':
		pontszam = '-999'
	return pontszam

###########################################################
# KORÁBBI LEGJOBB EREDMÉNY RAJZA ###########################
###########################################################
def convert_str2int(a):
	try:
		a = int(a)
		return a
	except:
		return a

def legjobb_matrix():
	try:
		url = (host_address+"legjobb_matrix.php?mac="+mac)
		r = retry_db().get(url,)
		matrix = str(r.content.decode("utf-8")).replace("vesszo","'")
		matrix = matrix.replace("[","")
		matrix = matrix.replace("]","")
		matrix = matrix.replace("'","")
		matrix = matrix.replace(" ","")
		matrix = matrix.split(",")
		tr1 = [matrix[x:x+6] for x in range(0, len(matrix), 6)]
		tr2 = [tr1[x:x+6] for x in range(0, len(tr1), 6)]

		j=0
		while j < 7:
			z = 0
			while z < 6:
				i = 0
				while i < 6:
					try:
						tr2[j][i][z] =  int(tr2[j][i][z])
					except:
						pass
					i += 1
				z += 1
			j += 1

		kepernyo_torles()
		rajz(tr2,oszlop,sor)
		teljessor('ures',2)
		teljessorszoveggel('dupla',txt['hit_enter'][nyelv],'kozep')
		input()
		intro()
	except:
		pass
######################################
#### NYELV + ZENE + SZÍNEK ###################
######################################
if oprendszer() == 'mac':
	if query_settings() == 1:
		if beallitasok['nyelv'] == '1':
			nyelv = 'hun'
		if beallitasok['nyelv'] == '2':
			nyelv = 'eng'
		########
		if beallitasok['zene'] == '1':
			zene = 'i'
		if beallitasok['zene'] == '0':
			zene = 'n'
		########
		if beallitasok['szin'] == '1':
			szinek = 'i'
		if beallitasok['szin'] == '0':
			szinek = 'n'

	if query_settings() == 0:
		while True:
			teljessor('ures',20)
			teljessorszoveggel('ures','1: magyar','kozep')
			teljessorszoveggel('ures','2: english','kozep')
			ch_nyelv = ord(getchar())
			if ch_nyelv in [49]: # magyar
				nyelv = 'hun'
				break
			if ch_nyelv in [50]: # angol
				nyelv = 'eng'
				break
			else:
				kepernyo_torles()

		while True:
			teljessor('ures',5)
			teljessorszoveggel('ures',txt['szeretnel_zenet'][nyelv],'kozep')
			teljessorszoveggel('ures',txt['szeretnel_zenet_internet'][nyelv],'kozep')
			ch_zene = ord(getchar())
			if ch_zene in [105,73,89,121]: # kér zenét
				zene = 'i'
				break
			if ch_zene in [110,78]: # nem kér zenét
				zene = 'n'
				break
			else:
				kepernyo_torles()

		while True:
			teljessor('ures',5)
			teljessorszoveggel('ures',txt['szeretnel_szineket'][nyelv],'kozep')
			teljessorszoveggel('ures',txt['szeretnel_szineket_warning'][nyelv],'kozep')
			ch_szin = ord(getchar())
			if ch_szin in [105,73,89,121]: # kér színeket
				szinek = 'i'
				break
			if ch_szin in [110,78]: # nem kér színeket
				szinek = 'n'
				break
			else:
				kepernyo_torles()

	if zene == 'i':
		try:
			import wget
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
		except:
			pass
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

		teljessorszoveggel('ures','© 2019 mforraix','jobb')
		teljessor('szimpla')
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
		teljessor('szimpla')

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

		teljessorszoveggel('ures','© 2019 mforraix','jobb')
		teljessor('szimpla')
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
		teljessor('szimpla')

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
	teljessor('ures',10)

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
	teljessor('ures',8)
	teljessor('szimpla')
	teljessorszoveggel('szimpla',txt['hit_enter'][nyelv], 'kozep')
	teljessor('szimpla')
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

	teljessor('szimpla')
	teljessorszoveggel('ures','© 2019 mforraix','jobb')
	teljessor('ures',3)
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

def multi_choose():

	teljessorszoveggel('ures','1. Publikus játék indítása','kozep')
	teljessorszoveggel('ures','2. Csatlakozás...','kozep')
	teljessor('ures',3)
	teljessorszoveggel('ures','3. Privát játék indítása','kozep')
	teljessorszoveggel('ures','4. Csatlakozás...','kozep')
	teljessor('ures',3)

def help():
	kepernyo_torles()
	teljessor('ures',9)
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
	teljessor('ures',9)
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
	teljessor('ures',9)
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
	teljessor('ures',9)
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
	teljessor('ures',9)
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
	print(txt['under_contstruction'][nyelv])
	print('')
	print('https://github.com/mforrai/szuret-pasziansz')
	input('')
	intro()

def szoveges_ertekeles(pont,nyelv):
	if nyelv == 'hun':
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

	if nyelv == 'eng':
		try:
			if pont == -999:
				return 'Not found previous results'

			if -50 <= pont <= 20:
				return 'Dreadful'

			if 20 <= pont <= 39:
				return 'Unsatisfactory'

			if 40 <= pont <= 59:
				return 'Mediocre'

			if 60 <= pont <= 79:
				return 'Quite good'

			if 80 <= pont <= 99:
				return 'Pretty good'

			if 100 <= pont <= 119:
				return 'Superb'

			if 120 <= pont <= 149:
				return 'Excellent'

			if 150 <= pont <= 500:
				return 'Outstanding'
		except:
			return '-'
#################################
# def eredmeny(kor):
# 	teljessorszoveggel('szimpla',version,'jobb')
# 	if kor == 1:
# 		teljessor('pottyos')
#
# 	if kor == 2:
# 		print(kihuzott_birtokok[1] + ': ' + str(resultkor[1]) + ' pont')
#
# 	if kor == 3:
# 		print(kihuzott_birtokok[1] + ': ' + str(resultkor[1]) + ' pont, ' + kihuzott_birtokok[2] + ': ' + str(resultkor[2]) + ' pont')
#
# 	if kor == 4:
# 		print(kihuzott_birtokok[1] + ': ' + str(resultkor[1]) + ' pont, ' + kihuzott_birtokok[2] + ': ' + str(resultkor[2]) + ' pont, ' + kihuzott_birtokok[3] + ': ' + str(resultkor[3]) + ' pont')
#
# 	if kor == 5:
# 		print(kihuzott_birtokok[1] + ': ' + str(resultkor[1]) + ' pont, ' + kihuzott_birtokok[2] + ': ' + str(resultkor[2]) + ' pont, ' + kihuzott_birtokok[3] + ': ' + str(resultkor[3]) + ' pont, ' + kihuzott_birtokok[4] + ': ' + str(resultkor[4]) + ' pont')
# 	teljessor('szimpla')

######

def eredmeny(kor):
	teljessorszoveggel('szimpla',version,'jobb')
	if kor == 1:
		teljessor('pottyos')

	if 1 < kor <= 5:
		try:
			i=1
			felirat = ''
			while i < kor:
				felirat += kihuzott_birtokok[i] + str(': ') + str(resultkor[i]) + str(' pont')
				if i == 5:
					break
				else:
					felirat += str(', ')
				i+=1
			teljessorszoveggel('ures',felirat,'bal')
		except:
			teljessor('pottyos')
	teljessor('szimpla')


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
		teljessor('ures',9)
		cim()
		teljessor('ures',3)
		print(txt['legjobb_eredmeny'][nyelv]+legmagasabb_pont()+txt['pont'][nyelv]+' - '+szoveges_ertekeles(int(legmagasabb_pont()),nyelv)+'    (*) - '+query_nick(mac))
		teljessor('szimpla')
		print(txt['fomenu'][nyelv])
		teljessor('szimpla')
		teljessorszoveggel('ures',version + ' ','jobb')
		teljessor('ures')
	#########################################
	# h: 104	H:72
	# ú: 250	Ú:218
	# i: 105	m:109	M:77
	# n: 110
	#########################################
		while True:
			ch = ord(getchar())
			if ch in [116,84]:	# MULTIPLAYER
				multi()
			if ch in [250,218,78,110]: # új játék
				jatek()
			if ch in [104,72]:	# help
				help()
			if ch in [109,77,65,97]:	# magamról
				magamrol()
			if ch in [42]:	# legjobb eremény rajza
				legjobb_matrix()
			else:
				pass
	else: #iOS miatt butított a menü
		kepernyo_torles()
		teljessor('ures',9)
		cim()
		teljessor('ures',3)
		print(txt['legjobb_eredmeny'][nyelv]+legmagasabb_pont()+txt['pont'][nyelv]+' - '+szoveges_ertekeles(int(legmagasabb_pont()),nyelv)+'    (*) - '+query_nick(mac))
		teljessor('szimpla')
		print(txt['fomenu_ios'][nyelv])
		teljessor('szimpla')
		teljessorszoveggel('ures',version + ' ','jobb')
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
		print(str(kor)+'. ' + txt['birtok'][nyelv]+ ': ' + birtok)
		birtokrajz(birtok)

	# INDUL A KÖR
		korstart[kor] = time.time()
		kepernyo_torles()
		eredmeny(kor)
		print(str(kor)+'. ' + txt['birtok'][nyelv] + ': ' + birtok)
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
			print(txt['kihuzott_sarga'][nyelv] + str(i))
			x=birtok_poziciok[birtok][0]
			y=birtok_poziciok[birtok][1]
			aktualis = zold_lanc(Matrix,x,y) + piros_lanc(Matrix,x,y)
			print(txt['points_expected'][nyelv], aktualis)
			while True:
				valasz = input(txt['where_road'][nyelv])
				if check(valasz) == 1:
					y_szam = valasz[:1].upper()
					x_szam = int(valasz[-1:])
					y = oszlopok.index(y_szam)
					x = x_szam-1
					if Matrix[x][y][:4] == [0,0,0,0]:
						kepernyo_torles()
						break
					else:
						print(txt['field_used'][nyelv])
				else:
					# KÖVETKEZŐ BIRTOK MEGTEKINTÉSE
					if valasz in ['BIRTOK','birtok','FARM','farm'] and kukk[kor] == 0 and i < 5 and kor < 5:
						kihuzott_birtokok[kor+1] = birtokok.pop()
						kepernyo_torles()
						eredmeny(kor)
						print(str(kor) + '. ' + txt['birtok'][nyelv] + ': ' + birtok)
						birtokrajz(kihuzott_birtokok[kor+1])
						kukk[kor] = 1

						# VISSZA AZ ADOTT KÖRBE
						if i < 4:
							eredmeny(kor)
							print(str(kor) + '. ' + txt['birtok'][nyelv] + ': ' + birtok)
							rajz(Matrix,oszlop,sor)
							if i < 4:
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
								print(txt['kihuzott_sarga'][nyelv] + str(i))
								print(txt['points_expected'][nyelv],aktualis)
							else:
								pass
						else:
							break
					else:
						if kukk[kor] == 1 and valasz in ['BIRTOK','birtok','FARM','farm']:
							print(txt['kukk_happened'][nyelv])
						else:
							if kor == 5 and valasz in ['BIRTOK','birtok','FARM','farm']:
								print(txt['last_round'][nyelv])
							else:
								if valasz in ['EXIT','exit']:
									intro()
								else:
									print(txt['not_valid_command'][nyelv])

			# ÚT ELHELYEZÉSE A MEGADOTT KOORDINÁTÁKRA
			Matrix[x][y][:4] = kihuzott_kartya[:4]
			eredmeny(kor)
			print(str(kor) + '. ' + txt['birtok'][nyelv] + ': ' + birtok)
			rajz(Matrix,oszlop,sor)


		# EREDMÉNY MEGHATÁROZÁSA
		x=birtok_poziciok[birtok][0]
		y=birtok_poziciok[birtok][1]
		resultkor[kor] = int(zold_lanc(Matrix,x,y))+int(piros_lanc(Matrix,x,y))
		#print(result_1)

		if resultkor[kor-1] is not None:
			if (resultkor[kor] <= resultkor[kor-1]) is True:
				print(txt['not_more'][nyelv]   + ' (' + str(resultkor[kor-1]) + ')')
				resultkor[kor] = 0
				print(birtok + txt['points_cur_round'][nyelv] + str(resultkor[kor]))
			else:
				print(birtok + txt['points_cur_round'][nyelv] + str(resultkor[kor]))
		else:
			print(birtok + txt['points_cur_round'][nyelv] + str(resultkor[kor]))

		hosszkor[kor] = copy.deepcopy(len(lanc(Matrix,x,y)))
		kihuzott_birtokok[kor] = birtok
		korvege[kor] = time.time()
		if kor == 5:
			teljessor('szimpla')
			teljessorszoveggel('szimpla',txt['end'][nyelv],'kozep',1)
			teljessorszoveggel('szimpla',txt['enter_results'][nyelv],'kozep')
			teljessor('szimpla')
			input('')
			kepernyo_torles()
		else:
			input(txt['hit_enter'][nyelv])
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
	teljessorszoveggel('dupla',str(kerekitett_ido_vezeto+' s'),'jobb')
	teljessorszoveggel('szimpla',txt['results'][nyelv], 'kozep', 1)
	teljessor('dupla')
	print(kihuzott_birtokok[1] + ' '+txt['birtok'][nyelv]+':                       ' + str(resultkor[1]).zfill(2) + txt['pont'][nyelv])
	print(kihuzott_birtokok[2] + ' '+txt['birtok'][nyelv]+':                       ' + str(resultkor[2]).zfill(2) + txt['pont'][nyelv])
	print(kihuzott_birtokok[3] + ' '+txt['birtok'][nyelv]+':                       ' + str(resultkor[3]).zfill(2) + txt['pont'][nyelv])
	print(kihuzott_birtokok[4] + ' '+txt['birtok'][nyelv]+':                       ' + str(resultkor[4]).zfill(2) + txt['pont'][nyelv])
	print(kihuzott_birtokok[5] + ' '+txt['birtok'][nyelv]+':                       ' + str(resultkor[5]).zfill(2) + txt['pont'][nyelv])
	teljessor('szimpla')
	osszes_birtok = resultkor[1]+resultkor[2]+resultkor[3]+resultkor[4]+resultkor[5]
	print(txt['every_birtok'][nyelv]+'               ' + str(osszes_birtok).zfill(3) + txt['pont'][nyelv])#Összesen
	teljessor('szimpla')
	zold_var = zold_lanc(Matrix,0,5)
	hossz_zold = len(lanc(Matrix,0,5))
	print(txt['green_castle'][nyelv]+'                 ' + str(zold_var).zfill(2) + txt['pont'][nyelv])# plusz a zöld vár
	piros_var = piros_lanc(Matrix,6,0)
	hossz_piros = len(lanc(Matrix,6,0))
	print(txt['red_castle'][nyelv]+'                ' + str(piros_var).zfill(2) + txt['pont'][nyelv])# plusz a piros vár
	teljessor('szimpla')
	nullasok = [resultkor[1],resultkor[2],resultkor[3],resultkor[4],resultkor[5]].count(0)*(-5)
	print(txt['zero_point_rounds'][nyelv]+' (' + str([resultkor[1],resultkor[2],resultkor[3],resultkor[4],resultkor[5]].count(0))+ txt['db'][nyelv] + '):   ' + str(nullasok).zfill(2) + txt['pont'][nyelv])# mínusz 5*(nullás várak)
	teljessor('dupla')
	grand_total = osszes_birtok + zold_var + piros_var + nullasok # grant total
	print(txt['total'][nyelv]+'                    ' + str(grand_total).zfill(3) + txt['pont'][nyelv]+' - ' + szoveges_ertekeles(grand_total,nyelv))
	teljessor('dupla')
	send_results_net(kihuzott_birtokok[1], resultkor[1], kihuzott_birtokok[2], resultkor[2], kihuzott_birtokok[3], resultkor[3], kihuzott_birtokok[4], resultkor[4], kihuzott_birtokok[5], resultkor[5], piros_var, zold_var, nullasok, grand_total, kerekitett_ido, koridok[1], koridok[2], koridok[3], koridok[4], koridok[5], hosszkor[1], hosszkor[2], hosszkor[3], hosszkor[4], hosszkor[5], hossz_zold, hossz_piros, mac, matrix_up)

	if query_nick(mac) == '' or None:
		teljessorszoveggel('ures',txt['add_nick'][nyelv],'kozep')
		a = ''
		nick = input(a.center(int(ydim/2)))
		send_nick(mac, nick)
		send_settings(mac, nyelv, zene, szinek)
	else:
		print(txt['hit_enter'][nyelv])
		input('')
	intro()





##################################################
##################################################
############ MULTIPLAYER ########################+
##################################################


import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


def retry_db(
    retries=3,
    backoff_factor=0.3,
    status_forcelist=(500, 502, 504),
    session=None,
):
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session


######################
def is_ready(game, whoisready):
	# host, connect
	url = (host_address+"multi_query_ready.php?game="+str(game)+"&case="+str(whoisready))
	try:
		r = retry_db().get(url,)
		is_ready = str(r.content.decode("utf-8"))
		return is_ready
	except Exception as x:
		print('It failed: (', x.__class__.__name__)
	else:
		pass


##################################################+
def query_birtokok(game):
	url = (host_address+"multi_query_birtokok.php?game="+game)
	try:
		r = retry_db().get(url,)
		birtokok = str(r.content.decode("utf-8"))
		return birtokok
	except Exception as x:
		print('It failed: (', x.__class__.__name__)
	else:
		pass

######################

def query_aktualis(game,case):
	url = (host_address+"multi_query_aktualis.php?game="+game+"&case="+case)
	try:
		r = retry_db().get(url,)
		aktualis = str(r.content.decode("utf-8"))
		return aktualis
	except Exception as x:
		print('It failed: (', x.__class__.__name__)
	else:
		pass
######################
def upload_aktualis_birtok (birtok, kor, game):
	url = (host_address+"multi_upload_birtok.php?game="+str(game)+"&aktualis_birtok="+str(birtok)+"&hanyadik_birtok="+str(kor))

	try:
		r = retry_db().get(url,)

	except Exception as x:
		print('It failed: (', x.__class__.__name__)
	else:
		pass



######################
def upload_next_birtok (game, kov_birtok_hanyadik, kov_birtok):
	url = (host_address+"multi_upload_next_birtok.php?game="+str(game)+"&kov_birtok_sorszama="+str(kov_birtok_hanyadik)+"&kov_birtok="+str(kov_birtok))

	try:
		r = retry_db().get(url,)

	except Exception as x:
		print('It failed: (', x.__class__.__name__)
	else:
		pass



######################
def upload_birtokok (game,birtokok):
	url = (host_address+"multi_upload_birtokok.php?game="+str(game)+"&birtokok="+str(birtokok))

	try:
		r = retry_db().get(url,)

	except Exception as x:
		print('It failed: (', x.__class__.__name__)
	else:
		pass

######################
def upload_aktualis_kartya(kartya, hanyadik, game):
	url = (host_address+"multi_upload_kartya.php?game="+str(game)+"&aktualis_kartya="+str(kartya)+"&hanyadik_kartya="+str(hanyadik))
	try:
		r = retry_db().get(url,)
	except:
		pass

######################
def increase_aktualis_kartya(hanyadik, game):
	url = (host_address+"multi_add_1_to_aktualis_kartya.php?game="+str(game)+"&hanyadik_kartya="+str(hanyadik))
	try:
		r = retry_db().get(url,)
	except Exception as x:
		print('It failed: (', x.__class__.__name__)
	else:
		pass


######################
def player_status(game, who):
	# hostready, connectready, hostunready, connectunready
	url = (host_address+"multi_update_ready.php?game="+str(game)+"&case="+str(who))
	try:
		r = retry_db().get(url,)
		player_status = str(r.content.decode("utf-8"))
		return player_status
	except Exception as x:
		print('It failed: (', x.__class__.__name__)
	else:
		pass

######################
def multi_results(game, mac):
	url = (host_address+"multi_query_results.php?game="+str(game)+"&mac="+str(mac))
	try:
		r = retry_db().get(url,)
		opponent_result = str(r.content.decode("utf-8"))
		return opponent_result
	except Exception as x:
		print('It failed: (', x.__class__.__name__)
	else:
		pass
######################
def choose_free_game():
	# hostready, connectready, hostunready, connectunready
	url = (host_address+"query_free_host.php")
	try:
		r = retry_db().get(url,)
		game = str(r.content.decode("utf-8"))
		if game == '':
			return 0
		return game
	except Exception as x:
		print('It failed: (', x.__class__.__name__)
	else:
		pass


######################
def kartya2string(kartya):
	kartya2upload = str(kartya[0])+str(kartya[1])+str(kartya[2])+str(kartya[3])+str(kartya[4])
	return kartya2upload

######################
def string2kartya(string):
	kartya= []
	kartya.append(int(string[0]))
	kartya.append(int(string[1]))
	kartya.append(int(string[2]))
	kartya.append(int(string[3]))
	kartya.append(int(string[4]+string[5]))
	return kartya

#################################################
def multi():
	multi_choose()
	while True:
		ch = ord(getchar())
		if ch in [49]:	# MULTIPLAYER
			valasztas = 'host'
			break
		if ch in [50]:	# MULTIPLAYER
			valasztas = 'connect'
			break
		if ch in [51]:	# MULTIPLAYER
			valasztas = 'host_private'
			break
		if ch in [52]:	# MULTIPLAYER
			valasztas = 'connect_private'
			break
		else:
			pass

	if valasztas == 'host':
	#	hosted_game = str(random.randint(1,9999))
		hosted_game = secrets.token_hex(25)
		game = hosted_game
		iamhost = 1
		url = (host_address+"multi_host_game.php?hosted_game="+hosted_game)
		try:
			r = retry_db().get(url,)
		except:
			pass

	if valasztas == 'connect':
		wait_s = 1
		while 1:
			print('Kapcsolódás' + wait_s*'.'+'\r', end='')
			time.sleep(1)
			wait_s += 1
			game = str(choose_free_game())
			if wait_s == 30:
				print()
				print('Sajnos nincs elérhető játékos...')
				time.sleep(2)
				intro()
			if game != '0':
				break
			else:
				time.sleep(1)
		game = str(choose_free_game())
		iamhost = 0
		url = (host_address+"multi_connect_game.php?game="+game)
		try:
			r = retry_db().get(url,)
		except:
			pass

	if valasztas == 'host_private':
	#	hosted_game = str(random.randint(1,9999))
		hosted_game = secrets.token_hex(3)
		game = hosted_game
		iamhost = 1
		url = (host_address+"multi_host_game.php?hosted_game="+hosted_game)
		try:
			r = retry_db().get(url,)
		except:
			pass

	if valasztas == 'connect_private':
		game = input('Játék azonosítója:')
		iamhost = 0
		url = (host_address+"multi_connect_game.php?game="+game)
		try:
			r = retry_db().get(url,)
			valasz = str(r.content.decode("utf-8"))
			if valasz == '!!!':
				pass
				intro()
			else:
				pass
		except:
			pass
			intro()
################################################################################################################
	birtokok = ['A','B','C','D','E','F']
	shuffle(birtokok)
	if iamhost == 1:
		deck = 3*[deck1] + 3*[deck2] + 3*[deck3] + 3*[deck4] + 4*[deck5] + 4*[deck6]
		deck += 4*[deck1s] + 4*[deck2s] + 4*[deck3s] + 4*[deck4s] + 3*[deck5s] + 3*[deck6s]
		shuffle(deck) #Keverés

	if iamhost == 0:
		pass
################################################################################################################

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
	kor=0

	hanyadik_kihuzott_kartya = 0
	utolso_kartya_sorszama = 0

################################################################################################################
	if iamhost == 1:
		print('Játék azonosítója: '+str(game))
		wait_s = 1
		while 1:	#várakozás a másik játékosra
			player_status(game,'hostunready')
			if int(is_ready(game,'2nd_player')) == 1:
				break
			else:
				print('Várakozás a másik játékosra' + wait_s*'.'+'\r', end='')
				time.sleep(1)
				wait_s += 1
				if wait_s == 30:
					print()
					print('Sajnos nincs elérhető játékos...')
					time.sleep(2)
					intro()
	if iamhost == 0:
		pass
################################################################################################################

	while kor < 6:

		if iamhost == 1:
			player_status(game,'hostunready')
			while 1:	#várakozás a másik játékosra
				# kepernyo_torles()
				print('Várakozás a másik játékosra...',)
				if int(is_ready(game,'mehet2')) == 1:
					player_status(game, 'nem_mehet2')
					break
				else:
					time.sleep(1)

		if iamhost == 0:
			while 1:
				print('Várakozás a másik játékosra...',)
				if int(is_ready(game,'mehet2')) == 0:
					break
				else:
					time.sleep(1)
################################################################################################################
	# BIRTOK FELFEDÉSE
		if iamhost == 1:
			if kor == 0:
				kor += 1
			if kihuzott_birtokok[kor] is not None:
				birtok = kihuzott_birtokok[kor]
			else:
				if int(query_aktualis(game,'kov_birtok_hanyadik')) == kor: # ha már szerepel az adatbázisban, akkor onnan frissíti
					birtok = query_aktualis(game,'kov_birtok')
					birtokok.remove(birtok) # ki kell venni a lehetséges értékek közül
				else:
					birtok = birtokok.pop() # ha nem szerepel, húz egyet
			upload_aktualis_birtok(birtok,kor,game) # feltölti a birtokot a másik játékosnak
			birtokok_string = ''.join(map(str, birtokok))
			upload_birtokok(game,birtokok_string)
			player_status(game,'hostready')
		if iamhost == 0:
			# player_status(game,'connectready')
			while 1:
					print('Várakozás a másik játékosra...')
					while 1:	#várakozás a másik játékosra
						if int(is_ready(game,'host')) == 1:
							break
						else:
							time.sleep(1)

					if int(query_aktualis(game,'birtok_hanyadik')) > int(kor):
						kor=int(query_aktualis(game, 'birtok_hanyadik'))
						birtok = query_aktualis(game, 'birtok')
						try:
							birtokok.remove(birtok)
						except:
							pass
						break
					else:
						time.sleep(1)
################################################################################################################
		kepernyo_torles()
		eredmeny(kor)
		print(str(kor)+'. ' + txt['birtok'][nyelv]+ ': ' + birtok)
		birtokrajz(birtok)
		if iamhost == 1:
			player_status(game,'mehet1')
		if iamhost == 0:
			# várjon addig, amíg elkészül a host
			player_status(game,'mehet2')

		# INDUL A KÖR
		if iamhost == 1:
			while 1:	#várakozás a másik játékosra
				print('Várakozás a másik játékosra...',)
				if int(is_ready(game,'mehet2')) == 1:
					break
				else:
					time.sleep(1)
			player_status(game,'hostunready')

		if iamhost == 0:
			# várjon addig, amíg elkészül a host
			player_status(game,'connectready')
			pass
		korstart[kor] = time.time()
		# kepernyo_torles()
		# eredmeny(kor)
		kukk[kor] = 0
		i=0
		while i < 4: #számolja a sárgákat
################################################################################################################
			if iamhost == 1:
				player_status(game,'nem_mehet1')
				player_status(game,'nem_mehet2')
				while 1:	#várakozás a másik játékosra
					print('Várakozás a másik játékosra...',)
					player_status(game,'hostready')		#lehet, hogy TÖRÖLNI KELL
					if int(is_ready(game,'connect')) == 1:
						player_status(game,'connectunready')      #ezt lehet, hogy vissza kell állítani, mert etőtl nem fog működni
						break
					else:
						time.sleep(1)

			if iamhost == 0:
				while 1:	#várakozás a másik játékosra
					print('Várakozás a másik játékosra...',)
					if int(is_ready(game,'host')) == 1:
						break
					else:
						time.sleep(1)
################################################################################################################
			kepernyo_torles()
			eredmeny(kor)
			print(str(kor) + '. ' + txt['birtok'][nyelv] + ': ' + birtok)
			print(game)
			rajz(Matrix,oszlop,sor)
################################################################################################################
			if iamhost == 1:
				kihuzott_kartya = deck.pop()
				hanyadik_kihuzott_kartya += 1
				upload_aktualis_kartya(kartya2string(kihuzott_kartya),hanyadik_kihuzott_kartya,game) # feltölti, hogy mi a következő kártya, és hogy hányadik
				while 1:
					if int(is_ready(game,'connect')) == 0:
						break
					else:
						time.sleep(1)
			if iamhost == 0:
				while 1:
					last_sorszam = int(query_aktualis(game,'kartya_hanyadik'))
					if last_sorszam > utolso_kartya_sorszama:
						kihuzott_kartya = query_aktualis(game,'kartya')
						kihuzott_kartya = string2kartya(kihuzott_kartya)
						utolso_kartya_sorszama = last_sorszam
						player_status(game,'connectunready')
						break
					else:
						time.sleep(1)
################################################################################################################
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

			if iamhost == 1:
				player_status(game,'hostunready')
			if iamhost == 0:
				player_status(game,'connectunready')

			print(txt['kihuzott_sarga'][nyelv] + str(i))
			x=birtok_poziciok[birtok][0]
			y=birtok_poziciok[birtok][1]
			aktualis = zold_lanc(Matrix,x,y) + piros_lanc(Matrix,x,y)
			print(txt['points_expected'][nyelv], aktualis)
			while True:
				valasz = input(txt['where_road'][nyelv])
				if check(valasz) == 1:
					y_szam = valasz[:1].upper()
					x_szam = int(valasz[-1:])
					y = oszlopok.index(y_szam)
					x = x_szam-1
					if Matrix[x][y][:4] == [0,0,0,0]:
						kepernyo_torles()
						break
					else:
						print(txt['field_used'][nyelv])
				else:
					# KÖVETKEZŐ BIRTOK MEGTEKINTÉSE
					if valasz in ['BIRTOK','birtok','FARM','farm'] and kukk[kor] == 0 and i < 5 and kor < 5:
################################################################################################################
						if iamhost == 1:
							if int(query_aktualis(game,'kov_birtok_hanyadik')) == kor+1:
								kihuzott_birtokok[kor+1] = query_aktualis(game,'kov_birtok')
							else:
								kihuzott_birtokok[kor+1] = birtokok.pop()
								upload_next_birtok(game,kor+1,kihuzott_birtokok[kor+1])

						if iamhost == 0:
							if int(query_aktualis(game,'kov_birtok_hanyadik')) == kor+1:
								kihuzott_birtokok[kor+1] = query_aktualis(game,'kov_birtok')
							else:
								kihuzott_birtokok[kor+1] = birtokok.pop()
								upload_next_birtok(game,kor+1,kihuzott_birtokok[kor+1])
################################################################################################################
						kepernyo_torles()
						eredmeny(kor)
						print(str(kor) + '. ' + txt['birtok'][nyelv] + ': ' + birtok)
						birtokrajz(kihuzott_birtokok[kor+1])
						kukk[kor] = 1

						if iamhost == 1:
							player_status(game,'hostready')   #  lehet, hogy ezt vissza kell állítani
						if iamhost == 0:
							# várjon addig, amíg elkészül a host
							player_status(game,'connectready')


						print('Várakozás a másik játékosra...',)
						if iamhost == 1:
							while 1:	#várakozás a másik játékosra
								if int(is_ready(game,'connect')) == 1:
									kepernyo_torles()
									break
								else:
									time.sleep(1)
						if iamhost == 0:
							while 1:	#várakozás a másik játékosra
								if int(is_ready(game,'host')) == 1:
									print('.')
									break
								else:
									time.sleep(1)



################################################################################################################
						# VISSZA AZ ADOTT KÖRBE
						if i < 4:
################################################################################################################
							if iamhost == 1:
								while 1:	#várakozás a másik játékosra
									if int(is_ready(game,'connect')) == 1:
										kepernyo_torles()
										break
									else:
										time.sleep(1)
							if iamhost == 0:
								while 1:	#várakozás a másik játékosra
									if int(is_ready(game,'host')) == 1:
										kepernyo_torles()
										break
									else:
										time.sleep(1)
################################################################################################################
							kepernyo_torles()
							eredmeny(kor)
							print(str(kor) + '. ' + txt['birtok'][nyelv] + ': ' + birtok)
							rajz(Matrix,oszlop,sor)
################################################################################################################
							if i <4:
								if iamhost == 1:
									kihuzott_kartya = deck.pop()
									hanyadik_kihuzott_kartya += 1
									upload_aktualis_kartya(kartya2string(kihuzott_kartya),hanyadik_kihuzott_kartya,game) # feltölti, hogy mi a következő kártya, és hogy hányadik
									while 1:
										if int(is_ready(game,'connect')) == 0:
											break
										else:
											time.sleep(1)
								if iamhost == 0:
									while 1:
										last_sorszam = int(query_aktualis(game,'kartya_hanyadik'))
										if last_sorszam > utolso_kartya_sorszama:
											kihuzott_kartya = query_aktualis(game,'kartya')
											kihuzott_kartya = string2kartya(kihuzott_kartya)
											utolso_kartya_sorszama = last_sorszam
											player_status(game,'connectunready')
											break
										else:
											time.sleep(1)
	################################################################################################################
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

								# if iamhost == 0:
								# 	player_status(game,'connectready')
								# if iamhost == 1:
								# 	player_status(game,'hostready')

								if iamhost == 0:
									player_status(game,'connectunready')
								if iamhost == 1:
									player_status(game,'hostunready')



								print(txt['kihuzott_sarga'][nyelv] + str(i))
								print(txt['points_expected'][nyelv],aktualis)
							else:
								pass
						else:
							break
					else:
						if kukk[kor] == 1 and valasz in ['BIRTOK','birtok','FARM','farm']:
							print(txt['kukk_happened'][nyelv])
						else:
							if kor == 5 and valasz in ['BIRTOK','birtok','FARM','farm']:
								print(txt['last_round'][nyelv])
							else:
								if valasz in ['EXIT','exit']:
									intro()
								else:
									print(txt['not_valid_command'][nyelv])
	# ÚT ELHELYEZÉSE A MEGADOTT KOORDINÁTÁKRA
			Matrix[x][y][:4] = kihuzott_kartya[:4]
			kepernyo_torles()
			eredmeny(kor)
			print(str(kor) + '. ' + txt['birtok'][nyelv] + ': ' + birtok)
			rajz(Matrix,oszlop,sor)

################################################################################################################
			if iamhost == 1:
				player_status(game,'hostready')
			if iamhost == 0:
				# várjon addig, amíg elkészül a host
				player_status(game,'connectready')
################################################################################################################

			print('Várakozás a másik játékosra...',)
			if iamhost == 1:
				while 1:	#várakozás a másik játékosra
					if int(is_ready(game,'connect')) == 1:
						kepernyo_torles()
						break
					else:
						time.sleep(1)
			if iamhost == 0:
				while 1:	#várakozás a másik játékosra
					if int(is_ready(game,'host')) == 1:
						kepernyo_torles()
						break
					else:
						time.sleep(1)
################################################################################################################
			kepernyo_torles()
			eredmeny(kor)
			print(str(kor) + '. ' + txt['birtok'][nyelv] + ': ' + birtok)
			rajz(Matrix,oszlop,sor)

		# EREDMÉNY MEGHATÁROZÁSA
		x=birtok_poziciok[birtok][0]
		y=birtok_poziciok[birtok][1]
		resultkor[kor] = int(zold_lanc(Matrix,x,y))+int(piros_lanc(Matrix,x,y))
		#print(result_1)

		if resultkor[kor-1] is not None:
			if (resultkor[kor] <= resultkor[kor-1]) is True:
				print(txt['not_more'][nyelv]   + ' (' + str(resultkor[kor-1]) + ')')
				resultkor[kor] = 0
				print(birtok + txt['points_cur_round'][nyelv] + str(resultkor[kor]))
			else:
				print(birtok + txt['points_cur_round'][nyelv] + str(resultkor[kor]))
		else:
			print(birtok + txt['points_cur_round'][nyelv] + str(resultkor[kor]))

		hosszkor[kor] = copy.deepcopy(len(lanc(Matrix,x,y)))
		kihuzott_birtokok[kor] = birtok
		korvege[kor] = time.time()
		if iamhost == 1:
			player_status(game,'mehet1')
		if iamhost == 0:
			player_status(game,'mehet2')
		if kor == 5:
			# teljessor('szimpla')
			# teljessorszoveggel('szimpla',txt['end'][nyelv],'kozep',1)
			# teljessorszoveggel('szimpla',txt['enter_results'][nyelv],'kozep')
			# teljessor('szimpla')
			# input('')
			# kepernyo_torles()
			if iamhost == 0:
				break
		else:
			input(txt['hit_enter'][nyelv])
			kepernyo_torles()
		if iamhost == 1:
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
	teljessorszoveggel('dupla',str(kerekitett_ido_vezeto+' s'),'jobb')
	teljessorszoveggel('szimpla',txt['results'][nyelv], 'kozep', 1)
	teljessor('dupla')
	print(kihuzott_birtokok[1] + ' '+txt['birtok'][nyelv]+':                       ' + str(resultkor[1]).zfill(2) + txt['pont'][nyelv])
	print(kihuzott_birtokok[2] + ' '+txt['birtok'][nyelv]+':                       ' + str(resultkor[2]).zfill(2) + txt['pont'][nyelv])
	print(kihuzott_birtokok[3] + ' '+txt['birtok'][nyelv]+':                       ' + str(resultkor[3]).zfill(2) + txt['pont'][nyelv])
	print(kihuzott_birtokok[4] + ' '+txt['birtok'][nyelv]+':                       ' + str(resultkor[4]).zfill(2) + txt['pont'][nyelv])
	print(kihuzott_birtokok[5] + ' '+txt['birtok'][nyelv]+':                       ' + str(resultkor[5]).zfill(2) + txt['pont'][nyelv])
	teljessor('szimpla')
	osszes_birtok = resultkor[1]+resultkor[2]+resultkor[3]+resultkor[4]+resultkor[5]
	print(txt['every_birtok'][nyelv]+'               ' + str(osszes_birtok).zfill(3) + txt['pont'][nyelv])#Összesen
	teljessor('szimpla')
	zold_var = zold_lanc(Matrix,0,5)
	hossz_zold = len(lanc(Matrix,0,5))
	print(txt['green_castle'][nyelv]+'                 ' + str(zold_var).zfill(2) + txt['pont'][nyelv])# plusz a zöld vár
	piros_var = piros_lanc(Matrix,6,0)
	hossz_piros = len(lanc(Matrix,6,0))
	print(txt['red_castle'][nyelv]+'                ' + str(piros_var).zfill(2) + txt['pont'][nyelv])# plusz a piros vár
	teljessor('szimpla')
	nullasok = [resultkor[1],resultkor[2],resultkor[3],resultkor[4],resultkor[5]].count(0)*(-5)
	print(txt['zero_point_rounds'][nyelv]+' (' + str([resultkor[1],resultkor[2],resultkor[3],resultkor[4],resultkor[5]].count(0))+ txt['db'][nyelv] + '):   ' + str(nullasok).zfill(2) + txt['pont'][nyelv])# mínusz 5*(nullás várak)
	teljessor('dupla')
	grand_total = osszes_birtok + zold_var + piros_var + nullasok # grand total
	print(txt['total'][nyelv]+'                    ' + str(grand_total).zfill(3) + txt['pont'][nyelv]+' - ' + szoveges_ertekeles(grand_total,nyelv))
	teljessor('dupla')
	# send_results_net(kihuzott_birtokok[1], resultkor[1], kihuzott_birtokok[2], resultkor[2], kihuzott_birtokok[3], resultkor[3], kihuzott_birtokok[4], resultkor[4], kihuzott_birtokok[5], resultkor[5], piros_var, zold_var, nullasok, grand_total, kerekitett_ido, koridok[1], koridok[2], koridok[3], koridok[4], koridok[5], hosszkor[1], hosszkor[2], hosszkor[3], hosszkor[4], hosszkor[5], hossz_zold, hossz_piros, mac, matrix_up,game)
	send_results_net(kihuzott_birtokok[1], resultkor[1], kihuzott_birtokok[2], resultkor[2], kihuzott_birtokok[3], resultkor[3], kihuzott_birtokok[4], resultkor[4], kihuzott_birtokok[5], resultkor[5], piros_var, zold_var, nullasok, grand_total, kerekitett_ido, koridok[1], koridok[2], koridok[3], koridok[4], koridok[5], hosszkor[1], hosszkor[2], hosszkor[3], hosszkor[4], hosszkor[5], hossz_zold, hossz_piros, mac, matrix_up,game)
	if query_nick(mac) == '' or None:
		teljessorszoveggel('ures',txt['add_nick'][nyelv],'kozep')
		a = ''
		nick = input(a.center(int(ydim/2)))
		send_nick(mac, nick)
		send_settings(mac, nyelv, zene, szinek)
	else:
		print(txt['hit_enter'][nyelv])
		input('')
	kepernyo_torles()
	sajatpont = int(grand_total)
	ellenfelpont = int(multi_results(game,mac))
	print('Saját pontszám: ' + str(grand_total))
	print('Ellenfél pontszáma: ' + str(multi_results(game,mac)))
	teljessor('ures',5)
	if sajatpont > ellenfelpont:
		teljessorszoveggel('dupla','Gratulálunk! Nyertél.','kozep')
	elif sajatpont < ellenfelpont:
		teljessorszoveggel('dupla','Sajnáljuk! Vesztettél.','kozep')
	else:
		teljessorszoveggel('dupla','Döntetlen.','kozep')
	teljessor('ures',2)
	print(txt['hit_enter'][nyelv])
	input('')
	intro()

##############################################################################
##### START
##############################################################################

kihuzott_birtokok = [None, None, None, None, None, None]
resultkor = [None, None, None, None, None, None]
intro()
