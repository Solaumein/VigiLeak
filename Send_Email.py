import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Paramètres du serveur SMTP
smtp_server = 'ssl0.ovh.net'
smtp_port = 465  # Assurez-vous d'utiliser le port correct pour votre serveur
smtp_username = 'postmaster@obrulez.fr'
smtp_password = 'r~5i@XfCZ&Y5x^WJ7mSUq~gFt'

# Paramètres de l'e-mail
sender_email = 'no-reply.vigileak@obrulez.fr'
subject = 'Very Important'
message = 'ça fuit.'


def send_email(receiver_email):
    # Création du message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # Ajout du corps du message
    msg.attach(MIMEText(message, 'plain'))

    # Connexion au serveur SMTP et envoi de l'e-mail
    try:
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(smtp_username, smtp_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        print('E-mail envoyé avec succès!')
    except Exception as e:
        print('Erreur lors de l\'envoi de l\'e-mail:', e)


#send_email("")