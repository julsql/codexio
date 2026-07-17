#!/usr/bin/env bash
#
# Backup codexio — archive les images utilisateur (dédicaces, exlibris, etc.).
# Pas de dump de la base : les données codexio sont facilement régénérables,
# seules les images uploadées sont précieuses.
#
# Usage (sur le VPS, typiquement via cron) :
#   BACKUP_DIR=/backup/current ./scripts/backup.sh
#
# Variables d'environnement :
#   BACKUP_DIR  répertoire de sortie          (défaut: /backup/current)
#   RETENTION   nb d'archives à conserver      (défaut: 7)
#
set -euo pipefail
export PATH="/usr/local/bin:/usr/bin:/bin:${PATH:-}"

APP="codexio"
BACKUP_DIR="${BACKUP_DIR:-/backup/current}"
RETENTION="${RETENTION:-7}"

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MEDIA_DIR="$REPO_ROOT/src/media"
STAMP="$(date +%Y%m%d_%H%M%S)"

mkdir -p "$BACKUP_DIR"

if [ ! -d "$MEDIA_DIR" ]; then
  echo "[$APP] ERREUR : dossier media introuvable ($MEDIA_DIR)" >&2
  exit 1
fi

echo "[$APP] Archive des images -> ${APP}_images_${STAMP}.tar.gz"
tar -czf "$BACKUP_DIR/${APP}_images_${STAMP}.tar.gz" -C "$REPO_ROOT/src" media

# Rétention : ne garder que les RETENTION archives les plus récentes
find "$BACKUP_DIR" -maxdepth 1 -type f -name "${APP}_images_*.tar.gz" -printf '%T@ %p\n' \
  | sort -rn | tail -n +$((RETENTION + 1)) | cut -d' ' -f2- | xargs -r rm -f

echo "[$APP] Termine -> $BACKUP_DIR"
