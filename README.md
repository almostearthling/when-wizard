# The When Wizard

![alarmclock_wand-256](https://cloud.githubusercontent.com/assets/11710868/14398667/3d93af04-fde6-11e5-9614-37c8f22cc526.png)


## Applications

The **When Wizard** is a suite of utilities that can be used to perform unattended actions under certain conditions within a Gnome graphical session in Ubuntu or a derivative. It provides a wizard-style interface to choose actions and circumstances, and uses the **When** Gnome [Scheduler](http://almostearthling.github.io/when-command/) to actually manage the jobs. Actions can be defined and managed using simple GUI applications.

More extended documentation for the **When Wizard** can be found [here](http://when-documentation.readthedocs.io/en/latest/wizard.html).


## Installation

The **When Wizard** still lacks the possibility to be installed using a package manager. However installation is quite simple:

```
$ sudo add-apt-repository ppa:franzg/when-command
$ sudo apt-get install when-command mailutils consolekit wget \
                       rsync libnotify-bin
$ mkdir Apps
$ cd Apps
~/Apps$ git clone https://github.com/almostearthling/when-wizard.git
~/Apps$ cd when-wizard
~/Apps/when-wizard$ chmod a+x when-wizard
~/Apps/when-wizard$ rm -Rf .git*
```

Start **When** from the *Dash*, and ensure that in the settings box the *Autostart* option is selected. That's it. the `rm -Rf .git*` step is optional, but saves some space. Also, you can clone the repository wherever you want, not necessarily in `~/Apps`.


## Usage

Refer to the [documentation](http://when-documentation.readthedocs.io/en/latest/wizard.html) for a more detailed description.

### The Wizard

The wizard lets you define actions as combinations of a task and a circumstance.

![when-wizard](https://cloud.githubusercontent.com/assets/11710868/14398454/a7429e4e-fde4-11e5-80bc-e11ac657299c.gif)

To start the **When Wizard**, just `cd` to the directory where the repository was cloned and start the application as follows:

```
$ cd Apps/when-wizard
~/Apps/when-wizard$ ./when-wizard start-wizard
```

and the wizard application appears. Choose the task first and then the condition: the **When Wizard** takes care to register it correctly.

### The Manager

Through the manager, actions can be enabled, disabled and deleted. Moreover, the **When Wizard Manager** allows to extend the capabilities of the wizard using plugins.

![when-wizard-manager](https://cloud.githubusercontent.com/assets/11710868/14398453/a7403ec4-fde4-11e5-83ed-325a4e3d14ba.gif)

To start the **When Wizard Manager**, just `cd` to the directory where the repository was cloned and start the application as follows:

```
$ cd Apps/when-wizard
~/Apps/when-wizard$ ./when-wizard start-manager
```

and the management application appears. Many operations can be performed from here: action management, history view, plugin and add-on management, **When** scheduler tuning. You can use the *Create or Restore Desktop Icons for Wizard Applications* entry in the *Utility* pane to be able to invoke both the **When Wizard** and the **When Wizard Manager** from the *Dash*.


## Credits

The [icons](https://icons8.com/) I use in the application are by @icons8 (the [flat color icons](https://github.com/icons8/flat-color-icons) set), and the screencast was made using [silentcast](https://github.com/colinkeenan/silentcast) by @colinkeenan. The icon used for applications is made out of parts by Rafi at [GraphicsFuel](http://www.graphicsfuel.com/). No credits for the wizard dialog side photo, I took it myself.
