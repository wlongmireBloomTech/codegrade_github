from github import Github
import codegrade
from credentials import cg_credentials, assignment, test_students

def reset_example():
    client = codegrade.login(
        username=cg_credentials['username'],
        password=cg_credentials['password'],
        tenant=cg_credentials['tenant']
    )

    #Be nice to delete submissions, but it doesn't look like we can...
    #submissions = client.assignment.get_all_submissions(assignment_id=assignment['codegrade-id'])

    test_student = test_students[cg_credentials['username']]
    
    g = Github(test_student['personal-access-token'])
    user = g.get_user()
    print (test_student['github_user'] + '/'  + assignment['github-name'])
    repo = g.get_repo(test_student['github_user'] + '/' +  assignment['github-name'])
    repo.delete()

    


reset_example()