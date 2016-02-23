# When Wizard
It turns out that [**When**](https://github.com/almostearthling/when-command) could be more productive for some users if there was a more streamlined interface to manage conditions and reactions, while other reports consider the interface already usable. I think that **When** should be able to behave in both ways:
- offer the usual interface, with direct access to _tasks_, _conditions_ and _signal handlers_
- provide a simpler, intuitive and wizard-based interface to hide the parts that require knowledge of the shell, scripting and maybe even some programming.

![anim](https://raw.githubusercontent.com/almostearthling/hello-world/master/images/when-wizard.gif)

Instead of boiling everything together, which would make **When** too heavy to both use and develop, I thought that a different approach could be taken that allows both aspects to coexist. On the applet side these features have been implemented:

1. the ability to manage _tasks_, _conditions_ and _signal handlers_ without directly accessing the configuration dialog boxes, that is using specific command line arguments and specially crafted text files and/or a generic DBus based [Remote API](http://contributing-to-when.readthedocs.org/en/latest/dbusapi.html) to interact with a running instance of **When**
2. the possibility to completely hide the _tasks_, _conditions_, _signal handlers_ and _task history_ dialog boxes from both menu and command line access

which were also discussed in **When** [Issue 65](https://github.com/almostearthling/when-command/issues/65). These features can be useful to create libraries of _items_ to be shared among systems, but their main goal was what the **When Wizard** tries to implement: control **When** with a separate application.

The main achievements that the **When Wizard** strives for are:
- an intuitive interface, with _step-by-step_ (wizard-like) procedures to define reactions to conditions
- the ability to manage _items_ in **When** directly, without user interaction with the actual applet
- a built-in library of _conditions_ and _tasks_ for many common use cases
- the possibility to extend the **When Wizard** functionality via _plugins_, which should be easy to install through the GUI
- direct management of **When**'s settings, especially for tuning and _Minimalistic Mode_
- a simple but complete documentation for end users and plugin developers.

The only requirement for the **When Wizard** at the moment is that it should not borrow code from **When** to perform _"magic"_ operations or interact with **When**'s internals: **When**'s command line, configuration file and remote API interface should be powerful enough to entirely control the applet.


## What is available for now
At present, since the beginning of this document, some of the goals have already been reached:
- a wizard-style application that can register tasks and conditions into a running instance of **When**, with plugins for several types of item
- a separate management application which allows to remove actions created through the wizard, to view the history of currently defined actions, to install and remove third party plugin packages and item definition files, and to manage a selection of settings in the **When** applet
- an incomplete but fairly working stock plugin library: although they have to be revised and refined, these plugins can serve as a base for future plugin development.

The plugin system for the **When Wizard** has been designed in such a way that it takes into account plugins that come with the application itself (and could possibly be installed in system directories) and plugins that can be added on a per-user basis (that will be installed in a subdirectory of `$HOME`): the application tries to dynamically load every file in a plugin directory (user or system) as a plugin, and their names have not to be known in advance. Also, it is possible to choose a directory where a plugin is developed and load it from there (more on this [here](http://contributing-to-when.readthedocs.org/en/latest/wizard.html#plugin-rationale), in the note): this allows experimental plugins to be tested without spoiling the entire installation and possibly even "third party" plugins. The application interacts with a running instance of **When** and is already able to register tasks and conditions.

Since plugins _must_ be coded deriving them from a base plugin class and defining some of its attributes, there are templates for the various plugin types, both for tasks and all types of conditions, that constitute a boilerplate for plugin development. Since plugins may (or may not) provide a configuration pane in the wizard, if applicable, a basic configuration pane template for the _Glade_ designer is also provided.

The **When Wizard** has to be considered sort of an application suite, as it consists at least of the following components:
- the wizard itself
- the management utility to manage general setup and possibly wizard-generated items
- a stub to run tasks, which are defined in a more convoluted way than in **When**
- a stub to run an application disowning it immediately, to work in an inherently multitasking environment
- command line utilities to install plugins and create plugin packages.

The management utility is a crucial part, as it is necessary to delete tasks and conditions, to configure **When**, to add or remove plugins and item definition files, and and to actually view the history of wizard-managed actions.

The following screencast briefly shows the management application:

![anim](https://raw.githubusercontent.com/almostearthling/hello-world/master/images/when-wizard-manager.gif)


## Documentation
As said above, the documentation is included in the main **When** documentation as a chapter and can be viewed [here](http://when-documentation.readthedocs.org/en/latest/wizard.html). Analogously as what happens for the **When** applet, the documentation for contributors is available separately as a subset of the main developer documentation [here](http://contributing-to-when.readthedocs.org/en/latest/wizard.html).


## Installation
There is no automatic or package-based installation procedure at present: the package has to be downloaded from the GitHub page or cloned directly. To run the wizard, `cd` to the folder where the **When Wizard** has been unpacked or cloned, and type

```
$ ./when-wizard start-wizard
```

at the `$` prompt. This will start the wizard GUI. To start the management application, change `start-wizard` to `start-manager`: this also gives the option to install icons, that should however be removed manually. Consider that it's in early alpha stage: it mostly works but it can produce some errors. Also consider that the **When Wizard** is used also to debug and improve **When**'s remote API: if something does not work it should be tested with the latest updates in the `devel` (_development_) branch of **When** before filing an issue.


## What still has to be done
The wizard interface is almost complete but it surely requires some refinements. Also, it completely lacks static configuration: although at the moment the application does not seem to need any form of configuration, as it relies on **When** and on its own datastore for static data, it might take advantage of some kind of settings in the future. The manager application is also quite complete and functional. Parts of its UI can be improved too, although in my opinion both GUI utilities now have reached an almost stable state.

The provided _stock plugins_ **do not always do what they promise**: sometimes they do or at least try to, but in many cases they just don't work, especially for tasks. Mostly because I have to find out what is the command for a specific action, as I focused more on how to get the whole application working instead of caring for plugin details.

The command line utilities (which are all subcommands of `when-wizard`) completely lack any output, and only rely on exit status code to inform the caller of errors and issues.

The language used throughout the UI has been taken care of, but still needs to be revised.

Localization is another argument that has to be faced: the plugin-based structure makes it hard to deal with localizations of third party components. While stock plugins will be handled just as if they were normal components, third-party plugins might have to be left out or find another way to be translated.

Everything has to be thoroughly tested: all functionality has been fairly checked, but exceptional situations (such as unexpected file formats, incorrectly written plugins and other unexpected events) might still break the applet. There is still **When** that can be used to correct possible errors: every operation performed by the **When Wizard** applications can be undone in **When**, and **When** appears to be quite robust at the moment. When testing this application suite, it's strongly advised to export **When** items before, using the `--export` switch.

## What more can be done
There are several elements that can be improved, besides what is strictly needed:
- _stock_ plugins should be improved and made more stable
- more stock plugins should be added (at least the ones promised in the documentation)
- the `PicklingDatastore` is definitely too rough to be considered definitive: probably something more robust, maybe based on _SQLite_, can be used; in the end the `Datastore` protocol just requires to store big strings (usually JSON data) indexed by short strings which seems a fairly simple task for a SQL DB
- **When** remote API has to be debugged, revised and made more consistent if necessary, and **When Wizard**'s client counterpart should change accordingly
- the application has to be packaged for Linux systems.

More fields of improvement can, and possibly will, be noted here.

# Credits
The icons I use in the application are from [icons8](https://icons8.com/) (the [flat color icons](https://github.com/icons8/flat-color-icons) set), and the screencast was made using [silentcast](https://github.com/colinkeenan/silentcast). The icon used for applications is made out of parts by Rafi at [GraphicsFuel](http://www.graphicsfuel.com/). No credits for the wizard dialog side photo, I took it myself.
