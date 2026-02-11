import os.path
import os
import platform
import time

# Class returns file modification / creation times
class FileInfo:
    def __init__(self, file_path):
        self.file_path = file_path
        self.exists = os.path.exists(file_path)

    def does_file_exist(self):
        return self.exists
    def get_file_path(self):
        return self.file_path
    # Returns modification time in seconds (float)
    def get_modified_time(self):
        if not self.exists:
            raise FileNotFoundError("File not found")
        return os.path.getmtime(self.file_path)
    # Function works well on windows, on Mac and Linux probably not
    # See https://stackoverflow.com/questions/237079/how-do-i-get-file-creation-and-modification-date-times
    def get_create_time(self):
        if not self.exists:
            raise FileNotFoundError("File not found")
        return os.path.getctime(self.file_path)

    # Function works everywhere (Windows / Linux / Mac) but only on Windows returns real creation time.
    # On Mac and Linux returns last modified time, so if file was only created and never modified, it's also it's creation time
    # In fact, most of Unix systems doesn't store file creation time anywhere; on some Unix Systems (like BSD)
    # creation time is stored inside st_birthtime
    # In summary, only solution on non-Windows systems is to use mtime
    # Returns creation / modification time in seconds (float)
    def get_create_time_extended(self):
        if not self.exists:
            raise FileNotFoundError("File not found")
        path_to_file = self.file_path
        if platform.system() == 'Windows':
            return os.path.getctime(path_to_file)
        else:
            return os.path.getmtime(path_to_file)

    def how_long_exists(self):
        if not self.exists:
            raise FileNotFoundError("File not found")
        ctime = self.get_create_time_extended()
        return time.time() - ctime

    def how_many_minutes_exists(self):
        return self.how_long_exists()/60

    def how_many_hours_exists(self):
        return self.how_long_exists()/60/60

# Class manages file deprecation: verification of file deprecation, removing deprecated files
class FileDeprecation:
    def __init__(self, deprecation_seconds = 60 * 15):
        self.deprecation_seconds = deprecation_seconds

    def is_deprecated(self, file_path):
        file_info = FileInfo(file_path)
        print(file_info.get_file_path())
        return file_info.how_long_exists() > self.deprecation_seconds

    # Remove file if deprecated
    # Returns True if removed, otherwise false
    def remove_file_if_deprecated(self, file_path):
        if self.is_deprecated(file_path):
            os.remove(file_path)
            return True
        return False

    def clean_directory_from_deprecated_files(self, directory):
        if not os.path.isdir(directory):
            raise FileNotFoundError("Directory not found")
        for file in os.listdir(directory):
            full_path = os.path.join(directory, os.fsdecode(file))
            self.remove_file_if_deprecated(full_path)