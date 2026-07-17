# Cashflow Compass

A personal-finance tracker for Android, built with **Kivy / KivyMD** and packaged
as an APK with Buildozer. Record income and expenses, organize them by account
and category, set budgets, and view spending analysis on a custom calendar and
matplotlib charts — all backed by local SQLite storage.

[![Build APK](https://github.com/VaigandlaHemanth/Cashflow-Compass-app/actions/workflows/build.yml/badge.svg)](https://github.com/VaigandlaHemanth/Cashflow-Compass-app/actions)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## Features

- **Transactions** — add records with category, account, amount, type, and date.
- **Budgets** — set and track budgets per category.
- **Categories & accounts** — manage your own lists.
- **Analysis** — matplotlib charts (via the kivy-garden backend) and a custom
  `AdvancedCalendar` widget for date-based views.
- **Local persistence** — SQLite; the schema is created on first run.
- **Android packaging** — `buildozer.spec` + a GitHub Actions workflow that
  builds the APK.

## Project layout

```
main.py              App shell + screen manager (entry point)
records.py           Add-transaction screen
budgetapp.py         Budgeting component
category.py          Category management
accountapp.py        Account management
analysis.py          Charts / analysis view
advancedcalender.py  Custom calendar widget
the_graph.py         Matplotlib graph rendering
viewsqlite.py        SQLite helpers (connection, table, insert, select)
circle_button.py     Circular button widget
libs/garden/         Vendored kivy-garden matplotlib backend
buildozer.spec       Android build config
```

## Run it (desktop)

```bash
pip install -r requirements.txt
python main.py
```

The SQLite database is created automatically on first run (it is gitignored).

## Build the Android APK

```bash
pip install buildozer
buildozer -v android debug
```

or let the GitHub Actions workflow (`.github/workflows/build.yml`) build it on push.

## Notes

- Local-only app: all data stays in an on-device SQLite database.
- Charts use the kivy-garden matplotlib backend, vendored under `libs/garden/`.

## License

Released under the [MIT License](LICENSE).
