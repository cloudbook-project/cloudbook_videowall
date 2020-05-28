
from ffpyplayer.player import MediaPlayer
import ffpyplayer
import sys
from ctypes import create_string_buffer
import ctypes
from sdl2 import *
import time
import sdl2.ext

import threading

				
from ctypes import *

#para obtener la resolucion del modo de video uso tkinter, que es multi O.S
import tkinter 

#def duerme():
#	time.sleep(5)
#kk=0

def get_screen_resolution():
	root = tkinter.Tk()
	screen_width = root.winfo_screenwidth()
	screen_height = root.winfo_screenheight()
	root.destroy()
	return screen_width,screen_height




	
def create_permanent_window_th(agentID,x,y,ancho,alto,flags):
	try:
		SDL_PollEvent(ctypes.byref(show.event))
		print ("intentando", agentID)
		show.window[agentID] = None
		cad=str(agentID)
		cad=cad.encode('utf8') 
		show.window[agentID] = SDL_CreateWindow(cad,x+1,y+1,ancho,alto,flags)
		#show.window[agentID] = SDL_CreateWindow(cad,x,y,ancho,alto,flags)
		print ("ok", agentID)
	except:
		print("joder")
	#print("hello")
	#t=threading.Timer(1,create_permanent_window_th, args=(agentID,x,y,ancho,alto,flags))
	#t.start()
	#time.sleep(1)	
	#while True:
	show.last_th[agentID]=show.thID[agentID]
	while show.thID[agentID]==show.last_th[agentID]: #True: #SDL_WasInit(SDL_INIT_EVENTS): #True: #show.window[agentID]!=None:
		#print ("last:",last_th, "  current:",show.thID[agentID] )
		try:
			SDL_PollEvent(ctypes.byref(show.event)) 
		except:
			return # window closed?
			pass
		time.sleep(0.5)	
	print ("closing ", agentID, "  last:",show.last_th[agentID], "  current:",show.thID[agentID] )
		
def silent_th(agentID,x,y,ancho,alto,flags):
	#t = threading.Timer(3.0, create_permanent_window_th(),[title,x,y,ancho,alto,flags])
	print ("HEY ", agentID)
	t=threading.Thread(target=create_permanent_window_th, args=(agentID,x,y,ancho,alto,flags), daemon=True)
	#t=threading.Timer(1,create_permanent_window_th, args=(agentID,x,y,ancho,alto,flags))
	t.start()
	
	
	#SDL_CreateThread(create_permanent_window_th,"kk", ctypes.cvoid_p(agentID,x,y,ancho,alto,flags)) 
	#para asegurar que la ventana esta creada, nos dormimos un poco
	counter=0
	while (show.window[agentID] ==None):
		print ("silent th ", agentID, "  waiting creation")
		time.sleep(0.5)
		counter+=1
		if counter ==10:
			return False

	return True


#__CLOUDBOOK:LOCAL__
def show(filename, portion,size,op,agentID, timestamp=None, mute=True, divergence=None, force='N',full_screen='N'):
	if not hasattr(show,"player"):
		show.player={}
		show.window={}
		show.windowsurface={}
		SDL_Init(0)
		show.img=None
		show.event = SDL_Event()
		SDL_PollEvent(ctypes.byref(show.event)) 
		
		show.ancho=0
		show.alto=0
		show.ancho_porcion=0;
		show.alto_porcion=0;
		show.r={} 
		show.r_dest={} 
		show.render={}
		show.time={}
		show.last_time={}

		#show.portion=0
		show.filename=""

		#show.glcontext={} # esto no se usa
		show.last_paused_at={}

		show.thID={}
		show.last_th={}

	if agentID not in show.thID:
			show.thID[agentID]=0	

	if op=="create":
	#------------------------------------------------------
		#SDL_PollEvent(ctypes.byref(show.event)) 
		#not hasattr(show,"player"):

		
		try:
			if (agentID in show.windowsurface and show.windowsurface[agentID]!=None):
				SDL_FreeSurface(show.windowsurface[agentID])
				print ("agent:",agentID," free surface OK")
		except Exception as e:
			print ("ALERT: agent ", agentID, "failed at create free surface ", e)
		
		try:
			if 	(agentID in show.window) : # and show.window[agentID]!=None):
				SDL_DestroyWindow(show.window[agentID])
				print ("agent:",agentID, " free window OK")
		except Exception as e:
			print ("ALERT: agent ", agentID, "failed at create destroy win ", e)
		"""
		try:
			if (agentID in show.player and show.player[agentID]!=None):
				show.player[agentID].close_player()
				print ("agent:",agentID," free player OK")
		except Exception as e:
			print ("ALERT: agent ", agentID, "failed at create free player ", e)
			pass	
		"""

		try:
			#SDL_Quit()
			#if SDL_WasInit(SDL_INIT_VIDEO)==False:
			SDL_Init(SDL_INIT_VIDEO)

		except Exception as e:
			print ("ALERT: agent ", agentID, "SDL failed on create ", e) 
			pass
		
		SDL_PollEvent(ctypes.byref(show.event)) 


		image = filename
		ff_opts={'an': False,'sync': 'audio'}
		show.player[agentID] = MediaPlayer(image);#,ff_opts=ff_opts)
		while show.player[agentID].get_metadata()['src_vid_size'] == (0, 0):
			time.sleep(0.01)
		video_frame_size = show.player[agentID].get_metadata()['src_vid_size']
		#print(" la ventana mide",video_frame_size)

		print(" agent ",agentID, "showing portion ", portion)
		
		ancho=video_frame_size[0]
		alto=video_frame_size[1]

		print ("media file resultion:", ancho, "x" ,alto)

		#screen_width, screen_height=get_screen_resolution()
		#print ("screen mode resultion:", screen_width, "x" ,screen_height)
		
		factor=ancho/alto;
		print ("factor es  ",factor )
		# vamos a crear una porcion mas grande que la imagen
		if (factor<1.77):
			alto_porcion=int(alto/size)
			ancho_porcion=int(alto_porcion*1.77)
			#ancho_porcion=int(alto_porcion*factor)
						
		else:
			ancho_porcion=int(ancho/size)
			alto_porcion=int(ancho_porcion/1.77)	
			#alto_porcion=int(ancho_porcion/factor)	
		print ("ancho porcion ", ancho_porcion, " altoporcion", alto_porcion)






		#ancho_porcion=int(ancho/size)

		# x,y are computed using portion coordinates. Therefore in local mode, each agent paints its portion
		# at correct position
		x=(portion%size)*ancho_porcion


		#esto es mejorable
		#alto_porcion=int(alto/size)		

		#alto_porcion=int(ancho_porcion*0.5625)		
		y=int(portion/size)*alto_porcion

		# x,y are dependant on agent, not portion
		x=((int(agentID)-10)%size)*ancho_porcion
		y=int((int(agentID)-10)/size)*alto_porcion

		print ("xy:",x,y)
		#SDL_Init(SDL_INIT_VIDEO)
		#show.window[agentID] = SDL_CreateWindow(b"Hello World",x, y,ancho, alto, SDL_WINDOW_SHOWN | SDL_WINDOW_BORDERLESS)


		#para recrear la ventana asigno none. de este modo si ha cambiado la dimension se vuelve a crear
		show.window[agentID]=None

		if (full_screen=='N'):
			flags=SDL_WINDOW_SHOWN | SDL_WINDOW_BORDERLESS
			dest_ancho_porcion=ancho_porcion
			dest_alto_porcion=alto_porcion
		else:
			flags=SDL_WINDOW_SHOWN | SDL_WINDOW_BORDERLESS | SDL_WINDOW_FULLSCREEN
			screen_width, screen_height=get_screen_resolution()
			print ("screen mode resultion:", screen_width, "x" ,screen_height)
			dest_ancho_porcion=screen_width
			dest_alto_porcion=screen_height

		# identifier for automatic closing window
		show.thID[agentID]=(show.thID[agentID]+1) % 10
		
		
		th=show.thID[agentID]
		silent_th(agentID,int (x*1.01), int(y*1.01),dest_ancho_porcion, dest_alto_porcion, flags)
		#show.window[agentID] = SDL_CreateWindow(b"Hello World",int (x*1.01), int(y*1.01),ancho_porcion, alto_porcion, SDL_WINDOW_BORDERLESS)
		

		show.windowsurface[agentID] = SDL_GetWindowSurface(show.window[agentID])
		#my_renderer = SDL_CreateRenderer(show.window[agentID], -1, SDL_RENDERER_ACCELERATED);


		show.filename=filename
		cadena = filename.encode('utf8')
		
		show.img = SDL_LoadBMP(cadena)

		#my_tx = SDL_CreateTextureFromSurface(my_renderer, show.img);

		
		#portion coordinates
		xp=(portion%size)*ancho_porcion
		yp=int(portion/size)*alto_porcion
		
		#calculamos el rectangulo basado en agent
		r=SDL_Rect(xp,yp,ancho_porcion,alto_porcion)
		show.r[agentID]=r

		print("create agent ",agentID, "  full_screen:", full_screen)
		
		"""
		dest_ancho_porcion=ancho_porcion
		dest_alto_porcion=alto_porcion
		if (full_screen=='Y'):
			screen_width, screen_height=get_screen_resolution()
			print ("screen mode resultion:", screen_width, "x" ,screen_height)
			dest_ancho_porcion=screen_width
			dest_alto_porcion=screen_height
			#dest_alto_porcion=720
			#dest_ancho_porcion=1280
		"""
			

		r_dest=SDL_Rect(0,0,dest_ancho_porcion,dest_alto_porcion)
		show.r_dest[agentID]=r_dest

		#SDL_BlitSurface(show.img, r, show.windowsurface[agentID], None)
		SDL_BlitScaled(show.img, show.r[agentID], show.windowsurface[agentID],show.r_dest[agentID])



		SDL_UpdateWindowSurface(show.window[agentID])
	
		#hilo1 = threading.Thread(target=duerme())
		#hilo1.start()
		#t = threading.Timer(30.0, hola)
		#t.start()
		#hilo_silencioso()
		

		return 0,0

		# player exists
	elif (op=="reload_image"): # ESTA FUNCION HAY QUE ELIMINARLA Y USAR SIEMPRE CREATE
	#------------------------------------------------------
		SDL_PollEvent(ctypes.byref(show.event)) 
		cadena = filename.encode('utf8')
		video_frame_size = show.player[agentID].get_metadata()['src_vid_size']
		ancho=video_frame_size[0]
		alto=video_frame_size[1]
		show.img = SDL_LoadBMP(cadena)
		

		ancho=video_frame_size[0]
		alto=video_frame_size[1]

		factor=ancho/alto;
		print ("reload: factor es  ",factor )
		if (factor<1.77):
			alto_porcion=int(alto/size)
			ancho_porcion=int(alto_porcion*1.77)
						
		else:
			ancho_porcion=int(ancho/size)
			alto_porcion=int(ancho_porcion/1.77)	


		#ancho_porcion=int(ancho/size)
		x=(portion%size)*ancho_porcion

		#esto es mejorable
		#alto_porcion=int(alto/size)		
		#alto_porcion=int(ancho_porcion*0.5625)		

		y=int(portion/size)*alto_porcion
		#calculamos el rectangulo basado en agent
		r=SDL_Rect(x,y,ancho_porcion,alto_porcion)
		show.r[agentID]=r
		
		print("reload agent ",agentID, "  full_screen:", full_screen)
		

		dest_ancho_porcion=ancho_porcion
		dest_alto_porcion=alto_porcion
		if (full_screen=='Y'):
			screen_width, screen_height=get_screen_resolution()
			print ("reload: screen mode resultion:", screen_width, "x" ,screen_height)
			dest_ancho_porcion=screen_width
			dest_alto_porcion=screen_height		

		r_dest=SDL_Rect(0,0,dest_ancho_porcion,dest_alto_porcion)
		show.r_dest[agentID]=r_dest    

		#SDL_HideWindow(show.window[agentID])
		#SDL_BlitSurface(show.img, r, show.windowsurface[agentID], None)
		SDL_BlitScaled(show.img, show.r[agentID], show.windowsurface[agentID], show.r_dest[agentID])
		#SDL_Delay(1000);
		SDL_UpdateWindowSurface(show.window[agentID])

		return 0,0
	#-----------------------------------------------------------------------------------------------
	elif (op=="play_video"):
		
		try:
			if (agentID in show.windowsurface and show.windowsurface[agentID]!=None):
				SDL_FreeSurface(show.windowsurface[agentID])
				print ("agent:",agentID," free surface OK")
		except Exception as e:
			print ("ALERT: agent ", agentID, "failed at play free surface ", e)

		try:
			if 	(agentID in show.window): # and show.window[agentID]!=None):
				SDL_DestroyWindow(show.window[agentID])
				print ("agent:",agentID, " free window OK")
		except Exception as e:
			print ("ALERT: agent ", agentID, "failed at play destroy win ", e)
		try:
			#SDL_Quit()
			#if SDL_WasInit(SDL_INIT_VIDEO)==False:
			SDL_Init(SDL_INIT_VIDEO)

		except Exception as e:
			print ("ALERT: agent ", agentID, "SDL failed on play ", e) 
			pass
		"""
		try:
			if (agentID in show.player and show.player[agentID]!=None):
				show.player[agentID].close_player()
				print ("agent:",agentID," free player OK")
		except Exception as e:
			print ("ALERT: agent ", agentID, "failed at create free player ", e)
			pass	


		try:
			#SDL_Quit() # ESTO PETA SIEMPRE AQUI NO SE PUEDE PONER, NO SE PORQUE
			SDL_Init(SDL_INIT_VIDEO)

		except Exception as e:
			print ("ALERT: agent ", agentID, "SDL failed on create ", e) 
			pass
		"""
		SDL_PollEvent(ctypes.byref(show.event)) 



		#SDL_PollEvent(ctypes.byref(show.event)) 
		#not hasattr(show,"player"):
		"""
		try:
			if (agentID in show.windowsurface and show.windowsurface[agentID]!=None):
				SDL_FreeSurface(show.windowsurface[agentID])
				print ("agent:",agentID," free surface OK")
		except Exception as e:
			print ("ALERT: agent ", agentID, "failed at play free surface ", e)

		try:
			if 	(agentID in show.window and show.window[agentID]!=None):
				SDL_DestroyWindow(show.window[agentID])
				print ("agent:",agentID, " free window OK")
		except Exception as e:
			print ("ALERT: agent ", agentID, "failed at play destroy win ", e)

		"""
		

		"""
		try:
			if (agentID in show.player and show.player[agentID]!=None):
				show.player[agentID].close_player()
				print ("agent:",agentID," free player OK")
		except Exception as e:
			print ("ALERT: agent ", agentID, "failed at play free player ", e)
			pass	
		try:
			#SDL_Quit()
			SDL_Init(SDL_INIT_VIDEO)
			print ("agent:",agentID," free SDL and INIT OK")
		except Exception as e:
			print ("ALERT: agent ", agentID, "failed at play free SDL ", e)
			pass	
		"""

		#SDL_Quit()
		#SDL_Init(SDL_INIT_VIDEO)
		"""	
		except Exception as e:
			print ("ALERT: agent ", agentID, "failed at play ", e)
			pass
		"""
		#SDL_PollEvent(ctypes.byref(show.event)) 

		video = filename
		show.filename=filename
		#ff_opts={'an': False,'sync': 'audio'}

		# para que suene una sola maquina de todas las del videowall. de momento es chapuza
		#mute=True
		#if (agentID==10):
		#	mute=False

		#ff_opts={'an': sound,'sync': 'audio','paused':True}

		# infbuf is mandatory, otherwise videostreaming can fail and not recover
		#ff_opts={'an': sound,'sync': 'audio','paused':True,'infbuf':True, 'framedrop':True,'drp':1}

		# mute is an invocation parameter

		#opciones teoricamente buenas: mute es un parametro que llega y sync a video
		#ff_opts={'an': mute,'sync': 'video','paused':True,'infbuf':True, 'framedrop':True,'drp':1}
		if (agentID=="10"):
			mute=False
		else:
			mute=True
		#ff_opts={'an': mute,'sync': 'ext','paused':True,'infbuf':True, 'framedrop':True,'drp':1}

		#ff_opts={'an': mute,'sync': 'video','paused':True,'infbuf':True, 'framedrop':True,'drp':1}

		ff_opts={'an': mute,'sync': 'video','paused':True,'infbuf':True, 'framedrop':False,'drp':1}
		

		#ff_opts={'an': mute,'sync': 'audio','paused':True,'infbuf':True, 'framedrop':True,'drp':1}
		
		#ff_opts={'an': mute,'sync': 'video','paused':True,'fast':True, 'framedrop':True,'drp':0}
		show.player[agentID] = MediaPlayer(video,ff_opts=ff_opts)
		
		while show.player[agentID].get_metadata()['src_vid_size'] == (0, 0):
			time.sleep(0.01)
		
		cadena = filename.encode('utf8')
		
		video_frame_size = show.player[agentID].get_metadata()['src_vid_size']
		print("play video: agent ",agentID, "showing portion ", portion, " width audio=",(not mute))
		

		
		ancho=video_frame_size[0]
		alto=video_frame_size[1]
		
		show.ancho=ancho
		show.alto=alto
		print ("play video: media file resultion:", ancho, "x" ,alto)

		#screen_width, screen_height=get_screen_resolution()
		#print ("screen mode resultion:", screen_width, "x" ,screen_height)
		factor=ancho/alto;
		print ("play video: factor=", factor)
		# en video lo hago diferente, no vale el 1.77, porque despues el rectangulo destino
		# es fijo a 1280x720
		if (factor<1.77):
			alto_porcion=int(alto/size)
			ancho_porcion=int(alto_porcion*factor)
						
		else:
			ancho_porcion=int(ancho/size)
			alto_porcion=int(ancho_porcion/factor)


		"""
		if (ancho<=alto):
			alto_porcion=int(alto/size)
			ancho_porcion=int(alto_porcion*1.7777)
		else:

			ancho_porcion=int(ancho/size)
			alto_porcion=int(ancho_porcion*0.5625)
			print ("ancho porcion ", ancho_porcion, " altoporcion", alto_porcion)
		"""
		print ("play video: ancho porcion ", ancho_porcion, " altoporcion", alto_porcion)
		#ancho_porcion=int(ancho/size)
		x=(portion%size)*ancho_porcion

		# esto es mejorable
		#alto_porcion=int(alto/size)		
		#alto_porcion=int(ancho_porcion*0.5625)		
		y=int(portion/size)*alto_porcion


		# x,y are dependant on agent, not portion
		x=((int(agentID)-10)%size)*ancho_porcion
		y=int((int(agentID)-10)/size)*alto_porcion
		#portion coordinates
		xp=(portion%size)*ancho_porcion
		yp=int(portion/size)*alto_porcion

		#calculamos el rectangulo basado en agent
		r=SDL_Rect(xp,yp,ancho_porcion,alto_porcion)
		show.r[agentID]=r

		
		#para full screen:
		print("agent ",agentID, "  full_screen:", full_screen)
		dest_ancho_porcion=ancho_porcion
		dest_alto_porcion=alto_porcion
		if (full_screen=='Y'):
			screen_width, screen_height=get_screen_resolution()
			print ("play_video:screen mode resultion:", screen_width, "x" ,screen_height)
			# no le doy la resolucion de pantalla sino una de proporcion identica a la pantalla fisica
			# de lo contrario el full screen presenta bandas negras
			dest_alto_porcion=720
			dest_ancho_porcion=1280
			"""
			if (factor<1.77):
				dest_alto_porcion=screen_height
				dest_ancho_porcion=screen_width #int(screen_height*factor)
			else:
				dest_ancho_porcion=screen_width
				dest_alto_porcion=screen_height #int(screen_width/factor)
			"""



		r_dest=SDL_Rect(0,0,dest_ancho_porcion,dest_alto_porcion)
		
		show.r_dest[agentID]=r_dest

		
		#cad="Hello World"+str(agentID)
		#cad = cad.encode('utf8')
		#show.window[agentID] = SDL_CreateWindow(b"hello",int(x*1.05), int (y*1.05),ancho_porcion, alto_porcion, SDL_WINDOW_BORDERLESS)
		
		show.window[agentID]=None
		
		

		if (full_screen=='N'):
			flags=SDL_WINDOW_SHOWN | SDL_WINDOW_BORDERLESS
			#win_ancho_porcion=ancho_porcion
			#win_alto_porcion=alto_porcion
		else:
			flags=SDL_WINDOW_SHOWN | SDL_WINDOW_BORDERLESS | SDL_WINDOW_FULLSCREEN
			#screen_width, screen_height=get_screen_resolution()
			#print ("screen mode resultion:", screen_width, "x" ,screen_height)
			#win_ancho_porcion=screen_width
			#win_alto_porcion=screen_height

		"""
		if agentID in show.thID:
			show.thID[agentID]=show.thID[agentID]+1
			show.thID[agentID]=show.thID[agentID] % 10 
		else:
			show.thID[agentID]=0
		"""
		
		# identifier for automatic closing window
		show.thID[agentID]=(show.thID[agentID]+1) % 10
		time.sleep(1.0) # para que se cierre la antigua ventana	

		#success_win_creation=False
		#while (success_win_creation==False):
		#	success_win_creation=


		silent_th(agentID,int(x*1.01), int (y*1.01),dest_ancho_porcion, dest_alto_porcion, flags)
		#silent_th(agentID,int(x*1.01), int (y*1.01),ancho_porcion, alto_porcion, SDL_WINDOW_BORDERLESS |SDL_WINDOW_OPENGL)
		
		#show.glcontext[agentID] = SDL_GL_CreateContext(show.window[agentID]);
		#show.window[agentID] = SDL_CreateWindowAndRenderer(b"hello",x, y,ancho_porcion, alto_porcion, SDL_WINDOW_BORDERLESS,render)
		#render=SDL_GetRenderer(show.window[agentID]
		#render=SDL_createRenderer(show.window[agentID],-1, SDL_RENDERER_ACCELERATED | SDL_RENDERER_PRESENTVSYNC)
		#show.render[agentID]=render


		show.windowsurface[agentID] = SDL_GetWindowSurface(show.window[agentID])
		
		show.time[agentID]=0.0
		show.last_time[agentID]=0.0
		show.last_paused_at[agentID]=0
		return 0,0
		"""
		val =''
		t=0
		while val != 'eof':
			frame, val = show.player[agentID].get_frame()
			if val != 'eof' and frame is not None:
				img, t = frame
				
				data = img.to_bytearray()[0]
				mydata = ctypes.c_char * img.get_linesizes()[0]
				aux = mydata.from_buffer(data)
				show.img = SDL_CreateRGBSurfaceWithFormatFrom(aux,ancho,alto,24, ancho*3,SDL_PIXELFORMAT_RGB24)
				SDL_BlitScaled(show.img, show.r[agentID], show.windowsurface[agentID], show.r_dest[agentID])
				SDL_UpdateWindowSurface(show.window[agentID])
				#time.sleep(val)
				break;
		
		
		return 0,0
	"""
	#-----------------------------------------------------------------------------------------------
	elif (op=="ffwd"):
		if (timestamp!= None):
			if (agentID in show.time and show.time[agentID]<timestamp):
				print ("agent", agentID, " ffwd!")
				try:
					SDL_PollEvent(ctypes.byref(show.event)) 
				except:
					pass

				try:	
				#show.player[agentID].toggle_pause()
					#if (portion!=0):
					#	show.player[agentID].seek(show.t_master,relative=False,accurate=False)

					#esto es como una pausa 
					if (show.time[agentID]>timestamp):
						print ("agent ", agentID, " pause force")
						return show.time[agentID],0
					else:
						print ("agent ", agentID, show.time[agentID], timestamp)

					if show.player[agentID].get_pause():
						show.player[agentID].set_pause(False)	
						return show.time[agentID],0

					frame, val = show.player[agentID].get_frame() # val is the duration of this frame
					#show.player[agentID].toggle_pause()
					t=0
					if val != 'eof' and frame is not None:
						
						img, t = frame
						

						data = img.to_bytearray()[0]
						mydata = ctypes.c_char * img.get_linesizes()[0]
						aux = mydata.from_buffer(data)
						show.img = SDL_CreateRGBSurfaceWithFormatFrom(aux,show.ancho,show.alto,24, show.ancho*3,SDL_PIXELFORMAT_RGB24)
						SDL_BlitScaled(show.img, show.r[agentID], show.windowsurface[agentID], show.r_dest[agentID])
						SDL_UpdateWindowSurface(show.window[agentID])
						show.time[agentID]=t
						return t,val # t is the timestamp, val is the duration of this frame
					elif frame is None and show.time[agentID]==0:
						print ("player ", agentID, " not ready but ok")
						
					else:
						if val=='eof':
							return 0,0
						#print("frame failed at agent:",agentID, "TS: ", show.time[agentID], "  values(ts,duration):",t,val,  "frame:",frame)
						return 0,0
						#close_player(show.player[agentID])
						print( "player cerrado")
						ff_opts={'an': sound,'sync': 'audio','paused':False} # 'ss':show.time[agentID]}
						show.player[agentID] = MediaPlayer("https://www.radiantmediaplayer.com/media/bbb-360p.mp4",ff_opts=ff_opts)
						print ("player creado")
						#show.player[agentID].seek(show.time[agentID],relative=False,accurate=False)
						while show.player[agentID].get_metadata()['src_vid_size'] == (0, 0):
							time.sleep(0.01)
						while frame is None:
							frame, val = show.player[agentID].get_frame()
						
						print ("funciona!", frame, val)
						return 0,0
				except:
					#print ("Ha habido una excepcion !!!!!")
					return 0,0	
				return 0,0






	#-----------------------------------------------------------------------------------------------
	elif (op=="play_stream"):
		SDL_PollEvent(ctypes.byref(show.event)) 
		#not hasattr(show,"player"):
		
		try:
			if (agentID in show.windowsurface and show.windowsurface[agentID]!=None):
				SDL_FreeSurface(show.windowsurface[agentID])
			if 	(agentID in show.window and show.window[agentID]!=None):
				SDL_DestroyWindow(show.window[agentID])
			if (agentID in show.player and show.player[agentID]!=None):
				show.player[agentID].close_player()
			#SDL_Quit()
			#SDL_Init(SDL_INIT_VIDEO)
		except:
			pass

		video = filename
		show.filename=filename
		#ff_opts={'an': False,'sync': 'audio'}

		# para que suene una sola maquina de todas las del videowall. de momento es chapuza
		sound=True
		if (agentID==10):
			sound=False

		#ff_opts={'an': sound,'sync': 'audio','paused':True}

		# infbuf is mandatory, otherwise videostreaming can fail and not recover
		#ff_opts={'an': sound,'sync': 'audio','paused':True,'infbuf':True, 'framedrop':True,'drp':1}
		ff_opts={'an': sound,'sync': 'ext','paused':True,'infbuf':False, 'framedrop':True,'drp':1} # ,'ss':0}
		show.player[agentID] = MediaPlayer(video,ff_opts=ff_opts)
		
		#wait till player initialization is complete
		while show.player[agentID].get_metadata()['src_vid_size'] == (0, 0):
			time.sleep(0.01)
		
		cadena = filename.encode('utf8')
		
		video_frame_size = show.player[agentID].get_metadata()['src_vid_size']
		#print(" agent ",agentID, "showing portion ", portion)
		

		
		ancho=video_frame_size[0]
		alto=video_frame_size[1]
		
		show.ancho=ancho
		show.alto=alto

		ancho_porcion=int(ancho/size)
		alto_porcion=int(alto/size)		
		

		# x,y are dependant on agent, not portion
		x=((agentID-10)%size)*ancho_porcion
		y=int((agentID-10)/size)*alto_porcion
		#portion coordinates
		xp=(portion%size)*ancho_porcion
		yp=int(portion/size)*alto_porcion

		#calculamos el rectangulo basado en agent
		r=SDL_Rect(xp,yp,ancho_porcion,alto_porcion)
		show.r[agentID]=r
		r_dest=SDL_Rect(0,0,ancho_porcion,alto_porcion)
		show.r_dest[agentID]=r_dest

		
		cad="Hello World"+str(agentID)
		cad = cad.encode('utf8')
		show.window[agentID] = SDL_CreateWindow(b"hello",int(x*1.05), int (y*1.05),ancho_porcion, alto_porcion, SDL_WINDOW_BORDERLESS)
		
		show.windowsurface[agentID] = SDL_GetWindowSurface(show.window[agentID])
		return 0,0
		
	#-----------------------------------------------------------------------------------------------
	elif (op=="next_frame"):
		#print (agentID, " entra en next_frame TS", timestamp)
		try:
			SDL_PollEvent(ctypes.byref(show.event)) 

		except:
			pass


		try:	
		#show.player[agentID].toggle_pause()

			#if show.player[agentID].get_pause():
			#	show.player[agentID].set_pause(False)	
			#	return show.time[agentID],0

			#si hay mas de un 250 ms de diferencia autopausamos
			#agentID=str(agentID)
			#print ("agentID:", agentID)
			#print (show.time[agentID])
			#print ("force:", force)
			if (timestamp!= None and timestamp!=0):
				#si hay mas de un 250 ms de diferencia autopausamos
				margin=0.25
				if force=="Y":
					magin=0.25 # 250 ms para pausar force, por estar muy adelantado. del resto se encarga sync
				else:
					margin=0.07  # pausa force con mucho menos. sync no vale en video LIVE
				if (agentID in show.time and show.time[agentID]>timestamp+margin and show.last_paused_at[agentID]<timestamp-1):
				#if (agentID in show.time and show.time[agentID]>timestamp+1):
					print ("agent ", agentID, " auto pause force, margin:",margin, " agent_TS:", show.time[agentID], " vs ",timestamp)
					show.player[agentID].set_pause(True)
					show.last_paused_at[agentID]=timestamp;
					return show.time[agentID],0
					
				if (agentID in show.time and show.time[agentID]>timestamp+margin):
					return show.time[agentID],0

			#si esta en pausa y estamos por debajo de 250 (seguro) ms se la quito		
			if show.player[agentID].get_pause():
				#print ("agent ", agentID, " auto pause OFF", show.time[agentID], " vs ",timestamp)
				#if (divergence!=None and divergence<0.04):
				show.player[agentID].set_pause(False)	
				#return show.time[agentID],0

				#if (show.time[agentID]==timestamp):
				"""
				if (divergence!=None and divergence==0.0):
					show.player[agentID].set_pause(False)
					#return show.time[agentID],0
				else: 
					return show.time[agentID],0
				"""
			
			frame, val = show.player[agentID].get_frame() # val is the duration of this frame
			#print ("SM : agent" , agentID, "  val:",val, " ts:", frame[1])
			#show.player[agentID].toggle_pause()

			# parche para cloudbook. por algun motivo a veces val es cero
			while val==0.0 and val!='eof' and val!='pause':
			#CON GRANO 30 frames no hace falta
					frame, val = show.player[agentID].get_frame()
			
			#print ("val ", val)
			t=0 # inicio el timestamp del frame (no la duracion)
			if val=='paused':
				#print (" PAUSED---------------------------------------------------")
				img, t = frame
				show.time[agentID]=t
				return t,0

			#val possible values: 'eof', 'paused' or a float
			if val != 'eof' and frame is not None:
				
				img, t = frame
		
				data = img.to_bytearray()[0]
				mydata = ctypes.c_char * img.get_linesizes()[0]
				aux = mydata.from_buffer(data)
				
				# esta funcion retorna una surface
				show.img = SDL_CreateRGBSurfaceWithFormatFrom(aux,show.ancho,show.alto,24, show.ancho*3,SDL_PIXELFORMAT_RGB24)
				SDL_BlitScaled(show.img, show.r[agentID], show.windowsurface[agentID], show.r_dest[agentID])
				SDL_UpdateWindowSurface(show.window[agentID])
				
				#liberamos las dos surfaces
				#SDL_FreeSurface(show.img)
				#SDL_FreeSurface(show.windowsurface[agentID])
				


				#lib.freeme(mydata)
				#ctypes.free (aux) #free(data) #free(aux) #free (mydata)
				#gc.collect()
				#SDL_FreeSurface(show.window[agentID])
				#SDL_GL_SwapWindow(show.window[agentID])
				
				#tex=SDL_CreateTextureFromSurface(show.render[agentID],show.windowsurface[agentID])

				#SDL_RenderClear(show.render[agentID])
				#SDL_RenderCopy(show.render[agentID],tex,None,None)
				#SDL_RenderPresent(show.render[agentID])
				show.time[agentID]=t

				#parche cloudbook
				aux=float(val)
				#val=0

				if (val==0):
					# esto es asignar la duracion actual a la del frame pasado, lo cual es erroneo
					# no se sincroniza bien
					#dif=t-show.last_time[agentID] 
					#val=dif #min (0.0333666, dif)
					pass

				show.last_time[agentID]=t
				#print ("SM: val=", val) #, "  dif:", dif)
				#return t, val
				#print (agentID," ha terminado")
				return t,val # t is the timestamp, val is the duration of this frame

			#llegamos aqui si val no es eof	
			elif frame is None and val==0: #show.time[agentID]==0:
				print ("player ", agentID, " not ready but ok")
				show.last_time[agentID]=t
				return show.last_time[agentID],0.0
			
			# llegamos aqui si val es eof	
			else:
				# fin de audio
				if val=='eof':

					show.player[agentID].set_pause(True) #pause image and sound
					show.time[agentID]=t
					return show.time[agentID],val

					#time.sleep(0.01)
					try:
						if (agentID in show.windowsurface and show.windowsurface[agentID]!=None):
							SDL_FreeSurface(show.windowsurface[agentID])
							print ("agent:",agentID," free surface OK")
					except Exception as e:
						print ("ALERT: agent ", agentID, "failed at stop free surface ", e)

					try:
						if 	(agentID in show.window and show.window[agentID]!=None):
							SDL_DestroyWindow(show.window[agentID])
							print ("agent:",agentID, " free window OK")
					except Exception as e:
						print ("ALERT: agent ", agentID, "failed at stop destroy win ", e)
					"""
					try:
						if (agentID in show.player and show.player[agentID]!=None):
							show.player[agentID].close_player()
							print ("agent:",agentID," free player OK")
					except Exception as e:
						print ("ALERT: agent ", agentID, "failed at stop free player ", e)
						pass

					try:
						#SDL_Quit()
						#SDL_Init(SDL_INIT_VIDEO)
						print ("agent:",agentID," free SDL  OK")
					except Exception as e:
						print ("ALERT: agent ", agentID, "failed at play free SDL ", e)
						pass
					"""
					print (agentID," eof")
					return show.last_time[agentID], 'eof'
		except:
			print ("Ha habido una excepcion !!!!!")
			return 0,0	

		print (agentID," ha terminado mal   val:",val)
		return 0,0


	#-----------------------------------------------------------------------------------------------
	elif (op=="sync"):
		# this function has been invoked using the minimum timestamp of the videowall videos
		#if (agentID!=10):
		try:
			SDL_PollEvent(ctypes.byref(show.event)) 

		except:
			pass

		print ("SYNC ENTRY")
		print ("agent:", agentID, "  ts:", timestamp, "  agent:",show.time[agentID], "\n")	
		if (timestamp!= None ):
			#agent 10 lleva el sonido
			if (agentID in show.time and agentID!="10" and show.time[agentID]>timestamp+0.03) :
				#pausing faster player, only if it is very advanced respect the rest
				show.player[agentID].set_pause(True)
				print ("MICROPAUSED : ", agentID)
				return show.time[agentID],0
				#print("pausing ", agentID, " time ",show.time[agentID])
				#paused=True;

			#como poco el ts del agente es timestamp	
			#no acelero el agente 10 pues lleva el sonido
			#elif (agentID in show.time and agentID!="10" and show.time[agentID]==timestamp): #0.07 =2 frames
			# al final he decidido acelerarlo tambien
			elif (agentID in show.time and  show.time[agentID]==timestamp): #0.07 =2 frames
				#speed up slower player ( get 1 frame)
				val=0.0
				# un bucle while puede ser eterno. mejor solo 2 veces
				#while val==0.0 and val!='eof' and val!='pause':

				frame, val = show.player[agentID].get_frame(show=False) #, force_refresh=True)
				#if val==0:
				#	frame, val = show.player[agentID].get_frame(show=False) #, force_refresh=True)
				print ("agent:", agentID, "  speedup:", val, "\n")	
				#img, t = frame
				#show.time[agentID]=t
				return show.time[agentID],0
			#	show.player[agentID].set_pause(False)
			#show.player[agentID].seek(timestamp,relative=False,accurate=False)
			#show.player[agentID].set_pause(False)	
		return show.time[agentID],0
	#-----------------------------------------------------------------------------------------------
	elif (op=="sync2"):
		# accelerate video getting frames
		#print ("agent:", agentID, "  ts:", timestamp, "  player:",show.time[agentID], "\n")
		#t=show.time[agentID]
		if (timestamp!= None ):
			if (agentID in show.time and show.time[agentID]<timestamp-0.04):
				val=0.0
				show.player[agentID].set_pause(False)
				#print ("speed1  ",agentID, "\n")
				# solo acelera en video en lata, no en live
				while val==0.0:
					frame, val = show.player[agentID].get_frame(show=False) #, force_refresh=True)
				print ("val:",val)
				img, t = frame
				show.time[agentID]=t
				return show.time[agentID],0
			elif (agentID in show.time and show.time[agentID]==timestamp and divergence>0):
				#print ("pausing1  ",agentID, "\n")
				#show.player[agentID].set_pause(True)
				return show.time[agentID],0
			

		return 0,0
	#-----------------------------------------------------------------------------------------------
	elif (op=="fullscreen"):
		SDL_SetWindowFullscreen(show.window[agentID],SDL_WINDOW_FULLSCREEN_DESKTOP)

		return 0,0
	#-----------------------------------------------------------------------------------------------
	elif (op=="seek"):
		show.player[agentID].seek(timestamp,relative=False,accurate=False)
			#show.player[agentID].set_pause(False)	
		return 0,0
	#------------------------------------------------------------------------------------------------
	elif (op=="togglepause"): # se usa para arrancar el video
		show.player[agentID].toggle_pause()
		return 0, 0
	#------------------------------------------------------------------------------------------------
		
	elif (op=="pause"): # se usa para arrancar el video
		show.player[agentID].set_pause(True)
		return 0, 0
	
	#------------------------------------------------------------------------------------------------
	
	elif (op=="continue"): # se usa para arrancar el video
		show.player[agentID].set_pause(False)
		return 0, 0

	#------------------------------------------------------------------------------------------------
	

	elif (op=="stop"):
		show.player[agentID].set_pause(True) #pause image and sound
		show.thID[agentID]=show.thID[agentID]+1
		return 0, 0

		try:
			if (agentID in show.player and show.player[agentID]!=None):
				show.player[agentID].close_player()
				print ("agent:",agentID," free player OK")
		except Exception as e:
			print ("ALERT: agent ", agentID, "failed at stop free player ", e)
			pass	
		return 0, 0
		#time.sleep(0.01)
		
		try:
			if 	(agentID in show.window ): #and show.window[agentID]!=None):
				SDL_DestroyWindow(show.window[agentID])
				print ("agent:",agentID, " free window OK")
		except Exception as e:
			print ("ALERT: agent ", agentID, "failed at stop destroy win ", e)

		try:
			if (agentID in show.windowsurface and show.windowsurface[agentID]!=None):
				SDL_FreeSurface(show.windowsurface[agentID])
				print ("agent:",agentID," free surface OK")
		except Exception as e:
			print ("ALERT: agent ", agentID, "failed at stop free surface ", e)
		
		
		try:
			if (agentID in show.player and show.player[agentID]!=None):
				show.player[agentID].close_player()
				print ("agent:",agentID," free player OK")
		except Exception as e:
			print ("ALERT: agent ", agentID, "failed at stop free player ", e)
			pass	

		try:
			SDL_Quit()
			print ("agent:",agentID," free SDL OK")
		except Exception as e:
			print ("ALERT: agent ", agentID, "failed at stop free SDL ", e)
			pass	
		show.thID[agentID]=show.thID[agentID]+1
		return 0, 0

	#return 
#-----------------------------------------------------------------------------------------------
	elif (op=="next_30_frames"):
		#print (agentID, " entra en next_frame TS", timestamp)

		#bucle for de N frames
		for frame in range(0,300): # incluye  0...29 ,es decir 30 frames
	

			try:
				SDL_PollEvent(ctypes.byref(show.event)) 

			except:
				pass


			try:	
			
				if (timestamp!= None and timestamp!=0):
					#si hay mas de un 250 ms de diferencia autopausamos
					"""
					margin=0.25
					if force=="Y":
						magin=0.25 # 250 ms para pausar force, por estar muy adelantado. del resto se encarga sync
					else:
						margin=0.07  # pausa force con mucho menos. sync no vale en video LIVE
					if (agentID in show.time and show.time[agentID]>timestamp+margin and show.last_paused_at[agentID]<timestamp-1):
					#if (agentID in show.time and show.time[agentID]>timestamp+1):
						print ("agent ", agentID, " auto pause force, margin:",margin, " agent_TS:", show.time[agentID], " vs ",timestamp)
						show.player[agentID].set_pause(True)
						show.last_paused_at[agentID]=timestamp;

						return show.time[agentID],0
						
					if (agentID in show.time and show.time[agentID]>timestamp+margin):
						return show.time[agentID],0
					"""
				# si esta en pausa y estamos por debajo de 250 (seguro) ms se la quito		
				 
				if show.player[agentID].get_pause():
					show.player[agentID].set_pause(False)	
					
				now=time.time()
				frame, val = show.player[agentID].get_frame() # val is the duration of this frame
				#print ("SM : agent" , agentID, "  val:",val, " ts:", frame[1])
				#show.player[agentID].toggle_pause()

				
				
				#print ("val ", val)
				t=0 # inicio el timestamp del frame (no la duracion)
				if val=='paused':
					#print (" PAUSED---------------------------------------------------")
					img, t = frame
					show.time[agentID]=t
					return t,0

				#val possible values: 'eof', 'paused' or a float
				if val != 'eof' and frame is not None:
					
					img, t = frame
			
					data = img.to_bytearray()[0]
					mydata = ctypes.c_char * img.get_linesizes()[0]
					aux = mydata.from_buffer(data)
					
					# esta funcion retorna una surface
					show.img = SDL_CreateRGBSurfaceWithFormatFrom(aux,show.ancho,show.alto,24, show.ancho*3,SDL_PIXELFORMAT_RGB24)
					SDL_BlitScaled(show.img, show.r[agentID], show.windowsurface[agentID], show.r_dest[agentID])
					SDL_UpdateWindowSurface(show.window[agentID])
					
					
					show.time[agentID]=t

					#parche cloudbook
					aux=float(val)
					#val=0

					show.last_time[agentID]=t
					now2=time.time()
					delta=now2-now
					if (val-delta)<0 :
						delta=0

					

					if (t >timestamp +1): # 1 segundo, 30 frames aprox
						return show.last_time[agentID],val
					else:
						time.sleep(val- delta)
						continue

					continue
					#return t,val # t is the timestamp, val is the duration of this frame

				#llegamos aqui si val no es eof	
				elif frame is None and val==0: #show.time[agentID]==0:
					print ("player ", agentID, " not ready but ok")
					show.last_time[agentID]=t

					
					return show.last_time[agentID],0.0
				
				# llegamos aqui si val es eof	
				else:
					# fin de audio
					if val=='eof':

						show.player[agentID].set_pause(True) #pause image and sound
						show.time[agentID]=t
						return show.time[agentID],val

						#time.sleep(0.01)
						try:
							if (agentID in show.windowsurface and show.windowsurface[agentID]!=None):
								SDL_FreeSurface(show.windowsurface[agentID])
								print ("agent:",agentID," free surface OK")
						except Exception as e:
							print ("ALERT: agent ", agentID, "failed at stop free surface ", e)

						try:
							if 	(agentID in show.window and show.window[agentID]!=None):
								SDL_DestroyWindow(show.window[agentID])
								print ("agent:",agentID, " free window OK")
						except Exception as e:
							print ("ALERT: agent ", agentID, "failed at stop destroy win ", e)
						
						print (agentID," eof")
						return show.last_time[agentID], 'eof'
			except:
				print ("Ha habido una excepcion !!!!!")
				return 0,0	

			#print (agentID," ha terminado mal   val:",val)
			#return 0,0


	#-----------------------------------------------------------------------------------------------
	return show.last_time[agentID],val
#===========================================================================================	

