"""
All templates for request handlers.
"""
# --------LOGIN-------------
LOGIN_TRUE = "\nYou have logged in successfully."
LOGIN_REQUIRED = "\nYou must be logged in to proceed."
LOGIN_WRONG_PASSWORD = "\nyo, Wrong password buddy!"
LOGIN_ALREADY = "\nYo, slow down buddy, you already logged in there!"
LOGIN_NO_USERNAME = "Yo, Check your username. Its not registered yet."

# --------ADMIN------------
ADMIN_REQUIRED = "\nYou must be admin to execute this command."

# -------REGISTER-----------
REGISTER_USERNAME_UNVAIL = "\nUsername not available.\nChoose Different Username."
REGISTER_INVALID = "\nInvalid Username / Password Entered."
REGISTER_SUCCESS = "\nRegistration Successfully done.\nYou are good to do login."

# ------QUIT-----------------
LOG_OUT_MSG = "\nYep, You logged out there."

# ------COMMANDS-------------
COMMANDS = "\n-----   Commands are as follows   -----"
COMMANDS += "\nCommands                                    | Description"
COMMANDS += "\nregister <username> <password> <privileges> | Register a new user."
COMMANDS += "\nlogin <username> <password>                 | Login."
COMMANDS += "\ndelete <username> <password>                | Delete the user with <username> (Only for admin)."
COMMANDS += "\nlist                                        | Print all file and folders."
COMMANDS += "\nchange_folder <name>                        | Change current folder to <name>."
COMMANDS += "\nread_file <name>                            | Read file with <name>."
COMMANDS += "\nwrite_file <name> <input>                   | Write <input> to file <name>."
COMMANDS += "\ncreate_folder <name>                        | Create a new folder with <name>."


# -----DELETE---------------------
def delete_success(user):
    """
    Delete user template.
    """
    return "\nYep, Deleted user with username " + user + " successfully"

def no_user_found(user):
    """
    No user found template
    """
    return "\nYo, No such user with username " + user + " found. Check username again."



# ----CHANGE FOLDER-----------------
INCORRECT_DIRECTORY = "\nYo, Check your directory name again. Its wrong."

def ch_dir_success(direc):
    """
    Change directory template.
    """
    return "\nYes, Changed directory to " + direc + " successfully"

# -------LIST-------------------
def list_folder(total_list):
    """
    List folder template.
    """
    return "\n" + "\n".join(total_list)

# ------READ FILE--------------
READ_WRONG_PATH = "\nYo, check your path again. Its Wrong."

def read_file(start, data):
    """
    Read file template.
    """
    return "\n" + "--------------------------FILE READER------------------------------\n-----------Currently showing characters " + start + " to " + str(int(start) + 100) + "------------------- \n" + data

# ------WRITE FLE--------------
WRITE_NEW_PATH = "\nWritten in new file."
WRITE_EXISTING = "\nCompleted."

# ------CREATE FOLDER----------
DIRECTORY_SUCCESS = "\nCompleted making a new directory!"
DIRECTORY_PRESENT = "\nDirectory exists already!"
