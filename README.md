# PAI_Project

## Overview

**PAI_Project** este o aplicație web dezvoltată cu Django, destinată automatizării utilităților casnice. Proiectul permite controlul dispozitivelor precum iluminatul și aerul condiționat printr-o interfață web, oferind și feedback asupra stării dispozitivelor conectate. Integrarea cu Arduino facilitează interacțiunea directă cu componentele hardware.

---

## Structura Proiectului

```plaintext
pai_project/
├── PAI_APP/               # Aplicația principală Django
│   ├── __init__.py        # Marchează directorul ca un modul Python
│   ├── settings.py        # Configurațiile globale ale proiectului
│   ├── urls.py            # Definirea rutelor URL principale
│   ├── wsgi.py            # Configurație pentru serverul WSGI
│   ├── asgi.py            # Configurație pentru serverul ASGI (opțional)
│
├── apps/                  # Aplicațiile specifice funcționalităților
│   ├── main/              # Aplicația pentru interfața utilizator
│   │   ├── admin.py       # Configurarea panoului de administrare
│   │   ├── apps.py        # Configurații specifice aplicației
│   │   ├── models.py      # Modele pentru baza de date
│   │   ├── views.py       # Logica principală a aplicației
│   │   ├── urls.py        # Rutele URL specifice aplicației
│   │   ├── templates/     # Șabloanele HTML
│   │   ├── static/        # Fișiere CSS și JavaScript pentru aplicație
│   │
│   ├── arduino_comm/      # Aplicația pentru comunicarea cu Arduino
│       ├── admin.py       # Configurarea panoului de administrare pentru senzori
│       ├── apps.py        # Configurații specifice aplicației
│       ├── models.py      # Modele pentru stocarea senzorilor
│       ├── views.py       # Funcții pentru gestionarea hardware-ului
│       ├── urls.py        # Rutele URL pentru API-ul de comunicare
│       ├── templates/     # Șabloane pentru configurarea senzorilor
│       ├── static/        # CSS și JavaScript specifice aplicației
│
├── static/                # Fișiere statice pentru interfața web
│   ├── css/               # Fișiere CSS pentru stilizare
│   ├── js/                # Fișiere JavaScript pentru interactivitate
│   ├── images/            # Resurse vizuale utilizate în interfață
│
├── templates/             # Șabloane HTML pentru paginile aplicației
│   ├── arduino_comm/      # Șabloane pentru configurarea hardware-ului
│   ├── main/              # Șabloane pentru autentificare și dashboard
│   ├── 403.html           # Pagina pentru eroare 403 (acces interzis)
│   ├── 404.html           # Pagina pentru eroare 404 (pagina nu există)
│   ├── 500.html           # Pagina pentru eroare 500 (eroare server)
│
├── ZSENSOR_COMUNICATION/  # Integrarea hardware-ului Arduino
│   ├── arduino.py         # Script Python pentru comunicarea cu Arduino
│   ├── arduino_script.ino # Codul pentru placa Arduino
│   ├── simulator.py       # Simulator pentru testarea comunicației hardware
│
├── manage.py              # Script pentru gestionarea proiectului Django
├── requirements.txt       # Lista dependențelor necesare proiectului
├── db.sqlite3             # Fișierul bazei de date SQLite
```

---

## Configurare și Instalare

### Cerințe Preliminare

Asigură-te că ai instalate următoarele pe sistemul tău:
- **Python**: versiunea 3.9 sau mai recentă
- **pip**: managerul de pachete pentru Python
- **Git**: pentru clonarea repository-ului
- **Arduino IDE**: pentru încărcarea codului pe placa Arduino (opțional)

### Pași pentru Instalare

1. **Clonarea Repository-ului:**

   ```bash
   git clone https://github.com/Akonomy/pai_project.git
   cd pai_project
   ```

2. **Crearea și Activarea unui Mediu Virtual:**

   ```bash
   python -m venv venv

   # Pentru Windows
   venv\Scripts\activate

   # Pentru Linux/MacOS
   source venv/bin/activate
   ```

3. **Instalarea Dependențelor:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Aplicarea Migrațiilor pentru Baza de Date:**

   ```bash
   python manage.py migrate
   ```

5. **Crearea unui Superuser:**

   ```bash
   python manage.py createsuperuser
   ```

   Urmează instrucțiunile pentru a configura contul de administrator.

6. **Pornirea Serverului de Dezvoltare:**

   ```bash
   python manage.py runserver
   ```

   Accesează aplicația la `http://127.0.0.1:8000`.

---

## Configurarea Hardware-ului

### Utilizarea Simulatorului Arduino

Dacă nu dispui de o placă Arduino fizică, poți utiliza simulatorul inclus în proiect:

1. **Rularea Simulatorului:**

   ```bash
   python ZSENSOR_COMUNICATION/simulator.py
   ```

   Simulatorul va emula comportamentul unei plăci Arduino, permițând testarea funcționalităților aplicației fără hardware fizic.

### Configurarea unei Plăci Arduino Fizice

Dacă ai acces la o placă Arduino, urmează pașii de mai jos:

1. **Încărcarea Codului pe Placă:**

   - Deschide `ZSENSOR_COMUNICATION/arduino_script.ino` în Arduino IDE.
   - Conectează placa Arduino la computer.
   - Selectează portul corespunzător și tipul plăcii din Arduino IDE.
   - Încarcă codul pe placă.

2. **Conectarea la Placă:**

   - Asigură-te că setările din `arduino.py` corespund portului la care este conectată placa.
   - Rulează scriptul pentru a iniția comunicarea:

     ```bash
     python ZSENSOR_COMUNICATION/arduino.py
     ```

---

## Detalii despre Conexiunile Hardware

Codul `arduino_script.ino` definește următoarele conexiuni și funcționalități:

- **Pini Digitali (12, 13):** Controlul ușilor (on/off).
- **Pini Analogici:** Controlează aerul condiționat și temperatura prin PWM (Pulse Width Modulation).
- **Pini de Intrare:** Confirmă dacă ușa s-a închis corect (valori primite de la senzori).

Exemplu de configurare pentru pini în `arduino_script.ino`:

```cpp
const int DOOR1_PIN = 12;  // Pin pentru controlul ușii 1
const int DOOR2_PIN = 13;  // Pin pentru controlul ușii 2
const int AC_PIN = A0;     // Pin analogic pentru aer condiționat
const int TEMP_PIN = A1;   // Pin analogic pentru temperatură
const int DOOR1_STATUS_PIN = 2;  // Confirmare stare ușă 1
const int DOOR2_STATUS_PIN = 3;  // Confirmare stare ușă 2
```

---

## Troubleshooting

- **Porturi Serial:** Dacă scriptul `arduino.py` nu se conectează, verifică portul USB utilizat:

  ```bash
  python -m serial.tools.list_ports
  ```

- **Probleme cu Dependențele:** Asigură-te că ai instalat toate bibliotecile necesare:

  ```bash
  pip install -r requirements.txt
  ```

- **Migrate Error:** Dacă baza de date SQLite nu funcționează corect, șterge fișierul `db.sqlite3` și rerulează migrațiile:

  ```bash
  python manage.py migrate
  ```

---

## License

This project is licensed under the MIT License. See the LICENSE file for details.
