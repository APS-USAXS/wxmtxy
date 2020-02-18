# README


*wxmtxy* (an EPICS GUI tool) provides support for an X,Y positioner 
(motor) pair by allowing users to define a table of known positions 
and providing a one-button click to drive a chosen X,Y pair to a specific
table setting.  Also can record current position into a setting.

Several sets of X,Y positioners can be configured.  (Each set is 
separate.)  In fact, the positioners do not have to be motors,
but can be any type of EPICS PV that will accept a numeric value.


wxmtxy is based on wxPython and relies on CaChannel to communicate 
with EPICS. 

In the Graphical User Interface (GUI), tooltips are provided for 
most items.  Moving and pausing the mouse over a widget (GUI 
component such as a button or a label) will cause a terse description 
of that widget to be displayed. Moving the mouse away will cause that 
tooltip to disappear. 

For more help, explanations are provided in the HTML pages.
