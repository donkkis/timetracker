import argparse
from datetime import datetime
from services import get_session, Project, TimeEntry
from commands import workon, stopwork, status, today, report

session = get_session()

def main(args):
    args.func(args, session)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Track time spent on projects.")
    subparsers = parser.add_subparsers(help="commands")

    # Workon command
    workon_parser = subparsers.add_parser('workon', help='Start working on a project')
    workon_parser.add_argument('project', type=str, help='The name of the project')
    workon_parser.set_defaults(func=workon)

    # Stopwork command
    stopwork_parser = subparsers.add_parser('stopwork', help='Stop working on a project')
    stopwork_parser.add_argument('project', type=str, help='The name of the project')
    stopwork_parser.set_defaults(func=stopwork)

    # Status command
    status_parser = subparsers.add_parser('status', help='Show current status')
    status_parser.set_defaults(func=status)

    # Report command
    report_parser = subparsers.add_parser('report', help='Report time for a project')
    report_parser.add_argument('project', type=str, help='The name of the project')
    report_parser.add_argument('starttime', type=str, help='The start time (HH:MM:SS)')
    report_parser.add_argument('endtime', type=str, help='The end time (HH:MM:SS)')
    report_parser.set_defaults(func=report)

    # Today command
    today_parser = subparsers.add_parser('today', help='Show today\'s time entries and total duration per project')
    today_parser.set_defaults(func=today)

    args = parser.parse_args()

    if hasattr(args, 'func'):
        main(args)

    else:
        parser.print_help()
