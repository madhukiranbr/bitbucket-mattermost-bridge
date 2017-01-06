

def _get_default_data():
    return {
                'color': '#FFFFFF',
                'text': 'Not implemented'
    }


def set_color_from_priority(priority):
    return {
        'trivial': '#205081',
        'minor': 'good',
        'major': 'warning',
        'critical': 'danger',
        'blocker': '#000000'
    }.get(priority, '#FFFFFF')


def set_author_infos(resp, data):
    if data.actor.display_name == 'Anonymous':
        resp['author_name'] = data.actor.display_name
        return resp

    resp['author_name'] = '%s (%s)' % (data.actor.display_name,
                                       data.actor.username)
    resp['author_icon'] = data.actor.links.avatar.href
    resp['author_link'] = data.actor.links.html.href

    return resp


def get_issue(data, action):
    resp = _get_default_data()
    resp = set_author_infos(resp, data)
    template = '%s a %s %s [#%s: %s](%s) (%s)'

    issue = data.issue
    resp['text'] = template % (action, issue.priority, issue.type, issue.id,
                               issue.title, issue.links.html.href, issue.state)

    resp['color'] = set_color_from_priority(issue.priority)
    return resp


def issue_comment_created(data):
    resp = get_issue(data, 'Commented')
    return resp


def issue_created(data):
    resp = get_issue(data, 'Opened')
    return resp


def issue_updated(data):
    resp = get_issue(data, 'Updated')
    return resp


def repo_commit_comment_created(data):
    resp = _get_default_data()
    resp = set_author_infos(resp, data)

    template = 'Commented commit %s at %s'
    commit_link = '[#%s](%s)' % (data.comment.commit.hash[:7],
                                 data.comment.links.html.href)
    repo_link = '[%s](%s)' % (data.repository.full_name,
                              data.repository.links.html.href)
    resp['text'] = template % (commit_link, repo_link)

    return resp


def repo_push(data):
    resp = _get_default_data()
    resp = set_author_infos(resp, data)

    changesets = len(data.push.changes[0].commits)
    repo_link = '[%s](%s)' % (data.repository.full_name,
                              data.repository.links.html.href)
    branch = data.push.changes[0].new.name
    commits = []
    for commit in data.push.changes[0].commits:
        text = '- [%s](%s): %s' % (commit.hash[:7],
                                   commit.links.html.href,
                                   commit.message.replace('\n', ' - '))
        commits.append(text)
    template = 'Pushed %s changesets to %s at %s\n%s'
    resp['text'] = template % (changesets, branch,
                               repo_link, '\n'.join(commits))
    return resp


def get_pullrequest(data, action):
    resp = _get_default_data()
    resp = set_author_infos(resp, data)

    pr = data.pullrequest
    pr_link = '[%s](%s)' % (pr.title, pr.links.html.href)
    pr_src_link = '%s/branch/%s' % (pr.source.repository.links.html.href,
                                    pr.source.branch.name)
    pr_dst_link = '%s/branch/%s' % (pr.destination.repository.links.html.href,
                                    pr.destination.branch.name)
    pr_src = '[%s:%s](%s)' % (pr.source.repository.full_name,
                              pr.source.branch.name,
                              pr_src_link)
    pr_dst = '[%s:%s](%s)' % (pr.destination.repository.full_name,
                              pr.destination.branch.name,
                              pr_dst_link)
    template = '%s pull request %s\nFrom %s to %s'
    resp['text'] = template % (action, pr_link, pr_src, pr_dst)

    return resp


def pullrequest_approved(data):
    resp = get_pullrequest(data, 'Approved')
    return resp


def pullrequest_created(data):
    resp = get_pullrequest(data, 'Opened')
    return resp


def pullrequest_fulfilled(data):
    resp = get_pullrequest(data, 'Merged')
    return resp


def pullrequest_rejected(data):
    resp = get_pullrequest(data, 'Rejected')
    return resp


def pullrequest_updated(data):
    resp = get_pullrequest(data, 'Updated')
    return resp

def pullrequest_unapproved(data):
    resp = get_pullrequest(data, 'Unapproved')
    return resp