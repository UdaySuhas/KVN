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
