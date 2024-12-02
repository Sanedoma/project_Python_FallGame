from importation import *
pygame.init()

#definir une clock
clock = pygame.time.Clock()
FPS = 60

#générer la fenetre de jeu
pygame.display.set_caption("emrys Fall")
screen = pygame.display.set_mode((1080, 720))
background = pygame.image.load('assets/bg.jpg')
banner = pygame.image.load('assets/banner.png')
banner = pygame.transform.scale(banner, (500,500))
banner_rect = banner.get_rect()
banner_rect.x = math.ceil(screen.get_width() / 4)

#bouton de lancement 
play_button = pygame.image.load('assets/button.png')
play_button = pygame.transform.scale(play_button, (400, 150))
play_button_rect = play_button.get_rect()
play_button_rect.x = math.ceil(screen.get_width() / 3.33)
play_button_rect.y = math.ceil(screen.get_height() / 2)
#charger le jeu
game = Game()

running = True

heal_message_timer = 0 
#Boucle pour ouvrir la fenetre
while running:
    #appliquer l'arriere plan
    screen.blit(background, (0,-200))
    
    if game.is_playing:
        if not game.is_paused:
            game.update(screen)
        else:
            # Afficher l'écran de pause
            pause_text = game.font.render("Jeu en pause. Appuyez sur 'entrer' ou 'esc' pour reprendre.", True, (0, 0, 0))
            text_rect = pause_text.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2))
            screen.blit(pause_text, text_rect)
    elif game.over:
        game.game_over(screen)
    else:
        screen.blit(play_button, play_button_rect)
        screen.blit(banner, (banner_rect.x, 0)) 
        
    #si le timeer est actif, afficher le message
    if heal_message_timer > pygame.time.get_ticks():
        cant_heal = game.font.render(
            "Vous n'avez pas suffisamment de points pour vous soigner", 
            True, 
            (255, 17, 17)
        )
        screen.blit(cant_heal, ((screen.get_width() / 4) - 20, (screen.get_height() / 2) + 50))

    #maj de l'ecran
    pygame.display.flip()
    
    #si le joueur ferme la fenetre
    for event in pygame.event.get():
        match event.type:
            case pygame.QUIT:
                running = False
                pygame.quit
                print('femeture de la fenetre')
            #detection de touch
            
            case pygame.KEYDOWN:
                game.perssed[event.key] = True
                #detecter si la touche est espace
                if event.key == pygame.K_SPACE :
                    game.player.launch_projectile()
                    if not game.is_playing:
                        #lancer le jeu
                        game.start()
                        game.sound_manager.playing('click')
                if event.key == pygame.K_p:
                    if game.score >= 200:
                        print('heal utiliser')
                        game.score -= 200
                        game.player.heal()
                    else:
                         # Démarrer le timer pour afficher le message pendant 5 secondes
                        heal_message_timer = pygame.time.get_ticks() + 2000
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_KP_ENTER:
                    if game.is_paused:
                        game.is_paused = False
                    else:
                        game.is_paused = True
                        
                    
            case pygame.KEYUP:
                game.perssed[event.key] = False
            
            case pygame.MOUSEBUTTONDOWN:
                #verification position de la souris
                if play_button_rect.collidepoint(event.pos) and game.is_playing is False:
                    #lancer le jeu
                    game.start()
                    game.sound_manager.playing('click')
    #fixer le nombre de fps sur la clock
    clock.tick(FPS)
    
    
