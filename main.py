import pygame
from game import Game

import utils.constants as constant

def main():
    # Initialize all imported pygame modules / Initialise tous les modules pygame importés 
    pygame.init()
    # Set the width and height of the screen [width, height] / Réglez la largeur et la hauteur de l'écran [width, height].
    screen = pygame.display.set_mode((constant.SCREEN_WIDTH, constant.SCREEN_HEIGHT))
    # Set the current window caption / Définit la légende de la fenêtre actuelle
    pygame.display.set_caption("PACMAN")
    # Loop until the user clicks the close button. / Boucle jusqu'à ce que l'utilisateur clique sur le bouton de fermeture.
    done = False
    # Used to manage how fast the screen updates / Permet de gérer la vitesse de mise à jour de l'écran
    clock = pygame.time.Clock()
    # Create a game object / Créer un élément de jeu
    game = Game()
    # -------- Main Program Loop / Boucle de jeu principale -----------
    while not done:
        # --- Process events (keystrokes, mouse clicks, etc) / Traiter les événements (frappes au clavier, clics de souris, etc.)
        done = game.process_events()
        # --- Game logic should go here / La logique du jeu
        game.run_logic()
        # --- Draw the current frame / Dessine le cadre
        game.display_frame(screen)
        # --- Limit to 30 frames per second / Limitation à 30 images par seconde
        clock.tick(30)
        #tkMessageBox.showinfo("GAME OVER!","Final Score = "+(str)(GAME.score))
    # Close the window and quit. / Ferme la fenêtre et quitte.
    # If you forget this line, the program will 'hang' / Si vous oubliez cette ligne, le programme se bloquera.
    # on exit if running from IDLE. / à la sortie si l'exécution se fait depuis IDLE.
    pygame.quit()

if __name__ == '__main__':
    main()
