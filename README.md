# CodeGrade - GitHub automation

Using the CodeGrade API and the GitHub API, you can automatically populate
your students' GitHub repositories with the deploy key and webhook details
needed to automatically hand in to CodeGrade with every `git push`.

## Setup
To use the CodeGrade API and GitHub API, first install the required packages:
`pip3 install codegrade`
`pip3 install PyGithub`

You also need to enable Git submissions for your CodeGrade assignment and
generate a (temporary) personal access token on GitHub.

## Course / GitHub structure
The current scripts assume you use CodeGrade stand-alone, with SSO or have
an LTI 1.3 integration with your LMS, so that we have a full list of all
students before an assignment starts.

The script is created to automatically populate the deploy keys and webhooks
for student repositories in an Organization managed by you. You can of
course use the GitHub API to automatically create these repos in your org
and invite your students to this.

## Step 1: Running `create_roster.py`
First, create the roster with Git details of all users in your course. By
running `python3 create_roster.py`. Before running, make sure to fill in
your CodeGrade credentials and assignment ID (found in the URL on CodeGrade).
By default this will be generated as `roster.csv`. The last column of this
roster should be manually filled in and is the mapping between the
CodeGrade accounts and GitHub repos / accounts. (For now, this mapping is
with repo names).

## Step 2: Importing this to GitHub using `import_to_github.py`
After generating and adding to `roster.csv`, you can run `import_to_github.py`
to set up all webhook information on GitHub.

Before running, fill in:

- GitHub personal access token
- GitHub organization name
- The name of the roster (by default `roster.csv`)
- The prefix of assignments

For this example, all assignments in our organization have a prefix (defined
in `import_to_github.py`) and a suffix (the manually filled in name per
student in `roster.csv`). For instance: **assignment1-johndoe**.

## Step 3: Confirm your setup and sit back!
Always a good idea to make sure everything went according to plan and going
through some repos in your organization to see if correct deploy keys and
webhooks were added. You can always use a test repo, make a push (easy way
is to just edit the readme in the GitHub UI) and check CodeGrade.

If everything is done correctly, your students can now start working in their
personal repo and will automatically hand in to CodeGrade with every push they
do!

Need more help? Check help.codegrade.com or send us an email at
support@codegrade.com!
