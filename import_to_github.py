# Additional script: Importing webhook data to GitHub
# Part of "Focus Group: Using the API" (12 March 2021)
# By Claudia Chirita (University of Edinburgh) & Devin Hillenius (CodeGrade)
#
# More info at codegrade.com

import sys
import csv
from github import Github


# Load the roster generated in `create_roster.py` and return list of users
def load_user_data(filename='roster.csv'):
    with open(filename) as user_data:
        reader = csv.DictReader(user_data)
        try:
            data = [line for line in reader if line['github-user'] != '?']
        except csv.Error as e:
            sys.exit(
                'file {}, line {}: {}'.format(
                    filename,
                    reader.line_num,
                    e
                )
            )
    return data


# Login to GitHub and set correct webhooks for student repos in organization
def sync(access, organization, roster, assignment):
    g = Github(access['github']['token'])
    students = load_user_data(roster)

    no_users = 0
    no_errors = 0

    # Loop over all users from the roster file and set webhook data if not set
    # already
    for student in students:
        try:
            # user = g.get_user(student['github-user'])
            # repo = g.get_repo("LambdaSchool/" + assignment['github-name'])
            # user.create_fork(repo)

            repo = g.get_repo(
                student['github-user'] + "/" + assignment['github-name']
            )

            # Set deploy key if none is set already
            repo.create_key(
                title='codegrade-key',
                key=student['deploy_key']
            )
        
            repo.create_hook(
                'web',
                config={
                    'url': student['webhook_url'],
                    'content_type': 'json',
                    'secret': student['secret']
                },
                events=['push'],
                active=True
            )
        except:
            e = sys.exc_info()[0]
            print('>', 'Error:', e.status)
            print('>', 'Error:', e.data)
            print('>', 'Error:', e.headers)
            no_errors += 1

    print('\nProcessed', no_users, 'student(s);', no_errors, 'error(s).')


def main():
    sync(

        # SET GITHUB API PERSONAL ACCESS TOKEN
        access={
            'github': {
                'token': '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'
            }
        },

        # SET GITHUB ORGANIZATION INFORMATION NAME
        organization={
            'github-name': 'LambdaSchool'
        },

        # SET ROSTER FILE (GENERATED BY `CREATE_ROSTER.PY`)
        roster='roster.csv',

        # SET GITHUB REPO NAME PREFIX
        assignment={
            'github-name': 'web-sprint-challenge-advanced-web-applications-solution'
        }
    )


if __name__ == '__main__':
    main()