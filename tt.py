import argparse
from datetime import datetime
from services import get_session, Project, TimeEntry

session = get_session()

# Command functions
def workon(args):
    project_name = args.project
    project = session.query(Project).filter_by(name=project_name).first()
    if not project:
        project = Project(name=project_name)
        session.add(project)
        session.commit()

    time_entry = TimeEntry(project=project, start_time=datetime.now())
    session.add(time_entry)
    session.commit()
    print(f"Started working on {project_name}.")

def stopwork(args):
    project_name = args.project
    project = session.query(Project).filter_by(name=project_name).first()
    if project:
        time_entry = session.query(TimeEntry).filter_by(project=project, end_time=None).first()
        if time_entry:
            time_entry.end_time = datetime.now()
            session.commit()
            print(f"Stopped working on {project_name}.")
        else:
            print(f"No active time entry for project {project_name}.")
    else:
        print(f"No project named {project_name}.")

def status(args):
    active_entries = session.query(Project.name, TimeEntry.start_time)\
                            .join(TimeEntry)\
                            .filter(TimeEntry.end_time == None).all()
    for project, start_time in active_entries:
        print(f"Currently working on {project} since {start_time}.")

def report(args):
    project_name, start_time_str, end_time_str = args.project, args.starttime, args.endtime
    today_date = datetime.now().date()  # Get the current date
    project = session.query(Project).filter_by(name=project_name).first()

    if project:
        # Combine the current date with the provided times
        start_time = datetime.strptime(f"{today_date} {start_time_str}", '%Y-%m-%d %H:%M:%S')
        end_time = datetime.strptime(f"{today_date} {end_time_str}", '%Y-%m-%d %H:%M:%S')

        overlaps = session.query(TimeEntry).filter(
            TimeEntry.project == project,
            (
                TimeEntry.start_time.between(start_time, end_time) |
                (TimeEntry.end_time != None) & TimeEntry.end_time.between(start_time, end_time)
            )
        ).count()

        if overlaps == 0:
            time_entry = TimeEntry(project=project, start_time=start_time, end_time=end_time)
            session.add(time_entry)
            session.commit()
            print(f"Report added for {project_name} from {start_time} to {end_time}.")
        else:
            print(f"Time entry overlaps with existing entries for project {project_name}.")
    else:
        print(f"No project named {project_name} found.")

def today(args):
    today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = datetime.now()
    
    entries = session.query(Project.name, TimeEntry.start_time, TimeEntry.end_time)\
                     .join(TimeEntry)\
                     .filter(TimeEntry.start_time >= today_start,
                             TimeEntry.end_time <= today_end).all()
    
    # Calculate total duration per project
    project_durations = {}
    for name, start_time, end_time in entries:
        if not end_time:
            end_time = datetime.now()
        duration = (end_time - start_time).total_seconds() / 3600  # Convert seconds to hours

        if name in project_durations:
            project_durations[name] += duration
        else:
            project_durations[name] = duration

    # Display the total duration for each project in hours:minutes format
    for project, duration in project_durations.items():
        hours = int(duration)
        minutes = int((duration - hours) * 60)
        print(f"{project}: {hours} hours, {minutes} minutes")


def main(args):
    args.func(args)

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
