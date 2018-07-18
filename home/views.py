import json
import time
import os
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
import smtplib

from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
# from django.views.decorators.csrf import csrf_exempt
# from django.utils.decorators import method_decorator
from django.core.mail import send_mail, get_connection
from django.template.loader import get_template

from survey.settings import (
    CLIENT_URL,
    AGENCY_URL,
    EMAIL_HOST,
    EMAIL_USERNAME,
    EMAIL_PASSWORD,
    EMAIL_PORT,
    EMAIL_SUBJECT,
    EMAIL_TO
)
from . import utils


class HomeView(View):
    template_name = 'home/main.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})


# @method_decorator(csrf_exempt, name='dispatch')
class IndexView(View):
    template_name = 'home/index.html'

    def get(self, request, *args, **kwargs):
        questions_data = utils.get_questions()
        section_1 = questions_data[0:10]
        section_2 = questions_data[10:20]
        section_3 = questions_data[20:30]
        template_context_data = dict()
        if request.path == CLIENT_URL:
            template_context_data = {
                'title': 'Client',
                'heading_1': 'Would you describe yourself as more ',
                'heading_2': 'this or that?',
                'section_1': section_1,
                'section_2': section_2,
                'section_3': section_3,
            }
        elif request.path == AGENCY_URL:
            template_context_data = {
                'title': 'Agency',
                'heading_1': 'Is your Agency more ',
                'heading_2': 'this or that?',
                'section_1': section_1,
                'section_2': section_2,
                'section_3': section_3,
            }
        return render(request, self.template_name, template_context_data)

    def post(self, request, *args, **kwargs):
        post_data = request.POST
        name = post_data.get('name', 'No Name')
        responseData = dict()
        time.sleep(2)
        # Client Section
        if request.path == CLIENT_URL:
            comparison_data = utils.compare_client_questions(post_data)
            # Save Client Survey Data
            utils.save_client_survey(post_data)
            responseData = {'success': True, 'type': 'client', 'data': comparison_data}
            try:
                # Send comparison stats to admin
                send_stats_email(name, comparison_data)
            except:
                print("Exception while sending stats email.")
        # Agency Section
        elif request.path == AGENCY_URL:
            # Save Agency Survey Data
            utils.save_agency_survey(post_data)

            # Generate Temporarily agencies json file
            temp_agency_data_file = utils.generate_agency_model_json()

            try:
                # Send agencies json and quesitons files in email
                send_agency_data_email(temp_agency_data_file)
            except Exception as err:
                print("Exception while sending agency data email.")

            # Removing Temporarily create agencies data json file
            try:
                os.remove(temp_agency_data_file)
            except:
                pass
            
            responseData = {'success': True, 'type': 'agency', 'detail': 'Survey Submitted'}

        dumpData = json.dumps(responseData)
        return HttpResponse(dumpData, content_type='application/json')


def send_stats_email(name, comparison_data):
    # email template
    t_html = get_template('home/email.html')
    context = {
        'name': name,
        'data': comparison_data
    }
    c_html = t_html.render(context)

    connection = get_connection(
        host=EMAIL_HOST,
        port=EMAIL_PORT,
        username=EMAIL_USERNAME,
        password=EMAIL_PASSWORD,
        use_ssl=False,
        use_tls=True)

    send_mail(EMAIL_SUBJECT, EMAIL_SUBJECT, EMAIL_USERNAME,
              EMAIL_TO,
              connection=connection,
              html_message=c_html)


def send_agency_data_email(filename):
    questions_file_path = os.getcwd() + "/home/static/questions.json"

    msg = MIMEMultipart()
    msg['Subject'] = 'Agencies Data'
    msg['From'] = EMAIL_USERNAME
    msg['To'] = ','.join(EMAIL_TO)

    msg.preamble = 'Multipart massage.\n'

    part = MIMEText("Hi, please find the attached agencies and questions files")
    msg.attach(part)

    # Attaching Agencies Data file
    agencies_file = MIMEApplication(open(filename, "rb").read())
    agencies_file.add_header('Content-Disposition', 'attachment', filename='agencies_data.json')

    # Attaching Questions Data file
    questions_file = MIMEApplication(open(questions_file_path, "rb").read())
    questions_file.add_header('Content-Disposition', 'attachment', filename='questions_data.json')

    msg.attach(agencies_file)
    msg.attach(questions_file)

    smtp_server = "{0}:{1}".format(EMAIL_HOST, EMAIL_PORT)
    server = smtplib.SMTP(smtp_server)
    server.ehlo()
    server.starttls()
    server.login(EMAIL_USERNAME, EMAIL_PASSWORD)

    server.sendmail(msg['From'], EMAIL_TO, msg.as_string())
