from importation import *
from monster import *
from comet_event import CometFallEvent
from sounds import * 
#class du jeu
class Game:
    def __init__(self):
        #in game ?
        self.is_playing = False
        #pause?
        self.is_paused = False
        #game over
        self.over = False
        #charger le joueur
        self.all_players = pygame.sprite.Group()
        self.player = Player(self)
        self.all_players.add(self.player)
        self.perssed = {}
        self.all_monsters = pygame.sprite.Group()
        self.comet_event = CometFallEvent(self)
        self.score = 0
        self.font = pygame.font.Font("assets/LibreBaskerville-Bold.ttf", 25)
        self.sound_manager = SoundManager()
        
    def add_score(self, point):
        self.score += point
        print(f"+{point}/ score actuelle: {self.score}")
    
    def start(self):
        self.is_playing =  True
        print('game on')
        self.spawn_monster(Mummy)
        self.spawn_monster(Mummy)
        self.spawn_monster(Alien)
        
    def game_over(self, screen):
        # Réinitialiser les variables du jeu
        self.is_playing = False
        self.over = True
        self.all_monsters = pygame.sprite.Group()
        self.comet_event.all_comets = pygame.sprite.Group()
        self.comet_event.percent = 0 
        self.score = 0
        self.player.health = self.player.max_health
        

        # Afficher l'écran "Game Over"
        game_over_text = self.font.render("GAME OVER", True, (255, 0, 0))
        text_rect = game_over_text.get_rect(center=(screen.get_width() / 2, screen.get_height() / 4))
        screen.blit(game_over_text, text_rect)

        # Boutons
        button_continue = pygame.image.load('assets/continue.png')
        button_continue = pygame.transform.scale(button_continue, (200, 80))
        button_continue_rect = button_continue.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2 - 50))
        screen.blit(button_continue, button_continue_rect)

        button_quit = pygame.image.load('assets/abandon.png')
        button_quit = pygame.transform.scale(button_quit, (200, 80))
        button_quit_rect = button_quit.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2 + 100))
        screen.blit(button_quit, button_quit_rect)

        # Gestion des clics
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_continue_rect.collidepoint(event.pos):
                    # Rejouer
                    self.start()
                elif button_quit_rect.collidepoint(event.pos):
                    # Quitter
                    #pygame.quit()
                    #exit()
                    self.over = False
        
    def update(self, screen):
        #afficher le score
        score_text = self.font.render(f'score: {str(self.score)}', 1, (0, 0, 0))
        screen.blit(score_text, (20, 20))        
        #appliquer le joueur
        screen.blit(self.player.image, self.player.rect)
        #bar de vie du joueur
        self.player.update_health_bar(screen) 
        if self.player.health <= 0:
            print("game over")
            self.game_over(screen)
            self.sound_manager.playing('game_over')       
        #animation du joueur
        self.player.update_animation()
        
        #verife si il camp
        if not self.player.mobil:
            self.player.imobilTime += 1 / 60  # Assume 60 FPS
        else:
            self.player.imobilTime = 0
            self.player.mobil = False
        
        self.comet_event.anti_camp()
        
        #actualiser la bar d'event
        self.comet_event.update_bar(screen)        
        
        #appliquer les Projectile
        self.player.all_projectiles.draw(screen)
        #Recuperer les projectile du joueur
        for project in self.player.all_projectiles:
            project.move()
        #créé les monstres
        
        #appliquer les monstres
        self.all_monsters.draw(screen)
        #recup des monstres
        for monster in self.all_monsters:
            monster.forward()
            monster.update_hp_bar(screen)
            monster.update_animate(screen)
  
        #appliquer les cometes
        self.comet_event.all_comets.draw(screen)
        
        #recup des cometes du jeu
        for comet in self.comet_event.all_comets:
            comet.fall()
        
        if self.perssed.get(pygame.K_RIGHT) and self.player.rect.x + self.player.rect.width < screen.get_width():
            self.player.move_rigth()
        elif self.perssed.get(pygame.K_LEFT) and self.player.rect.x > 0:
            self.player.move_left()
        
    def check_collision(self, sprite, group):
        return pygame.sprite.spritecollide(sprite, group, False, pygame.sprite.collide_mask)
    def spawn_monster(self, monster_class_name):
        try:
            monster = monster_class_name(self)
            self.all_monsters.add(monster)
            print(f"Spawned monster: {monster_class_name.__name__} at position {monster.rect.x}, {monster.rect.y}")
        except Exception as e:
            print(f"Error spawning monster {monster_class_name.__name__}: {e}")
