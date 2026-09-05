## Was

<!-- Ein bis zwei Saetze: was aendert sich, aus Sicht des Betreibers. -->

## Warum

<!-- Welches Problem loest das. Bei einem Fix: was war kaputt. -->

## Wie geprueft

- [ ] `python3 -m py_compile update.py`
- [ ] `python3 -m unittest discover -s tests -v`
- [ ] `python3 tools/check_data.py`
- [ ] `python3 tools/check_html.py`
- [ ] `/dashboard-preview` (nur wenn `docs/index.html` geaendert wurde)

## Unveraendert geblieben

- [ ] `docs/data.json` (schreibt der Bot)
- [ ] `.github/workflows/update.yml`
- [ ] `HANDLES` in `update.py`

<!-- Falls eins davon doch angefasst wurde: hier begruenden. -->
