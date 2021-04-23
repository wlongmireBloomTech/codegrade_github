# CodeGrade API: Export student Git information to roster.csv
# Part of "Focus Group: Using the API" (12 March 2021)
#
# More info at codegrade.com

import csv
import os

import codegrade


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


# Write exported users and webhook information to a CSV
def init_roster(client, assignment_id, roster):
    allusers = get_users(
        client,
        client.assignment.get_course(assignment_id=assignment_id).id
    )

    users = list(filter(lambda u: u.user.username == '17eae2b2-b658-448c-b239-c74e7ec52d0b', allusers))

    print("users: ", users)

    # Open / create roster file and write header and row per user
    with open(roster, mode='w', newline='') as out:
        w = csv.writer(out)
        w.writerow([
            'name',
            'username',
            'user_id',
            'webhook_url',
            'secret',
            'deploy_key',
            'github_user',
            'personal-access-token'
        ])

        # Loop over all users in the course and write webhook data in row
        for u in users:
            
            webhook = generate_webhook_dict(
                webhookdata_per_user(client, u.user.username, assignment_id),
                client,
            )

            w.writerow([
                u.user.name,
                u.user.username,
                u.user.id,
                webhook['url'],
                webhook['secret'],
                webhook['key'],
                'wlongmireLambda',
                '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'
            ])


def main():

    # SET CODEGRADE CREDENTIALS AND TENANT NAME
    client = codegrade.login(
        username='17eae2b2-b658-448c-b239-c74e7ec52d0b',
        password='greenGrass1982',
        tenant='Lambda School'
    )

    # SET ASSIGNMENT ID AND EXPORT FILE NAME
    init_roster(
        client,
        assignment_id=2496,
        roster='roster.csv'
    )


if __name__ == '__main__':
    main()
