from flask import Flask, render_template, request
import psycopg2

app = Flask(__name__)

def get_connection():
    return psycopg2.connect(
        database="lifelink_db",
        user="postgres",
        password="123",
        host="localhost",
        port="5432"
    )

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/donor', methods=['GET', 'POST'])
def donor():
    if request.method == 'POST':
        name = request.form.get('name')
        blood_group = request.form.get('blood_group')
        age = request.form.get('age')
        contact = request.form.get('contact')
        city = request.form.get('city')

        if not all([name, blood_group, age, contact, city]):
            print("Missing donor fields", flush=True)
            return render_template('donor.html')

        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO donor (name, blood_group, age, contact, city)
                VALUES (%s, %s, %s, %s, %s)
            """, (name, blood_group, int(age), contact, city))
            conn.commit()
            cur.close()
            conn.close()
            print("Data saved successfully!", flush=True)
        except Exception as e:
            print("Error inserting donor:", e, flush=True)

    return render_template('donor.html')

@app.route('/recipient', methods=['GET', 'POST'])
def recipient():
    if request.method == 'POST':
        name = request.form.get('patient_name')
        blood_group = request.form.get('blood_group')
        hospital_name = request.form.get('hospital')
        city = request.form.get('city')
        contact = request.form.get('contact')

        if not all([name, blood_group, hospital_name, city, contact]):
            print("⚠️ Missing recipient fields", flush=True)
            return render_template('recipient.html')

        try:
            conn = get_connection()
            cur = conn.cursor()

            # ✅ Find or create hospital
            cur.execute("SELECT hospital_id FROM hospital WHERE hospital_name ILIKE %s LIMIT 1", (hospital_name,))
            row = cur.fetchone()
            if row:
                hospital_id = row[0]
            else:
                cur.execute("""
                    INSERT INTO hospital (hospital_name, city, contact)
                    VALUES (%s, %s, %s) RETURNING hospital_id
                """, (hospital_name, city, contact))
                hospital_id = cur.fetchone()[0]
                conn.commit()

            # ✅ Insert recipient
            cur.execute("""
                INSERT INTO recipient (name, blood_group_needed, contact, hospital_id, city)
                VALUES (%s, %s, %s, %s, %s)
            """, (name, blood_group, contact, hospital_id, city))
            conn.commit()

            # ✅ Find matching donors
            cur.execute("""
                SELECT * FROM donor
                WHERE blood_group = %s AND city ILIKE %s
            """, (blood_group, f"%{city}%"))
            donors = cur.fetchall()

            cur.close()
            conn.close()

            print(f"💌 Recipient saved. Found {len(donors)} matching donors!", flush=True)

            # 🔄 Show matched donors on Search page & auto-scroll
            return render_template('search.html', donors=donors, matched=True, scroll_to_results=True)

        except Exception as e:
            print("❌ Error saving recipient data:", e, flush=True)

    return render_template('recipient.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    donors = []
    searched = False

    if request.method == 'POST':
        blood_group = request.form.get('blood_group')
        city = request.form.get('city')
        searched = True

        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("""
                SELECT * FROM donor
                WHERE blood_group = %s AND city ILIKE %s
            """, (blood_group, f"%{city}%"))
            donors = cur.fetchall()
            cur.close()
            conn.close()
            print("Fetched donors:", donors, flush=True)
        except Exception as e:
            print("Error fetching donors:", e, flush=True)

    return render_template('search.html', donors=donors, searched=searched)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        print(f"New message from {name} ({email}): {message}", flush=True)
    return render_template('contact.html')

@app.route('/faq')
def faq():
    return render_template('faq.html')

if __name__ == '__main__':
    app.run(debug=True)