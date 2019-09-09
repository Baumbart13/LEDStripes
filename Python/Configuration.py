import neopixel

class Configuration:
	Mode = -1
	length = 0
	
	Delay = 0
	CurrentTime = 0
	LastTimeChanged = 0
	LastTimeStep = 0

	def __init__(self, Stripe):
		self.Stripe = Stripe
		self.length = len(Stripe)
