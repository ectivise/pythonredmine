# Import the Redmine class
import sys

from redminelib import Redmine
from dateutil.relativedelta import relativedelta
from dateutil.parser import parse
from prettytable import PrettyTable
import datetime

load_local_data = True
save_local_data = False

issues_newopen = PrettyTable()
issues_newopen.field_names = ["Project", "Ticket No.", "Subject", "Description(brief)", "Status", "Created",
                              "Created by", "Priority", "Assigned to"]
issues_overdue = PrettyTable()
issues_overdue.field_names = ["Project", "Ticket No.", "Subject", "Description(brief)", "Status", "Created",
                              "Created by", "Priority", "Assigned to"]


class EsplRedmine():
    def __init__(self, host='172.16.0.24', port='80', username='liqin', password='Abcd-1234'):
        pass


def print_attribute(i_issue):
    print(i_issue["id"])
    print(i_issue["tracker"])
    print(i_issue["status"])
    # print(i_issue["description"])
    print(i_issue["created_on"])
    print(i_issue["updated_on"])
    print(i_issue["project"])
    print(i_issue["subject"])
    print(i_issue["priority"])
    print(i_issue["author"])
    assignedto = getattr(i_issue, 'assigned_to', None)
    if assignedto:
        print(i_issue["assigned_to"])


def issue_processing():
    # generate a session
    redmine = Redmine('http://172.16.0.24', username='liqin', password='Abcd-1234')

    # get an issue by id
    iss = redmine.issue.get(601, include=['children', 'journals', 'watchers'])
    print_attribute(iss)

    # get the project by identifier or id
    # project = redmine.project.get('city-developments-limited') # le grove
    project = redmine.project.get('outpost-village-hotel-sentosa')  # clan
    # project = redmine.project.get('outpost-village-hotel-sentosa') # ovh
    print(project.identifier, project.id, project.name, dir(project.issues[0]), project.issues[0].subject)

    # iterate the items in the projects
    # normally we use the ones in the above print_attribute function
    totalcound = project.issues.total_count
    print(totalcound)
    for issue in project.issues:
        print_attribute(issue)
        """
        1, check the open date
        2, if it's today then cat 1 
        3, if the open date more than 2 days then cat 2 
        """
        issueid = str(issue["id"])
        tracker = issue["tracker"]
        status = issue["status"]
        # description = issue["description"]
        created_on = issue["created_on"]
        updated_on = issue["updated_on"]
        project = issue["project"]
        subject = issue["subject"]
        priority = issue["priority"]
        author = issue["author"]
        assigned_to = issue["assigned_to"] if getattr(issue, 'assigned_to', None) else ''
        # check the create day
        dt, today = parse(created_on).date(), datetime.date.today()
        # dt, today = parse(created_on).date(), datetime.date.today()


def test_pickle():
    import pickle
    fname = 'issue_file.pkl'
    global allissues
    allissues = None
    # get the project
    redmine = Redmine('http://172.16.0.24', username='liqin', password='Abcd-1234')
    project = redmine.project.get('city-developments-limited')  # le grove
    # dump the object
    if save_local_data:
        with open(fname, 'wb') as f:
            pickle.dump(project.issues, f, pickle.HIGHEST_PROTOCOL)
    # Reload the file
    try:
        f = open(fname, 'rb')
    except FileNotFoundError:
        print(f"File {fname} not found.  Aborting")
        sys.exit(1)
    except OSError:
        print(f"OS error occurred trying to open {fname}")
        sys.exit(1)
    except Exception as err:
        print(f"Unexpected error opening {fname} is", repr(err))
        sys.exit(1)  # or replace this with "raise" ?
    else:
        with f:
            allissues = pickle.load(open(fname, "rb"))
            # print('total issues = ', allissues.total_count)

    # issues_reloaded = pickle.load(open("issue_file.pkl", "rb"))
    # if issues_reloaded:
    #     print('total issues = ', issues_reloaded.total_count)
    #     for issue in issues_reloaded:
    #         print_attribute(issue)


def get_issues_by_project():
    pass


if __name__ == '__main__':
    if load_local_data:
        test_pickle()
    if allissues:
        print('total issues = ', allissues.total_count)
    print('start issue processing')
    # issue processing
    issue_processing()
    print('end issue processing')
