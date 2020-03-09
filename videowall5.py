# VIDEOWALL program Description
# ========================================================================================================
# IMPORTANT: this program has a section at parallel_show_image() to be removed befor cloudbook make
# The section has testing purposes in non-cloudbook version
#
#                   ------ program description ------
# this program uses NONSHARED variables mechanism to asign a token to each different agent
# each token identifies univocally each agent. once the token is asigned to an agent, it must not change 
# a dicctionaty matches agents with portions. portions are exchanged to order the whole image/video
# interactive functions fall in Agent0 as well as main() funcion.
# rest of agents only will execute 2 fuctions: parallel_set_portion_and_unique_ID() , parallel_show_image()
# It means that DU_default will contain only these 2 functions.
# this programs offers help at program launching and shows detailed options and menus (easy to use)
# ========================================================================================================
import os

#os.environ["PYSDL2_DLL_PATH"]="."+os.sep+"sdl2_library"
from ffpyplayer.player import MediaPlayer
import ffpyplayer
import sys
from ctypes import create_string_buffer
import ctypes

from sdl2 import *


import time
from simpleMedia import simpleMedia
import random
from glob import glob
#======================= GLOBAL VARS  =====================================================
#__CLOUDBOOK:GLOBAL__

# image for re-ordering purposes. show a list of numbers. one per agent
image_test="" 

# matches agentID with screens
videowall_dict={}

# counter to be assigned to each agent
portion_counter=0

# size of the side of the videowall. A 16 screens size is 4
size=0

# sync dictionary
videowall_time={}

frame_duration=0
global_timestamp=0


#__CLOUDBOOK:NONSHARED__
unique_id=10 # non shared value for agent_ids. starts at 10 for clarity


# ==========================================================================================
# MAIN function always falls into Agent0
#__CLOUDBOOK:MAIN__
def main():
	global size
	global videowall_dict
	os.system('cls')  # on windows
	#########################################
	#main program to execute by command line
	#=======================================
	print (" ")
	print (" ")
	print ("Welcome to videowall  (V1.1)")
	print ("============================")
	text=input ("number of screens in row?:")
	
	
	size=int(text)
	#global size

	#creation of image test
	image_test="./lena_portions/lena_256_"+str(size)+"x"+str(size)+".bmp"
	#image_test="lena_256_3x3.bmp"
	# assign a portion to each machine invoking all
	# ----------------------------------------------
	for i in range(0,size*size):
		parallel_set_portion_and_unique_ID(i,i+10) # this is a parallel function invoked on all agents
	#launch visualization of image_test in all machines

	#__CLOUDBOOK:SYNC__

	print ("videowall dictionary after assigning portions:")
	print (videowall_dict)
	print ("starting show...")

	
	for i in range(0,size*size):
		parallel_show_image(image_test, size,"create")	

	#__CLOUDBOOK:SYNC__
	
	# This is a random reorder for testing purposes
	# ---------------------------------------------
	#for i in range(0,4):
	#	non_interactive_reorder(random.randint(0,size*size-1),random.randint(0,size*size-1))
		
	# now is time to re-order the screens
	print ("entering in interactive reorder...")
	interactive_reorder()
	#it is time to start the show
	main_videowall_menu()


# ==========================================================================================
#__CLOUDBOOK:DU0__
def interactive_reorder():
	global size
	global videowall_dict

	image_test="./lena_portions/lena_256_"+str(size)+"x"+str(size)+".bmp"
	for i in range(0,size*size):
		parallel_show_image(image_test,size,"create")

	#__CLOUDBOOK:SYNC__

	print ("Interactive Screen Reordering")
	print ("-----------------------------")
	print (" c : exchange 2 screens")
	print (" r : random reorder")
	print (" x : exit")
	command=input ("command?(c|x):")
	while (command!="x"):
		if (command=="c"):
			portion_a=int(input ("screen A?:"))
			portion_b=int(input ("screen B?:"))
			print ("a=",portion_a,"b=",portion_b)
			#look for screens at agent_dict
			print (portion_a, portion_b)
			for a in videowall_dict:
				#print ("agent=",a, videowall_dict[a])
				if videowall_dict[a]==portion_a:
					#print ("found a")
					agent_a=a
					for b in videowall_dict:
						if videowall_dict[str(b)]==portion_b:
							#print ("found b")
							agent_b = b
							break
					break
			videowall_dict[str(agent_a)]=portion_b
			videowall_dict[str(agent_b)]=portion_a

		elif (command=="r"):
			for i in range(0,4):
				non_interactive_reorder(random.randint(0,size*size-1),random.randint(0,size*size-1))

		image_test="./lena_portions/lena_256_"+str(size)+"x"+str(size)+".bmp"
	
		for i in range(0,size*size):
			parallel_show_image(image_test,size,"reload_image")
		#__CLOUDBOOK:SYNC__

		#next command
		command=input ("command?(c|x):")

# ==========================================================================================
#__CLOUDBOOK:DU0__
def non_interactive_reorder(portion_a, portion_b):
	global videowall_dict
	global size		
	#look for screens at agent_dict

	print (portion_a, portion_b)
	for a in videowall_dict:
		#print ("agent=",a, videowall_dict[a])
		if videowall_dict[str(a)]==portion_a:
			#print ("found a")
			agent_a=a
			for b in videowall_dict:
				if videowall_dict[str(b)]==portion_b:
					#print ("found b")
					agent_b = b
					break
			break
	videowall_dict[str(agent_a)]=portion_b
	videowall_dict[str(agent_b)]=portion_a
	
	#image_test="lena_256_3x3.bmp"
	image_test="./lena_portions/lena_256_"+str(size)+"x"+str(size)+".bmp"
	
	for i in range(0,size*size):
		parallel_show_image(image_test,size,"reload_image")
	#__CLOUDBOOK:SYNC__

		
# ==========================================================================================
# esta funcion la va a ejecutar cada una de los agentes, invocada desde main() en agent0
# al invocarla sobre un agente cualquiera, se le asigna porcion y token y se almacena en el diccionario
# como un par (token, porcion). El token asigna univocamente a un agente.
# Una vez asignado, el token no se le debe cambiar al agente pero la porcion se le puede cambiar
#__CLOUDBOOK:PARALLEL__
def parallel_set_portion_and_unique_ID(portion, token):
	global unique_id
	global videowall_dict
	unique_id=token
	videowall_dict[str(unique_id)]=portion
	
# ==========================================================================================
#__CLOUDBOOK:PARALLEL__
def parallel_show_image(filename,size,op, timestamp=None, mute=True):
	global videowall_dict
	global unique_id
	global frame_duration
	
	val=0

	#__CLOUDBOOK:BEGINREMOVE__  
	# -------------------------------
	unique_id+=1
	if (unique_id==size*size+10):
		unique_id=10
	#__CLOUDBOOK:ENDREMOVE__
	
	
	#print (videowall_dict)
	my_portion=videowall_dict[str(unique_id)]
	#print ("I am agent:",unique_id,"showing portion: ",my_portion)
	t,val=simpleMedia.show(filename,my_portion,size,op,unique_id, timestamp,mute=mute)
	if (t!=0):
		videowall_time[str(unique_id)]=t

	if val!=0:
		frame_duration=max(val, frame_duration) # biggest of all screens ( each frame starts at 0)
	
# ==========================================================================================
#__CLOUDBOOK:DU0__
def interactive_play_single_image():
	filename=input ("image filename?:")
	for i in range(0,size*size):
		#debe ser create pues la ultima imagen puede tener otro tamaño
		parallel_show_image(filename, size,"create")
# ==========================================================================================
#__CLOUDBOOK:DU0__
def interactive_play_video():
	global global_timestamp
	global frame_duration

	print ("for playing a filename :")
	print ("   example: videos/friends.mp4")
	print (" ")
	print ("for playing a url (LIVE or not)")
	print( "   example1: https://www.radiantmediaplayer.com/media/bbb-360p.mp4") 
	print ("   example2: http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/Sintel.mp4")
	print ("")
	print ("for LIVE video:")
	print ("   you may use a multicast live video (such as OBS tool custom streaming):")
	print ("     example: udp://224.0.0.1:9999  with container mpegts configured at server")
	print ("     VLC player also is valid as streaming server but remenber:")
	print ("         - VLC config:")
	print ("              > configure VLC with UDP as protocol and IP of this computer as destination")
	print ("              > configure h264+mp3 with MP4/MOV container (faster)")
	print ("              > or configure MPEG2+MPGA with TS container (more delay)")
	print ("         - This application : use udp://<IP_vlc_computer>:port")
	
	
	
	
	
	print ("")
	print ("for LIVE you may use also a url from a LIVE streaming http service ")
	print ("   you may found urls at https://www.jwplayer.com/developers/web-player-demos/live-streaming/")
	print ("    such as https://wowzaec2demo.streamlock.net/live/bigbuckbunny/playlist.m3u8")
	filename=input ("video filename?:")
	if (filename==""):
		#filename="https://www.radiantmediaplayer.com/media/bbb-360p.mp4"
		filename="videos/toystory.mp4"


	# this SDL init and window creation is mandatory to read keyboard
	SDL_Init(0)
	keyb_window=SDL_CreateWindow(b"KEYBOARD",1000,600,100,100, SDL_WINDOW_SHOWN|SDL_WINDOW_INPUT_FOCUS)	
	my_event = SDL_Event()
	

	mute= False # only the first will sound
	for i in range(size*size):
		# la ultima imagen mostrada ( en otro video o foto) puede tener otro tamaño, 
		# de modo que hay que recrear cada window
		parallel_show_image(filename, size,"play_video",mute=mute)
		mute=True


	
	time.sleep(1)	
	print (" at any time during show you may press P:PAUSE, C:CONTINUE, S:STOP")
	input("start? (press ENTER)")

	

	# toggle ALL pause quickly at same time
	for i in range(size*size):
		parallel_show_image(filename, size,"togglepause") 

	k=0
	cosa=0
	

	frame_duration=0.025 # para empezar
	after=time.time()

	
	
	pause=False
	stop=False

	while (True):	
		try:
			SDL_PollEvent(ctypes.byref(my_event)) 
		except:
			pass
		keystatus = SDL_GetKeyboardState(None)
		if keystatus[SDL_SCANCODE_P]:
			if pause==False:
				print("the P key (PAUSE) was pressed")
				for i in range(size*size):
					parallel_show_image(filename, size,"pause") 
				pause=True
		elif keystatus[SDL_SCANCODE_C]:
			if pause:
				print("the C key (CONTINUE) was pressed")
				k=38 # para sincronizar asap
				after=time.time();
				pause=False
		elif keystatus[SDL_SCANCODE_S]:
			print("the S key (STOP) was pressed")
			for i in range(size*size):
				parallel_show_image(filename, size,"stop") 
				stop=True
		if stop:
			SDL_DestroyWindow(keyb_window)
			SDL_Quit()
			return

		if pause:
			continue


		#muestra un frame
		for i in range(size*size):
			parallel_show_image(filename, size,"next_frame",global_timestamp)	
		
		#chequea sincronizacion y pausa los mas adelantados respecto del master
		#el master es el mas retrasado
		k=k+1
		if k==40: # asi es cada 30 frames
			k=10
			#print (videowall_time)
			agente=10+(size*size-1)
			slowest=agente
			fastest=agente
			#print ("buscando ", agente)
			paused=False
			if str(agente) in videowall_time:
				mint=videowall_time[str(agente)]
				maxt=videowall_time[str(agente)]
				for i in range(10, 10+size*size-1):
					#print ("checking ", i, "  -> ",videowall_time[i])
					if (videowall_time[str(i)] is not None and mint is not None):
						if (videowall_time[str(i)]<mint):
							mint=videowall_time[str(i)]
							slowest=i
						elif (videowall_time[str(i)]>maxt):
							maxt=videowall_time[str(i)]
							fastest=i
				#print ("---------------- SYNC CONTROL --------------------")	
				#print ("slowest is ", slowest, "at portion ", videowall_dict[slowest]," time:", mint)
				#print ("fastest is ", fastest, "at portion ", videowall_dict[fastest]," time:", maxt)
				
				#print (videowall_dict)
				#print ("FRAME DURATION:", frame_duration)
				divergence=maxt-mint
				
				global_timestamp=mint
				print ("SYNC CTRL: Current Divergence:", int((maxt-mint)*1000)," ms", " TS:",global_timestamp,end='\r', flush=True) #, " margin", margen)

				#esto pausa a los mas adelantados
				#---------------------------------
				if (divergence>0.03 ):
					for i in range(size*size-1):
						parallel_show_image(filename, size,"sync", timestamp=mint)
		
		now=time.time()
		margen=now-after
		frame_duration=frame_duration-margen
		if (frame_duration<=0.0):
			frame_duration=0.0 
		time.sleep(frame_duration)
		after=time.time();
		frame_duration=-1 # new frame 	
		
# ==========================================================================================
#__CLOUDBOOK:DU0__
def interactive_play_directory():
	path=input ("directory name?: [default =images]")
	if (path==""):
		path="images"
	files=[]
	spath=path + os.sep+"*.jpeg"
	files=glob(spath)
	spath=path + os.sep+"*.jpg"
	files+=glob(spath)
	spath=path + os.sep+"*.bmp"
	files+=glob(spath)
	spath=path + os.sep+"*.png"
	files+=glob(spath)

	print ("files:", files)
	for filename in files:		
		for i in range(0,size*size):
			#debe ser create pues la ultima imagen puede tener otro tamaño
			parallel_show_image(filename, size,"create")
		command=input ("command?:")
		if command=="x" :
			break
		

#===========================================================================================	
#__CLOUDBOOK:DU0__
def main_videowall_menu():

	while (True):		
		#os.system('cls')  # on windows
		print("")
		print ("main menu options")
		print ("=================")
		print (" r: reorder screens")
		print (" i: play image from a single file")
		print (" d: play images from a directory")
		print (" v: play video ( file , url or LIVE)")
		print (" x: exit")
		
		command=input ("command?:")
		if (command=="r"):
			interactive_reorder()
		elif (command=="x"):
			sys.exit()
		elif (command=="i"):
			interactive_play_single_image()
		elif (command=="v"):
			interactive_play_video()
		elif (command=="l"):
			interactive_play_streaming()
		elif (command=="d"):
			interactive_play_directory()
#===========================================================================================	

main()