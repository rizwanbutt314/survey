from django.shortcuts import render
from django.views import View
from django.http import HttpResponse

from survey.settings import CLIENT_URL, AGENCY_URL

import json
import time


class IndexView(View):
    template_name = 'home/index.html'

    def get(self, request, *args, **kwargs):
        template_context_data = dict()
        if request.path == CLIENT_URL:
            template_context_data = {
                'title': 'Client'
            }
        elif request.path == AGENCY_URL:
            template_context_data = {
                'title': 'Agency'
            }
        return render(request, self.template_name, template_context_data)

    def post(self, request, *args, **kwargs):
        post_data = request.POST
        responseData = dict()
        time.sleep(2)
        if request.path == CLIENT_URL:
            # TODO: compare client data with agencies
            responseData = {'success': True, 'detail': 'Survey Result'}
        elif request.path == AGENCY_URL:
            # TODO: Submit agency data
            responseData = {'success': True, 'detail': 'Survey Submitted'}

        dumpData = json.dumps(responseData)
        return HttpResponse(dumpData, content_type='application/json')
