from flask import Flask, request, jsonify, render_template,url_for,redirect,flash
import random
app = Flask(__name__)
Excuses = ['Het was de schuld van de prof','Ik heb echt ongeluk gehad','Het was mijn dag niet','Met 5 minuutjes meer had ik die oef echt wel nog gevonden',
'Hij heeft mensen echt gewoon genaaid.','Het was echt een moeilijker examen dan vorig jaar','Er zaten echt onmogelijke vragen tussen']
app.secret_key = "Waterballet"  # Choose your own password/admin wachtwoord
def calculate_score(dag, uur, nieuwe_serie, uren,hoeveelste_zit = 0):
    score = 0
    hoeveelste_zit +=1
    aantal_lesuren = 3 * 12
    if nieuwe_serie == 'ja':
        score = 0
    else:
        if int(uren) <aantal_lesuren:
            #clique = input('Had je een clique met de prof? (ja/nee):') (eventueel nog toevoegen)
            if dag == 'chill' and uur == 'chill':
                if hoeveelste_zit >= 2:
                    score = random.randint(0,80)
                else:
                    score = random.randint(0,51)
            
                
            else:
                score = random.randint(0,51)
            
        else:
            if dag == 'chill' and uur == 'chill':
                score = random.randint(0,90)
            else:
                score = random.randint(0,70)
    return score

@app.route('/')
def index():
    return render_template('website_san.html',
                           diploma_url=url_for('static', filename='foto_san.jpg'),
                           secret_url=url_for('static', filename='sports-funny.mp4'),
                           rechts_url= url_for('static',filename = 'san_waterballet_1.mp4'))

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    dag = data['dag']
    uur = data['uur']
    nieuwe_serie = data['serie']
    uren = data['uren']
    score = calculate_score(dag, uur, nieuwe_serie, uren)
    hoeveelste_zit = 1

    all_messages = []

    if score >= 50:
        message = f"""
Proficiat:
WE ❤️ 🫵\n
Hoeveel zits: {hoeveelste_zit}\n
U mag zichzelf nu Master Programmer en Python Expert noemen"""

        image_url = "/static/Foto andreas.jpg"

        # 🟡 Load all messages
        try:
            with open('submissions.txt', 'r', encoding='utf-8') as f:
                all_messages = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            all_messages = []

    else:
        message = random.choice(Excuses)
        image_url = None

        if nieuwe_serie == 'ja' and int(uren) > 20:
            message = """
Je mama zegt dat je niet mag liegen! <br>
Je kan niet zoveel gestudeerd hebben."""
            image_url = None

    return jsonify({
        'Score': score,
        'message': message,
        'image_url': image_url,
        'all_messages': all_messages if score >= 50 else None
    })

@app.route('/andere-pagina', methods=['GET', 'POST'])
def andere_pagina():
    if request.method == 'POST':
        if 'delete' in request.form:
            index = int(request.form['delete'])
            password = request.form.get('admin_password', '')
            if password == app.secret_key:
                try:
                    with open('submissions.txt', 'r', encoding='utf-8') as f:
                        messages = f.readlines()
                    messages.pop(index)
                    with open('submissions.txt', 'w', encoding='utf-8') as f:
                        f.writelines(messages)
                    flash('Bericht verwijderd.')
                except:
                    flash('Kon bericht niet verwijderen.')
            else:
                flash('Ongeldig admin wachtwoord.')
        else:
            name = request.form['name'].strip()
            message = request.form['message'].strip()
            if name and message:
                with open('submissions.txt', 'a', encoding='utf-8') as f:
                    f.write(f"{message} ~{name}\n")
        return redirect('/andere-pagina')

    try:
        with open('submissions.txt', 'r', encoding='utf-8') as f:
            messages = f.readlines()
    except FileNotFoundError:
        messages = []

    messages = [msg.strip() for msg in messages if msg.strip()]
    return render_template('andere_pagina.html', messages=messages)

if __name__ == '__main__':
    app.run(debug=True)
