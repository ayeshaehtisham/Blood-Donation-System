# 🩸 LifeLink - Blood Donation Management System

A full-stack Flask + PostgreSQL web app designed to connect blood donors and recipients seamlessly. LifeLink bridges the gap between those who want to give life and those in need of it — because every drop counts. 

---

## 🚀 Features

* 💉 **Donor Registration**

  * Donors can register with their name, age, blood group, city, and contact.
  * Stored in the database and made available for matching requests.

* 🏥 **Recipient Request**

  * Patients or their families can request blood by submitting a form.
  * Automatically matches with available donors based on city and blood group.

* 🔍 **Search Functionality**

  * Users can manually search donors by blood group and city.
  * Shows results instantly with donor details.

* 💬 **Contact Form**

  * Visitors can reach out via the contact form (future: database/email integration).

* ❓ **FAQ Page** 

  * Answers to common doubts about donation, eligibility, and safety.

---

## 🛠️ Tech Stack

* **Frontend**: HTML5, CSS3, JavaScript
* **Backend**: Python (Flask Framework)
* **Database**: PostgreSQL (via psycopg2)

---

## 🗄️ Database Schema

* `donor` – stores donor details (name, blood group, age, city, contact)
* `recipient` – stores patient/recipient details (name, hospital, city, contact, required blood group)
* `hospital` – stores hospital name, city, and contact info

---

## 📂 Project Structure
  
LifeLink - Blood Donation Management System/
│── app.py                  # Main Flask app
│
├── templates/              # HTML templates  
│   ├── home.html  
│   ├── donor.html  
│   ├── recipient.html  
│   ├── search.html  
│   ├── about.html  
│   ├── contact.html  
│   └── faq.html  
│
├── static/                 # Static files  
│   ├── css/  
│   │   ├── home.css  
│   │   ├── donor.css  
│   │   ├── recipient.css  
│   │   ├── search.css  
│   │   ├── about.css  
│   │   ├── contact.css  
│   │   └── faq.css  
│   └── assets/             # Images   

---

## ▶️ Getting Started

1. Clone the repository

   ```bash
   git clone https://github.com/your-username/blood-donation-system.git
   cd blood-donation-system
   ```

2. Install dependencies

   ```bash
   pip install flask psycopg2-binary
   ```

3. Set up PostgreSQL

  * Create a database (e.g., lifelink_db)
  * Update connection info in get_connection() inside app.py

4. Run the app

   ```bash
   flask run
   ```   