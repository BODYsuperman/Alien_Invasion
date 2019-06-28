import sys
from time import sleep
import pygame
from bullet import Bullet
from alien import Alien
from game_stats import GameStats

def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
	"""Respond to keypresses and move events."""
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

		elif event.type == pygame.KEYDOWN:
			check_keydown_events(event, ai_settings, screen, ship, bullets)
			#print(event.key)

		elif event.type == pygame.KEYUP:
			check_keyup_events(event, ship)
			#print(event.key)
		elif event.type == pygame.MOUSEBUTTONDOWN:
			mouse_x, mouse_y = pygame.mouse.get_pos()
			check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)

def check_play_button(ai_settings, screen, stats, sb, play_button,
					 ship, aliens, bullets, mouse_x, mouse_y):
	"""Start a new game when the player clicks Play."""
	button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
	if button_clicked and not stats.game_active:
		ai_settings.initialize_dynamic_settings()
		start_game(ai_settings, screen, stats, sb, ship, aliens, bullets)

def start_game(ai_settings, screen, stats, sb, 
			   ship, aliens, bullets):
		# Hide the mouse cursor
		pygame.mouse.set_visible(False)
		# Reset the game statistics
		stats.reset_stats()
		print("score ", stats.score)
		stats.game_active = True

		# Reset the scoreboard images.
		sb.prep_images()

		# Empty the list of aliens and bullets
		aliens.empty()
		bullets.empty()

		# Create a new fleet and center the ship
		create_fleet(ai_settings, screen, ship, aliens)
		ship.center_ship()

def check_keydown_events(event, ai_settings, screen, ship, bullets):
	"""Respond to key presses"""
	if event.key == pygame.K_RIGHT:
		ship.moving_right = True
	elif event.key == pygame.K_LEFT:
		ship.moving_left = True	
	elif event.key == pygame.K_SPACE:
		fire_bullet(ai_settings, screen, ship, bullets)
	elif event.key == pygame.K_q:
		sys.exit()

def fire_bullet(ai_settings, screen, ship, bullets):
	"""Fire a bullet if limit not reached yet."""
	if len(bullets) < ai_settings.bullets_allowed:
		new_bullet = Bullet(ai_settings, screen, ship)
		bullets.add(new_bullet)	

def check_keyup_events(event, ship):
	"""Respond to key presses. """
	if event.key == pygame.K_RIGHT:
		ship.moving_right = False
	elif event.key == pygame.K_LEFT:
		ship.moving_left = False

def update_screen(ai_settings, screen, stats, sb, ship, 
				  aliens, bullets, play_button):
	"""Update images on the screen and flip to the new screen"""
	# Redraw the screen during each pass through the loop
	screen.fill(ai_settings.bg_color)

	# Redraw all the bullets behind the ship and aliens.
	for bullet in bullets.sprites():
		bullet.draw_bullet()
	ship.blitme()
	aliens.draw(screen)

	# Draw the score information
	sb.show_score()

	#Draw the play button if the game is inactive
	if not stats.game_active:
		play_button.draw_button()
	#Make the most recently drawn screen visible.
	pygame.display.flip()

def update_bullets(ai_settings, screen, stats, sb, 
				   ship, aliens, bullets):
	"""Update position of bullets and get rid of old bullets"""
	# Update bullet position
	bullets.update()

	# Get rid of bullets that have disappeared
	for bullet in bullets.copy():
		if bullet.rect.bottom <= 0:
			bullets.remove(bullet)


	check_bullet_alien_collisions(ai_settings, screen, stats, 
								  sb, ship, aliens, bullets)

def check_bullet_alien_collisions(ai_settings, screen, stats, 
								  sb, ship, aliens, bullets):
	"""Respond to bullet-alien collisions."""
	collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
	#print(len(bullets))
	if collisions:
		for alien in collisions.values():
			stats.score += ai_settings.alien_points * len(aliens)
			sb.prep_score()
		check_high_score(stats, sb)

	if len(aliens) == 0:
		bullets.empty()
		ai_settings.increase_speed()

		stats.level += 1
		sb.prep_level()

		create_fleet(ai_settings, screen, ship, aliens)

def check_fleet_edges(ai_settings, aliens):
	for alien in aliens. sprites():
		if alien.check_edges():
			change_fleet_direction(ai_settings, aliens)
			break

def change_fleet_direction(ai_settings, aliens):
	for alien in aliens.sprites():
		alien.rect.y += ai_settings.fleet_drop_speed
	ai_settings.fleet_direction *= -1

def update_aliens(ai_settings, stats, screen, sb, ship,
				  aliens, bullets):
	check_fleet_edges(ai_settings, aliens)
	aliens.update()
	if pygame.sprite.spritecollideany(ship, aliens):
		ship_hit(ai_settings, stats, screen, sb, ship, 
				 aliens, bullets)
		print("Ship hit!!!")
	check_aliens_bottom(ai_settings, stats, screen, 
						sb, ship, aliens, bullets)

def get_number_aliens_x(ai_settings, alien_width):
	available_space_x = ai_settings.screen_width - 2 * alien_width
	number_aliens_x = int(available_space_x / (2 * alien_width))
	return number_aliens_x

def get_number_rows(ai_settings, ship_height, alien_height):
	available_space_y = ai_settings.screen_height - 3 * alien_height - ship_height
	number_rows = int(available_space_y / (2 * alien_height))
	return number_rows

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
	alien = Alien(ai_settings, screen)
	alien_width = alien.rect.width
	alien.x = alien_width + 2* alien_width * alien_number
	alien.rect.x = alien.x
	alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
	aliens.add(alien)


def create_fleet(ai_settings, screen, ship,  aliens):
	alien = Alien(ai_settings, screen)
	number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
	number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

	for row_number in range(number_rows):
		for alien_number in range(number_aliens_x):
			create_alien(ai_settings, screen, aliens, alien_number, row_number)

	
def ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets):
	"""Respond to ship being hit by alien"""
	stats.ship_left -= 1

	# Decrement ships left
	if stats.ship_left > 0:
		# Update scorebaords
		sb.prep_score()
		#sb.prep_ships()

		# Empty the list of aliens and bullets.
		aliens.empty()
		bullets.empty()

		# Create a new fleet and center the ship.
		create_fleet(ai_settings, screen, ship, aliens)
		ship.center_ship()

		# Pause
		sleep(0.5)
	else:
		stats.game_active = False
		pygame.mouse.set_visible(True)

def check_aliens_bottom(ai_settings, stats, screen, sb, 
						ship, aliens, bullets):
	screen_rect = screen.get_rect()
	for alien in aliens.sprites():
		if alien.rect.bottom >= screen_rect.bottom:
			# Treat this the same as if the ship got hit.
			ship_hit(ai_settings, stats, screen, sb,
					 ship, aliens, bullets)
			break

def check_high_score(stats, sb):
	if stats.score > stats.high_score:
		stats.high_score = stats.score
		sb.prep_high_score()