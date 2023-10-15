# Récupérer le chemin absolu du script Bash en cours d'exécution
script_directory="$(dirname "$(dirname "$(dirname "$(realpath "$0")")")")"
echo "Chemin absolu du script Bash : $script_directory"
