# -*- coding: utf-8 -*-
from jira import JIRA

#watchers
def zaza(str1):
    size_arr = int(str1.count('JIRA User'))

    str1 = str1.split('=')
    str1 = str(str1)
    str1 = str1.split(',')
    arr = []

    for i in range(1, size_arr + 1):
        if i == 1:
            arr.append(str1[5])
        else:
            arr.append(str1[(i - 1) + (i * 5)])

    return arr


def without(u1):
    u1 = u1.replace("\'>", '')
    u1 = u1.replace("' \"\'", '')
    u1 = u1.replace("'", '')
    u1 = u1.replace(' "', '')
    u1 = u1.replace(']"]', '')
    return u1

def attachi(issue, chaild):
    arr_jira_filename = []
    way = "C:\\Users\\pozdnyakov-io\\Desktop\\buffer\\"
    for attachment in issue.fields.attachment:
        image = attachment.get()
        jira_filename = attachment.filename
        arr_jira_filename.append(jira_filename)
        with open(str(way) + str(jira_filename), 'wb') as f:
            f.write(image)

    issue = jira.issue(chaild.key)
    print(len(arr_jira_filename))

    for i in range(0, len(arr_jira_filename)):
        jira.add_attachment(issue=issue, attachment=str(way) + str(arr_jira_filename[i]))

    import os
    for i in range(0, len(arr_jira_filename)):
        if os.path.isfile(str(way) + str(arr_jira_filename[i])):
            os.remove(str(way) + str(arr_jira_filename[i]))
            print("success")
            print(str(way) + str(arr_jira_filename[i]))
        else:
            print("File doesn't exists!")
            print(str(way) + str(arr_jira_filename[i]))

def subtask(issue, name_list):
    issue = jira.issue(issue)

    rootnn_dict = {
        'project': {'key': 'CON'},
        'summary': issue.fields.__dict__.get('summary'),
        'description': issue.fields.description,
        # 'components': [{'name': 'Component'}],
        "issuetype": {'id': '21', 'name': 'Task', 'subtask': False}, #66
        #'reporter' : {'name': reporter_old},
        # "attachment": {'filename': issue.fields.attachment[0]},
        'parent': {'key': issue.key},
    }


    #print(reporter_old)

    watcher = jira.watchers(issue)
    str1 = str(watcher.watchers)

    #watchers
    arr = zaza(str1)

    for i in range(0, len(arr)):
        arr[i] = without(arr[i])
    #-----------------------------
    old_kira_key = issue
    old_url_face = issue.raw["fields"]["customfield_18201"]["value"]
    old_kontragent = []
    old_kontragent = issue.raw["fields"]["customfield_18200"]
    reporter_old = issue.raw["fields"]['reporter']['name']

    child = jira.create_issue(fields=rootnn_dict)
    print("created child: " + child.key)
    issue = jira.issue(child.key)
    #---------------------------------

    issue.update(customfield_18201={'value': old_url_face})
    issue.update(fields={'customfield_18200': old_kontragent})

    for i in range(0, len(arr)):
        jira.add_watcher(issue, str(arr[i]))

    issue.update(assignee={'name': name_list})
    comment = jira.add_comment(child.key, 'Subtask is done',
                               visibility={'type': 'role', 'value': 'Администраторы'})
    issue.update(reporter={'name': reporter_old})
    attachi(old_kira_key, issue)




jira_options = {'server': 'https://issues.gamma-center.com'}
jira = JIRA(options=jira_options, basic_auth=("", ""))
jira_search = jira.search_issues("project=ITS AND created > '-1d' AND issuetype = 'Task'")

really = []
for i in jira_search:
    issue = jira.issue(i)
    a = ''
    a = a + str(issue.fields.__dict__.get('parent'))
    if issue.fields.__dict__.get('subtasks') == [] and a == 'None':
        really.append(i)
    # print(i)

print("-----------")
really = ['CON-14001']
name_list = ['shirokov-da','pozdnyakov-io']
for i in really:
    for j in name_list:
        #print(i)
        # print(j)
        subtask(i, j)
