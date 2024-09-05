import sys
import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien

class ShipShooter:
    """
    General class for managing resources and the way of working with the game.
    This class initializes the game and sets up the necessary resources.
    """

    def __init__(self) -> None:
        """
        Initialize the game.
        This function initializes the pygame module, which is necessary for creating the game window and handling game events.
        """
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        width = self.settings.screen_width
        height = self.settings.screen_height
        self.screen = pygame.display.set_mode((width, height))
        
        # self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        # self.settings.screen_width = self.screen.get_rect().width
        # self.settings.screen_height = self.screen.get_rect().height
        
        self.ship = Ship(self)
        self.bullets: pygame.sprite.Group[Bullet] = pygame.sprite.Group()
        self.aliens: pygame.sprite.Group[Alien] = pygame.sprite.Group()
        
        self._create_fleet()

        pygame.display.set_caption("Ship Shooter")
        
    def run_game(self) -> None:
        """
        Run the main loop for the game.
        This function contains an infinite loop that runs the game. It checks for events, updates the screen, and limits the frame rate.
        """
        while True:
            self._check_events()
            self.ship.update()
            self._update_bullets()
            self._update_aliens()
            self._update_screen()
            self.clock.tick(60)
            
    def _check_events(self) -> None:
        """
        Check for keyboard events and update the ship's position accordingly.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_envents(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
             
                    
    def _check_keydown_envents(self, event) -> None:
        """
        Check for key press events and update the ship's movement flags accordingly.
        Parameters:
        event (pygame.event.Event): The event object representing the key press event.
        """
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
            
    def _fire_bullet(self) -> None:
        """
        Create a new bullet and add it to the bullets group.
        """
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
        
            
    def _check_keyup_events(self, event) -> None:
        """
        Check for key release events and update the ship's movement flags accordingly.
        Parameters:
        event (pygame.event.Event): The event object representing the key release event.
        """
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
            
    def _update_bullets(self) -> None:
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collision()
        
    def _check_bullet_alien_collision(self) -> None:
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
                
    def _update_aliens(self) -> None:
        self._check_fleet_edges()
        self.aliens.update()
    
    def _update_screen(self) -> None:
        """
        Update the screen with the new position of the ship.
        """
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
            
        self.ship.blitme()
        self.aliens.draw(self.screen)
        
        pygame.display.flip()
        
    def _create_fleet(self) -> None:
        """
        Create a fleet of aliens.
        """
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        
        current_x, current_y = alien_width, alien_height
        while current_y < (self.settings.screen_height - 3 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width
            current_x = alien_width
            current_y += 2 * alien_height
            
    def _create_alien(self, x_position: float, y_position: float) -> None:
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position - 30
        self.aliens.add(new_alien)
        
    def _check_fleet_edges(self) -> bool:
        for alien in self.aliens.sprites():
            if alien.check_edges():
               self._change_fleet_direction()
               break
    
    def _change_fleet_direction(self) -> None:
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1
        

if __name__ == '__main__':
    game = ShipShooter()
    game.run_game()

          

      