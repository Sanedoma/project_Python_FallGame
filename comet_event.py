from importation import * 
from comet import Comet

#class pour gerer l'event
class CometFallEvent:
    
    #lors du chargement -> créé un conmpteur
    def __init__(self, game):
        self.percent = 0
        self.percent_speed = 10  
        #groupe de cometes
        self.all_comets = pygame.sprite.Group()
        self.game = game
        self.fall_mode = False
        
    def meteor_fall(self):
        for i in range(1, 10):
            self.all_comets.add(Comet(self))
        
    def add_percent(self):
        self.percent += self.percent_speed / 100
        
    def attempt_fall(self):
        #la jauge d'evenement est totalement charger
        if self.is_full_load() and len(self.game.all_monsters) == 0:
            print('lancement de la pluie de cometes ...')
            self.meteor_fall()
            self.fall_mode = True           
    
    def is_full_load(self): 
        return self.percent >= 100
        
    def update_bar(self, surface):
        self.add_percent()        
        
        #bar d'arriere plan
        pygame.draw.rect(surface, (0, 0, 0), [ 0, surface.get_height() - 20, surface.get_width(), 20])
        #jauge de l'event
        pygame.draw.rect(surface, (187, 11, 11), [ 0, surface.get_height() - 20, (surface.get_width() / 100) * self.percent, 20])
        
    def anti_camp(self):
        # Si le joueur reste immobile pendant trop longtemps
        if not self.game.player.mobil and self.game.player.imobilTime >= 5:
            print("Anti-camp activé : le joueur est immobile depuis trop longtemps.")
            for i in range(1, 100):
                comet = Comet(self)
                comet.rect.x = self.game.player.rect.x
                self.all_comets.add(comet)
                # Réinitialisation des compteurs
                self.game.player.imobilTime = 0
