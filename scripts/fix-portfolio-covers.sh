#!/usr/bin/env bash
# Fix portfolio covers: rebuild backend+frontend, reload nginx, ensure cases loaded.
set -Eeuo pipefail
cd "$(dirname "$0")/.."

echo "==> Rebuild backend (media URL fix)"
docker compose build backend
docker compose up -d --force-recreate backend

echo "==> Ensure real portfolio cases + covers"
docker compose exec -T backend python manage.py load_real_portfolio_cases
docker compose exec -T backend python manage.py shell -c '
from apps.website.models import PortfolioProject
keep = {"luxmeb", "rudwood", "elvet-group", "notarius-korneenkova"}
order = ["luxmeb", "rudwood", "elvet-group", "notarius-korneenkova"]
for i, slug in enumerate(order, start=1):
    p = PortfolioProject.objects.get(slug=slug)
    p.status = "published"
    p.featured = True
    p.sort_order = i
    p.save(update_fields=["status", "featured", "sort_order"])
PortfolioProject.objects.exclude(slug__in=keep).update(status="draft", featured=False)
print("published:", list(PortfolioProject.objects.filter(status="published").order_by("sort_order").values_list("slug", flat=True)))
'

echo "==> Rebuild frontend (cover URL handling)"
docker compose build frontend
docker compose up -d --force-recreate frontend

echo "==> Reload nginx (media proxy + Host header)"
docker compose restart nginx
sleep 2

echo "==> Check API covers"
curl -s -H "Host: localhost:8080" "http://127.0.0.1:${HTTP_PORT:-8080}/api/v1/website/portfolio/" \
  | python3 -c 'import sys,json; d=json.load(sys.stdin); items=d.get("data") or d
print("count", len(items))
for i,x in enumerate(items,1):
    print(i, x["title"], x.get("coverImage"))'

COVER=$(curl -s -H "Host: localhost:8080" "http://127.0.0.1:${HTTP_PORT:-8080}/api/v1/website/portfolio/" \
  | python3 -c 'import sys,json; d=json.load(sys.stdin); items=d.get("data") or d; print(items[0].get("coverImage") or "")')
if [[ -n "$COVER" ]]; then
  if [[ "$COVER" == /* ]]; then COVER="http://127.0.0.1:${HTTP_PORT:-8080}${COVER}"; fi
  echo "==> Cover HTTP:"
  curl -sI -H "Host: localhost:8080" "$COVER" | head -5
fi

echo "Done. Open http://localhost:${HTTP_PORT:-8080}/#portfolio"
