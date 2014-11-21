greatlakes-call-data
====================

Data analysis and visualizations of phone data from the Great Lakes region in East Africa (Rwanda, Uganda).

This is an accumulation of analysis and visualizations I created while working at the UC Berkeley School of Information in conjunction with the Grameen Foundation/MTN Uganda. The projects are split up into two countries - Rwanda
and Uganda and the analyses vary for each.

Under Uganda:
** user_features: Collecting basic features about each phone user that can be used to predict attributes and conversions to other products provided by the telecom. In addition to simple features such as the number of incoming/outgoing, weekend/weekday and rural/urban calls, we can also calculate user mobility metrics, including the user's "center of mass" (the average of all the latitude and longitudes of the user's locations, weighted by frequency), radius of gyration (how far the user deviates from the center of mass) and the user's total distance covered and velocity. We also perform simple graph analysis on users and their contacts, with edges weighed by the frequency and duration of contact.
** charts: Used R to test out features to be used in prediction of user conversion (from phone to mobile money users) and to create graphs of weekday/weekend and urban/rural usage.

Under Rwanda:
** earthquake - On a map of Rwanda, this animation shows the regions with relatively high numbers of incoming phone calls to an area of Rwanda that was affected by the 2008 Lake Kivu earthquake. This was done by
(1) generating a Voronoi diagram based off of all phone tower coordinates in Rwanda
(2) highlighting each Voronoi polygon depending on the relative number of incoming phone calls from that phone tower to the destination tower, where on a scale from blue to red, red means greater activity
** intl_calls - A similar animation was created for international incoming phone calls
** me2u - Analysis of mobile money transfers in Rwanda and the factors that cause user conversions

