#!/bin/bash
cd /home/ubuntu/alg-website

echo "=== 1. TAA/BAA/Made-in-USA in trackstar ==="
grep -n "TAA\|BAA\|Made.in.USA\|Made.in.Mexico" public/products/trackstar/index.html | grep -v "<!--" | head -40

echo ""
echo "=== 2. Internal notes in trackstar (rendered copy only) ==="
grep -n "CFG-\|heads up:\|NOTE:\|datasheet pg\|per Rebate Center" public/products/trackstar/index.html | grep -v "<!--" | head -30

echo ""
echo "=== 3. Solstice/LCDL in trackstar ==="
grep -n "Solstice\|LCDL\|solstice" public/products/trackstar/index.html | grep -v "<!--" | head -30

echo ""
echo "=== 4. Tier badge in trackstar ==="
grep -n "tier-badge\|tier-eco\|tier-pro\|ECO.*badge\|PRO.*badge" public/products/trackstar/index.html | head -10

echo ""
echo "=== 5. Orphaned -tier fragments ==="
grep -n "\-tier " public/products/trackstar/index.html | grep -v "<!--" | head -20

echo ""
echo "=== 6. Family card truncated nouns ==="
grep -n "Commercial \.\|Can-Less Commercial\|Adjustable Architectural Commercial" public/products/trackstar/index.html | grep -v "<!--" | head -10

echo ""
echo "=== REPO-WIDE: CFG- in rendered copy ==="
grep -rn "CFG-" public/products/ --include="*.html" | grep -v "<!--" | head -30

echo ""
echo "=== REPO-WIDE: heads up: in rendered copy ==="
grep -rn "heads up:" public/products/ --include="*.html" | grep -v "<!--" | head -20

echo ""
echo "=== REPO-WIDE: NOTE: in rendered copy ==="
grep -rn "NOTE:" public/products/ --include="*.html" | grep -v "<!--" | head -20

echo ""
echo "=== REPO-WIDE: Cross-product SKU contamination matrix ==="
echo "--- LCDL outside /solstice/ ---"
grep -rn "LCDL" public/products/ --include="*.html" | grep -v "solstice" | grep -v "<!--" | head -20
echo "--- LTRK outside /trackstar/ ---"
grep -rn "LTRK" public/products/ --include="*.html" | grep -v "trackstar" | grep -v "<!--" | head -20
echo "--- Solstice (word) outside /solstice/ ---"
grep -rn "Solstice" public/products/ --include="*.html" | grep -v "solstice" | grep -v "<!--" | head -20
echo "--- Illuminator outside /illuminator/ (sanity check) ---"
grep -rn "Illuminator" public/products/ --include="*.html" | grep -v "illuminator" | grep -v "<!--" | head -10
