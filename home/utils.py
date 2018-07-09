from home.models import AgencySurvey
from survey.settings import QUESTIONS_COUNT, QUESTION_START_FORMULA

import json


def compare_client_questions(client_data):
    mapped_data = map_survey_data(client_data)
    compared_data = list()

    for agency in AgencySurvey.objects.all()[:10]:
        agency_data = json.loads(agency.survey)

        score = calculate_comparison_score(mapped_data, agency_data)
        compared_data.append({
            'name': agency.name,
            'id': agency.id,
            'score': score
        })
    # Sorting List of objects using score value
    compared_data = sorted(compared_data, key=lambda x: x['score'], reverse=True)
    return compared_data


def calculate_comparison_score(client_data, agency_data):
    client_diff = list()
    for key, value in client_data.items():
        temp_agency_val = int(agency_data[key])
        temp_client_val = int(client_data[key])
        temp_diff = temp_agency_val - temp_client_val
        client_diff.append(abs(temp_diff))

    sum_diff = sum(client_diff)
    level_1 = abs(QUESTION_START_FORMULA - sum_diff)
    level_2 = level_1 / QUESTION_START_FORMULA
    level_3 = level_2 * 100
    score = "{0:.2f}".format(level_3)
    return float(score)


def map_survey_data(post_data):
    mapped_data = dict()
    for q_num in range(1, QUESTIONS_COUNT + 1):
        q_key = 'q' + str(q_num)
        mapped_data[q_key] = post_data.get(q_key, '')

    return mapped_data


def save_agency_survey(data):
    mapped_data = map_survey_data(data)
    agency_data = AgencySurvey.objects.create(
        name=data.get('name', 'No Name'),
        survey=json.dumps(mapped_data)
    )
