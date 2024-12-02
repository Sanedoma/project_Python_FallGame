from importation import *

class AnimateSprite(pygame.sprite.Sprite):
    
    def __init__(self, sprite_name, size= (200, 200)):
        super().__init__()
        self.size = size
        self.image = pygame.image.load(f'assets/{sprite_name}.png')
        self.current_image = 0
        self.images = animation.get(sprite_name)
        self.animation = False
        self.image = pygame.transform.scale(self.image, self.size)
    #methode qui demare l'anim
    def start_animation(self):
        self.animation = True
    
    #methode pour animer le sprite
    def animate(self, loop=False):
        #verif si animation active
        if self.animation:
            #passer à l'image suivante
            self.current_image += 1
            #verif la fin de l'anim
            if self.current_image >= len(self.images):
                #revenir au debut
                self.current_image = 0
                if loop is False:
                    self.animation = False
                
            self.image = self.images[self.current_image]

def load_animation_images(sprite_name, size):
    images = []
    path = f"assets/{sprite_name}/{sprite_name}"
    
    for num in range(1, 24):
        image_path = path + str(num) + '.png'
        image = pygame.image.load(image_path)  # Charge l'image
        image = pygame.transform.scale(image, size)  # Redimensionne l'image
        images.append(image)  # Ajoute l'image redimensionnée à la liste
        
    return images
#dico qui contient les img charger
animation = {
    'mummy' : load_animation_images("mummy", (130, 130)),
    'player' : load_animation_images("player", (200, 200)),
    'alien' : load_animation_images("alien", (300, 300))
}