from datetime import datetime, timedelta
import pandas as pd

def parse_time(time_str):
    try:
        return datetime.strptime(time_str, '%H:%M').time()
    except ValueError:
        # If the time_str is not valid, return None
        return None

def format_timedelta(td):
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    return f"{hours}:{str(minutes).zfill(2)}"

def calculate_daily_hours(times):
    daily_hours = timedelta()
    if times:
        time_list = times.split() if isinstance(times, str) else times
        parsed_times = [parse_time(t) for t in time_list if t.strip()]

         # If there's only one log, set daily hours to zero
        if len(parsed_times) == 1:
            return timedelta(hours=0)
        
        # Apply penalty for odd number of time entries
        if len(parsed_times) % 2 != 0:
            daily_hours -= timedelta(minutes=30)  # Subtracting 30 minutes for not swiping after the break
            parsed_times = parsed_times[:1] + parsed_times[-1:]  # Take the first and last times
        
        for i in range(0, len(parsed_times), 2):
            start_time = parsed_times[i]
            end_time = parsed_times[i + 1] if i+1 < len(parsed_times) else None
            if start_time and end_time:
                start_dt = datetime.combine(datetime.today(), start_time)
                end_dt = datetime.combine(datetime.today(), end_time)
                daily_hours += end_dt - start_dt

    return daily_hours

def calculate_hours(df, num_ph):
    results = []
    public_holidays_hours = timedelta(hours=num_ph * 8)

    for index, row in df.iterrows():
        employee_hours = [row['No'], row['Name']]
        total_hours = timedelta()

        for day in df.columns[2:]:  # Skip 'No' and 'Name' columns
            daily_hours = max((timedelta(hours=4) if calculate_daily_hours(row[day]) else timedelta(hours=0)),calculate_daily_hours(row[day]))
            total_hours += daily_hours
            employee_hours.append(format_timedelta(daily_hours))

        # Append total hours worked
        total_hours += public_holidays_hours
        employee_hours.append(format_timedelta(total_hours))
        results.append(employee_hours)

    # Create DataFrame with the results
    columns = ['Employee ID', 'Employee Name'] + [f'Day {i}' for i in range(1, len(df.columns) - 1)] + ['Total Hours']
    calculated_df = pd.DataFrame(results, columns=columns)

    return calculated_df