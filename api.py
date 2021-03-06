"""
Server Requesthandler Class.
"""

import json
import os
import shutil
from os.path import join, normpath, realpath, isfile, isdir
from .templates import *

class RequestHandler():
    """
    Class - RequestHandler
    Manages all the user commands and its interactions

    Attributes:
    -----------------
        username : str
            username of user logged in.

        login_flag : bool
            Is user logged in or not.

        user_passwords : dict(user:password)
            Registered user passwords.

        user_privileges : dict(user:privileges)
            Registered user privileges.

        present_directory : str
            Current directory user working on.

        read_record : dict{path:index}
            Read file status till where it has already read.

    Methods:
    -----------------
        respond(statement):
            Map the statement to valid commands.

        register(username, password, privileges):
            Register a new user.

        login(username, password):
            Login a user.

        list():
            List of all files in directory.

        quit():
            Logout and reset all session.

        change_folder(directory):
            Change folder to desired directory.

        read_file(path):
            Read a specified file.

        write_file(path, data):
            Write file with data.
    """
    def __init__(self):
        """
        Init
        """
        self.username = None
        self.login_flag = False
        self.user_passwords = self.load_passwords()
        self.user_privileges = self.load_privileges()
        self.present_directory = ""
        self.read_record = {}
        self.read_char = 100

    def load_passwords(self):
        """
        Load passwords form session

        Return : dict{user:password}
            Returns a dictionary of username and passwords.

        """
        with open("server_session/server_data") as file:
            data = json.load(file)
        return data["passwords"][0]

    def load_privileges(self):
        """
        Load privileges form session

        Return : dict{user:privileges}
            Returns a dictionary of username and privileges.

        """
        with open("server_session/server_data") as file:
            data = json.load(file)
        return data["privileges"][0]

        
        
     def respond(self, statement):
        """
        Respont to execute all of the commands

        Parameters:
            statement : str

        Return: str
            Return the command output in string.
        """
        statement = statement.rstrip("\n")
        statement = statement.split(" ")
        executer = statement[0]
        if executer == "commands":
            return self.commands()
        if executer == "register":
            if len(statement) == 4:
                try:
                    username = statement[1]
                    password = statement[2]
                    privileges = statement[3]
                except:
                    return "Wrong input"
                return self.register(username, password, privileges)
            return "Check your input again"
        if executer == "quit":
            return self.quit()
        if executer == "login":
            if len(statement) == 3:
                try:
                    username = statement[1]
                    password = statement[2]
                except:
                    return "Wrong input"
                return self.login(username, password)
            return "Check your input again"
        if executer == "list":
            return self.list()
        if executer == "change_folder":
            return self.change_folder(statement[1])
        if executer == "read_file":
            return self.read_file(statement[1])
        if executer == "write_file":
            return self.write_file(statement[1], " ".join(statement[2:]))
        if executer == "create_folder":
            return self.create_folder(statement[1])
        if executer == "delete":
            return self.delete(statement[1], statement[2])
        return "Invalid command"
    
    
    def add_new_user(self, user, password, privileges):
        """
        Add a new user and save the user to session.

        Parameters:
            user : str
            password : str
            privileges : str

        """
        self.user_passwords[user] = password
        self.user_privileges[user] = privileges
        with open("server_session/server_data", "w+") as file:
            json.dump({"passwords":[self.user_passwords], "privileges":[self.user_privileges]}, file)
        os.mkdir(join("server_session", user))

    def rewrite_session(self):
        """
        Update the session.
        """
        with open("server_session/server_data", "w+") as file:
            json.dump({"passwords":[self.user_passwords], "privileges":[self.user_privileges]}, file)

    def commands(self):
        """
        All available commands on server

        Return: str
            List of all commands.
        """
        return COMMANDS

    def login_required(self):
        """
        Is logged in or not.

        Return: bool
            Logged in or not
        """
        return not self.login_flag

    def admin_required(self):
        """
        Is admin or not.

        Return: bool
            Is admin or not
        """
        return not self.user_privileges[self.username] == "admin"

    def user_availability(self, user):
        """
        User available in session data or not.

        Parameters:
            user : str

        Return: bool
            User available or not
        """
        return not user in list(self.user_passwords.keys())

    def password_check(self, user, password):
        """
        Validate password of the user.

        Parameters:
            user : str
            password : str

        Return: bool
            correct password ot wrong.
        """
        return not password == self.user_passwords[user]

    def self_password_check(self, password):
        """
        Validate self password.

        Parameters:
            password : str

        Return: bool
            Check self password.
        """
        return self.password_check(self.username, password)

        
     def login(self, user, password):
        """
        Login command.
        Parameters:
            user : str
            password : str

        Return: str
            Login response.
        """
        if not self.login_required():
            return LOGIN_ALREADY
        if self.user_availability(user):
            return LOGIN_NO_USERNAME
        if self.password_check(user, password):
            return LOGIN_WRONG_PASSWORD
        self.login_flag = True
        self.username = user
        self.present_directory = ""
        return LOGIN_TRUE

    def quit(self):
        """
        Quit Command.

        Return: str
            Quit response
        """
        self.present_directory = ""
        self.login_flag = False
        self.username = None
        self.read_record = {}
        return LOG_OUT_MSG

    def register(self, user, password, privileges):
        """
        Register command

        Parameters:
            user : str
            password : str
            privileges : str

        Return: str
            Register response.

        """
        if user in list(self.user_passwords.keys()):
            return REGISTER_USERNAME_UNVAIL
        if user == "" or password == "" or privileges == "":
            return REGISTER_INVALID
        self.add_new_user(user, password, privileges)
        return REGISTER_SUCCESS

    def delete(self, user, password):
        """
        Delete command

        Parameters:
            user : str
            password : str

        Return: str
            Delete response

        """
        if self.login_required():
            return LOGIN_REQUIRED
        if self.admin_required():
            return ADMIN_REQUIRED
        if self.user_availability(user):
            return no_user_found(user)
        if self.self_password_check(password):
            return LOGIN_WRONG_PASSWORD
        del self.user_passwords[user]
        del self.user_privileges[user]
        self.rewrite_session()
        if user == self.username:
            self.login_flag = False
        user_path = join("server_session", user)
        shutil.rmtree(user_path)
        return delete_success(user)
    
    def check_folder_path(self, directory):
        """
        Check available folders in a directory

        Parameters:
            directory : str

        Return: bool
            Directory in available directories.
        """
        total = []
        for direc, files, sub in os.walk(join("server_session", self.username)):
            total.append(normpath(realpath(direc)))
        total_path = join("server_session", self.username, self.present_directory, directory)
        real_path = realpath(total_path)
        path_to_be_change = normpath(real_path)
        return not path_to_be_change in total

    def change_folder(self, directory):
        """
        Change folder command.

        Parameters:
            directory : str

        Return: str
            Change folder response

        """
        if self.login_required():
            return LOGIN_REQUIRED
        if self.check_folder_path(directory):
            return INCORRECT_DIRECTORY
        self.present_directory = join(self.present_directory, directory)
        return ch_dir_success(directory)

    def list(self):
        """
        List command.

        Return: str
            List response.
        """
        if self.login_required():
            return LOGIN_REQUIRED
        total_files = []
        for file in os.listdir(join("server_session", self.username, self.present_directory)):
            total_files.append(file)
        return list_folder(total_files)

    def list_files(self):
        """
        Available files in folder.

        Return: list
            List of files
        """
        available_files = []
        for file in os.listdir(join("server_session", self.username, self.present_directory)):
            if isfile(join("server_session", self.username, self.present_directory, file)):
                available_files.append(file)
        return available_files

    def load_read_indexes(self, path):
        """
        Load the read index status of user's session.

        Parameters:
            path : str

        Return: int
            index of file read.
        """
        try:
            return self.read_record[path]
        except KeyError:
            self.read_record[path] = 0
            return self.read_record[path]

    def get_total_path(self, path):
        """
        Get full path.

        Parameters:
            path : str

        Return: str
            absolute path of the path parameter.
        """
        return join("server_session", self.username, self.present_directory, path)

    def read_content(self, path):
        """
        Read content with its read index.

        Parameters:
            path : str

        Return: str
            Data of file.

        """
        path = self.get_total_path(path)
        self.load_read_indexes(path)
        with open(path, "r") as file:
            contents = file.read()
        index = str(self.read_record[path]*self.read_char)
        data = contents[self.read_record[path]*self.read_char:((self.read_record[path]*self.read_char)+1)*self.read_char]
        self.read_record[path] += 1
        self.read_record[path] %= len(contents)//self.read_char + 1
        return read_file(index, data)

    def check_file_path_to_read(self, path):
        """
        File in folder or not.

        Parameters:
            path : str

        Return: bool
            File to be read in path or not.
        """
        total_files = self.list_files()
        return not path in total_files

    def read_file(self, path):
        """
        Read file command.

        Parameters:
            path : str

        Return: str
            Read file response
        """
        if self.login_required():
            return LOGIN_REQUIRED
        if self.check_file_path_to_read(path):
            return READ_WRONG_PATH
        return self.read_content(path)

    def check_file_path_to_write(self, path):
        """
        Check file in folder or not.

        Parameters:
            path : str

        Return: bool
            File in directory or not.
        """
        total_files = self.list_files()
        return not path in total_files

    def write(self, path, data, method):
        """
        Write data to file.

        Parameters:
            path : str
            data : str
            method : str
                Write or append method.
        """
        path = self.get_total_path(path)
        if method == "w":
            with open(path, "w+") as file:
                file.write(data)
                return
        with open(path, "a+") as file:
            file.write("\n" + data)

    def write_file(self, path, data):
        """
        Write file command.

        Parameters:
            path : str
            data : str

        Return: str
            Write file response
        """
        if self.login_required():
            return LOGIN_REQUIRED
        if self.check_file_path_to_write(path):
            self.write(path, data, "w")
            return WRITE_NEW_PATH
        self.write(path, data, "a")
        return WRITE_EXISTING

    def check_subdirectories(self, path):
        """
        Check subdirectories of a path

        Parameters:
            path : str

        Return: bool
            Path in available directories.
        """
        present_directory = join("server_session", self.username, self.present_directory)
        directories = []
        for sub in os.listdir(present_directory):
            if isdir(join(present_directory, sub)):
                directories.append(sub)
        return path in directories

    def create_folder(self, path):
        """
        Create folder in a path.

        Parameters:
            path : str

        Return: str
            Create folder response
        """
        if self.login_required():
            return LOGIN_REQUIRED
        if self.check_subdirectories(path):
            return DIRECTORY_PRESENT
        os.mkdir(self.get_total_path(path))
        return DIRECTORY_SUCCESS
