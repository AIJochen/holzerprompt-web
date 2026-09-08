# Welche Einstellungen gehören nicht fest in `settings.py`?

Grundregel: Alles, was geheim, umgebungsabhängig oder deployment-spezifisch ist, sollte nicht als realer Wert im Quellcode stehen.

## Bereits ausgelagert

| Einstellung | Grund |
|---|---|
| `DJANGO_SECRET_KEY` | kryptografisches Geheimnis |
| `DJANGO_DEBUG` | unterscheidet Development und Production |
| `DJANGO_ALLOWED_HOSTS` | domainspezifisch |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | domainspezifisch |
| `CI_MACHINE_API_BASE_URL` | umgebungsabhängiger Endpunkt |
| `CI_MACHINE_API_TOKEN` | geheimes API-Credential |

## Später ebenfalls auslagern

Für PostgreSQL: `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`.

Für E-Mail: `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `EMAIL_USE_TLS`, `DEFAULT_FROM_EMAIL`.

Für externe Dienste: `TURNSTILE_SITE_KEY`, `TURNSTILE_SECRET_KEY`, Analytics-IDs und weitere API-Schlüssel oder Tokens.

## Was darf in `settings.py` bleiben?

Struktur- und Anwendungsentscheidungen wie `INSTALLED_APPS`, `MIDDLEWARE`, Template-Konfiguration, Sprache und Zeitzone, Static-/Media-Pfade, Passwort-Validatoren und sichere Standardwerte.

## Serverbetrieb

`.env` ist primär für die lokale Entwicklung gedacht. Auf dem späteren Server können dieselben Variablen über eine geschützte Environment-Datei für systemd/Gunicorn oder ein Secret-Management-System gesetzt werden.
