import mysql.connector
from tabulate import tabulate
from datetime import date
from datetime import date, timedelta

db=mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_password",
    database="study_tracker"
)
cursor=db.cursor()

def add_entry():
    date=input("\n Enter date (YYYY-MM-DD): ")
    day=input(" Enter day: ")
    subject=input(" Enter subject: ")
    topic=input(" Enter topic: ")
    study_time=(input(" Enter study time (HH:MM:SS): "))

    query="INSERT INTO study_sessions (date, day, subject, topic, study_time) VALUES (%s, %s, %s, %s, %s)"
    values=(date, day, subject, topic, study_time)

    cursor.execute(query, values)
    db.commit()

    print(" Study Session Added!")

def view_entries():
    cursor.execute("SELECT * FROM study_sessions")
    records = cursor.fetchall()

    headers = ["ID", "Date", "Day", "Subject", "Topic", "Time"]

    print(" \n Study Sessions: \n")
    print(tabulate(records, headers=headers, tablefmt="fancy_grid"))

def total_time():
    cursor.execute("""
    SELECT SUM(TIME_TO_SEC(study_time))
    FROM study_sessions
    """)

    total_seconds = cursor.fetchone()[0]

    if total_seconds is None:
        print(" No study data available.")
        return

    # Days format
    days = total_seconds // (24 * 3600)
    remaining = total_seconds % (24 * 3600)

    hours = remaining // 3600
    minutes = (remaining % 3600) // 60
    seconds = remaining % 60

    # Total hours format
    total_hours = total_seconds // 3600

    print(f"\n Total Study Time: {days} days, {hours:02}:{minutes:02}:{seconds:02}")
    print(f" ({total_hours}:{minutes:02}:{seconds:02})")

def update_entry():
    view_entries()

    try:
        entry_id = int(input("\n Enter ID of the entry to update: "))
    except ValueError:
        print(" Invalid ID!")
        return

    print("\n What do you want to update?")
    print(" 1. Date")
    print(" 2. Day")
    print(" 3. Subject")
    print(" 4. Topic")
    print(" 5. Time")

    choice = input("\n Enter choice: ")

    if choice == "1":
        new_value = input("\n Enter new date (YYYY-MM-DD): ")
        column = "date"
    elif choice == "2":
        new_value = input(" Enter new day: ")
        column = "day"
    elif choice == "3":
        new_value = input(" Enter new subject: ")
        column = "subject"
    elif choice == "4":
        new_value = input(" Enter new topic: ")
        column = "topic"
    elif choice == "5":
        new_value = input(" Enter new time (HH:MM:SS): ")
        column = "study_time"
    else:
        print(" Invalid choice!")
        return

    query = f"UPDATE study_sessions SET {column} = %s WHERE id = %s"
    values = (new_value, entry_id)

    cursor.execute(query, values)
    db.commit()

    print(" Entry updated successfully!")

def subject_stats():
    query = """
    SELECT subject, SEC_TO_TIME(SUM(TIME_TO_SEC(study_time)))
    FROM study_sessions
    WHERE subject IS NOT NULL AND subject != '' AND subject != 'NA'
    GROUP BY subject
    ORDER BY SUM(TIME_TO_SEC(study_time)) DESC
    """
    
    cursor.execute(query)
    results = cursor.fetchall()

    if not results:
        print(" No data available.")
        return

    print("\n Study Time by Subject:\n")

    headers = ["Subject", "Total Time"]
    print(tabulate(results, headers=headers, tablefmt="fancy_grid"))

def today_summary():
    today = date.today()

    cursor.execute("""
    SELECT SEC_TO_TIME(SUM(TIME_TO_SEC(study_time)))
    FROM study_sessions
    WHERE date = %s
    """, (today,))

    result = cursor.fetchone()[0]

    if result is None:
        print("\n You haven't studied today yet!")
    else:
        print(f"\n Today's Study Time: {result}")

def monthly_view():
    year=input(" Enter year (YYYY): ")
    month=input(" Enter month (MM): ")

    #fetch entries of the month
    query_entries = """
    SELECT id, date, day, subject, topic, study_time
    FROM study_sessions
    WHERE YEAR(date) = %s AND MONTH(date) = %s
    ORDER BY date
    """

    cursor.execute(query_entries, (year, month))
    records=cursor.fetchall()

    if not records:
        print("\n No data for this month.")
        return
    print("\n Monthly Entries:\n")
    header = ["ID", "Date", "Day", "Subject", "Topic", "Time"]
    print(tabulate(records, headers=header, tablefmt="fancy_grid"))

def monthly_total_time():
    year = input(" Enter year (YYYY): ")
    month = input(" Enter month (MM): ")

    query = """
    SELECT SUM(TIME_TO_SEC(study_time))
    FROM study_sessions
    WHERE YEAR(date) = %s AND MONTH(date) = %s
    """

    cursor.execute(query, (year, month))
    total_seconds = cursor.fetchone()[0]

    if total_seconds is None:
        print("\n No study data for this month.")
        return

    days = total_seconds // (24 * 3600)
    remaining = total_seconds % (24 * 3600)

    hours = remaining // 3600
    minutes = (remaining % 3600) // 60
    seconds = remaining % 60

    total_hours = total_seconds // 3600

    print(f"\n Total Study Time for {month}-{year}: {days} days, {hours:02}:{minutes:02}:{seconds:02}")
    print(f" ({total_hours:02}:{minutes:02}:{seconds:02} hours)")

def weekly_report():
    today = date.today()
    last_week = today - timedelta(days=6)

    # Total time in last 7 days
    cursor.execute("""
    SELECT SUM(TIME_TO_SEC(study_time))
    FROM study_sessions
    WHERE date BETWEEN %s AND %s
    """, (last_week, today))

    total_seconds = cursor.fetchone()[0]

    if total_seconds is None:
        print("\n No study data for the last 7 days.")
        return

    # Convert total
    total_h = total_seconds // 3600
    total_m = (total_seconds % 3600) // 60
    total_s = total_seconds % 60

    # Average per day
    avg_seconds = total_seconds // 7
    avg_h = avg_seconds // 3600
    avg_m = (avg_seconds % 3600) // 60
    avg_s = avg_seconds % 60

    # Best & worst day
    cursor.execute("""
    SELECT date, SUM(TIME_TO_SEC(study_time)) as total
    FROM study_sessions
    WHERE date BETWEEN %s AND %s
    GROUP BY date
    ORDER BY total DESC
    """, (last_week, today))

    results = cursor.fetchall()

    best_day = results[0][1]
    worst_day = results[-1][1]

    # Convert best
    b_h = best_day // 3600
    b_m = (best_day % 3600) // 60
    b_s = best_day % 60

    # Convert worst
    w_h = worst_day // 3600
    w_m = (worst_day % 3600) // 60
    w_s = worst_day % 60

    print("\n Weekly Report (Last 7 Days):\n")

    print(f" Total: {total_h:02}:{total_m:02}:{total_s:02}")
    print(f" Average per day: {avg_h:02}:{avg_m:02}:{avg_s:02}")
    print(f" Best Day: {b_h:02}:{b_m:02}:{b_s:02}")
    print(f" Worst Day: {w_h:02}:{w_m:02}:{w_s:02}")

def menu():
    while True:
        print("\n Study Tracker \n")
        print(" 1. Add Entry")
        print(" 2. View Entries")
        print(" 3. Total Study Time")
        print(" 4. Update Entry")
        print(" 5. Subject wise stats")
        print(" 6. Today's Summary")
        print(" 7. Monthly View")
        print(" 8. Monthly Total Time")
        print(" 9. Weekly Report")
        print(" 10. Exit")

        choice=input("\n Enter choice: ")

        if choice=="1":
            add_entry()
        elif choice=="2":
            view_entries()
        elif choice=="3":
            total_time()
        elif choice=="4":
            update_entry()
        elif choice=="5":
            subject_stats()
        elif choice=="6":
            today_summary()
        elif choice=="7":
            monthly_view()
        elif choice=="8":
            monthly_total_time()
        elif choice=="9":
            weekly_report()
        elif choice=="10":
            break
        else:
            print(" Invalid choice!")
menu()


