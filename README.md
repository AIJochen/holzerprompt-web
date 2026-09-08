# HolzerPrompt Web

Eigenständige Django-Anwendung für die HolzerPrompt-Website und das schlanke CMS.

Die Website bleibt technisch von der CI-Machine getrennt. Beide Anwendungen verwenden Django/Python und werden später über eine definierte API miteinander verbunden.

## Lokale Entwicklung

```bash
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Standardadresse: `http://127.0.0.1:8000/`

## Umgebungsvariablen

Lokale und sensible Einstellungen werden in `.env` gespeichert. `.env` darf niemals in Git eingecheckt werden.

`.env.example` dokumentiert die benötigten Variablen ohne echte Geheimnisse.

Aktuell ausgelagert:

- `DJANGO_SECRET_KEY`
- `DJANGO_DEBUG`
- `DJANGO_ALLOWED_HOSTS`
- `DJANGO_CSRF_TRUSTED_ORIGINS`
- `CI_MACHINE_API_BASE_URL`
- `CI_MACHINE_API_TOKEN`

Später sollten auch produktive Datenbank-Zugangsdaten, SMTP-Zugangsdaten, Turnstile-Schlüssel und weitere externe API-Credentials ausschließlich über Umgebungsvariablen bzw. Secret Management gesetzt werden.

## Geplante Apps

```text
config/         Django-Konfiguration
website/        Öffentliche Website
cms/            Content-Management-Funktionen
integrations/   Externe Integrationen, insbesondere CI-Machine
```

Die CI-Machine selbst ist kein Bestandteil dieses Projekts.

## Testbetrieb

```text
dev-cim.de      → CI-Machine
hp.dev-cim.de   → HolzerPrompt Website
```

Beide Anwendungen können zunächst auf demselben Server laufen, bleiben aber durch getrennte Projekte, virtuelle Umgebungen, Gunicorn-Services und Datenbanken voneinander isoliert.
