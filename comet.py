from importation import *
import random
from monster import *
#Créé les cometes
class Comet(pygame.sprite.Sprite):
    
    def __init__(self, comet_event):
        super().__init__()
        self.image = pygame.image.load('assets/comet.png')
        self.rect = self.image.get_rect()
        self.velocity = random.randint(1, 2)
        self.rect.x = random.randint(15, 940)
        self.rect.y = random.randint(-150 , 10)
        self.dgt = random.randint(1000, 2000)
        self.size = self.dgt / 10
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.comet_event = comet_event
    
    def remove(self):
        self.comet_event.all_comets.remove(self)
        self.comet_event.game.sound_manager.playing('meteorite')
        #verif si nb de comet est de 0
        if len(self.comet_event.all_comets) == 0:
            print("fin de l'event")
            #bar a 0
            self.comet_event.percent = 0
            #invoque les monstres
            self.comet_event.game.start()
            
    def fall(self):
        self.rect.y += self.velocity
        #touce le sol?
        if self.rect.y >= 510:
            print("sol")
            self.remove()
            #si il n'y a pplus de boule?
            if len(self.comet_event.all_comets) == 0:
                print("fin de l'event")
                # reset la jauge
                self.comet_event.percent = 0
                self.comet_event.fall_mode = False  

        if self.comet_event.game.check_collision(self,self.comet_event.game.all_players):
            print('joueur toucher')
            self.remove()
            self.comet_event.game.player.damage(self.dgt)