# 🔁 10. feladat

Készítsen olyan mintarendszert, ami képes működés közben updgradel-ni. Adott egy kliens komponens (A), ami 2 másodpercenként üzenetet küld a tasks üzenetsornak. A kezdeti üzenetek verziója V1.0. Készítsen egy consumer komponenst (B), ami feldolgozza az üzeneteket és a finishedTasks üzenetsorra küldi a kész üzeneteket, az üzenetekhez hozzáfűzi az aktuális időt. A B komponens fel legyen készítve arra az esetre, ha az üzenet verziószáma nem V1.0, ekkor az üzenetet az invalidTasks üzenetsorra továbbítja. A (C) consumer komponens az invalidTasks üzenetsorról leveszi az üzeneteket és 5 másodperc késleltéssel visszateszi a tasks üzenetsorra. Mutassuk be, ha a (A) komponens módosításával v2.0 verziószámú üzeneteket küldünk és a (B) komponensben feldolgozzuk a V2.0 üzeneteket (azaz nem küldjük az invalidTasks sorra őket) akkor a rendszer kis késleltetéssel, de leállítás nélkül tud üzemelni.

---

## 🧱 Felépítés

A rendszer 3 fő komponensből áll:

| Szereplő         | Feladat                                                                 |
|------------------|-------------------------------------------------------------------------|
| 🟡 Producer (A)   | Taskokat küld a `tasks` queue-ra verzióval ellátva                     |
| 🟢 Consumer B     | Érvényes verziójú taskokat feldolgozza, többit `invalidTasks` queue-ra |
| 🔁 Consumer C     | Hibás taskokat újrapróbálja → visszaküldi a `tasks` queue-ra           |

---

## 🚀 Indítás

A projekt futtatásához Docker és Docker Compose szükséges.

### 1. Build & Run

```bash
docker compose up --build
