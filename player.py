from importation import *
from projectile import Projectile
import animation

#player class
class Player(animation.AnimateSprite):
    
    def __init__(self, game):
        super().__init__("player")
        self.game = game
        self.health = 10000
        self.max_health = 10000
        self.attack = 20
        self.fixAttack = 20
        self.all_projectiles = pygame.sprite.Group()
        self.fixVelocity = 2
        self.velocity = 2
        self.rect = self.image.get_rect()
        self.rect.x = 400
        self.rect.y = 500
        self.mobil = False
        self.imobilTime = 0
        self.kaioken = False
    
    def heal(self):
        if self.health + 800 < self.max_health:
            self.health += 800
        else: 
            self.health = self.max_health 
        
    def damage(self, dgt):
    #infliger les dgt
        if self.health >= 0:
            self.health -= dgt
            print(f"dégât reçu: {dgt} / nouvelle vie restante: {self.health}")
        else:
            print('game over')
    
    def update_health_bar(self, surface):
        #definir la bar de health       
        pygame.draw.rect(surface, (104, 11, 103), [self.rect.x + 50, self.rect.y + 20, self.max_health / 100, 3])
        pygame.draw.rect(surface, (88, 255, 51), [self.rect.x + 50, self.rect.y + 20, self.health / 100, 3])
        
    def launch_projectile(self):
        self.start_animation()
        print('tire')
        self.all_projectiles.add(Projectile(self))
        self.game.sound_manager.playing('tir')
        
    def move_rigth(self):
        #si pas de colision
        if not self.game.check_collision(self, self.game.all_monsters):
            self.rect.x += self.velocity
            self.mobil = True
        
    def move_left(self):
        self.rect.x -= self.velocity
        self.mobil =True
        
    def update_animation(self):
        self.animate()
        
    def kaioken_mode(self):
        if self.kaioken == False:
            self.kaioken = True
            self.velocity += 50
            self.attack *= 30
    def normal_mode(self):
        if self.kaioken == True:
            self.kaioken = False
            self.velocity = self.fixVelocity
            self.attack = self.fixAttack