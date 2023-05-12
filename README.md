# Implementing Helion on Home Assistant (HelionHA)

### Table of Contents
- [Helion Setup](#helion)
- [Home Assistant Setup](#home-assistant)
- [Instructions on Modifying Home Assistant Dashboard](#modifying-home-assistant-dashboard)
- [Project Components](#components)

## Helion

All the instruction for setting up Helion are inside the `helion` Directory.

## Home Assistant

The documentation of architecture can be found [here](https://developers.home-assistant.io/docs/architecture/core).

### Using [Pycharm IDE](https://www.jetbrains.com/pycharm/):

I had the best experience using Pycharm to setup Home Assistant Core.

1. Install Pycharm.

2. Clone this repository through git. (Using a token for authentication seems to be the best method of cloning)

3. Load the ha-core project in Pycharm. It creates virtual environment with required dependencies.

4. Run ha-core/homeassistant/\_\_main\_\_.py   (NOTE: for Windows users, run `__main__.py` in the PycharmProjects terminal. Please ensure the terminal is a predefined Ubuntu terminal)

5. Through a browser of your choice, go to http://localhost:8123

6. Setup login credentials. All the setup information are stored inside ~/.homeassistant/ directory

### Manually Installing Home Assistant

Without the virtual environment detailed above, the dependencies need to be manually installed. The instructions for installation on each platform can be found [here](https://www.home-assistant.io/installation/). Note: after choosing your platform, scroll to the Install Home Assistant Core section of the page.

As mentioned in the architecture documentation, Home Assistant can only run natively on Linux and Mac OS systems.
To run Home Assistant on Windows, you will need to use the Windows Subsystems for Linx (WSL).
The instructions can be found [here](https://docs.microsoft.com/en-us/windows/wsl/install).

Alternatively, you can set up a Linux Virtual Machine.
The instructions for that can be found [here](https://www.home-assistant.io/installation/windows)

If the instructions provided in the link do not work, the following instructions may work (tested on Windows WSL):

1. In the ha-core directory, run `pip install -r requirements.txt -r requirements_all.txt`. This will take several minutes. **Make sure the `pip` version is between 8.0.3 and 20.3**

2. The `homeassistant-pyozw` dependency may fail to install. To install it, first install `libudev-dev` to your system. Next, you should be able to run `pip install homeassistant-pyozw` to complete the installation. [More information here](https://github.com/home-assistant/core/issues/18659).

3. Run `python3 homeassistant/__main__.py` while in the `hacore/homeassistant` directory. It cannot be run from other directories.

4. Setup login credentials as above.


### Setting up Appdaemon

Appdaemon is an execution environment that we use to automate and connect the Home Assistant and helion processes. In order to properly run our application please install Appdaemon by using the following command in your terminal:

```
sudo pip3 install appdaemon
```

**Note: Do not run this command in the same virtual environment that you run Home Assistant!**

Appdaemon will access your Home Assistant account and server through a long-term access token. To find this token:

1. Run Home Assistant, making sure to login with your credentials if necessary

2. On the left side-bar, click on the very bottom tab (the circular image) that represents the user's account

3. Scroll to the bottom of the page to `Long-Lived Access Tokens`

4. Hit create token (you may name this token whatever you would like)

5. Copy the generated access token (Keep this token somewhere safe as you will not be able to see it again on Home Assistant)

Once you have created an access token, you will need to change contents of the file `appdaemon.yaml` located in the `~/.homeassistant/appdaemon/` folder you located in the previous `Modifying Home Assistant Dashboard` section.

Open `appdaemon.yaml` in a text editor of your choice.

You will notice a token on line 11. This token must be replaced with the one you just created.

Upon running, Appdaemon is now able to access your Home Assistant by being authenticated by the access token.
Now that Appdaemon can connect to Home Assistant, we can focus on the script that connects helion automations to Home Assistant.

The `helion.py` application located in appdaemon/apps/ requires the location of the helion scripts to run. Please locate your helion/scripts folder.
If you are using PycharmProjects, the path may look like the following:

- WSL: `mnt/c/Users/<user>/PycharmProjects/CSci435-Fall21-Helion/helion/scripts`
- MacOS: `/Users/<user>/PycharmProjects/CSci435-Fall21-Helion/helion/scripts`

Now open `apps.yaml` located in `~/.homeassistant/appdaemon/apps/`. Put the location path of the helion/scripts folder in line 5 for "param1"

Appdaemon will update itself every time you save a related file so you do not have to terminate Home Assistant and rerun it.
If you did stop Home Assistant, rerun the application.

Appdaemon should connect to Home Assistant without any problems, allowing you to utilize the buttons and services located on the UI dashboard.


### Resetting Home Assistant Configurations/Login Credentials

Your configuration files and login information for Home Assistant is stored in the ~/.homeassistant/ directory. If you are having issues using Home Assistant or if you need to reset your login credentials, run the command `rm -rf ~/.homeassistant` to remove the directory. Alternatively, you can locate the directory and manually delete it. Once you remove the directory, run the command to start Home Assistant, and access the home page, you should be prompted to create new credentials.

**Doing this will also delete all Home Assistant data, and the Helion configuration.yaml, ui-lovelace.yaml, and helion.yaml will need to be readded**

## Modifying Home Assistant Dashboard

Make sure you have setup your login credentials in Home Assistant before proceeding to this step!

After Home Assistant has been set up, you need to copy the contents of the `hass_configuration` directory to the `/.homeassistant` directory.
To do that, navigate to the `hass_configuration` directory and run the following command below:
```
cp -r . ~/.homeassistant
```

Alternatively, you can drag and drop all of the files and folders manually to the `/.homeassistant` directory in your file explorer.

Working with Home Assistant requires modifications to the `~/.homeassistant` directory.
Note that the directory is hidden, so in your base directory to view it you would need to run `ls -a`.

### Home Assistant Term Definitions

Some important terms in Home Assistant and their definitions:

- Entity: Home Assistant's representation of the function of a device

- Token: Helion's representation of an device, its attribute, and its state.
Format: <device,attribute,state>

    - Atomic Token: Tokens that represent a singular device, its attribute,  and its state.

- Lovelace: A customizable Home Assistant dashboard

- Cards: Home Assistant's representation of entities on the UI.
The code for these cards is stored in helion.yaml

As it is currently configured, there are two things that new developers should be aware of: entities and cards.

Entities can be thought of as objects that hold the state of the simulated device.
To elaborate, Home Assistant allows users to connect to physical devices, and usually entities only serve as the interface to those devices.
However, because Helion primarily uses simulated devices, we utilized templated entities, which only hold simple states, to simulate actually having those physical devices.

Cards are what is actually displayed on the Home Assistant dashboard, and represent an entity.
Through them, you can see and change the state of the entity.
Be careful, as cards can be improperly configured such that multiple cards correspond to the same entity, in which case changing the state of one card will modify all of the cards that correspond to that entity.

The entities can be found in `~/.homeassistant/configuration.yaml`.
We primarily used two types of entities:
- `input_boolean`: This corresponds to when we only need to keep track of two states, an example of this would be on or off.
- `input_select`: This corresponds to when there can be multiple or complex states, such as the `motion_sensor_motion` having four states: `activated`, `deactivated`, `detected`, and `not_detected`.

The cards can be found in `~/.homeassistant/helion.yaml`, with each of the cards are set up to correspond to an entity.
Note that by default, we have set up the dashboard to only have cards that correspond to running Helion.
You can then input a token through an input card which will run a script to modify `helion.yaml`, which is detailed more in the `helion` directory.

## Components

__folders__ of interest are bolded, and _files_ of interest are italicized.

In the base Helion directory there are three directories of interest.

### ha-core

This is the installation of the core Home Assistant package pulled from the Home Assistant Github page.
The only change of interest is in the `ha-core/homeassistant/__main__.py`, where we have inserted a call to `appdaemon`.
If developers run into issues they can move the call to `appdaemon` or move it to a different location.
The original team wanted a location that would ensure it would be ran on startup, but there are alternative locations that the call to `appdaemon` can be placed.

It should be noted that there is a directory that houses the integrations and components in `ha-core/homeassistant/components`.
This is where the code for such integrations as the `input_boolean` and `input_select` are stored.
There are also third-party integrations which connect to IoT devices, so if future teams wish to connect those devices and run into issues, they should look to make sure that the IoT device is supported by ha-core.

### hass_configuration

This folder contains all of the code that must be placed in the `.homeassistant` directory in the user's folder.
As mentioned above, the folder can be copied with one command by navigating to the `hass_configuration` directory and running the command `cp -r . ~/.homeassistant`.

__appdaemon__: Contains all of the code for `appdaemon`, which, as mentioned above, allows Home Assistant to run the scripts the team has developed.

__custom_components__: Custom components are integrations that normally belong in the `ha-core/homeassistant/components` directory, but have not been approved by Home Assistant itself, and have thus not been added to the directory.

The only current major custom component is `browser_mod`, which allows us to modify the Home Assistant browser window.
Among other things, it allows us to refresh the page, which is required to display new cards once they have been added to the `helion.yaml` dashboard page.

__www__: This houses the custom card that we have created to easily choose different Helion configuration options.

_change\_ui\_cards.py_: This is the script that is used to create the cards that are displayed on the Home Assistant dashboard.
When tokens are output from the `helion_predictions.py` script, we take the tokens that are output and pass them to this script, which finds the corresponding card and modifies `helion.yaml`.
Once that is completed, the Home Assistant browser is refreshed, and the card is displayed.

_configuration.yaml_: This holds all of the templated entities and their respective states.

_ui-lovelace.yaml_: This is the display on the main dashboard.

_helion.yaml_: This holds cards on a separate dashboard to display the `helion_predictions.py` output.

### helion

This holds all of the files that correspond to actually running Helion token generation and retrieving the data.

__results__: Once `helion_predictions.py` is ran, it will be output here.

__scripts__: This folder holds the various scripts and their output files.

_helion\_predictions.py_: What is actually run to generate the tokens.

_parse\_token.py_: As the token does not correspond to the entity name, this script takes in a token and gives back the corresponding entity.
This entity is then added to the `ui-lovelace.yaml` or `helion.yaml` file.

parsed_token.txt: Holds the output of the `parse_token.py` script.

_write\_to\_text\_file.py_: This script is ran by Home Assistant.
When the user inputs the token with proper formatting on the dashbaord, it sends the token to this script, which outputs it to the `/data/generated_data/validation/scenarios_from_evaluators/ha-scenarios.txt` text file, which is the input file for `helion_predictions.py`.

In the base directory, we have also included the `ui-compiled_cards.yaml` file.
This file contains all of the cards that correspond to all of the entities.
This should give future development teams an idea of how any one card will correspond to an entity.
**Doing this will also delete all Home Assistant data, and the Helion configuration.yaml and ui-lovelace will need to be readded**

### Setting Up Your Own Device to Home Assistant and Helion 

The goal of Helion is to ultimately be integrated with real devices. This is the process to set up a real device to your Helion and Home Assistant. 

1. The first step is to hook your device to your wifi. There might be different ways to do this, dependent on your device. This is an example of how to do this using the [iHome Smart Plug](https://ethitter.com/2020/01/connect-ihome-smartplug-home-assistant-homekit/).

2. Once your device is hooked up to your wifi, you will want to add the respective integration to your Home Assistant. ([This](https://www.home-assistant.io/integrations/homekit/) is the Home Assistant integration documentation that is specifc to the iHome Smart Plug.)

    To add an integration, first run Home Assistant. Then go into your Home Assistant sidebar, and navigate to: 

    **Configuration > Integrations > Add Integration.** 

    From here, you can search your specific integration that you're trying to add, and add your integration. 

3. Now that the integration is added, and that your device is hooked up to your wifi, the device should be discoverable by Home Assistant. You should recieve a notification from your new Home Assistant Integration that a new device was discovered. 

    To be sure of this, you can also navigate to: **Configuration > Entities** from the sidebar, and you should see your new device in the list. 

4. Next, to be able to see this device visible on your dashboard as a card, you will have to alter the entity ID.

    First, comment out the entity in your coniguration.yaml file that you would like to use for your token. For the iHome Smart Plug example, Light Bulb was chosen.  Replace the entity ID with the entity in the configuration.yaml file you commented out.  In this case the entity ID was replaced with switch.light_bulb. 

<img width="635" alt="Screen Shot 2021-12-21 at 12 22 31 AM" src="https://user-images.githubusercontent.com/71198847/146875809-018b5a19-e02e-463d-b788-fc72689a85fe.png">

5. Once that is replaced, you can go back to the configuration.yaml file and uncomment out the entity you used. If you do not do this, then when you try to change the entity ID you will get an error stating that ID already exists for some entity.

6. After this, restart Home Assistant, and you should be able to see a new switch on the dashboard that represents your real device. 
