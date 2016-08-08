<!--
Copyright (c) 2016, Paul-Edouard Sarlin
All rights reserved.

Project:     Autonomous Monitoring System
File:        temp_bootstrap_banner_css.tpl
Date:        2016-08-08
Author:      Paul-Edouard Sarlin
Website:	 https://github.com/skydes/monitoring
-->

<%
if active:
    active_color = "#AAFFAA"
else:
    active_color = "#FFAAAA"
end
%>

.jumbotron {
    background-color: {{active_color}};
    font-family: courier;
    padding-top: 10px;
    padding-bottom: 10px;
}
.glyphicon {
    top: 3px;
}