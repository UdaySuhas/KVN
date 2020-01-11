import unittest
import sys
import random
import string

from server.api import RequestHandler
from server.templates import *

def random_folder(string_length=6):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(string_length))


class ReqClassTestingStepOne(unittest.TestCase):
    """Handles the test for command and quit response"""

    def test_commands_response(self):
        """
        This test will check whether req_handle responds commands.
        """

        req_handle = RequestHandler()

        output = req_handle.commands()

        self.assertTrue(output)

    def test_commands_quit(self):
        """
        This test will check quit response.
        """
        expected_results = [LOG_OUT_MSG]
        results = []

        req_handle = RequestHandler()

        results.append(req_handle.quit())

        self.assertListEqual(results, expected_results)


class ReqClassTestingStepTwo(unittest.TestCase):
    """Handles the tests for login and listing the files"""

    def test_server_login(self):
        """
        This test will check login.
        Test1 : Wrong password
        Test2 : Wrong username
        Test3 : Proper login
        """
        req_handle = RequestHandler()
        req_handle.user_passwords = {"test":"123"}
        expected_results = [LOGIN_WRONG_PASSWORD, LOGIN_NO_USERNAME, LOGIN_TRUE]
        results = []
        tests = [
            ["test", "1234"],
            ["test2", "123"],
            ["test", "123"]
        ]

        for test in tests:
            results.append(req_handle.login(
                test[0], test[1]))

        self.assertListEqual(results, expected_results)

    def test_server_list(self):
        """
        This test will check list command.
        Test1 : Listing without login.
        Test2 : Listing folder for user test
        """
        results = []
        expected_results = [LOGIN_REQUIRED, "\ntestfolder1"]
        req_handle = RequestHandler()
        req_handle.user_passwords = {"test":"123"}
        results.append(req_handle.list())
        req_handle.login("test", "123")
        results.append(req_handle.list())

        self.assertListEqual(results, expected_results)

        
 class ReqClassTestingStepThree(unittest.TestCase):
    """Handles the tests to check response for change folder and create folder"""

    def test_server_change_folder(self):
        """
        This test will check response for change folder.
        Test1 : Change folder without login.
        Test2 : Wrong directory change.
        Test3 : Proper directory change.
        """
        results = []
        expected_results = [LOGIN_REQUIRED, INCORRECT_DIRECTORY, ch_dir_success("testfolder1")]
        req_handle = RequestHandler()
        req_handle.user_passwords = {"test":"123"}
        results.append(req_handle.change_folder("testfolder1"))
        req_handle.login("test", "123")
        results.append(req_handle.change_folder("testfolder2"))
        results.append(req_handle.change_folder("testfolder1"))

        self.assertListEqual(results, expected_results)

    def test_server_create_folder(self):
        """
        This test will check response for create folder.
        Test1 : Create already present directory.
        Test2 : Proper directory with random name.
        """
        results = []
        expected_results = [DIRECTORY_PRESENT, DIRECTORY_SUCCESS]
        req_handle = RequestHandler()
        req_handle.user_passwords = {"test":"123"}
        req_handle.login("test", "123")
        results.append(req_handle.create_folder("testfolder1"))
        req_handle.change_folder("testfolder1")
        results.append(req_handle.create_folder("test" + random_folder())

        self.assertListEqual(results, expected_results)


class ReqClassTestingStepFour(unittest.TestCase):
    """Handles the final part of the tests inculting tests for read and write the files"""

    def test_server_read_file(self):
        """
        This test will check read file.
        Test1 : Read the non existing file.
        Test2 : Proper read file.
        """
        results = []
        expected_results = [READ_WRONG_PATH, read_file("0","DontChangeThisContent")]
        req_handle = RequestHandler()
        req_handle.user_passwords = {"test":"123"}
        req_handle.login("test", "123")
        req_handle.change_folder("testfolder1")
        results.append(req_handle.read_file("test_read2.txt"))
        results.append(req_handle.read_file("test_read.txt"))

        self.assertListEqual(results, expected_results)

    def test_server_write_file(self):
        """
        This test will check write file.
        Test1 : Write on non existing file.
        Test2 : Proper write file.
        """
        results = []
        expected_results = [WRITE_NEW_PATH, WRITE_EXISTING]
        req_handle = RequestHandler()
        req_handle.user_passwords = {"test":"123"}
        req_handle.login("test", "123")
        req_handle.change_folder("testfolder1")
        results.append(req_handle.write_file(random_folder() + ".txt", "content"))
        results.append(req_handle.write_file("test_write.txt", "content"))

        self.assertListEqual(results, expected_results)
