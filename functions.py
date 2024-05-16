import requests
import shutil
import os
from bs4 import BeautifulSoup
import pandas as pd
import sys
from datetime import datetime, timedelta
import openpyxl


def get_raw_data(website_url="https://www.sis.itu.edu.tr/EN/student//course-schedules//course-schedules.php?seviye=",
                 seviye_list=['OL', 'LS', 'LU']):
    headers = None
    codes = []
    for seviye in seviye_list:
        codes.append(extract_options_from_website(website_url+seviye+'&derskodu'))
    data = []
    len_codes = sum([len(code) for code in codes]) - len(codes)
    i = 1
    for index, subsegments in enumerate(codes):
        for code in subsegments[1:]:
            sys.stdout.write("\rStatus: {}/{}".format(i, len_codes))
            sys.stdout.flush()
            i += 1
            sub_url = f"{website_url}{seviye_list[index]}&derskodu={code}"
            sub_response = requests.get(sub_url)
            if sub_response.status_code == 200:
                sub_soup = BeautifulSoup(sub_response.content, 'html.parser')
                sub_table = sub_soup.find('table')
                if sub_table:
                    sub_rows = sub_table.find_all('tr')
                    if headers is None:
                        sub_cells = sub_rows[1].find_all('td')
                        headers = [cell.get_text(strip=True) for cell in sub_cells]
                    for sub_row in sub_rows[2:]:
                        sub_cells = sub_row.find_all('td')
                        data_row = [cell.get_text(" ", strip=True) for cell in sub_cells[:]]
                        data.append(data_row)
    print()
    df = pd.DataFrame(data, columns=headers)
    timestamp = datetime.now().strftime("%Y-%m-%d")
    if os.path.exists("scraped_data"):
        shutil.rmtree("scraped_data")
    os.makedirs("scraped_data")
    df.to_excel(f"scraped_data/{timestamp}.xlsx", index=False)
    print("Data has been scraped successfully.")
    return


def crn(df, c):
    index = df.index[df.iloc[:, 0] == int(c)].tolist()
    if index:
        max_header_len = max(len(header) for header in df.columns)
        print("########################################")
        for idx in index:
            for header, value in zip(df.columns, df.iloc[idx]):
                padding = max_header_len - len(header) + 2
                print(f"{header}:{' ' * padding}{value}")
            print("########################################")
    else:
        print("CRN not found")


def extract_options_from_website(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        dropdown = soup.find('select', {'name': 'derskodu'})
        if dropdown:
            options = [option.text.strip() for option in dropdown.find_all('option')]
            return options
        else:
            print("Dropdown not found on the webpage.")
            return []
    else:
        print("Failed to fetch webpage:", response.status_code)
        return []


def split_sections(df):
    new_rows = []
    for index, row in df.iterrows():
        if len(row["Time"]) >= 19:
            if len(row["Building"].split()) == 1:
                row["Building"] = "-- --"
            if len(row["Room"].split()) == 1:
                row["Room"] = "-- --"
            new_row1, new_row2 = row.copy(), row.copy()
            new_row1["Time"], new_row2["Time"] = row["Time"].split()[0], row["Time"].split()[1]
            new_row1["Building"], new_row2["Building"] = row["Building"].split()[0], row["Building"].split()[1]
            new_row1["Room"], new_row2["Room"] = row["Room"].split()[0], row["Room"].split()[1]
            new_row1["Day"], new_row2["Day"] = row["Day"].split()[0], row["Day"].split()[1]
            new_rows.extend([new_row1, new_row2])
        if len(row["Time"]) == 29:
            new_row3 = row.copy()
            new_row3["Time"] = row["Time"].split()[2]
            new_row3["Building"] = row["Building"].split()[2]
            new_row3["Room"] = row["Room"].split()[2]
            new_row3["Day"] = row["Day"].split()[2]
            new_rows.append(new_row3)
        if len(row["Time"]) < 19:
            new_rows.append(row)
    df = pd.DataFrame(new_rows)
    return df


def round_up_time(dt):
    if dt.minute == 59:
        dt += timedelta(hours=1)
        dt = dt.replace(minute=0)
    if dt.minute == 29:
        dt = dt.replace(minute=30)
    return dt


def find_empty(df):
    building_list = df["Building"].unique().tolist()
    building_list = [building for building in building_list if not building.startswith("-")]
    building_list.sort()
    day_list = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma"]
    while True:
        print("Chose an available building : ")
        for building in building_list:
            print(building, end=" ")
        building = input("\nYour choice : ").upper().strip()
        if building not in building_list:
            print("Invalid, please try again.")
        else:
            break
    while True:
        print("Chose a day:", end=" ")
        for day in day_list:
            print(day, end=" ")
        day = input("\nYour choice : ").capitalize().strip()
        if day not in day_list:
            print("Invalid, please try again.")
        else:
            break
    filtered_df = df[df['Building'] == building]
    rooms = filtered_df["Room"].unique().tolist()
    rooms = [room for room in rooms if not room.startswith("-")]
    filtered_df = filtered_df[(filtered_df["Day"] == day) & (filtered_df["Room"].isin(rooms))]
    # filtered_df.to_excel("b.xlsx", index=False)
    rooms.sort()
    occupied_rooms = {room: [] for room in rooms}
    for index, row in filtered_df.iterrows():
        time_interval = row['Time']
        room = row['Room']
        start_time, end_time = time_interval.split('/')
        start_datetime = datetime.strptime(start_time, '%H%M')
        end_datetime = datetime.strptime(end_time, '%H%M')
        end_datetime = round_up_time(end_datetime)
        occupied_rooms[room].append([start_datetime.strftime('%H:%M'), end_datetime.strftime('%H:%M')])
    occupied_rooms = {key: sorted(value, key=lambda x: x[0]) for key, value in occupied_rooms.items()}
    while True:
        start_input = input("From what time are you searching? (Format = HH:MM) : ")
        end_input = input("Till what time are you searching? (Format = HH:MM) : ")
        interval_len = input("How many minutes do you need? : ")
        try:
            interval_len = int(interval_len) - 1
        except ValueError:
            interval_len = 1
        try:
            range_start = datetime.strptime(start_input, '%H:%M')
            range_end = datetime.strptime(end_input, '%H:%M')
            break
        except ValueError:
            print("Invalid values, please re-enter in desired format.")
    unoccupied_rooms = {room: find_unoccupied_intervals(interval, range_start, range_end) for room, interval
                        in occupied_rooms.items()}
    for room, intervals in unoccupied_rooms.items():
        for interval in intervals:
            if ((datetime.strptime(interval[1], '%H:%M') - datetime.strptime(interval[0], '%H:%M')).total_seconds() / 60
                    >= interval_len):
                print(f"{room:<4} is unoccupied from {interval[0]} to {interval[1]}.")
    if not unoccupied_rooms:
        print("No unoccupied rooms are available.")


def find_unoccupied_intervals(occupied_intervals, range_start_time, range_end_time):
    occupied_intervals = [(datetime.strptime(start, '%H:%M'), datetime.strptime(end, '%H:%M')) for start, end in
                          occupied_intervals]
    possible_intervals = [(range_start_time, range_start_time)]
    current_time = range_start_time
    while current_time < range_end_time:
        next_time = current_time + timedelta(minutes=30)
        possible_intervals.append([current_time, next_time])
        current_time = next_time
    for interval in occupied_intervals:
        possible_intervals = [[start, end] for start, end in possible_intervals if
                              end <= interval[0] or start >= interval[1]]
    unoccupied_intervals = [[start.strftime('%H:%M'), end.strftime('%H:%M')] for start, end in possible_intervals if
                            start >= range_start_time and end <= range_end_time]
    merged_intervals = []
    for start, end in sorted(unoccupied_intervals):
        if merged_intervals and start <= merged_intervals[-1][1]:
            merged_intervals[-1][1] = end
        else:
            merged_intervals.append([start, end])
    return [interval for interval in merged_intervals if interval[0] != interval[1]]


def fix_instructor(df):
    new_rows = []
    for index, row in df.iterrows():
        new_row = row.copy()
        new_row["Instructor"] = " ".join(row["Instructor"].split())
        new_row["Course Title"] = " ".join(row["Course Title"].split())
        new_rows.append(new_row)
    return pd.DataFrame(new_rows)


def find_schedule(df, df_not_split):
    while True:
        print("Chose one of the following : ")
        a = input("1 - Instructor\n2 - Classroom\n")
        if a == "1" or a == "2":
            break
        else:
            print("Invalid. Please try again.")
    if a == "1":
        while True:
            print("Do you wish to see the instructors' names? Y/N? : ")
            a = input().upper()
            i = ""
            if a == "Y":
                i = input("Enter the a part of the instructor's name: ").title()
            instructors = df['Instructor'].unique().tolist()
            result = []
            for instructor in instructors:
                if "," in instructor:
                    instructo = instructor.split(",")
                    for ins in instructo:
                        ins = ins.strip()
                        if ins not in result:
                            result.append(ins)
                else:
                    result.append(instructor)
            result = list(set(result))
            instructors = [instructor for instructor in result if i in instructor]
            if a == "Y":
                print(instructors)
            instructor = input("Enter the instructor you wish to find the instructor's schedule : ").title()
            if instructor in instructors:
                break
            else:
                print(instructor, "not found. Try again.")
        schedule = df[df['Instructor'].str.contains(instructor, na=False)]
        crn_list = []
        for index, row in schedule.iterrows():
            crn_list.append([row['CRN'], row['Day'], row['Time'], row['Building'], row['Room'], row['Course Code']])
        if crn_list:
            print(instructor, "is the instructor of", len(crn_list), "lectures.")
            for crns in crn_list:
                print(f"{crns[0]:<5} - {crns[5]:<8} - {crns[1]:<10} - {crns[2]:<10} - {crns[3]:<8} - {crns[4]:<10}")
            a = input("Do you wish to see the lectures in detail? Y/N? : ").upper()
            if a == "Y":
                b = []
                for i in crn_list:
                    b.append(i[0])
                b = list(set(b))
                for c in b:
                    crn(df_not_split, c)
        else:
            print("No lecture found.")
        return

    if a == "2":
        building_list = df["Building"].unique().tolist()
        building_list = [building for building in building_list if not building.startswith("-")]
        building_list.sort()
        while True:
            print("Chose an available building : ")
            for building in building_list:
                print(building, end=" ")
            building = input("\nYour choice : ").upper().strip()
            if building not in building_list:
                print("Invalid, please try again.")
            else:
                df2 = df[df['Building'] == building]
                room_list = df2["Room"].unique().tolist()
                if room_list:
                    room_list = [room for room in room_list if not room.startswith("-")]
                    if room_list:
                        room_list.sort()
                        break
                    print("No rooms available in this building.")
                else:
                    print("No rooms available in this building.")
        while True:
            print("Chose an available classroom : ")
            for room in room_list:
                print(room, end=" ")
            room = input("\nYour choice : ").upper().strip()
            if room not in room_list:
                print("Invalid, please try again.")
            else:
                break
        schedule = df2[df2['Room'] == room]
        crn_list = []
        for index, row in schedule.iterrows():
            crn_list.append([row['CRN'], row['Day'], row['Time'], row['Instructor'], row['Course Code']])
        if crn_list:
            print(len(crn_list), f"lectures are held in {room}.")
            for cr in crn_list:
                print(f"{cr[0]} - {cr[4]:<8} - {cr[1]:<10} - {cr[2]:<10} - {cr[3]}")
            a = input("Do you wish to see the lectures in detail? Y/N? : ").upper()
            if a == "Y":
                b = []
                for i in crn_list:
                    b.append(i[0])
                b = list(set(b))
                for c in b:
                    crn(df_not_split, c)
