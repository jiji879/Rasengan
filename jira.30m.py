#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python
# coding=utf-8

import jira


def main():
    jira_client = jira.JIRA(server='{jira host}',
                            basic_auth=('{username}', '{password}'))

    jql_str = u'status in (Open, 处理中, Reopened, 待处理, "To Do", Doing, Planning, Waiting, "In Progress", Delayed) AND assignee in (currentUser())'
    todos = jira_client.search_issues(jql_str=jql_str)

    desc = ':1234: {} TODOS| dropdown=false'.format(len(todos))
    print desc
    print '---\nMy Jira TODOs'

    todos = sorted(todos, key=lambda x: x.fields.created)

    for idx, todo in enumerate(todos, start=1):
        reporter_name = todo.fields.reporter.displayName
        title = todo.fields.summary
        proj = todo.fields.project.name
        issue_type = todo.fields.issuetype.name
        link = todo.permalink()

        created = todo.fields.created
        priority = todo.fields.priority.name
        color = get_color(priority)

        duedate = (todo.fields.duedate or '').split('-', 1)[-1]

        output = u'--{idx} {duedate} {issue_type} · {reporter_name} · {proj} · {title} | length=60 href={link} color={color}'
        print output.format(**locals()).encode('utf-8').strip()


def get_color(priority):
    if priority == 'High/P1':
        color = '#ff0000'
    else:
        color = ''
    return color


if __name__ == '__main__':
    main()
