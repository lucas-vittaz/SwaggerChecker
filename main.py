from src.gui.user_interface import UserInterface

def main():
    """
    Point d'entrée principal de l'application Swagger Validator.

    Cette fonction initialise l'interface utilisateur en créant une instance
    de la classe `UserInterface`, puis lance la boucle principale de Tkinter.
    La boucle principale est responsable de maintenir l'application active,
    en attente des interactions de l'utilisateur.

    Fonctionnement:
    ---------------
    1. Crée une instance de `UserInterface`, qui configure et affiche l'interface graphique.
    2. Appelle `app.mainloop()` pour démarrer la boucle principale Tkinter,
       permettant à l'utilisateur d'interagir avec l'application.
    """
    app = UserInterface()
    
    app.mainloop()

if __name__ == "__main__":
    """
    Vérifie si le script est exécuté directement (et non importé comme un module).
    Si oui, appelle la fonction `main()` pour démarrer l'application.
    """
    main()