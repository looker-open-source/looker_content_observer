# Looker Content Observer (LCO)

# Quickstart

## [Pre-Step] looker.ini File
The Looker Content Observer leverages Looker's API to programatically check the data from dashboards. In order to accompolish this, the API credentialy will need to be set up in advance in a 'looker.ini' file.

The project includes a sample looker.ini file here: 
 - [Example of looker.ini file](looker_example.ini)
 - **Note**: The looker.ini file contains multiple sections, each section is assosciated with the API credentials of an individual instance.


### Resources to Set up looker.ini File
- [See Configuring the SDK](https://developers.looker.com/api/getting-started)
- [What are INI Files](https://www.advancedinstaller.com/what-is-ini-file.html)
- [Setup User's API Credentials](https://cloud.google.com/looker/docs/api-auth)


## Install / Setup

### [1] Create a virtual 'test' environment
```
$ virtualenv lco   
$ source lco/bin/activate         
```

### [2] Install the 'mydvp' package
```
$ pip3 install --editable .  
```

### [3] Confirm Initial Packages
![install_pic](screenshots/fresh_install_pip_list.png)


# Demo 

## CLI Skeleton / how to run:
- Example comamnds: 
  - `lco init` : Commands here will be used to set up instances and environment
    - For the first time running the script, users should `init` as the first step
  - `lco run`: Commands here will be involved with running the dashboard/Look checkers
    - Run leverages the file created from the init phase 



# CLI Flows

## [1] init 
Used to set up the instance + environment (dev or prod). There are two ways of setting up the cli, either through a guided, user-input `[A] Setup` 

### [A] Setup
Run setup via user inputs within the command line. Unless you are frequently switching the branch / project, user's will only have to run the `init setup` commands infrequently. Setup values are stored to a yaml file which will be used during the `run` comamnds

#### `Setup` Flow
- See Recording: **[lco init](https://screencast.googleplex.com/cast/NjQ3NDc0MTcxMjk0NTE1MnwwNzE1ZDllZC00Ng)**

### [B] CLI
Skips the guided setup and allows users to enter in the instance + environment information as command line args. For users running automated bash type scripts, this will likely be the preferred method if they are switching between branches, projects, and instances frequently.

####  `CLI` Flow
- See Recording: TBD