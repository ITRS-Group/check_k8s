# Contributing to check_k8s
Thanks for your interest in contributing to check_k8s! Below follows a short
set of contributing guidelines.

## Testing
We currently have a number of pytests, in the /tests directory. New code must
in almost all cases, come with a suitable set of tests. All tests are executed
in our CI system (see more in the later section), and must pass for changes to
be approved.

## Commit messages
Before you submit your change, please take your time to write a thorough commit
message. Chris Beams has written a very good [blog post](https://chris.beams.io/posts/git-commit/#seven-rule)
with seven rules of a great commit message. Please follow these.

## Submitting your PR
All changes should be submitted as a PR on the GitHub project. After the PR has
been submitted a member of the ITRS Group development team will review the PR,
suggest changes if necessary, and then merge the code to the master branch.

## CI System
We utilize two CI systems. Buildbot and Travis-CI. Buildbot is used internally
at ITRS Group, and is not available publicly. The results of the CI run from
Buildbot can for community contributions be ignored. For a PR to be merged the
Travis-CI build must have executed without failures.

## LGTM
Further to using the CI systems above to run our test suite, we are using
lgtm.com to analyze code. For a PR to be merged, no new alerts should be
flagged by LGTM.
