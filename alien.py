import pygame
from pygame.sprite import Sprite 


class Alien(Sprite):

	def __init__(self, ai_settings, screen):
		"""initialize the alien and set its starting position"""
		super().__init__()
		self.screen = screen
		self.ai_settings = ai_settings

		# Load the alien image and set rect attribute.
		self.image = pygame.image.load('images/alien.bmp')
		self.rect = self.image.get_rect()

        # Start each new alien near the top of the screen
		self.rect.x = self.rect.width
		#print(self.rect.width)
		self.rect.y = self.rect.height
		#print(self.rect.height)

		# Store the alien's rect position
		self.x = float(self.rect.x)
		#print(self.rect.x)

	def blitme(self):
		self.screen.blit(self.image, self.rect)

	def update(self):
		self.x += self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction 
		self.rect.x = self.x
	
	def check_edges(self):
		"""Return True if alien is at the edge of screen"""
		screen_rect = self.screen.get_rect()
		if self.rect.right >= screen_rect.right:
			return True
		elif self.rect.left <= 0:
			return True








