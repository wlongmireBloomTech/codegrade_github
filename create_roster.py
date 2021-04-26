import codegrade
from credentials import test_students

# Generate webhook information (webhook url, secret and key)
def generate_webhook_dict(webhook, client):
    return {
        'url': '{}/api/v1/webhooks/{}'.format(
            client.http.base_url,
            webhook.id,
        ),
        'secret': webhook.secret,
        'key': webhook.public_key,
    }

# Get list of all students in the course
def get_users(client, course_id):
    return client.course.get_all_users(course_id=course_id)


# Get Git webhook data for a user in an assignment
def webhookdata_per_user(client, username, assignment_id):
    return client.assignment.get_webhook_settings(
        assignment_id=assignment_id,
        webhook_type='git',
        extra_parameters={'author': username}
    )

def get_roster(client, assignment_id):
    allusers = get_users(
        client,
        client.assignment.get_course(assignment_id=assignment_id).id
    )

    users = list(filter(lambda u: u.user.username == '17eae2b2-b658-448c-b239-c74e7ec52d0b', allusers))
    results = []

    for u in users:
        webhook = generate_webhook_dict(
            webhookdata_per_user(client, u.user.username, assignment_id),
            client,
        )
        user = {
            'name': u.user.name,
            'username': u.user.username,
            'user_id': u.user.id,
            'webhook_url': webhook['url'],
            'secret': webhook['secret'],
            'deploy_key': webhook['key'],
            
            #both the github_user and the personal-access-token would need to be accessed and reference elsewhere
            'github_user': test_students[u.user.username]['github_user'],
            'personal-access-token': test_students[u.user.username]['personal-access-token']
        }

        results.append(user)
    
    return results