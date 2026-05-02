#!/usr/bin/env bash
# Run Lighthouse on all 7 routes. Outputs JSON to qa/2026-05-02-launch/lighthouse/.
set -e
BASE="${1:-http://localhost:8765}"
OUT="qa/2026-05-02-iteration-3/lighthouse"
mkdir -p "$OUT"

CHROME_PATH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
export CHROME_PATH

ROUTES=(index go-big fogo-live ride obrigado obrigado-go-big obrigado-orlando obrigado-financial-guide)

for r in "${ROUTES[@]}"; do
  echo "▶ Lighthouse: $r"
  node_modules/.bin/lighthouse "$BASE/$r.html" \
    --output=json \
    --output-path="$OUT/$r.json" \
    --only-categories=performance,accessibility,best-practices,seo \
    --quiet \
    --chrome-flags="--headless=new --no-sandbox" \
    --form-factor=mobile \
    --throttling-method=simulate \
    2>/dev/null || echo "  FAIL $r"
done

echo ""
echo "── Summary ──"
for r in "${ROUTES[@]}"; do
  if [ -f "$OUT/$r.json" ]; then
    node -e "
      const j = require('./$OUT/$r.json');
      const get = (k) => Math.round((j.categories[k]?.score || 0) * 100);
      console.log(['$r'.padEnd(22),
        'Perf ' + String(get('performance')).padStart(3),
        'A11y ' + String(get('accessibility')).padStart(3),
        'BP ' + String(get('best-practices')).padStart(3),
        'SEO ' + String(get('seo')).padStart(3)
      ].join(' | '));
    "
  else
    echo "$r: NO REPORT"
  fi
done
