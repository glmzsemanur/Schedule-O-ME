import os
import pandas as pd
import functions
import subprocess


# First start menu, checks if scraped data is present or not.
# If data is not available, asks for permission to download it.
# If the data is available, proceeds with the main menu.
print("WELCOME TO Schedule-O-ME.")
folder_name = "scraped_data"
while True:
    if os.path.exists(folder_name):
        if os.listdir(folder_name):
            file, _ = os.listdir(folder_name)[0].split(".")
            if file:
                print(f"The last time data has been updated is {file}. Proceeding with main menu.")
                break
    print(f"There isn't any data in the directory, please confirm to update data.")
    while True:
        print(
            "Updating the data requires internet access and may take up to 10 minutes. Do you wish to proceed? Y/N?")
        if input().upper() == "Y":
            functions.get_raw_data()
            break
        else:
            print("The application cannot function without data. You may terminate the application or "
                  "proceed with updating the data.")
raw_file = f"scraped_data\\{file}.xlsx"

# Right before Main Menu, the data is read and formats/edits for better use.
df = pd.read_excel(raw_file).fillna("---")

# Removes double spaces between words.
df = functions.fix_double_space(df)

# Splits lectures with multiple sections if any, and saves it as another dataframe.
df_by_sections = functions.split_sections(df)

# Main menu after first start
# Prints out the Main Menu and runs the corresponding function to the user's input.
while True:
    print("MAIN MENU")
    print("1. Find-ME an empty classroom.")
    print("2. Fetch-ME a CRN.")
    print("3. Find-ME the schedule of a instructor/classroom.")
    print("4. Update-ME")
    print("5. Help-ME")
    print("0. Exit")
    inp = input("Your choice : ")
    if inp == "0":
        exit("User terminated the application")
    elif inp == "1":
        functions.find_empty(df_by_sections)
    elif inp == "2":
        functions.search_crn(df, input("Enter a CRN: "))
    elif inp == "3":
        functions.find_schedule(df_by_sections, df)
    elif inp == "4":
        if input("Are you sure? Updating will take couple of minutes. Y/N? ").upper() == "Y":
            try:
                functions.get_raw_data()
                df.to_excel("a.xlsx", index=False)
            except Exception as e:
                print("Cannot update without internet connection.", e)
    elif inp == "5":
        result = subprocess.run(["start", "README.md"], shell=True, stdout=subprocess.DEVNULL,
                                stderr=subprocess.DEVNULL)
        if result.returncode == 0:
            print("Read-ME file has been opened successfully.")
        else:
            print("Cannot open file, you may find the Read-ME.md file in the current directory.")
    else:
        print("Invalid choice.")
    input("Press enter to continue with Main Menu.")
