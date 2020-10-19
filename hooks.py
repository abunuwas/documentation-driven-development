import json
import dredd_hooks

response_stash = {}


@dredd_hooks.after('/todo/ > Creates an task > 201 > application/json')
def save_created_task(transaction):
    response_payload = transaction['results']['fields']['body']['values']['actual']
    task_id = json.loads(response_payload)['id']
    response_stash['created_task_id'] = task_id


@dredd_hooks.before('/todo/{item_id} > Returns the details of a task > 200 > application/json')
def before_get_task(transaction):
    transaction['fullPath'] = '/todo/' + response_stash['created_task_id']


@dredd_hooks.before('/todo/{item_id} > Updates an existing task > 200 > application/json')
def before_put_task(transaction):
    transaction['fullPath'] = '/todo/' + response_stash['created_task_id']


@dredd_hooks.before('/todo/{item_id} > Deletes an existing task > 204')
def before_delete_task(transaction):
    transaction['fullPath'] = '/todo/' + response_stash['created_task_id']
