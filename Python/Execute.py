#import Configuration as Conf
import neopixel
import random

# Pixels are getting set to "Color1", then 2 are black, next one is "Color2",
# another 2 are set black. Start then over again
# Template class -- needs to be changed, as wanted
class Mode_ColorOffColorOff:
	currentPixel = 0
	col = 0	# Which color is set? Color1, Color2, or another one?
	colAlternatives = 5	# Black pixel is also an alternative. This
				# represents the "length" of "color-array"
				# ..dude, I have no clue how to explain this
				# please just look it up yourself
	
	def update(self, Config):
		
		# First clear the Stripe
		Config.Stripe.fill(0x000000)
		
		# Then set the Colors
		i = self.currentPixel
		for count in range(0, Config.length):
			
			#  Change this section as you want it to be
			if(self.col == 0):
				if(0 <= i < Config.length):
					Config.Stripe[i] = 0x00ff00
			elif(self.col == 3):
				if(0 <= i < Config.length):
					Config.Stripe[i] = 0x0000ff
			#  End of Changeable Section
			
			# "col" reached max amount of color-alternative?
			self.col = self.col+1 if self.col < self.colAlternatives else 0
			
			# if "i" overshoots pixelamount
			i = i+1 if i < Config.length else 0
		
		# if "currentPixel" overshoots pixelamount
		self.currentPixel = self.currentPixel+1 if self.currentPixel < Config.length else 0
		
		# Show changed pixels
		Config.Stripe.show()
		return

# Some "Pulse-Effect, Good for underglow on cars
class Mode_ColorFade:
	fadeDown = True
	rgb = [0xff, 0xff, 0xff]
	
	def update(self, Config):
		
		for i in range(0, Config.length):
			if(0 <= i < Config.length):
				Config.Stripe[i] = (self.rgb[0], self.rgb[1], self.rgb[2])
		
		#  Change this section as you want it to be
		#  Shown here: only green
		# Just changing if it should get darker or brighter
		if(self.fadeDown):
			if(self.rgb[1] > 0xff/20):
				self.rgb[1] -= 3
			else:
				self.fadeDown = not self.fadeDown
		else:
			if(self.rgb[1] < 0xff):
				self.rgb[1] += 3
				if(self.rgb[1] > 0xff):
					self.rgb[1] = 0xff
			else:
				self.fadeDown = not self.fadeDown
		# End of changeable section
		
		# Show changed pixels
		Config.Stripe.show()
		return

# Simple Rainbow flowing along the Stripe
class Mode_RainbowFlow:
	currentPos = 0
	
	# following function "wheel" is from "https://circuitpython.readthedocs.io/projects/neopixel/en/latest/examples.html"
	def wheel(self, pos):
		if(pos < 0 or pos > 255):
			r = g = b = 0
		elif(pos < 85):
			r = int(pos *3)
			g = int(255 - pos*3)
			b = 0
		elif(pos < 170):
			pos -= 85
			r = int(255 - pos*3)
			g = 0
			b = int(pos*3)
		else:
			pos -= 170
			r = 0
			g = int(pos*3)
			b = int(255 - pos*3)
		return (r, g, b)
	
	# following function "update" is from "https://circuitpython.readthedocs.io/projects/neopixel/en/latest/examples.html" --> rainbow_cycle(wait)
	def update(self, Config):
		for i in range(0, Config.length):
			pixel_index = (i*256 // Config.length) + self.currentPos
			
			if(0 <= i < Config.length):
				Config.Stripe[i] = self.wheel(self.currentPos & 255)
		
		# if "currentPos" overshoots 255
		self.currentPos = self.currentPos+1 if self.currentPos < 255 else 0
		
		# Show changed pixels
		Config.Stripe.show()
		return

# A specific amount of Packs with a specific amount of Pixels in it are
# walking over the stripe
class Mode_PackChaser:
	
	currentPixel = 0
	length = 5
	amount = 2
	
	def update(self, Config, rgb):
		
		i = self.currentPixel
		for count in range(0, Config.length):
			
			# Pack length? (kinda...)
			if(self.col < self.length):
				if(0 <= i < Config.length):
					Config.Stripe[i] = (rgb[0], rgb[1], rgb[2])
			else:
				if(0 <= i < Config.length):
					Config.Stripe[i] = 0x000000
			
			# How many Packs
			#
			# Nope.not how many Packs; True meaning here:
			# col reached max-alternatives?
			self.col = self.col+1 if (self.col < int(Config.length / self.amount)) else 0
			
			# if "i" overshoots pixelamount
			i = i+1 if i < Config.length else 0
		
		# if "currentPixel" overshoots pixelamount
		self.currentPixel = self.currentPixel+1 if self.currentPixel < Config.length else 0
		
		# Show changed pixels
		Config.Stripe.show()
		return

# You know "Knight Rider"?
# You know "Kitt"? Or even "Karr"?
# It is this little lightbar on the front
class Mode_KnightRider:
	forward = True
	currentPixel = 0
	length = 12
	
	def update(self, Config):
		colorUp = True
		
		# Setup for Karr (yellow)
		const_deltaRed = 255/self.length
		const_deltaGreen = 180/self.length
		const_deltaBlue = 255/self.length
		countSteps = 1
		
		# Set Pixels
		Config.Stripe.fill(0x000000)
		#for(int i = currentPixel - (KnightRider.length / 2); i < (currentPixel + KnightRider.length / 2); ++i){
		i = currentPixel - (KnightRider.length / 2);
		while(i < (currentPixel + KnightRider.length / 2)):
			
			if(0 <= i < Config.length):
				Config.Stripe[i] = (const_deltaRed*countSteps, const_deltaGreen*countSteps, const_deltaBlue*countSteps)
			
			# change countSteps
			countSteps = countSteps+1 if colorUp else countSteps-1
			
			if(i == self.currentPixel):
				colorUp = not colorUp
			
			i += 1
		
		# move forward or backwards?
		self.currentPixel = self.currentPixel+1 if self.forward else self.currentPixel-1
		
		# change direction
		if(self.currentPixel == 0 and not self.forward):
			self.forward = True
		elif(self.currentPixel == Config.length and self.forward):
			self.forward = False
		
		# Show changed pixels
		Config.Stripe.show()
		return

# US-Policelights
# I am not from the US, so please forgive me, if it's an absolutely wrong pattern
# P.S.: I am not responsible for anyone to break the law
class Mode_Police:
	sections = 7
	
	def __init__(self):
		random.seed(7)
	
	def update(self, Config):
		# Pattern:
		#					White
		#				Red		Blue
		#			White				White
		#		Red						Blue
		# Ends with:
		#		1	2	3	4	5	6	7
		
		const_pixelsPerSection = int(Config.length / self.sections)
		
		activateSection = int(random(0, 100))
		deactivateSection = int(random(0, 100))
		
		const_RED	= 5
		const_WHITE	= 2
		const_BLUE	= 7
		
		#Section 1 - RED
		for i in range(0*const_pixelsPerSection, 1*const_pixelsPerSection):
			if(activateSection % const_RED == 0):
				Config.Stripe[i] = 0xff0000
			elif(deactivateSection % const_RED == 0):
				Config.Stripe[i] = 0x000000
		#Section 2 - WHITE
		for i in range(1*const_pixelsPerSection, 2*const_pixelsPerSection):
			if(activateSection % const_WHITE == 0):
				Config.Stripe[i] = 0xffffff
			elif(deactivateSection % const_WHITE == 0):
				Config.Stripe[i] = 0x000000
		#Section 3 - RED
		for i in range(2*const_pixelsPerSection, 3*const_pixelsPerSection):
			if(activateSection % const_RED == 0):
				Config.Stripe[i] = 0xff0000
			elif(deactivateSection % const_RED == 0):
				Config.Stripe[i] = 0x000000
		#Section 4 - WHITE
		for i in range(3*const_pixelsPerSection, 4*const_pixelsPerSection):
			if(activateSection % const_WHITE == 0):
				Config.Stripe[i] = 0xffffff
			elif(deactivateSection % const_WHITE == 0):
				Config.Stripe[i] = 0x000000
		#Section 5 - BLUE
		for i in range(4*const_pixelsPerSection, 5*const_pixelsPerSection):
			if(activateSection % const_BLUE == 0):
				Config.Stripe[i] = 0x0000ff
			elif(deactivateSection % const_BLUE == 0):
				Config.Stripe[i] = 0x000000
		#Section 6 - WHITE
		for i in range(5*const_pixelsPerSection, 6*const_pixelsPerSection):
			if(activateSection % const_WHITE == 0):
				Config.Stripe[i] = 0xffffff
			elif(deactivateSection % const_WHITE == 0):
				Config.Stripe[i] = 0x000000
		#Section 7 - BLUE
		for i in range(6*const_pixelsPerSection, Config.length):
			if(activateSection % const_BLUE == 0):
				Config.Stripe[i] = 0x0000ff
			elif(deactivateSection % const_BLUE == 0):
				Config.Stripe[i] = 0x000000
		
		# Show changed pixels
		Config.Stripe.show()
		return
