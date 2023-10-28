import pygame


class UI:
    def __init__(self, surface):
        # Setup
        self.display_surface = surface

        # Health
        self.health_bar = pygame.image.load("graphics/ui/health_bar.png")
        self.health_bar_topleft = (54, 39)
        self.health_bar_width = 152
        self.health_bar_height = 4

        # Coins
        self.coin = pygame.image.load("graphics/ui/coin.png")
        self.coin_rect = self.coin.get_rect(topleft=(50, 61))
        self.font = pygame.font.Font("graphics/ui/ARCADEPI.TTF", 30)

    def show_health_bar(self, current, full):
        self.display_surface.blit(self.health_bar, (20, 10))
        current_health_ratio = current / full
        current_bar_width = self.health_bar_width * current_health_ratio
        health_bar_rect = pygame.Rect((self.health_bar_topleft), (current_bar_width, self.health_bar_height))
        pygame.draw.rect(self.display_surface, "#dc4949", health_bar_rect)

    def show_coin(self, amount):
        self.display_surface.blit(self.coin, (50, 61))
        coin_amount_surf = self.font.render(str(amount), False, "#33323d")
        coin_amount_rect = coin_amount_surf.get_rect(midleft=(self.coin_rect.right + 5, self.coin_rect.centery))
        self.display_surface.blit(coin_amount_surf, coin_amount_rect)
