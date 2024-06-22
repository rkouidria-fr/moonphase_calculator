"""
Ce module fournit un calculateur pour visualiser les phases de la lune à une
date donnée. Il utilise la bibliothèque ephem pour calculer la phase de la lune
et affiche une représentation graphique de la lune en fonction de sa phase.
"""

from datetime import datetime
from tkinter import ttk
import tkinter as tk
import ephem

def get_moon_phase(date: str) -> str:
    """
    Récupère la phase de la lune pour une date donnée

    Args:
        date (str): la date pour laquelle la phase de la lune doit être calculée

    Returns:
        str: la phase de la lune correspondante à la date donnée.
    """
    # Création de l'observateur et de l'objet Lune
    observer = ephem.Observer()
    observer.date = date
    lune = ephem.Moon(observer)

    # Calcul de la phase lunaire en pourcentage
    phase_lunaire = lune.phase
    return phase_lunaire

def draw_moon(phase: float) -> None:
    """
    Dessine une représentation graphique de la Lune en fonction de sa phase

    Args:
        phase (float): représente le pourcentage d'obscurité de la Lune à tracer

    """
    canvas.delete("all")

    # Calculer l'éclairement de la Lune
    phase_ratio = phase / 100.0
    if phase_ratio <= 0.5:
        illumination = 1 - (phase_ratio * 2)
    else:
        illumination = (phase_ratio - 0.5) * 2

    # Dessiner la pleine lune
    canvas.create_oval(50, 50, 250, 250, fill='white', outline='gray')

    # Dessiner l'ombre
    if illumination < 1:
        if phase_ratio <= 0.5:
            canvas.create_oval(50, 50, 50 + 200 * illumination, 250,
                               fill='black', outline='gray')
        else:
            canvas.create_oval(50 + 200 * (1 - illumination), 50, 250, 250,
                               fill='black', outline='gray')

def update_phase() -> None:
    """
    Mets à jour la visualisation de la lune en fonction de la date entrée par
    l'utilisateur.
    cette fonction est appelée suite à l'appuis sur le bouton "Mettre à jour".
    Elle récupère alors la valeur saisie dans l'input et màj le dessin.

    Returns:
        None
    Raises:
        ValueError: si la date entrée n'est pas au format JJ-MM-AAAA
    """
    date_str = date_to_use.get()  # récupère la date saisie
    try:
        date = datetime.strptime(date_str.replace('/', '-'), '%d-%m-%Y')
        phase = get_moon_phase(date)
        phase_label.config(text=f'Obscurité: {phase:.2f}%')
        draw_moon(phase)
    except ValueError:
        phase_label.config(text='Format de date invalide. Utilisez JJ-MM-AAAA.')

# Configuration de l'interface utilisateur
root = tk.Tk()
root.title("Visualisation des phases de la lune")

# Label et entrée pour la date
ttk.Label(root, text="Entrez la date (JJ-MM-AAAA):").grid(column=0, row=0, padx=10, pady=10)
date_to_use = ttk.Entry(root)
date_to_use.grid(column=1, row=0, padx=10, pady=10)

# Bouton pour mettre à jour la phase de la Lune
maj_btn = ttk.Button(root, text="Mettre à jour", command=update_phase)
maj_btn.grid(column=0, row=1, columnspan=2, padx=10, pady=10)

# Label pour afficher la phase de la Lune
phase_label = ttk.Label(root, text="Phase de la Lune: ")
phase_label.grid(column=0, row=2, columnspan=2, padx=10, pady=10)

# Canvas pour dessiner la Lune
canvas = tk.Canvas(root, width=300, height=300, bg='black')
canvas.grid(column=0, row=3, columnspan=2, padx=10, pady=10)

# Lancer l'application
root.mainloop()
