# When Wizard

It turns out that [**When**](https://github.com/almostearthling/when-command) could be more productive for some users if there was a more streamlined interface to manage conditions and reactions, while other reports consider the interface already usable. I think that the applet should be able to behave in both ways:

* offer the usual interface, with direct access to *tasks*, *conditions* and *signal handlers*
* provide a simpler, intuitive and wizard-based interface to hide the parts that require knowledge of the shell, scripting and maybe even some programming.

Instead of boiling everything together, which would make **When** too heavy to both use and develop, I thought that a different approach could be taken that allows both aspects to coexist. On the applet side two features have been implemented:

1. the ability to manage *tasks*, *conditions* and *signal handlers* without directly accessing the configuration dialog boxes, that is using specific command line arguments and specially crafted text files
2. the possibility to completely hide the *tasks*, *conditions* and *signal handlers* dialog boxes from both menu and command line access

which were also discussed in **When** [Issue 65](https://github.com/almostearthling/when-command/issues/65). These features can be useful to create libraries of *items* to be shared among systems, but their main goal was what the **When Wizard** tries to implement: control **When** with a separate application.

The main achievements that the **When Wizard** strives for are:

* an intuitive interface, with *step-by-step* (wizard-like) procedures to define reactions to conditions
* the ability to manage *items* in **When** directly, without user interaction with the actual applet
* a built-in library of *conditions* and *tasks* for many common use cases
* the possibility to extend the **When Wizard** functionality via *plugins*, which should be easy to install through the GUI
* direct management of **When**'s settings, especially for tuning and *Minimalistic Mode*
* a simple but complete documentation for end users and plugin developers.

The only requirement for the **When Wizard** for now is that it should not borrow code from **When** to perform *"magic"* operations or interact with **When**'s internals: the command line and the configuration file should be powerful enough to entirely control the applet.
