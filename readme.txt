Travel Blog - Un Blog de Călătorii Interactiv

Travel Blog este o aplicație web dezvoltată cu framework-ul Django, care oferă utilizatorilor o platformă pentru a descoperi destinații turistice prin articole detaliate, imagini și videoclipuri. Proiectul este conceput pentru a oferi o experiență modernă și prietenoasă utilizatorilor.

I. Funcționalități:
- Căutare avansată a articolelor după titlu.
- Posibilitatea de a integra imagini și videoclipuri relevante pentru fiecare articol.
- Administrarea articolelor prin intermediul unui panou de control dedicat.
- Design responsive pentru o utilizare optimă pe diferite dispozitive.

1. Instrucțiuni de Instalare

II. Cerințe preliminare:
Pentru a rula aplicația, este necesar să aveți instalate următoarele:
- Python 3.8+ (recomandat Python 3.10+)
- Un sistem de gestionare a mediului virtual Python (venv, pipenv sau altă soluție)

Instalare:
1. Crearea și activarea mediului virtual:
Pe Windows:
python -m venv venv
venv\Scripts\activate

Pe macOS/Linux:
python3 -m venv venv
source venv/bin/activate

2. Instalarea pachetelor necesare  
Rulați comanda pentru a instala dependențele din fișierul requirements.txt:
pip install -r requirements.txt

3. Configurarea bazei de date  
Aplicați migrațiile pentru a configura baza de date local:
python manage.py makemigrations
python manage.py migrate

4. Crearea unui superuser pentru accesul în panoul de administrare  
Rulați comanda și introduceți datele cerute:
python manage.py createsuperuser

5. Pornirea serverului local  
Porniți serverul local Django:
python manage.py runserver
Accesați aplicația la http://127.0.0.1:8000.

III. Structura Proiectului
- blog/: Aplicația principală care gestionează articolele și conținutul.
- static/: Fișiere statice, inclusiv CSS și imagini.
- templates/: Template-uri HTML pentru paginile aplicației.
- media/: Fișiere media încărcate, precum imagini sau videoclipuri.
- requirements.txt: Lista dependențelor proiectului.