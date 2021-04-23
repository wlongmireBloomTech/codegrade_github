import sys
import csv
from datetime import datetime
from github import Github
import codegrade
import json

# Load the roster generated in `create_roster.py` and return list of users
def load_user_data(filename='roster.csv'):
    with open(filename) as user_data:
        reader = csv.DictReader(user_data)
        try:
            data = [line for line in reader if line['github_user'] != '?']
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
def sync(organization, roster, assignment):
    students = load_user_data(roster)

    no_users = 0
    no_errors = 0

    # Loop over all users from the roster file and set webhook data if not set
    # already
    for student in students:
        try:
            g = Github(student['personal-access-token'])
            user = g.get_user()
            repo = g.get_repo("LambdaSchool/" + assignment['github-name'])
            repo = user.create_fork(repo)
            
            repo = g.get_repo(
                student['github_user'] + "/" + assignment['github-name']
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

            today = datetime.today()
            repo.create_file("codegrade_log.md", "codegrade", "Connected to codegrade: " + today.strftime("%m/%d/%Y %H:%M:%S"))

            client = codegrade.login(
                username='17eae2b2-b658-448c-b239-c74e7ec52d0b',
                password='greenGrass1982',
                tenant='Lambda School'
            )

            submissions = client.assignment.get_submissions_by_user(assignment_id=assignment['codegrade-id'], user_id=student['user_id'])

            if len(submissions) > 0:
                print("codegrade integration was successful")
            else:
                print("codegrade intergration not successful")
            
            
        except:
            e = sys.exc_info()[0]
            print('>', 'Error:', e.status)
            print('>', 'Error:', e.data)
            print('>', 'Error:', e.headers)
            no_errors += 1

    print('\nProcessed', no_users, 'student(s);', no_errors, 'error(s).')


def main():
    organization = {'github-name': 'LambdaSchool' }
    roster='roster.csv'
    assignment={
        'github-name': 'web-sprint-challenge-advanced-web-applications-solution',
        'codegrade-id': 2496
    }

    sync(
        # SET GITHUB ORGANIZATION INFORMATION NAME
        organization,

        # SET ROSTER FILE (GENERATED BY `CREATE_ROSTER.PY`)
        roster,

        # SET GITHUB REPO NAME PREFIX
        assignment
    )


if __name__ == '__main__':
    main()
