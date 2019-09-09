# import
import time
import Configuration as Conf
import Execute as Exe
import neopixel
import board
import wiringpi

# Define
NumPixels = 30
PIN_LED = board.D18

# Global
const_changeModeDelay = 125	# msec
#tempStripe = neopixel.NeoPixel(PIN_LED, NumPixels, 1, False, neopixel.GRB)
Config = Conf.Configuration(neopixel.NeoPixel(PIN_LED, NumPixels, brightness=0.2, auto_write=False, pixel_order=neopixel.GRB))

# Modes
ColorOffColorOff = Exe.Mode_ColorOffColorOff()
ColorFade = Exe.Mode_ColorFade()
RainbowFlow = Exe.Mode_RainbowFlow()
PackChaser = Exe.Mode_PackChaser()
KnightRider = Exe.Mode_KnightRider()
Police = Exe.Mode_Police()

# millis-lambda
def millis():
	return int(round(time.time() * 1000))

# Setup
if __name__ == "__main__":
	Config.Stripe.fill(0x000000)
	Config.Stripe.show()
	
	Config.Mode = 5
	
	print("Setup done!!\n")
	
	Config.CurrentTime = millis()
	
	
	# Loop
	while True:
		
		# Change mode
		if(Config.CurrentTime > Config.LastTimeChanged + const_changeModeDelay):
			
			# Certain trigger to change mode, like a
			# buttonpress wopuld be ok.
			# Or an argument has been committed to the program
			
			Config.LastTimeChanged = Config.CurrentTime
		
		# Run chosen Mode
		if(Config.CurrentTime > Config.LastTimeStep + Config.Delay):
			
			# i miss my old switch-statements.. :(
			if(Config.Mode == 0):
				Config.Delay = 70
				ColorOffColorOff.update(Config)
			elif(Config.Mode == 1):
				Config.Delay = 20
				ColorFade.update(Config)
			elif(Config.Mode == 2):
				Config.Delay = 10
				RainbowFlow.update(Config)
			elif(Config.Mode == 3):
				Config.Delay = 20
				PackChaser.update(Config)
			elif(Config.Mode == 4):
				Config.Delay = 20
				KnightRider.update(Config)
			elif(Config.Mode == 5):
				Config.Delay = 50
				Police.update(Config)
			else:
				Config.Delay = 1000
				Config.Stripe.fill(0x880088)
				Config.Stripe.show()
			
			Config.LastTimeStep = Config.CurrentTime
		
		# Update Time
		Config.CurrentTime = millis()
