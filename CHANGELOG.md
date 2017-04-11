##### 02.13.16 #####
- fixed bug where large messages from websocket server breaks remote Jarvis connections

##### 11.18.15 #####
- websocketserver no longer gets stuck when ctrl-c is pressed
- alert when trying to change settings without websocket connection

##### 11.11.15 #####
- added cat-ion to photon counter

##### 11.09.15 #####
- added option to do pulse programmer plot via Flot
- added save status indicator to pulse programmer widget and no longer allows overwriting of files

##### 11.06.15 #####
- added sound when pulse programmer script is finished
- pulse programmer now reads out the entire output at the end of script execution if in auto readout mode

##### 10.15.15 #####
- moved X88 websocketserver to wigner
- updated blog_screenshot to always take screenshot of rabi (need certificate SSH access to rabi)
- added invert colors mode (click little lightbulb below the logo)

##### 10.14.15 #####
- loading trap electrode graphics as background instead of drawing it every time
- adding new widgets will now work with cookies

##### 10.12.15 #####
- pulse programmer now only outputs nonzero values in both readout and PMT readout

##### 10.2.15 #####
- added device file option (-f) in websocketserver, now running two instances
- user friendly labels

##### 10.1.15 #####
- HTML headers to prevent caching (otherwise Chrome cache folder grows very big)
- PMT readout in pulse programmer
- Newport 461, 1033, and 844 TA controls

##### 9.10.15 #####
- made pulse programmer auto readout an option
- added reload button to each widget on the sidebar (the refresh icon) to reload widget HTML files without refreshing the page
- UI fix to make it obvious which script tab is currently being selected

##### 9.7.15 #####
- pulse programmer now reads out automatically when a script is running

##### 9.4.15 #####
- added HELPERS.h variable definitions to pulse programmer widget
- added feature to save readout data from pulse programmer widget

##### 9.3.15 #####
- trap electrodes can now change to new secular frequency voltages slowly

##### 8.31.15 #####
- scripts now get to use their own plot handler if PlotHandlerFlag is set to True (see QuantumJump.py for example)

##### 8.6.15 #####
- logs bug fix
- *real* pulse programmer fix
- adding plot functions to scripts

##### 8.5.15 #####
- pulse programmer now indicates if script is running
- logs have individual devices

##### 4.8.15 #####
- pulse programmer readout plots now have zeros at end trimmed

##### 4.3.15 #####
- 2D and heatmap plots now have option to return to start at end of plot

##### 4.2.15 #####
- pulse programmer scripts directory listing fixed; it was a permissions issue fixed by running nginx as X88
- changed pulse programmer readout to arrayed format, good for plotting and importing (was using toString which stripped all brackets)
- added timeout to websocket client communication, hopefully has fixed the occasional unresponsive server problem

##### 4.1.15 #####
- pulse programmer wasn't reading out the graph, now fixed
- /Dropbox/Quanta/Software/GitHub/Jarvis now running at quanta-rabi/devel; had to change nginx to be run by X88 instead of www-data

##### 3.31.15 #####
- moved data and screenshots to dropbox folder (Quanta/Data)
- moved DeviceWorkers to dropbox folder (Quanta/Software/GitHub)
- changed horizontal compensation to update pairwise instead of one side before other side
- plots now save all of current_states in the header
- changed mousein/out detection for dialogs to individual element hover detection when user is updating settings (so updates don't override what they're trying to do)

##### 3.30.15 #####
- fixed plotting bugs (need new line at end of every device setting)

##### 3.27.15 #####
- fixed compensation in trap electrodes
