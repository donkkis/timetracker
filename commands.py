from datetime import datetime
from services import Project, TimeEntry

def _project_currently_worked_on(project: str, session):
    active_entries = session.query(Project.name, TimeEntry.start_time)\
                            .join(TimeEntry)\
                            .filter(TimeEntry.end_time == None).all()
    if project in map(lambda e: e[0], active_entries):
        return True
    return False

# Command functions
def workon(args, session):
    project_name = args.project
    if _project_currently_worked_on(project_name, session):
        print(f'Already working on {project_name}')
        return
    project = session.query(Project).filter_by(name=project_name).first()
    if not project:
        project = Project(name=project_name)
        session.add(project)
        session.commit()

    time_entry = TimeEntry(project=project, start_time=datetime.now())
    session.add(time_entry)
    session.commit()
    print(f"Started working on {project_name}.")

def stopwork(args, session):
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

def status(args, session):
    active_entries = session.query(Project.name, TimeEntry.start_time)\
                            .join(TimeEntry)\
                            .filter(TimeEntry.end_time == None).all()
    for project, start_time in active_entries:
        print(f"Currently working on {project} since {start_time}.")

def report(args, session):
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

def today(args, session):
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
