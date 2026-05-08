# -----------------------------------------------------------
# Name: Olorunsogo (Bidemi) Adeoye
# Course: KSU Python Course
# Project: Healthcare Appointment No-Show Analysis Program
# Description:
# This program analyzes healthcare appointment data from a CSV file
# and identifies patterns in missed appointments (no-shows).
# It uses a menu-driven interface and does not require external libraries:
# - Overall no-show rate
# - No-show rate by day of week
# - No-show rate by time of day
# - No-show rate by age group
# -----------------------------------------------------------

import csv
import os

# -----------------------------------------------------------
# Load Data
# -----------------------------------------------------------
def load_data():
    file_name = input("\nEnter the CSV file name: ")

    try:
        with open(file_name, mode='r') as file:
            # DictReader converts each CSV row into a dictionary
            # using the column headers as keys.
            reader = csv.DictReader(file)
            # Convert the CSV data into a list so it can be reused
            # throughout the program without reopening the file.
            data = list(reader)

            if not data:
                print("\nERROR: File is empty.\n")
                return None

            print("\nData loaded successfully.\n")
            print("Detected columns:", list(data[0].keys()), "\n")

            if validate_columns(data):
                return data
            else:
                return None

    except FileNotFoundError:
        print("\nError: File not found.\n")
        return None


# -----------------------------------------------------------
# Using a safe getter prevents crashes caused by missing
# or improperly formatted CSV fields.
# -----------------------------------------------------------
def safe_get(row, key):
    return row.get(key, "").strip()

# -----------------------------------------------------------
# Validate required columns
# -----------------------------------------------------------
def validate_columns(data):
    required_columns = [
        'age',
        'appointment_time',
        'day_of_week',
        'attended'
    ]

    actual_columns = list(data[0].keys())

    missing = [col for col in required_columns if col not in actual_columns]

    if missing:
        print("\nERROR: Missing required columns:")
        for col in missing:
            print("-", col)

        print("\nPlease load a properly formatted CSV file.\n")
        return False

    return True

# -----------------------------------------------------------
# Overall No-Show Rate
# -----------------------------------------------------------
def overall_no_show_rate(data):
    try:
        total = len(data)
        # Count how many appointments were marked as "no"
        # to calculate the missed appointment rate.
        no_show = sum(1 for row in data if safe_get(row, 'attended').lower() == 'no')

        rate = (no_show / total) * 100
        print(f"\nOverall No-Show Rate: {rate:.2f}%\n")

    except Exception as e:
        print("Error processing data:", e)


# -----------------------------------------------------------
# Text-based charts were intentionally used instead of
# external visualization libraries to maximize portability.
# -----------------------------------------------------------
def print_bar_chart(results):
    for key, value in results.items():
        # Scale the number of stars to visually represent
        # percentages in a simple text-based chart.
        bar = '*' * int(value / 2)
        print(f"{key:15} | {bar} ({value:.2f}%)")
    print()


# -----------------------------------------------------------
# No-Show by Day
# -----------------------------------------------------------
def no_show_by_day(data):
    try:
        results = {}

        for row in data:
            day = safe_get(row, 'day_of_week')

            if not day:
                continue

            # Create a new tracking entry for each day
            # encountered in the dataset.
            if day not in results:
                results[day] = {'total': 0, 'no_show': 0}

            results[day]['total'] += 1
            if safe_get(row, 'attended').lower() == 'no':
                results[day]['no_show'] += 1

        rates = {d: (v['no_show']/v['total'])*100 for d, v in results.items()}

        print("\nNo-Show Rate by Day:\n")
        print_bar_chart(rates)

    except Exception as e:
        print("Error:", e)


# -----------------------------------------------------------
# No-Show by Time
# -----------------------------------------------------------
def no_show_by_time(data):
    try:
        results = {'Morning': {'total': 0, 'no_show': 0},
                   'Afternoon': {'total': 0, 'no_show': 0}}

        for row in data:
            time_val = safe_get(row, 'appointment_time')

            if not time_val:
                continue

            # Extract the hour portion of the appointment time
            # so appointments can be grouped by time of day.
            hour = int(time_val.split(':')[0])
            category = 'Morning' if hour < 12 else 'Afternoon'

            results[category]['total'] += 1
            if safe_get(row, 'attended').lower() == 'no':
                results[category]['no_show'] += 1

        rates = {k: (v['no_show']/v['total'])*100 for k, v in results.items() if v['total'] > 0}

        print("\nNo-Show Rate by Time:\n")
        print_bar_chart(rates)

    except Exception as e:
        print("Error:", e)


# -----------------------------------------------------------
# No-Show by Age
# -----------------------------------------------------------
def no_show_by_age(data):
    try:
        groups = {
            'Child': {'total': 0, 'no_show': 0},
            'Adult': {'total': 0, 'no_show': 0},
            'Middle Age': {'total': 0, 'no_show': 0},
            'Senior': {'total': 0, 'no_show': 0}
        }

        for row in data:
            age_val = safe_get(row, 'age')

            if not age_val.isdigit():
                continue

            age = int(age_val)

            # Patients are grouped into age categories
            # to identify trends among different populations.
            if age < 18:
                group = 'Child'
            elif age < 40:
                group = 'Adult'
            elif age < 65:
                group = 'Middle Age'
            else:
                group = 'Senior'

            groups[group]['total'] += 1
            if safe_get(row, 'attended').lower() == 'no':
                groups[group]['no_show'] += 1

        rates = {k: (v['no_show']/v['total'])*100 for k, v in groups.items() if v['total'] > 0}

        print("\nNo-Show Rate by Age:\n")
        print_bar_chart(rates)

    except Exception as e:
        print("Error:", e)


# -----------------------------------------------------------
# Export Summary
# -----------------------------------------------------------
def export_summary(data):
    try:
        results = {}

        for row in data:
            day = safe_get(row, 'day_of_week')

            if not day:
                continue

            if day not in results:
                results[day] = {'total': 0, 'no_show': 0}

            results[day]['total'] += 1
            if safe_get(row, 'attended').lower() == 'no':
                results[day]['no_show'] += 1

        file_name = "no_show_summary.csv"

        with open(file_name, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Day', 'NoShowRate'])

            for day, vals in results.items():
                rate = (vals['no_show']/vals['total'])*100
                # Write column headers into the exported CSV file
                # for easier readability outside the program.
                writer.writerow([day, round(rate, 2)])

        print("\nSummary exported successfully.")
        print("Saved at:", os.path.abspath(file_name), "\n")

    except Exception as e:
        print("Error:", e)


# -----------------------------------------------------------
# Menu
# -----------------------------------------------------------
def show_menu():
    print("===================================")
    print(" Healthcare No-Show Analysis Tool")
    print("===================================")
    print("\nPlease select an option from 1-7.")
    print("\n1. Overall No-Show Rate")
    print("2. No-Show by Day")
    print("3. No-Show by Time")
    print("4. No-Show by Age")
    print("5. Export Summary")
    print("6. Load New File")
    print("7. Exit")


# -----------------------------------------------------------
# Main
# -----------------------------------------------------------
def main():
    data = None

    # Main application loop keeps the program running
    # until the user chooses to exit.
    while True:
        if data is None:
            data = load_data()
            continue

        show_menu()
        choice = input("\nEnter choice: ").strip()

        if choice == '1':
            overall_no_show_rate(data)
        elif choice == '2':
            no_show_by_day(data)
        elif choice == '3':
            no_show_by_time(data)
        elif choice == '4':
            no_show_by_age(data)
        elif choice == '5':
            export_summary(data)
        elif choice == '6':
            data = load_data()
        elif choice == '7':
            print("\nThank you for using the Healthcare No-Show Analysis Tool.")
            break
        else:
            print("\nInvalid input. Please try again.\n")

# This ensures the program only runs when executed directly
# rather than when imported into another Python file.
if __name__ == "__main__":
    main()