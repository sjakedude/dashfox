# dashFox

run with launch.bat

The purpose of this repo is to provide HTTP endpoints for performing actions on the server.

Hitting an endpoint calls a windows batch script, which runs many commands and calls other batch scripts. These scripts are located in the ConeCommons project. But the user does not have to worry about understanding ConeCommons, they just have to learn what the dashfox endpoints are.

## Endpoints

- theconeportal.net:5000
    - Basic connection

- theconeportal.net:5000/plutonium/status
    - Returns what game mode is currently loaded in plutonium

- theconeportal.net:5000/plutonium/gungame
    - Selects the gungame gamemode for plutonium and restarts the server

- theconeportal.net:5000/plutonium/domination
    - Selects the domination gamemode for plutonium and restarts the server

- theconeportal.net:5000/git/deploy/theconeportal
    - Fetches the latest commit from the master branch of TheConeNetworkPortal repo and deploys it

- theconeportal.net:5000/git/deploy/conecommons
    - Fetches the latest commit from the master branch of ConeCommons repo and deploys it

- theconeportal.net:5000/git/deploy/dashfox
    - Fetches the latest commit from the master branch of Dashfox repo and deploys it

