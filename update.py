import git
from subprocess import Popen
import os

# Close the current instance of the app
print("Closing the current instance of the app")
p = Popen(["powershell.exe", r'bat_files/stop_background_process.ps1']).wait()


# Pull the latest changes from the remote repository
print("Pulling the latest app from remote repo...")
repo = git.Repo('')
repo.remotes.origin.pull()

# Generate the new version of the app
print("Generating the new version of the app")
os.system("cd bat_files && generate_exe.bat")

# Start the updated app
print("Starting the updated app")
os.system("cd bat_files && run.bat")

print("Update complete")
exit(0)