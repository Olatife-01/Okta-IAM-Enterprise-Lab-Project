mkdir -p image-backup
find . -type f \( -iname "*.png" -o -iname "*.jpg" -o -iname "*.jpeg" -o -iname "*.gif" -o -iname "*.svg" -o -iname "*.bmp" -o -iname "*.webp" \) -exec cp --parents {} image-backup/ \;
