<!--
Copyright (c) 2016, Paul-Edouard Sarlin
All rights reserved.

Project:     Autonomous Monitoring System
File:        temp_bootstrap_banner.tpl
Date:        2016-08-08
Author:      Paul-Edouard Sarlin
Website:	 https://github.com/skydes/monitoring
-->

<%
if conf["capture"]:
    active_button_label = "Inactivate"
    active_state = "active"
else:
    active_button_label = "Activate"
    active_state = "inactive"
end

error_list = []
if conf["error"]["capture"]:
    error_list.append("Capture")
end
if conf["error"]["dropbox"]:
    error_list.append("Dropbox")
end

button_home = '<a href="/" class="btn btn-default btn-md" role="button"><span class="glyphicon glyphicon-home"></span> Home</a>'
button_settings = '<a href="/settings/" class="btn btn-default btn-md" role="button"><span class="glyphicon glyphicon-cog"></span> Settings</a>'
button_log = '<a href="/log/" class="btn btn-default btn-md" role="button"><span class="glyphicon glyphicon-wrench"></span> Log</a>'
%>



<div class="jumbotron text-center">
    <h1>Monitoring System</h1>
    <p>The system is currently <strong>{{active_state}}</strong>.</p>
    <div class="list-group">
        <a href="/toggle/" class="btn btn-default btn-md" role="button">
            <span class="glyphicon glyphicon-off"></span> {{active_button_label}}
        </a>

        % if (parent == "home"):
        {{!button_settings}}
        {{!button_log}}
        % elif (parent == "settings"):
        {{!button_home}}
        {{!button_log}}
        % elif (parent == "log"):
        {{!button_home}}
        {{!button_settings}}
        % end
    </div>
% for error in error_list:
<div class="container">
<div class="alert alert-warning">
<strong>Warning:</stron> {{error}} has been automatically disabled due to a technical problem.
</div>
</div>
% end
</div>
