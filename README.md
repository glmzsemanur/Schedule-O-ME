Attention! Currently Out of Date
## Schedule-O-ME
### Description
- Schedule-O-ME is designed for students who are seeking unoccupied classrooms to study in silence.
- With Schedule-O-ME, the user can find unoccupied classrooms in a given building and a given time interval.
- Schedule-O-ME also offers to search lecture by CRN code, as well as creating the schedule of an intructor or a classroom.
### Installation
- Schedule-O-ME is designed/and should work with Python 3.12.3
- Python must be installed from [Python Official Website](https://www.python.org/)
- All the required libraries are listed in the requirements.txt file and can be installed using the following steps:
-   1. Extract the zip file
    2. Open cmd at the folder of Schedule-O-ME
    3. Run the command below and wait until the installation is done.
    - pip install -r requirements.txt
- To run Schedule-O-ME, basically double click the Shedule-O-ME.py file.
### Usage
! You do not need to read this section, Schedule-O-ME will guide you through steps on its own.
- Schedule-O-ME requires internet connection to download data from web. A sample data is provided with the zip file.
- At first start, since there's already data, Schedule-O-ME will printout when the data was last updated and proceed with Main Menu.
- At first start, if there isn't any data, user needs to confirm downloading data from web, otherwise Schedule-O-ME will not work as intended.
- To download the data, enter Y or y to confirm downloading; anything else is regarded as a rejection.
- NOTICE: Updating the data will delete the existing data, and will take a couple of minutes.
- The Main Menu has 6 options; each option can be selected by its corresponding number.
-   1. Find-ME an empty classroom.
       - To find an unoccupied classroom, chose this option. (Enter 1 in the Main Menu.)
       - Chose a building from the list.
       - Chose a day you want to search in.
       - Enter the starting time that you want the search to start from. The format should be HH:MM For example: 09:20 or 18:30
       - Enter the ending time that you want the search to stop at.
       - Enter at least how long you want the classroom to be unoccupied in minutes. For example 120 for 2 hours.
       - Available classrooms will be printed out.
       - NOTICE: if a classroom's unoccupied time ends at the same time the search ends, then the classroom may be unoccupied further.
       - Hit enter to go back to Main Menu.
-  2. Fetch-ME a CRN.
       - To search a lecture by its CRN value, chose this option. (Enter 2 in the Main Menu.)
       - Enter the CRN you want to find.
       - If the CRN is found, corresponding lecture's information will be printed out.
       - Hit enter to go back to Main Menu.
-  3. Find-ME the schedule of a instructor/classroom.
       - To get the schedule of an instructor or a classroom, chose this option. (Enter 3 in the Main Menu)
       - Enter 1 to find the schedule of an instructor,
           -  If you don't know the instructor's full name, confirm (Y or y).
               - Enter a part of instructor's full name, all possible instructors will be printed out.
           -  Enter instructor's full name.
           -  How many lectures are held by the instructor will be printed out, with the information of the lectures.
           -  If you wish to see the lectures in full detail, confirm (Y or y).
           -  All lectures associated with the instructor will be printed out in full view.
       - Enter 2 to find the schedule of a classroom.
           -  Chose a building that the classroom is in.
           -  The classroom list will be printed out. Chose one.
           -  The schedule of the classroom will be printed out.
           -  NOTICE: Schdele may contain double CRNs, this is due to same lecture being in different times.
           -  If you wish to see the lectures in full detail, confirm (Y or y).
       - Hit enter to go back to Main Menu.
- 4. Update-ME
       - To update the data, chose this option. (Enter 4 in the Main Menu.)
       - Internet access is required to update the data.
       - Confirm if you wish to update the data.
       - NOTICE: Updating the data may take a couple of minutes and deletes the previous data.
       - Hit enter to go back to Main Menu.
- 5. Help-ME
       - To get information about Schedule-O-ME, chose this option. (Enter 5 in the Main Menu.)
       - Current file will be opened.
       - Hit enter to go back to Main Menu.
- 0. Exit
       - To terminate Schedule-O-ME, chose this option. (Enter 0 in the Main Menu.)

You are free to use, modify, and distribute this software for any purpose without worrying about licensing restrictions.
- Contact: gulmez22@itu.edu.tr
- GitHub: [Schedule-O-ME](https://github.com/glmzsemanur/Schedule-O-ME/tree/main)
