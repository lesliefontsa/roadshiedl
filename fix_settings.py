import os
import shutil

# Supprimer l'ancien fichier et renommer le nouveau
old_file = r"c:\Users\user\RoadShiel Sentinelle\backend\travel_agency\settings.py"
new_file = r"c:\Users\user\RoadShiel Sentinelle\backend\travel_agency\settings_fixed.py"

if os.path.exists(old_file):
    os.remove(old_file)

if os.path.exists(new_file):
    shutil.move(new_file, old_file)
    print("Fichier settings.py corrigé avec succès !")
else:
    print("Erreur: fichier settings_fixed.py non trouvé")