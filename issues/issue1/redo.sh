#!/bin/bash
# Regenerate all temp files and diff to produce log3.diff.
#   step1.py: temp_shs_0.txt (CDSL) → temp_shs_1.txt (corrected)
#   step2.py: shs-AB.txt          → temp_shs_2.txt (AB baseline)
#   temp_shs_3.txt = copy of temp_shs_2.txt
#   log3.diff   = diff temp_shs_1.txt temp_shs_3.txt

SELF_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "=== Step 1: temp_shs_0.txt → temp_shs_1.txt (CDSL-derived, all fixes) ==="
python3 "$SELF_DIR/step1.py"

echo ""
echo "=== Step 2: shs-AB.txt → temp_shs_2.txt (AB-derived, minimal transforms) ==="
python3 "$SELF_DIR/step2.py"

echo ""
echo "=== Step 3: Copy temp_shs_2.txt → temp_shs_3.txt ==="
cp "$SELF_DIR/temp_shs_2.txt" "$SELF_DIR/temp_shs_3.txt"
echo "Done."

echo ""
echo "=== Step 4: Diff temp_shs_1.txt vs temp_shs_3.txt → log3.diff ==="
diff "$SELF_DIR/temp_shs_1.txt" "$SELF_DIR/temp_shs_3.txt" > "$SELF_DIR/log3.diff" 2>&1
echo "log3.diff: $(wc -l < "$SELF_DIR/log3.diff") lines"

echo ""
echo "=== Summary ==="
wc -l "$SELF_DIR/temp_shs_0.txt"
wc -l "$SELF_DIR/temp_shs_1.txt"
wc -l "$SELF_DIR/temp_shs_2.txt"
wc -l "$SELF_DIR/temp_shs_3.txt"
wc -l "$SELF_DIR/log3.diff"
