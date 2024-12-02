from importation import *
import random
import animation
import pygame

class Monster(animation.AnimateSprite):
    
    def __init__(self, game, name, size, offset=0):
        super().__init__(name, size)
        self.game = game
        self.hp = 100
        self.max_hp = 100
        self.attack = 5
        self.rect = self.image.get_rect()
        self.rect.x = 1000 + random.randint(0, 80)
        self.rect.y = 540 - offset
        self.start_animation()
        
    def set_speed(self, speed):
        self.default_speed = speed
        self.velocity = random.randint(1, self.default_speed)
        
    def damage(self, dgt):
        #infliger les degat
        self.hp -= dgt
        #si plus de hp
        if self.hp <= 0:
            self.rect.x = 1000 + random.randint(0, 80)
            self.hp = self.max_hp
            self.game.add_score(self.point)
        #si la barre d'evenement est charger
        if self.game.comet_event.is_full_load():
            #suppr les monstres
            self.game.all_monsters.remove(self)
            #appeler les cometes
            self.game.comet_event.attempt_fall()
                           
    def update_hp_bar(self, surface):
        #definir la bar de hp
        bar_color= (88, 255, 51)
        bg_bar_color = (104, 11, 103)
        bar_position = [self.rect.x + 10, self.rect.y - 20, self.hp, 7]
        bg_bar_position = [self.rect.x + 10, self.rect.y - 20, self.max_hp, 7]        
        pygame.draw.rect(surface, bg_bar_color, bg_bar_position)
        pygame.draw.rect(surface, bar_color, bar_position)
        
    def update_animate(self, surface):
        self.animate(loop=True)
    
    def forward(self):
        if not self.game.check_collision(self, self.game.all_players):
            self.rect.x -= self.velocity
        else:
            #infliger de degat
            self.game.player.damage(self.attack)

#definir un class pour la momie
class Mummy(Monster):
    
    def __init__(self, game):
        super().__init__(game, "mummy", (130, 130))
        self.set_speed(3)
        self.point = 20

#definir un class pour l'alien
class Alien(Monster):
    
    def __init__(self, game):
        super().__init__(game, "alien", (300, 300), 140)
        self.point = 50
        self.hp = 250
        self.max_hp = 250
        self.attack = 20
        self.set_speed(1)
        
