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
import threading
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

movie_timestamp=0

full_screen_mode='N'
#__CLOUDBOOK:NONSHARED__
unique_id=10 # non shared value for agent_ids. starts at 10 for clarity
frame_number=-1000



"""
def silent_th(num):
	if not hasattr(silent_th,"counter"):
		silent_th.counter=0 
	
	#print ("hola", num, silent_th.counter)
	if (num==silent_th.counter+1):
		silent_th.counter=silent_th.counter+1
		print ("th:",num)
		t = threading.Timer(3.0, silent_th,[num+1])
		t.start()
"""
# ==========================================================================================
# MAIN function always falls into Agent0
#__CLOUDBOOK:MAIN__
def main():
	global size
	global videowall_dict
	global full_screen_mode

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
	
	fs=input ("full screen?[N]:")
	if fs=="Y":
		full_screen_mode='Y'
	else:	
		full_screen_mode='N'

	#creation of image test
	#image_test="./lena_portions/lena_256_"+str(size)+"x"+str(size)+".bmp"
	image_test="./images/kodim15.bmp"

	# assign a portion to each machine invoking all
	# ----------------------------------------------
	for i in range(0,size*size):
		parallel_set_portion_and_unique_ID(i,i+10) # this is a parallel function invoked on all agents	
	#__CLOUDBOOK:SYNC__

	print ("videowall dictionary after assigning portions:")
	vd=refresh_videowall_dict()
	print ("videowall_dict ", vd)
	print ("starting show...")

	#launch visualization of image_test in all machines
	for i in range(size*size):
		print ("invocando", i)
		parallel_show_image(image_test, size,"create",full=full_screen_mode)
	#__CLOUDBOOK:SYNC__
	
	# This is a random reorder for testing purposes
	# ---------------------------------------------
	#for i in range(0,4):
	#	non_interactive_reorder(random.randint(0,size*size-1),random.randint(0,size*size-1))
		
	# now is time to re-order the screens
	# ---------------------------------------------
	print ("entering in interactive reorder?[Y|N]")
	ir=input ("")
	if ir ==("Y"):
		interactive_reorder()
	

	# It is time to start the show
	# ---------------------------
	main_videowall_menu()


# ==========================================================================================
#__CLOUDBOOK:DU0__
def interactive_reorder():
	global size
	global videowall_dict

	vd=videowall_dict

	#image_test="./lena_portions/lena_256_"+str(size)+"x"+str(size)+".bmp"
	image_test="./images/kodim15.bmp"
	print ("loading test image...please wait")
	for i in range(size*size):
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
			for a in vd:
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

		#image_test="./lena_portions/lena_256_"+str(size)+"x"+str(size)+".bmp"
		image_test="./images/kodim15.bmp"
		for i in range(size*size):
			parallel_show_image(image_test,size,"reload_image")
		vd=refresh_videowall_dict()
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
	
	for i in range(0,size*size-1):
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
	unique_id=str(token)
	videowall_dict[unique_id]=portion
	
# ==========================================================================================
#__CLOUDBOOK:PARALLEL__
def parallel_show_image(filename,size,op, timestamp=None, mute=True, divergence=None, force='N',full='N'):
	global videowall_dict
	global unique_id
	global frame_duration
	global videowall_time
	#global frame_number
	global movie_timestamp

	

	val=0
	#print (" agent ", unique_id, " entra en show image TS:", timestamp)

	#__CLOUDBOOK:BEGINREMOVE__  
	# -------------------------------
	unique_id=int(unique_id)
	unique_id+=1
	if (unique_id==size*size+10):
		unique_id=10
	unique_id=str(unique_id)
	#__CLOUDBOOK:ENDREMOVE__
	
	
	# comprobamos si nos han invocado ya
	# en modo no cloudbook no tiene sentido ojo.
	"""
	if (frame!=None and op=="next_frame"):
		if (frame_number==frame*unique_id):
			print ("invocado ya ",unique_id, frame_number, frame)
			return
		else:
			frame_number=frame
	"""
	#print (videowall_dict)
	my_portion=videowall_dict[str(unique_id)]
	#print ("I am agent:",unique_id,"showing portion: ",my_portion)
	t,val=simpleMedia.show(filename,my_portion,size,op,unique_id, timestamp,mute,divergence, force,full)
	#print ("agent", unique_id, "val is ",val, "t is ",t)
	if (t!=0):
		videowall_time[str(unique_id)]=t
		# el movietimestamp deberia ser el minimo pero cojo el max
		# de lo contrario la pelicula va mas despacio pues puede coger a un pausado
		# en live video curiosamente debe ser al reves
		# estrategia MIN: hay que pausar a los adelantados 
		# estrategia MAX: hay que pasar mas fps en los atrasados
		movie_timestamp=min(movie_timestamp,t) 

	#if val!=0:
		#print ("hey", val, "   framedur:",frame_duration)
	try:
		#val puede ser un string, como "eof" o "pause"
		frame_duration=max(val, frame_duration) # biggest of all screens ( each frame starts at -1)

	except:
		#estamos en pause o eof
		if val=='eof':
			frame_duration=1000000
		else: # pause 
			frame_duration=0

	#else:
	#	pass
		#print ("hey0", val, "   framedur:",frame_duration)
		
	#print (" agent ", unique_id, " sale de show image TS:", timestamp)

# ==========================================================================================
#__CLOUDBOOK:DU0__
def interactive_play_single_image():
	global size
	global full_screen_mode

	filename=input ("image filename?[./images/kodim23.bmp]:")
	if (filename==""):
		filename="./images/kodim23.bmp"
	for i in range(size*size):
		#debe ser create pues la ultima imagen puede tener otro tamaño
		parallel_show_image(filename, size,"create", full=full_screen_mode)
		
# ==========================================================================================
#__CLOUDBOOK:LOCAL__
def refresh_videowall_time():
	global videowall_time
	x=videowall_time
	return x
# ==========================================================================================
#__CLOUDBOOK:LOCAL__
def refresh_videowall_dict():
	global videowall_dict
	x=videowall_dict
	return x
#__CLOUDBOOK:LOCAL__
def refresh_frame_duration():
	global frame_duration
	x=frame_duration
	return x
#__CLOUDBOOK:LOCAL__
def refresh_movie_timestamp():
	global movie_timestamp
	x=movie_timestamp
	return x
# ==========================================================================================

#__CLOUDBOOK:DU0__
def interactive_play_video():
	global global_timestamp
	global frame_duration
	global size
	global videowall_time
	global movie_timestamp # es global
	global full_screen_mode


	vt=videowall_time
	fd=frame_duration
	movie_timestamp=0
	mt=movie_timestamp

	divergencia=0
	#last_timestamp=

	t0=0;

	print ("for playing a filename :")
	print ("   example: ./videos/friends.mp4")
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

	# esta linea la he puesto por precaucion pero no sirve de nada
	#__CLOUDBOOK:SYNC:1__
	if (filename==""):
		#filename="https://www.radiantmediaplayer.com/media/bbb-360p.mp4"
		filename="./videos/toystory.mp4"

	while (not	os.path.exists(filename) and ':' not in filename):
		print ("ERROR: file not exists")
		filename=input ("video filename?:")
		if (filename==''):
			filename="./videos/toystory.mp4"

	# this SDL init and window creation is mandatory to read keyboard
	SDL_Init(0)
	# esta ventana es un truco para poder capturar los eventos nuevos de teclado.
	# si no creo una ventana y le doy foco, captare indefinidamente los eventos de la ultima ventana cerrada
	# y si he puslsado stop, captare indefinidamente la tecla S
	keyb_window=SDL_CreateWindow(b"KEYBOARD",1000,600,100,100, SDL_WINDOW_SHOWN|SDL_WINDOW_INPUT_FOCUS)	
	SDL_SetWindowInputFocus(keyb_window)
	SDL_DestroyWindow(keyb_window)

	my_event = SDL_Event()
	

	mute= True #False # only the first agent will sound
	fulls=full_screen_mode
	for i in range(size*size):
		print ("Invoking playvideo on agent ", i)
		# la ultima imagen mostrada ( en otro video o foto) puede tener otro tamaño, 
		# de modo que hay que recrear cada window

		parallel_show_image(filename, size,"play_video",mute=mute, full=fulls)
		mute=True

	print ("waiting for sync...")
	#__CLOUDBOOK:SYNC:__
	print ("...sync ALL agents :OK")
	

	time.sleep(1)	
	print (" at any time during show you may press P:PAUSE, C:CONTINUE, S:STOP")
	
	# voy a dar tiempo a que se inicien todos los agentes antes de preguntar
	time.sleep(3)	
	forcesync=input ("force sync video (for LIVE videos consider both options)?:[Y]")
	if forcesync=="":
		forcesync="Y"

	
	

	input("start? (press ENTER)")

	
	print ("deactivating pause...")
	for i in range(size*size):
		print ("invoking agent ", i)
		parallel_show_image(filename, size,"continue") 
	#__CLOUDBOOK:SYNC__
	print ("...pause quit OK")
	k=0
	cosa=0
	

	frame_duration=0.025 # para empezar
	fd=frame_duration
	last_fd=fd
	#fd=refresh_frame_duration()
	after=time.time()

	
	
	pause=False
	stop=False
	invocaciones=0
	keystatus=[]
	while (True):	

		
		


		try:
			SDL_PollEvent(ctypes.byref(my_event)) 
			keystatus = SDL_GetKeyboardState(None)
		except:
			print ("excepcion evento")
			pass
		#keystatus = SDL_GetKeyboardState(None)
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
			print("the S key (STOP) was pressed", keystatus[SDL_SCANCODE_S])
			for i in range(size*size):
				parallel_show_image(filename, size,"stop") 
				stop=True
		elif keystatus[SDL_SCANCODE_F]:
			print("the F key (full screen) was pressed")
			for i in range(size*size):
				parallel_show_image(filename, size,"pause") 
				pause=True

			for i in range(size*size):
				parallel_show_image(filename, size,"fullscreen") 
			#__CLOUDBOOK:SYNC__	
		
		if stop:
			#SDL_DestroyWindow(keyb_window)
			#SDL_Quit()
			return

		if pause:
			continue


		#muestra el next frame, y envia el global_timestamp

		last_mt=mt
		
		mt=refresh_movie_timestamp()
		if mt==0:
			mt=last_mt
		
		movie_timestamp=mt + 100000 # asi se escoge el menor

		#print ("movie ts:",mt)
		#if (k %2 ==0):
		for i in range(size*size):
			# los show images se autopausan si van mas de 250 ms adelantados
			# en caso de video LIVE se autopausan con solo 70 ms de adelanto  
			# por eso les paso el movie_timestamp
			#print ("invocando agente ", i)
			#parallel_show_image(filename, size,"next_frame",timestamp=mt, divergence=divergencia, force=forcesync)	
			parallel_show_image(filename, size,"next_30_frames",timestamp=mt+2000, divergence=divergencia, force=forcesync)	
		#print ("waiting sync after next frame")
		#__CLOUDBOOK:SYNC__
		#print ("sync ok")
		
		#print ("antes de refresh")
		fd=refresh_frame_duration()
		#print ("despues fd:",fd)
		if (fd==-1):
			print ("warning, all agents are in pause")
			fd=last_fd

		if (fd==1000000): # eof de algun player
			print ("automatic stop. EOF \n")
			for i in range(size*size):
				parallel_show_image(filename, size,"stop") 
			#SDL_DestroyWindow(keyb_window)
			SDL_Quit()
			return


		#el master es el mas retrasado
		#print ("k:",k)

		invocaciones=invocaciones+1
		k=k+1  #al comentar esta linea NUNCA ENTRO EN SYNC
		k=40 # con esta asignacion SIEMPRE ENTRA, ( grano =30 frames)
		if k==40: # asi entro cada 30 frames
			#print ("k:", k, "\n")
			k=10 #10 =asi entro cada 30 frames
			
			# el ultimo agente creado es el que va mas retrasado (en principio)
			agente=10+(size*size-1)
			slowest=agente
			fastest=agente

			# el ultimo agente es el que va mas retrasado
			paused=False
			vt=refresh_videowall_time() # se ejecuta cada 30 frames

			if str(agente) in vt: # esto siempre es true
				#print ("encontrado")
				mint=vt[str(agente)]
				maxt=vt[str(agente)]
				for i in range(10, 10+size*size-1):
					#print ("checking ", i, "  -> ",videowall_time[i])
					if (vt[str(i)] is not None and mint is not None):
						if (vt[str(i)]<mint):
							mint=vt[str(i)]
							slowest=i
						elif (vt[str(i)]>maxt):
							maxt=vt[str(i)]
							fastest=i
				#print ("---------------- SYNC CONTROL --------------------")	
				#print ("slowest is ", slowest, "at portion ", videowall_dict[slowest]," time:", mint)
				#print ("fastest is ", fastest, "at portion ", videowall_dict[fastest]," time:", maxt)
				
				#print (videowall_dict)
				#print ("FRAME DURATION:", frame_duration)
				
				#movie_timestamp=mint
				movie_timestamp=mint
				#movie_timestamp=mt
				mt=mint
				
				divergencia=maxt-mint
				#print ("mint :", mint, "  mt:", mt)
				#print ("\n")
				#print ("SYNC CTRL: invocations", invocaciones, " Divergence:", int((maxt-mint)*1000)," ms", " TS:",mt, " maxTS:", maxt, "FD:",int(fd*1000),"  ",end='\r', flush=True) #, " margin", margen)
				print ("SYNC CTRL: invocations", invocaciones, " Divergence:", int((maxt-mint)*1000)," ms", " TS:",mt)
				#esto pausa a los mas adelantados durante este frame
				#----------------------------------------------------
				#if (divergencia>0.04 ): # >1 frame pues 1frame =0.033
				if (divergencia>=0.03 ): # >1 frame pues 1frame =0.033
				#if (divergencia>0.03 ): # >1 frame pues 1frame =0.033
					#print ("pausing...")
					#print ("speedup..")
					k=30 # la proxima vez entra antes
					# solo una llamada, para no retrasar todo pues esto es costoso
					#for i in range(size*size):
						#pause if esta adelantado respecto timestamp
						#parallel_show_image(filename, size,"sync", timestamp=mint)
						#acelera si va retrasado
					if (forcesync=="Y"):
						parallel_show_image(filename, size,"sync", timestamp=mint, divergence=divergencia)
							#pass
						#print ("i:",i)
					#print ("waiting SYNC after players-sync")
					#__CLOUDBOOK:SYNC:__
		

		now=time.time()
		margen=now-after
		#print ("FD ",fd ," ms", "  consumo:", margen)
		#print ("  30 frames processed)
		fd=fd-margen
		if (fd<=0.00):
			fd=0.00
		#print ("sleeping ",fd ," ms")	
		fd=0
		time.sleep(fd)
		after=time.time();
		last_fd=fd
		#global_timestamp=global_timestamp+fd
		frame_duration=-1 # new frame
		fd=-1 	

		
# ==========================================================================================
#__CLOUDBOOK:DU0__
def interactive_play_directory():
	global size
	global full_screen_mode

	path=input ("directory name?: [default =images]")
	if (path==""):
		path="./images"
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
			parallel_show_image(filename, size,"create",full=full_screen_mode) # MUST BE CREATE. image can change size
		command=input ("command?:")
		if command=="x" :
			break
		

#===========================================================================================	
#__CLOUDBOOK:DU0__
def main_videowall_menu():
	global full_screen_mode

	while (True):		
		#os.system('cls')  # on windows
		print("")
		print ("main menu options")
		print ("=================")
		print (" r: reorder screens")
		print (" i: play image from a single file")
		print (" d: play images from a directory")
		print (" v: play video ( file , url or LIVE)")
		print (" f: set full screen")
		print (" w: set windowed mode")
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
		elif (command=="f"):
			full_screen_mode='Y'
			print ("full screen mode set")
		elif (command=="w"):
			full_screen_mode='N'
			print ("window mode set")


#===========================================================================================	
#__CLOUDBOOK:DU0__
def du0_print(cad):
	print (cad)



#silent_th(1)

main()
