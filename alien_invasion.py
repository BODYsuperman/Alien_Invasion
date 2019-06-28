import sys

import pygame

from settings import Settings
from ship import Ship
from alien import Alien
import game_functions as gf
from pygame.sprite import Group
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

def run_game():
	"""Initialzie pygame, settings and create a screen object"""
	pygame.init()
	ai_settings = Settings()
	screen = pygame.display.set_mode((ai_settings.screen_width, 
									  ai_settings.screen_height))

	pygame.display.set_caption(ai_settings.caption)

	ship = Ship(ai_settings, screen)
	alien = Alien(ai_settings, screen)
	stats = GameStats(ai_settings)
	sb = Scoreboard(ai_settings, screen, stats)
	play_button = Button(ai_settings, screen, "Play")
	bullets = Group()
	aliens = Group()

	gf.create_fleet(ai_settings, screen, ship,  aliens)
	#开始游戏的主循环
	while True:
		#监视键盘和鼠标
		gf.check_events(ai_settings, screen, stats, sb, 
						play_button, ship, aliens, bullets)
		if stats.game_active:

			ship.update()
			gf.update_bullets(ai_settings, screen, stats, sb, 
							  ship, aliens, bullets)
			gf.update_aliens(ai_settings, stats, screen, sb,
							 ship, aliens, bullets)
		gf.update_screen(ai_settings, screen, stats, sb,
						 ship, aliens, bullets, play_button)


run_game()