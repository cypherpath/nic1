# How to contribute efficiently

**Please read the first section before reporting a bug!
or proposing a new feature**

## Reporting bugs or proposing features

Please **always open *one* issue for *one* bug**. If you notice
several bugs and want to report them, make sure to create one new issue for
each of them.

Everything referred to hereafter as "bug" also applies for feature requests.

#### Search first in the existing database

Issues can be reported several times by various users. It's a good practice
to **search first** in the issues database before reporting your issue. If you
don't find a relevant match or if you are unsure, don't hesitate to **open a
new issue**. The devs will handle it from there if it's a duplicate.

#### Specify as much detail as possible

* Operating system
* Example pcap if available
* Error messages if any, etc

#### Specify steps to reproduce

Many bugs can't be reproduced unless specific steps are taken. Please **specify
the exact steps** that must be taken to reproduce the condition, and try to
keep them as minimal as possible.

#### Provide a simple, example script

Sometimes an unexpected behavior happens in your project. In such case,
understand that:
* What happens to you may not happen to other users.
* We can't take the time to look at your project, understand how it is set up
  and then figure out why it's failing.

To speed up our work, please prepare for us **a simple script** that isolates
and reproduces the issue. This is always **the best way for us to fix it**.

## Contributing pull requests

If you want to add new nic1 functionality, please make sure that:

* This functionality is desired.
* You talked to other developers on how to implement it best. This can be done
  in a GitHub issue first before making your PR).
* Even if it does not get merged, your PR is useful for future work by another
  developers.

Similar rules can be applied when contributing bug fixes - it's always best to
discuss the implementation in the bug report first if you are not 100% about
what would be the best fix.

#### Be nice to the git history

Try to make simple PRs with that handle one specific topic. Just like for
reporting issues, it's better to open 3 different PRs that each address a
different issue than one big PR with three commits.

When updating your fork with upstream changes, please use ``git pull --rebase``
to avoid creating "merge commits". Those commits unnecessarily pollute the git
history when coming from PRs.

Also try to make commits that bring the compiler from one stable state to another
stable state, i.e. if your first commit has a bug that you fixed in the second
commit, try to merge them together before making your pull request (see ``git
rebase -i`` and relevant help about rebasing or amending commits on the
Internet).

This git style guide has some good practices to have in mind:
[Git Style Guide](https://github.com/agis-/git-style-guide)

#### Format your commit logs with readability in mind

The way you format your commit logs is quite important to ensure that the
commit history and changelog will be easy to read and understand. A git commit
log is formatted as a short title (first line) and an extended description
(everything after the first line and an empty separation line). Also, make
sure you refer to the ticket your commit is addressing.

## Communicating with developers

To communicate with developers (e.g. to discuss a feature you want to implement
or a bug you want to fix), the following channels can be used:
- [GitHub issues](https://github.com/cypherpath/nic1/issues): If there is an
  existing issue about a topic you want to discuss, just add a comment to it -
  all developers watch the repository and will get an email notification. You
  can also create a new issue - please keep in mind to create issues only to
  discuss quite specific points about the development, and not general user
  feedback or support requests.
- email - sources@cypherpath.com 

Thanks!

The nic1 development team
