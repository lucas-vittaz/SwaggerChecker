#!/bin/bash

if [ ! -d "venv" ]; then
    echo "Création de l'environnement virtuel..."
    python -m venv venv
else
    echo "L'environnement virtuel existe déjà."
fi

echo "Activation de l'environnement virtuel..."
if [ "$OSTYPE" == "msys" ] || [ "$OSTYPE" == "win32" ]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

echo "Installation des dépendances..."
pip install -r requirements.txt

echo "Configuration terminée. L'environnement virtuel est activé."
