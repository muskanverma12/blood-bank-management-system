from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///patients.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'secretkey123'

# Initialize the database
db = SQLAlchemy(app)

# Define Donor model
class Donor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    blood_group = db.Column(db.String(10), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    city = db.Column(db.String(100), nullable=False)

# Define BloodRequest model
class BloodRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_name = db.Column(db.String(100), nullable=False)
    required_blood = db.Column(db.String(10), nullable=False)
    hospital = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(15), nullable=False)

# Create the database tables
with app.app_context():
 db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/donor', methods=['GET', 'POST'])
def donor():
    if request.method == 'POST':
        name = request.form['name']
        blood_group = request.form['blood_group']
        phone = request.form['phone']
        city = request.form['city']
        
        new_donor = Donor(name=name, blood_group=blood_group, phone=phone, city=city)
        db.session.add(new_donor)
        db.session.commit()

        flash('Donor registered successfully!')
        return redirect('/donor')

    donors = Donor.query.all()
    return render_template('donor.html', donors=donors)

@app.route('/donor/edit/<int:id>', methods=['GET', 'POST'])
def edit_donor(id):
    donor = Donor.query.get_or_404(id)
    
    if request.method == 'POST':
        donor.name = request.form['name']
        donor.blood_group = request.form['blood_group']
        donor.phone = request.form['phone']
        donor.city = request.form['city']

        db.session.commit()

        flash('Donor details updated successfully!')
        return redirect('/donor')

    return render_template('edit_donor.html', donor=donor)

@app.route('/donor/delete/<int:id>', methods=['GET', 'POST'])
def delete_donor(id):
    donor = Donor.query.get_or_404(id)
    db.session.delete(donor)
    db.session.commit()

    flash('Donor deleted successfully!')
    return redirect('/donor')

@app.route('/request', methods=['GET', 'POST'])
def request_blood():
    if request.method == 'POST':
        patient_name = request.form['patient_name']
        required_blood = request.form['required_blood']
        hospital = request.form['hospital']
        contact = request.form['contact']

        new_request = BloodRequest(patient_name=patient_name, required_blood=required_blood, hospital=hospital, contact=contact)
        db.session.add(new_request)
        db.session.commit()

        flash('Blood request submitted successfully!')
        return redirect('/request')

    requests = BloodRequest.query.all()
    return render_template('request.html', requests=requests)

@app.route('/request/edit/<int:id>', methods=['GET', 'POST'])
def edit_request(id):
    blood_request = BloodRequest.query.get_or_404(id)
    
    if request.method == 'POST':
        blood_request.patient_name = request.form['patient_name']
        blood_request.required_blood = request.form['required_blood']
        blood_request.hospital = request.form['hospital']
        blood_request.contact = request.form['contact']

        db.session.commit()

        flash('Blood request details updated successfully!')
        return redirect('/request')

    return render_template('edit_request.html', blood_request=blood_request)

@app.route('/request/delete/<int:id>', methods=['GET', 'POST'])
def delete_request(id):
    blood_request = BloodRequest.query.get_or_404(id)
    db.session.delete(blood_request)
    db.session.commit()

    flash('Blood request deleted successfully!')
    return redirect('/request')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
