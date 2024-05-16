import os
import pandas as pd
import functions


# First start menu
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

df = pd.read_excel(raw_file).fillna("---")
df = functions.fix_instructor(df)
df_by_sections = functions.split_sections(df)
#df_by_sections.to_excel("a.xlsx", index=False)

# Main menu after first start
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
        input("Press enter to continue with Main Menu.")
    elif inp == "2":
        functions.crn(df, input("Enter a CRN: "))
        input("Press enter to continue with Main Menu.")
    elif inp == "3":
        functions.find_schedule(df_by_sections, df)
        input("Press enter to continue with Main Menu.")
    elif inp == "4":
        if input("Are you sure? Updating will take couple of minutes. Y/N? ").upper() == "Y":
            try:
                functions.get_raw_data()
                df.to_excel("a.xlsx", index=False)
            except :
                print("Cannot update without internet connection.")
        input("Press enter to continue with Main Menu.")
    elif inp == "5":
        try:
            os.startfile("README.md")
        except:
            print("Cannot open file, you can find the Read-ME file in the current directory.")

