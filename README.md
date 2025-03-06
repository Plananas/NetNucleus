A simple program for managing a group of computers on a network

- Program must be run in administrator mode to work

Python Version 3.10

List of Programs to install for testing:
-all of these programs are in need of an update

choco install notepadplusplus --version=8.4.2 -y
choco install 7zip --version=22.00 -y
choco install vlc --version=3.0.16 -y
choco install winscp --version=5.21.6 -y


some handy tools:
services.msc
event viewer


These commands get the service running as a python script:
python .\NetworkAutomationService.py install
python .\NetworkAutomationService.py start
python .\NetworkAutomationService.py stop
python .\NetworkAutomationService.py remove


