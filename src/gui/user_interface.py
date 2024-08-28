import tkinter as tk
import os
from tkinter import filedialog, messagebox, scrolledtext

from src.validators.openapi.openapi_validator import OpenAPIValidator
from src.validators.projet.projet_rules_validator import ProjetRulesValidator
from src.utils.swagger_loader import load_swagger

class UserInterface(tk.Tk):
    """
    Classe représentant l'interface utilisateur pour le validateur Swagger.

    Cette classe hérite de `tk.Tk` et crée une interface graphique permettant à l'utilisateur
    d'importer un fichier Swagger et de le valider selon les normes OpenAPI et les règles
    définies pour le projet.

    Attributs:
    ----------
    swagger_dict : dict
        Contient le fichier Swagger chargé sous forme de dictionnaire.
    swagger_file_path : str
        Chemin vers le fichier Swagger importé.
    swagger_text : str
        Contenu du fichier Swagger sous forme de chaîne de caractères.
    upload_button : tk.Button
        Bouton pour importer le fichier Swagger.
    validate_button : tk.Button
        Bouton pour valider le fichier Swagger.
    result_text : scrolledtext.ScrolledText
        Zone de texte défilante pour afficher les résultats de la validation.
    
    Méthodes:
    ---------
    upload_file():
        Ouvre une boîte de dialogue pour sélectionner un fichier Swagger (JSON ou YAML),
        charge le contenu et le convertit en dictionnaire.
    
    validate_swagger():
        Valide le fichier Swagger importé contre les normes OpenAPI et les règles du projet.
        Affiche les résultats de la validation dans la zone de texte.
    """

    def __init__(self):
        """
        Initialise l'interface utilisateur avec les boutons et la zone de texte.
        """
        super().__init__()

        # Configurer la fenêtre principale
        self.title("Swagger Validator")
        self.geometry("1000x1000")
        self.swagger_dict = None
        self.swagger_file_path = None
        self.swagger_text = None

        # Bouton pour importer le fichier Swagger
        self.upload_button = tk.Button(self, text="Importer Swagger", command=self.upload_file, height=2, width=20)
        self.upload_button.pack(pady=10)

        # Bouton pour valider le fichier Swagger
        self.validate_button = tk.Button(self, text="Valider", command=self.validate_swagger, height=2, width=20)
        self.validate_button.pack(pady=10)

        # Zone de texte pour afficher les résultats
        self.result_text = scrolledtext.ScrolledText(self, wrap=tk.WORD, height=30, width=120)
        self.result_text.pack(pady=10)

        # Configurer les tags pour le style du texte
        self.result_text.tag_configure("success", foreground="green")
        self.result_text.tag_configure("error", foreground="red")

    def upload_file(self):
        """
        Ouvre une boîte de dialogue pour sélectionner un fichier Swagger.

        Cette méthode charge le fichier Swagger sélectionné, que ce soit en JSON ou en YAML,
        et le convertit en dictionnaire. Le contenu du fichier est également stocké en tant que
        chaîne de caractères pour un accès facile lors de la validation.
        """
        self.swagger_file_path = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json"), ("YAML Files", "*.yaml"), ("YML Files", "*.yml")])
        if self.swagger_file_path:
            try:
                with open(self.swagger_file_path, 'r') as file:
                    self.swagger_text = file.read()
                    self.swagger_dict = load_swagger(self.swagger_file_path)
                    swagger_name = os.path.basename(self.swagger_file_path)
                self.result_text.insert(tk.END, f"Fichier importé avec succès: {swagger_name}\n\n", "success")
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible de charger le fichier Swagger : {str(e)}")

    def validate_swagger(self):
        """
        Valide le fichier Swagger importé contre les normes OpenAPI et les règles du projet.

        Cette méthode utilise les classes `OpenAPIValidator` et `ProjetRulesValidator` pour vérifier
        la conformité du fichier Swagger aux normes OpenAPI et aux règles spécifiques du projet.
        Les résultats de la validation sont affichés dans la zone de texte. Les messages d'erreur
        sont affichés en rouge, et les messages de succès en vert. Un double retour à la ligne est ajouté
        entre chaque erreur pour une meilleure lisibilité.
        """
        if not self.swagger_dict:
            messagebox.showwarning("Attention", "Veuillez d'abord importer un Swagger.")
            return

        self.result_text.delete(1.0, tk.END)  # Effacer le texte précédent

        # Validation OpenAPI
        openapi_validator = OpenAPIValidator(self.swagger_dict, self.swagger_text)
        openapi_valid, openapi_message = openapi_validator.validate()

        if openapi_valid:
            self.result_text.insert(tk.END, "Le swagger est conforme aux normes OpenAPI.\n\n", "success")
        else:
            self.result_text.insert(tk.END, f"Erreur OpenAPI :\n{openapi_message}\n\n", "error")

        # Validation des règles du projet
        project_validator = ProjetRulesValidator(self.swagger_dict, self.swagger_text)
        project_valid, project_message = project_validator.validate()

        if project_valid:
            self.result_text.insert(tk.END, "Le Swagger est conforme aux normes du Projet.\n", "success")
        else:
            # Ajout d'un double retour chariot entre chaque erreur
            formatted_message = "\n\n".join(project_message.split("\n"))
            self.result_text.insert(tk.END, f"Erreur, le swagger n'est pas conforme aux normes du projet :\n {formatted_message}\n", "error")

        if openapi_valid and project_valid:
            messagebox.showinfo("Validation", "Swagger est valide selon les normes OpenAPI et les règles du projet.")

if __name__ == "__main__":
    app = UserInterface()
    app.mainloop()
