from flask import Flask, render_template, request, flash, redirect, url_for
from flask_mail import Mail, Message

app = Flask(__name__)

# --- Configuration ---
# Load configuration from config.py
# Make sure you have created a config.py file in the same directory.
try:
    app.config.from_pyfile('config.py')
except FileNotFoundError:
    print("="*80)
    print("WARNING: config.py not found. The application will not work correctly.")
    print("Please create a config.py file with your settings.")
    print("="*80)

if not app.config.get('MAIL_USERNAME') or app.config.get('MAIL_USERNAME') == 'your_email@gmail.com':
    print("="*80)
    print("WARNING: Email credentials are not set or are still the default in config.py.")
    print("The contact form will not be able to send emails.")
    print("="*80)

mail = Mail(app)

# --- Routes ---
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/resume')
def resume():
    return render_template('resume.html')

@app.route('/work')
def work():
    return render_template('work.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Get form data
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message_body = request.form.get('message')

        # Prevent sending email if the app is not configured
        if not app.config['MAIL_DEFAULT_SENDER']:
            flash('The mail server is not configured. Please contact the site administrator.', 'danger')
            return redirect(url_for('contact'))

        # Create and send email
        msg = Message(subject=f"New Contact Form Submission: {subject}",
                      recipients=[app.config['MAIL_DEFAULT_SENDER']]) # Send to yourself
        msg.body = f"From: {name} <{email}>\n\n{message_body}"

        try:
            mail.send(msg)
            flash('Your message has been sent successfully!', 'success')
        except Exception as e:
            flash(f'An error occurred while sending the message. Please try again later.', 'danger')
            print(f"Mail Error: {e}") # For debugging

        return redirect(url_for('contact'))

    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)