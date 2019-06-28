class Settings():
	"""A class to store all settings for Alien invasion"""

	def __init__(self):
		self.screen_width = 1200
		self.screen_height = 800
		self.bg_color = (235, 235, 235)
		self.caption = "Alien Invasion"

		self.ship_limit = 3
		self.fleet_drop_speed = 10

		#Bullet settings

		self.bullet_width = 150
		self.bullet_height = 15
		self.bullet_color = 60, 60, 60
		self.bullets_allowed = 3

		#How quickly the game speeds up
		self.speedup_scale = 1.1
		#How quickly the alien point value increase
		self.score_sclae = 1.5

		self.initialize_dynamic_settings()


	def initialize_dynamic_settings(self):
		"""initialize settings that change throught the game"""
		self.ship_speed_factor = 1.5
		self.alien_speed_factor = 1
		self.bullet_speed_factor = 3 
		#1 means right; -1 means left 
		self.fleet_direction = 1

		#Scoring
		self.alien_points = 50

	def increase_speed(self):
		"""increase speed settings and alien point values"""
		self.ship_speed_factor *= self.speedup_scale
		self.bullet_speed_factor *= self.speedup_scale
		self.alien_speed_factor *= self.speedup_scale

		self.alien_points = int(self.alien_points * self.score_sclae)
		print(self.alien_points)