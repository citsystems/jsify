#!/bin/bash

FOLDERS=('source')
GPT_DIR="../gpt"
PATTERNS=('*.rst')
EXCLUDED_DIRS=('node_modules' '.git' '.idea' '.vscode' '__pycache__')

mkdir -p "$GPT_DIR"

# Tworzymy opcje do find -prune dla wykluczonych katalogów
PRUNE_OPTS=()
for excl in "${EXCLUDED_DIRS[@]}"; do
    PRUNE_OPTS+=( -name "$excl" -prune -o )
done

for dir in "${FOLDERS[@]}"; do
  for pattern in "${PATTERNS[@]}"; do
    EXT="${pattern##*.}"
    OUT="$GPT_DIR/Dokumentacja Jsify - $(basename "$dir").batch.$EXT"

    # Szukamy plików z wykluczeniem katalogów z EXCLUDED_DIRS
    FILES=()
    while IFS= read -r -d $'\0' file; do
      FILES+=("$file")
    done < <(
      find "$dir" \
        "${PRUNE_OPTS[@]}" \
        -type f -name "$pattern" -print0
    )

    if [ "${#FILES[@]}" -eq 0 ]; then
      continue
    fi

    echo "This is a library archive containing multiple files." > "$OUT"
    echo "Each file starts with a line *** [ relative path of file ] ***" >> "$OUT"
    echo "" >> "$OUT"

    for f in "${FILES[@]}"; do
      echo "*** [${f#./}] ***" >> "$OUT"
      cat "$f" >> "$OUT"
      echo "" >> "$OUT"
    done
  done
done
