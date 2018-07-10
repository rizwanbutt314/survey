from django.shortcuts import render
from django.views import View
from django.http import HttpResponse

from survey.settings import CLIENT_URL, AGENCY_URL
from . import utils

import json
import time


class HomeView(View):
    template_name = 'home/main.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})


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
                'section_1': section_1,
                'section_2': section_2,
                'section_3': section_3,
            }
        elif request.path == AGENCY_URL:
            template_context_data = {
                'title': 'Agency',
                'section_1': section_1,
                'section_2': section_2,
                'section_3': section_3,
            }
        return render(request, self.template_name, template_context_data)

    def post(self, request, *args, **kwargs):
        post_data = request.POST
        responseData = dict()
        time.sleep(2)
        if request.path == CLIENT_URL:
            comparison_data = utils.compare_client_questions(post_data)
            responseData = {'success': True, 'type': 'client', 'data': comparison_data}
        elif request.path == AGENCY_URL:
            utils.save_agency_survey(post_data)
            responseData = {'success': True, 'type': 'agency', 'detail': 'Survey Submitted'}

        dumpData = json.dumps(responseData)
        return HttpResponse(dumpData, content_type='application/json')
