
from ffpyplayer.player import MediaPlayer
import ffpyplayer
import sys
from ctypes import create_string_buffer
import ctypes
from sdl2 import *
import time
import sdl2.ext

#__CLOUDBOOK:LOCAL__
def show(filename, portion,size,op,agentID, timestamp=None, mute=True):
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
		#show.portion=0
		show.filename=""
	if op=="create":
	#------------------------------------------------------
		SDL_PollEvent(ctypes.byref(show.event)) 
		#not hasattr(show,"player"):
		
		try:
			SDL_FreeSurface(show.windowsurface[agentID])
			SDL_DestroyWindow(show.window[agentID])
			close_player(show.player[agentID])
			SDL_Quit()
			SDL_Init(SDL_INIT_VIDEO)
		except: 
			pass
		



		image = filename
		ff_opts={'an': False,'sync': 'audio'}
		show.player[agentID] = MediaPlayer(image);#,ff_opts=ff_opts)
		while show.player[agentID].get_metadata()['src_vid_size'] == (0, 0):
			time.sleep(0.01)
		video_frame_size = show.player[agentID].get_metadata()['src_vid_size']
		#print(" la ventana mide",video_frame_size)

		print("@ agent ",agentID, "showing portion ", portion)
		
		ancho=video_frame_size[0]
		alto=video_frame_size[1]
		ancho_porcion=int(ancho/size)

		# x,y are computed using portion coordinates. Therefore in local mode, each agent paints its portion
		# at correct position
		x=(portion%size)*ancho_porcion
		alto_porcion=int(alto/size)		
		y=int(portion/size)*alto_porcion

		# x,y are dependant on agent, not portion
		x=((agentID-10)%size)*ancho_porcion
		y=int((agentID-10)/size)*alto_porcion

		#SDL_Init(SDL_INIT_VIDEO)
		#show.window[agentID] = SDL_CreateWindow(b"Hello World",x, y,ancho, alto, SDL_WINDOW_SHOWN | SDL_WINDOW_BORDERLESS)
		show.window[agentID] = SDL_CreateWindow(b"Hello World",int (x*1.01), int(y*1.01),ancho_porcion, alto_porcion, SDL_WINDOW_BORDERLESS)
		show.windowsurface[agentID] = SDL_GetWindowSurface(show.window[agentID])

		show.filename=filename
		cadena = filename.encode('utf8')
		
		show.img = SDL_LoadBMP(cadena)

		
		#portion coordinates
		xp=(portion%size)*ancho_porcion
		yp=int(portion/size)*alto_porcion
		
		#calculamos el rectangulo basado en agent
		r=SDL_Rect(xp,yp,ancho_porcion,alto_porcion)
		show.r[agentID]=r
		r_dest=SDL_Rect(0,0,ancho_porcion,alto_porcion)
		show.r_dest[agentID]=r_dest

		#SDL_BlitSurface(show.img, r, show.windowsurface[agentID], None)
		SDL_BlitScaled(show.img, show.r[agentID], show.windowsurface[agentID],show.r_dest[agentID])
		SDL_UpdateWindowSurface(show.window[agentID])
	
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
		ancho_porcion=int(ancho/size)
		x=(portion%size)*ancho_porcion
		alto_porcion=int(alto/size)		
		y=int(portion/size)*alto_porcion
		#calculamos el rectangulo basado en agent
		r=SDL_Rect(x,y,ancho_porcion,alto_porcion)
		show.r[agentID]=r
		r_dest=SDL_Rect(0,0,ancho_porcion,alto_porcion)
		show.r_dest[agentID]=r_dest    

		#SDL_HideWindow(show.window[agentID])
		#SDL_BlitSurface(show.img, r, show.windowsurface[agentID], None)
		SDL_BlitScaled(show.img, show.r[agentID], show.windowsurface[agentID], show.r_dest[agentID])
		#SDL_Delay(1000);
		SDL_UpdateWindowSurface(show.window[agentID])

		return 0,0
	#-----------------------------------------------------------------------------------------------
	elif (op=="play_video"):
		SDL_PollEvent(ctypes.byref(show.event)) 
		#not hasattr(show,"player"):
		
		try:
			SDL_FreeSurface(show.windowsurface[agentID])
			SDL_DestroyWindow(show.window[agentID])
			close_player(show.player[agentID])
			SDL_Quit()
			SDL_Init(SDL_INIT_VIDEO)
		except:
			pass

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

		
		ff_opts={'an': mute,'sync': 'video','paused':True,'infbuf':True, 'framedrop':True,'drp':1}
		#ff_opts={'an': mute,'sync': 'video','paused':True,'fast':True, 'framedrop':True,'drp':0}
		show.player[agentID] = MediaPlayer(video,ff_opts=ff_opts)
		
		while show.player[agentID].get_metadata()['src_vid_size'] == (0, 0):
			time.sleep(0.01)
		
		cadena = filename.encode('utf8')
		
		video_frame_size = show.player[agentID].get_metadata()['src_vid_size']
		print("@ agent ",agentID, "showing portion ", portion)
		

		
		ancho=video_frame_size[0]
		alto=video_frame_size[1]
		
		show.ancho=ancho
		show.alto=alto

		ancho_porcion=int(ancho/size)
		x=(portion%size)*ancho_porcion
		alto_porcion=int(alto/size)		
		y=int(portion/size)*alto_porcion


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
		
		

		#show.window[agentID] = SDL_CreateWindowAndRenderer(b"hello",x, y,ancho_porcion, alto_porcion, SDL_WINDOW_BORDERLESS,render)
		#render=SDL_GetRenderer(show.window[agentID]
		#render=SDL_createRenderer(show.window[agentID],-1, SDL_RENDERER_ACCELERATED | SDL_RENDERER_PRESENTVSYNC)
		#show.render[agentID]=render


		show.windowsurface[agentID] = SDL_GetWindowSurface(show.window[agentID])
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
			SDL_FreeSurface(show.windowsurface[agentID])
			SDL_DestroyWindow(show.window[agentID])
			close_player(show.player[agentID])
			SDL_Quit()
			SDL_Init(SDL_INIT_VIDEO)
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
		print("@ agent ",agentID, "showing portion ", portion)
		

		
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
		try:
			SDL_PollEvent(ctypes.byref(show.event)) 

		except:
			pass


		try:	
		#show.player[agentID].toggle_pause()

			#if (portion!=0):
			#	show.player[agentID].seek(show.t_master,relative=False,accurate=False)
			if show.player[agentID].get_pause():
				show.player[agentID].set_pause(False)	
				return show.time[agentID],0


			if (timestamp!= None):
				if (agentID in show.time and show.time[agentID]>timestamp+1):
					#print ("agent ", agentID, " pause force", show.time[agentID])
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
				#SDL_UpdateRect(show.windowsurface[agentID],0,0,ancho,alto)


				#tex=SDL_CreateTextureFromSurface(show.render[agentID],show.windowsurface[agentID])

				#SDL_RenderClear(show.render[agentID])
				#SDL_RenderCopy(show.render[agentID],tex,None,None)
				#SDL_RenderPresent(show.render[agentID])
				show.time[agentID]=t
				return t,val # t is the timestamp, val is the duration of this frame
			elif frame is None and show.time[agentID]==0:
				print ("player ", agentID, " not ready but ok")
				
			else:
				if val=='eof':

					show.player[agentID].set_pause(True) #pause image and sound
					#time.sleep(0.01)
					try:
						SDL_PollEvent(ctypes.byref(show.event)) 
						SDL_FreeSurface(show.windowsurface[agentID])
						SDL_DestroyWindow(show.window[agentID])
						close_player(show.player[agentID])
						SDL_Quit()
					except:
						pass	
					return 0, 0




					
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
				#show.player[agentID].toggle_pause()
				"""
				if (show.time[agentID]!=0):
					print (" restarting player...", agentID)
					close_player(show.player[agentID])
					#show.player[agentID].seek(show.time[agentID],relative=False,accurate=False)
					sound=True
					if (agentID==10):
						sound=False
					ff_opts={'an': sound,'sync': 'audio','paused':False}
					show.player[agentID] = MediaPlayer("https://www.radiantmediaplayer.com/media/bbb-360p.mp4",ff_opts=ff_opts)
					while show.player[agentID].get_metadata()['src_vid_size'] == (0, 0):
						time.sleep(0.01)
					#show.player[agentID].seek(show.time[agentID],relative=False,accurate=False)

				return 0,0	
				
				if (val=='paused'):
					return 0,0
					elif (val!='eof'):
						print ("frame is None")
						sound=True
						if (agentID==10):
							sound=False
						ff_opts={'an': sound,'sync': 'audio','paused':False}
						show.player[agentID] = MediaPlayer("https://www.radiantmediaplayer.com/media/bbb-360p.mp4",ff_opts=ff_opts)
						return 0,0	
					
				else:
					print("valores:",t,val,  "frame:",frame)
					return 0,0	
				"""

		except:
			#print ("Ha habido una excepcion !!!!!")
			return 0,0	
		return 0,0


	#-----------------------------------------------------------------------------------------------
	elif (op=="sync"):
		# this function has been invoked using the minimum timestamp of the videowall videos
		#if (agentID!=10):	
		if (timestamp!= None):
			if (agentID in show.time and show.time[agentID]>timestamp+0.03):
				show.player[agentID].set_pause(True)
				#print("pausing ", agentID, " time ",show.time[agentID])
				#paused=True;
			#else:
			#	show.player[agentID].set_pause(False)
			#show.player[agentID].seek(timestamp,relative=False,accurate=False)
			#show.player[agentID].set_pause(False)	
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
		#time.sleep(0.01)
		try:
			SDL_PollEvent(ctypes.byref(show.event)) 
			SDL_FreeSurface(show.windowsurface[agentID])
			SDL_DestroyWindow(show.window[agentID])
			close_player(show.player[agentID])
			SDL_Quit()
			#SDL_Init(SDL_INIT_VIDEO)
		except:
			pass	
		return 0, 0

	return 

#===========================================================================================	

