# When Wizard
It turns out that [**When**](https://github.com/almostearthling/when-command) could be more productive for some users if there was a more streamlined interface to manage conditions and reactions, while other reports consider the interface already usable. I think that **When** should be able to behave in both ways:
- offer the usual interface, with direct access to _tasks_, _conditions_ and _signal handlers_
- provide a simpler, intuitive and wizard-based interface to hide the parts that require knowledge of the shell, scripting and maybe even some programming.

Instead of boiling everything together, which would make **When** too heavy to both use and develop, I thought that a different approach could be taken that allows both aspects to coexist. On the applet side these features have been implemented:

1. the ability to manage _tasks_, _conditions_ and _signal handlers_ without directly accessing the configuration dialog boxes, that is using specific command line arguments and specially crafted text files and/or a generic [Remote API](http://contributing-to-when.readthedocs.org/en/latest/dbusapi.html) to interact with a running instance of **When**
2. the possibility to completely hide the _tasks_, _conditions_, _signal handlers_ and _task history_ dialog boxes from both menu and command line access

which were also discussed in **When** [Issue 65](https://github.com/almostearthling/when-command/issues/65). These features can be useful to create libraries of _items_ to be shared among systems, but their main goal was what the **When Wizard** tries to implement: control **When** with a separate application.

![anim](https://cloud.githubusercontent.com/assets/11710868/12705464/adb9a38c-c872-11e5-9f64-474b27a034a5.gif)

The main achievements that the **When Wizard** strives for are:
- an intuitive interface, with _step-by-step_ (wizard-like) procedures to define reactions to conditions
- the ability to manage _items_ in **When** directly, without user interaction with the actual applet
- a built-in library of _conditions_ and _tasks_ for many common use cases
- the possibility to extend the **When Wizard** functionality via _plugins_, which should be easy to install through the GUI
- direct management of **When**'s settings, especially for tuning and _Minimalistic Mode_
- a simple but complete documentation for end users and plugin developers.

The only requirement for the **When Wizard** for now is that it should not borrow code from **When** to perform _"magic"_ operations or interact with **When**'s internals: **When**'s command line, configuration file and remote API interface should be powerful enough to entirely control the applet.


## Installation
There is no automatic installation procedure at present: the package has to be downloaded from the GitHub page or cloned directly. To run the wizard, `cd` to the folder where the **When Wizard** has been unpacked or cloned, and type

```
$ ./when-wizard start-wizard
```

at the `$` prompt. This will start the wizard GUI. Consider that it's in early alpha stage: it mostly works but it can produce some errors. Also consider that the **When Wizard** is used to debug **When**'s remote API: if something does not work it should be tested with the latest updates in the ``devel`` (_development_) branch before filing an issue.

## What is available for now
At present, since the beginning of this document, some of the goals have already been reached:
- a wizard-style application that can register tasks and conditions into a running instance of **When**, with plugins for several types of item
- an incomplete but working "stock" plugin library: although they have to be revised and refined, these plugins can serve as a base for future plugin development.

The plugin system for the **When Wizard** has been designed in such a way that it takes into account plugins that come with the application itself (and could possibly be installed in system directories) and plugins that can be added on a per-user basis (that will be installed in a subdirectory of `$HOME`): the application tries to dynamically load every file in a plugin directory (user or system) as a plugin, and their names have not to be known in advance. This allows experimental plugins to be tested without spoiling the entire installation and possibly even "third party" plugins. The application interacts with a running instance of **When** and is already able to register tasks and conditions.

Since plugins _must_ be coded deriving them from a base plugin class and defining some of its attributes, there are templates for the various plugin types, both for tasks and all types of conditions, that constitute a boilerplate for plugin development. Since plugins may (or may not) provide a configuration pane in the wizard, if applicable, a basic configuration pane template for the _Glade_ designer is also provided.

The **When Wizard** has to be considered sort of an application suite, as it consists at least of the following components:
- the wizard itself
- a management utility to manage general setup and possibly wizard-generated items (still to be developed)
- a stub to run tasks (which are defined in a more convoluted way than in **When**)
- a stub to run an application disowning it immediately, to work in an inherently multitasking environment.

The management utility will be a crucial part, as it will be needed to delete tasks and conditions, to configure **When**, to add or remove plugins and to actually view the task history.

## What still has to be done
The wizard interface is almost complete but might require some refinements. Also, it completely lacks any form of configuration: although at the moment the application does not seem to need any form of configuration, it might do in the future.

The language used throughout the UI is, at best, inaccurate. Sometimes it just sucks. Styles are mixed, wording is far from being consistent, and I still need to decide how the user has to be addressed -- I'd like to stay on the colloquial side, but the over-proactive language of some recent _apps_ sounds irritating to me to the very least.

As pointed out above, the other mandatory component of the suite is the management application, that has to be created from scratch. The plugin installation, uninstallation and management interface will be an interesting part of the application: it will need to handle plugin code, UI (graphics and configuration pane resource file), scripts and possibly user-defined signal handlers that have to be registered. The packaging format for plugins still has to be defined.

The documentation for the **When Wizard** has still to be written: the user part should be a chapter in the **When** documentation, while in the developer documentation there have to be one or more chapters dedicated to plugin development.

Localization is another argument that has to be faced: the plugin-based structure makes it hard to deal with localizations of third party components. While stock plugins will be handled just as if they were normal components, third-party plugins might have to be left out or find another way to be translated.

## What more can be done
There are several elements that can be improved, besides what is strictly needed:
- _stock_ plugins should be improved and made more stable
- more stock plugins should be added
- the `PicklingDatastore` is definitely too rough to be considered definitive: probably something more robust, maybe based on *SQLite*, can be used; in the end the `Datastore` protocol just requires to store big strings (usually JSON data) indexed by short strings which seems a fairly simple task for a SQL DB
- **When** remote API has to be debugged, revised and made more consistent if necessary, and **When Wizard**'s client counterpart should change accordingly
- the application has to be packaged for Linux systems.

More fields of improvement can, and possibly will, be noted here.

# Credits
The icons I use in the application are from [icons8](https://github.com/icons8/flat-color-icons), and the screencast was made using [silentcast](https://github.com/colinkeenan/silentcast). Application icon is made out of parts by Rafi at [GraphicsFuel](http://www.graphicsfuel.com/).
