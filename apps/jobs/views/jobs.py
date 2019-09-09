from flask import Blueprint, request

from apps.jobs.business.jobs import JobsRecordBusiness
from apps.jobs.extentions import parse_list_args
from library.api.render import json_list_render, json_detail_render

jobs = Blueprint('jobs', __name__)


@jobs.route('/', methods=['GET'])
def credit_index_handler():
    limit, offset = parse_list_args()

    job_id = request.args.get('job_id')

    if job_id:
        data = JobsRecordBusiness.query_json_by_job_id(job_id)
        return json_list_render(0, data, limit, offset)

    data = JobsRecordBusiness.query_all_json(limit, offset)
    return json_detail_render(0, data)
