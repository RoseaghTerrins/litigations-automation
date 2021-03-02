import sendgrid
from sendgrid.helpers.mail import Email, To, Content, Mail, Attachment, FileContent, FileName, FileType, Disposition
import settings
import base64


def send_email(now, email_address):
    sg = sendgrid.SendGridAPIClient(settings.SEND_GRID_API_KEY)
    from_email = Email("dev@justdebt.co.uk")
    to_email = To(email_address)
    subject = "ACTION REQUIRED: Recoveries Management Files Ready To Process"
    content = Content("text/plain", "Please find attached a report on the import of Recoveries Management Files "
                                    "into the central database.\n\nFiles marked as successful are now ready to be "
                                    "processed in the Recoveries Management Application.\n\nIf you have any queries "
                                    "please contact sean.lawrence@justdebt.co.uk or a member of the Data Analytics "
                                    "team.")
    mail = Mail(from_email, to_email, subject, content)

    with open(f'{settings.IMPORT_REPORTS}\\DCA_Import_Report_{now}.csv', 'rb') as fd:
        data = fd.read()
        fd.close()
    encoded = base64.b64encode(data).decode()
    attachment = Attachment()
    attachment.file_content = FileContent(encoded)
    attachment.file_type = FileType('application/pdf')
    attachment.file_name = FileName(f'DCA_Import_Report_{now}.csv')
    attachment.disposition = Disposition('attachment')
    mail.attachment = attachment

    mail_json = mail.get()

    # Send an HTTP POST request to /mail/send
    sg.client.mail.send.post(request_body=mail_json)

def send_email_to_credit_safe(email_address):
    sg = sendgrid.SendGridAPIClient(settings.SEND_GRID_API_KEY)
    from_email = Email("dev@justdebt.co.uk")
    to_email = To(email_address)
    subject = "ACTION REQUIRED: Recoveries Management Files Ready To Process"
    content = Content("text/plain", "Hey Grant, Hope you are well! \n\n I have dropped a file on the SFTP, could you arrange for a cleanse and append please? \n\n Thanks,")
    mail = Mail(from_email, to_email, subject, content)
    mail_json = mail.get()

    # Send an HTTP POST request to /mail/send
    sg.client.mail.send.post(request_body=mail_json)
