# --------------------------------------------------------------------------- #
# Title: Assignment07
# Desc: This assignment demonstrates using data classes
#       with structured error handling
# Change Log: (Who, When, What)
#   PAlves,8/27/2025,Created Script
# --------------------------------------------------------------------------- #

# --------------------------------------------------------------------------- #
# ------------------------- Imports ----------------------------------------- #
# --------------------------------------------------------------------------- #
import json

# --------------------------------------------------------------------------- #
# ------------------- Define the Data Constants ----------------------------- #
# --------------------------------------------------------------------------- #
MENU: str = '''
---- Course Registration Program ----
  Select from the following menu:  
    1. Register a Student for a Course
    2. Show current data  
    3. Save data to a file
    4. Exit the program
----------------------------------------- 
'''
FILE_NAME: str = "Enrollments.json"


# --------------------------------------------------------------------------- #
# ---------------------- Define the Global Data Variables ------------------- #
# --------------------------------------------------------------------------- #
students: list = []  # a table of student data
menu_choice: str  # Hold the choice made by the user.


# --------------------------------------------------------------------------- #
# ------------------------ Processing Layer --------------------------------- #
# --------------------------------------------------------------------------- #

# --------------------- Person class  --------------------------------------- #
class Person:
    """
    A class representing person data.

    Properties:
        first_name (str): The student's first name.
        last_name (str): The student's last name.

    ChangeLog:
        - PAlves, 8/27/2025, Created the class.
    """

    # Add first_name and last_name properties to the constructor
    def __init__(self, first_name: str = '', last_name: str = ''):
        self.first_name = first_name
        self.last_name = last_name

    # Getter for the first_name property
    @property
    def first_name(self):
        return self.__first_name.title()  # formatting code

    # Setter for the first_name property
    @first_name.setter
    def first_name(self, value: str):
        if value.isalpha():  # is character
            self.__first_name = value
        else:
            raise ValueError("The first name should not contain numbers or be blank.")

    # Getter for the last_name property
    @property
    def last_name(self):
        return self.__last_name.title()  # formatting code

    # Setter for the last_name property
    @last_name.setter
    def last_name(self, value: str):
        if value.isalpha():  # is character
            self.__last_name = value
        else:
            raise ValueError("The last name should not contain numbers or be blank.")

    # Override the __str__() method to return Person data
    def __str__(self):
        return f'{self.first_name},{self.last_name}'


# --------------------- Student class  --------------------------------------- #
# Inherit code from the Person class
class Student(Person):
    """
    A class representing student data.

    Properties:
        first_name (str): The student's first name.
        last_name (str): The student's last name.
        course_name (str): The name of the course the student will be enrolled in.

    ChangeLog: (Who, When, What)
    PAlves,08/27/2025,Created Class
    """

    def __init__(self, first_name: str = '', last_name: str = '', course_name: str = ''):
        #Use first name and last name from parent class (Person)
        super().__init__(first_name=first_name, last_name=last_name)

        #Define a course name property for child class Student
        self.course_name = course_name

    # Getter for the course_name property
    @property
    def course_name(self):
        return self.__course_name

    # Setter for the course_name property
    @course_name.setter
    def course_name(self, value: str):
        if value != '':
            self.__course_name = value
        else:
            raise ValueError("The course name should not be blank.")

    # Override the Parent __str__() method behavior to return a coma-separated string of data
    def __str__(self):
        return f'{self.first_name},{self.last_name},{self.course_name}'



# --------------------------------------------------------------------------- #
# -------------------------- Data Layer ------------------------------------- #
# --------------------------------------------------------------------------- #

# --------------------- FileProcessor class  -------------------------------- #
class FileProcessor:
    """
    A collection of processing layer functions that work with Json files

    ChangeLog: (Who, When, What)
    PAlves, 8/20/2025,Created Class

    """

    # ---------------------- read_data_from_file function ------------------- #
    @staticmethod
    def read_data_from_file(file_name: str):
        """ This function read data from the JSON file into student_data list

        ChangeLog: (Who, When, What)
        PAlves, 8/20/2025,Created function

        :param file_name: string data with name of file to read from

        :return: list
        """

        student_object = []

        try:
            file = open(file_name, "r")

            # the load function returns a list of dictionary rows from the json data file
            json_students = json.load(file)

            #define local variable
            student_object = []

            #Convert the list of dictionaries into a list of Student objects

            student_object = [Student(first_name=student["FirstName"],
                                       last_name=student["LastName"],
                                       course_name=student["CourseName"])
                              for student in json_students]

            file.close()

        except FileNotFoundError as e:
            IO.output_error_messages("Text file must exist before\
             running this script!", e)

        except Exception as e:
            IO.output_error_messages("There was a non-specific error!", e)

        finally:
            if not file.closed:
                file.close()

        return student_object


    # --------------------- write_data_to_file function --------------------- #
    @staticmethod
    def write_data_to_file(file_name: str, student_data: list):
        """ This function writes data onto the JSON file

        ChangeLog: (Who, When, What)
        PAlves, 8/20/2025,Created function

        :param file_name: string data with name of file to write to
        :param student_data: list of dictionary rows to be writen to the file

        :return: None
        """

        try:
            file = open(file_name, "w")

            json_students_dict = []

            for student in student_data:
                json_students_dict.append({
                            "FirstName": student.first_name,
                            "LastName": student.last_name,
                            "CourseName": student.course_name})

            json.dump(json_students_dict, file,indent=2)
            file.close()
            IO.output_current_student_data(student_data=student_data)

        except TypeError as e:
            IO.output_error_messages("Please check that the data is \
            a valid JSON format", e)
        except Exception as e:
            IO.output_error_messages("There was a non-specific error!", e)
        finally:
            if not file.closed:
                file.close()


# --------------------------------------------------------------------------- #
# --------------------- Presentation Layer ---------------------------------- #
# --------------------------------------------------------------------------- #

# -------------------------- IO class  -------------------------------------- #
class IO:
    """
    A collection of presentation layer functions that manage user
    input and output

    ChangeLog: (Who, When, What)
    PAlves, 8/20/2025,Created Class
    """

    # ------------------ output_error_messages function --------------------- #
    @staticmethod
    def output_error_messages(message: str, error: Exception = None):
        """ This function displays a custom error messages to the user

        ChangeLog: (Who, When, What)
        PAlves, 8/20/2025,Created function

        :return: None
        """
        print("-" * 65)
        print(message, end="\n\n")
        print("-" * 65)
        if error is not None:
            print("-" * 65)
            print("-- Technical Error Message -- ")
            print(error, error.__doc__, type(error), sep='\n')
            print("-" * 65)

    # ------------------------ output_menu function ------------------------- #
    @staticmethod
    def output_menu(menu: str):
        """ This function displays the menu of choices to the user

        ChangeLog: (Who, When, What)
        PAlves, 8/20/2025,Created function

        :return: None
        """
        print()
        print(menu)
        print()  # Adding extra space to make it look nicer.

    # ------------------- input_menu_choice function ------------------------ #
    @staticmethod
    def input_menu_choice():
        """ This function gets a menu choice from the user

        ChangeLog: (Who, When, What)
        PAlves, 8/20/2025,Created function

        :return: string with the users choice
        """
        choice = "0"
        try:
            choice = input("Enter your menu choice number: ")
            if choice not in ("1","2","3","4"):  # Note these are strings
                raise Exception("Error: Please, choose only 1, 2, 3, or 4")

        except Exception as e:
            IO.output_error_messages(e.__str__())

        return choice

    # ----------------- input_student_data function ------------------------- #
    @staticmethod
    def input_student_data(student_data: list):
        """ This function gets the first name, last name, and Course Name

        ChangeLog: (Who, When, What)
        PAlves, 8/20/2025,Created function

        :return: None
        """

        try:
            # Input the data

            #student = Student()  # Note this will use the default empty string arguments
            #student.first_name: str = input("What is the student's first name? ")
            #student.last_name: str = input("What is the student's last name? ")
            #student.course_name: str  = input("What is the course name? ")

            student_first_name = input("Enter the student's first name: ")
            student_last_name = input("Enter the student's last name: ")
            course_name = input("Enter the name of the course: ")

            student = Student(first_name=student_first_name,
                               last_name=student_last_name,
                               course_name=course_name)

            student_data.append(student)
            print()
            print(f"You have enrolled {student_first_name} {student_last_name} in course  {course_name}.")

        except ValueError as e:
            IO.output_error_messages("That value is not the correct "\
                                     "type of data!", e)
        except Exception as e:
            IO.output_error_messages("There was a non-specific error!", e)
        return student_data

    # ----------- output_current_student_data function --------------------- #
    @staticmethod
    def output_current_student_data(student_data: list):
        """ This function Displays the current student data

        ChangeLog: (Who, When, What)
        PAlves, 8/20/2025,Created function

        :param student_data: list of dictionary rows to be displayed

        :return: None
        """

        student_object: str =''

        try:
            print("-" * 65)
            print("List of students currently registered for courses:")
            print("-" * 65)

            for student in student_data:
                #student_object: Student = Student(first_name=student["FirstName"],
                #                                  last_name=student["LastName"],
                #                                  course_name=student["CourseName"])
                print(student)

            print("-" * 65)
            print("IMPORTANT")
            print("- Some of these registrations might not be yet saved")
            print("- Make sure you use save registrations before exit")
            print("-" * 65)

        except ValueError as e:
            IO.output_error_messages(e)
        except Exception as e:
            IO.output_error_messages("There was a\
             non-specific error!", e)


    # ------------- output_check_unsaved_student_data function -------------- #
    @staticmethod
    def output_check_unsaved_student_data(file_name: str,student_data: list):
        """ This function Checks if there are any unsaved student data

        ChangeLog: (Who, When, What)
        PAlves, 8/20/2025,Created function

        :param file_name: json file name
        :param student_data: list of dictionary rows to be displayed

        :return: None
        """

        rec_on_file = []  # a table of student data already saved on JSON file

        try:
            rec_on_file = FileProcessor.read_data_from_file(file_name=FILE_NAME)

            if (len(student_data) != len(rec_on_file)):
                print("-" * 65)
                print("Warning: There are registrations not yet saved.")
                print("-" * 65)
                pend_save = input("Do you want to save the data? (y/n): ")
                if (pend_save == "y"):
                    # Invoke FileProcessor.write_data_to_file function to save data
                    FileProcessor.write_data_to_file(file_name=FILE_NAME,\
                                                     student_data=students)
                    print("-" * 65)
                    print("Unsaved data was written to JSON file!")
                    for row in student_data:
                        print(row.first_name, row.last_name, row.course_name)
                    print("-" * 65)

                else:
                    print("-" * 65)
                    print("Pending data were not saved to file!")
                    print("-" * 65)
        except ValueError as e:
            IO.output_error_messages(e)
        except Exception as e:
            IO.output_error_messages("There was a non-specific error!", e)


# --------------------------------------------------------------------------- #
# ------------------ Script Main body --------------------------------------- #
# --------------------------------------------------------------------------- #

# When the program starts:
#      Read from the Json file to extract data
#      Load extracted/read data into student_data list of lists (table)

students = FileProcessor.read_data_from_file(file_name=FILE_NAME)

# ------------ Infinite loop until menu_option 4 is chosen ------------------ #
while True:
    IO.output_menu(menu=MENU)
    menu_choice = IO.input_menu_choice()

    # ---------- menu_option 1 - Register a Student for a Course ------------ #
    if menu_choice == "1":
        students = IO.input_student_data(student_data=students)
        continue

    # ---------- menu_option 2 - Show current data -------------------------- #
    elif menu_choice == "2":
        IO.output_current_student_data(student_data=students)
        continue

    # ---------- menu_option 3 - Save student data to JSON file ------------- #
    elif menu_choice == "3":
        FileProcessor.write_data_to_file(file_name=FILE_NAME,student_data=students)
        continue

    # - menu_option 4 - Check unsaved data and break loop to finish script -- #
    elif menu_choice == "4":
        IO.output_check_unsaved_student_data(file_name=FILE_NAME,student_data=students)
        break

# --------------------------------------------------------------------------- #
# -------------------- End of script  --------------------------------------- #
# --------------------------------------------------------------------------- #