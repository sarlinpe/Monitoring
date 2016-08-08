<!--
Copyright (c) 2016, Paul-Edouard Sarlin
All rights reserved.

Project:     Autonomous Monitoring System
File:        temp_bootstrap_settings.tpl
Date:        2016-08-08
Author:      Paul-Edouard Sarlin
Website:	 https://github.com/skydes/monitoring
-->

<!DOCTYPE html>
<html lang="en">
<head>
    <title>Monitoring settings</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
    <script src="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js"></script>
    
    <link href="https://gitcdn.github.io/bootstrap-toggle/2.2.2/css/bootstrap-toggle.min.css" rel="stylesheet">
    <script src="https://gitcdn.github.io/bootstrap-toggle/2.2.2/js/bootstrap-toggle.min.js"></script>
    
    <style>
        .glyphicon {
            top: 3px;
        }
        form {
            font-family: courier;
        }
        .form-horizontal .checkbox {
            padding-top: 0px;
        }
        % include('temp_bootstrap_banner_css', active=conf["capture"])
        % include('temp_bootstrap_footer_css')
    </style>
</head>

<body>

% include('temp_bootstrap_banner', conf=conf, parent="settings")

<div class="container">
    <div class="row">
        <div class="col-md-8 col-md-offset-2">
            <form class="form-horizontal" role="form" method="post">
                
                <h3 class="col-md-6 col-md-offset-6"><span class='glyphicon glyphicon-facetime-video'></span> Motion detection</h3>
                <div class="form-group">
                    <label class="control-label col-md-6">Minimum consecutive motion frames:</label>
                    <div class="col-md-6">
                        <input type="number" name="proc-min-motion-frames" class="form-control" min="1" max="100" value={{conf["proc-min-motion-frames"]}}>
                    </div>
                </div>
                <div class="form-group">
                    <label class="control-label col-md-6">Motion detection threshold:</label>
                    <div class="col-md-6">
                        <input type="number" name="proc-motion-thresh" class="form-control" min="1" max="100" value={{conf["proc-motion-thresh"]}}>
                    </div>
                </div>
                <div class="form-group">
                    <label class="control-label col-md-6">Minimum motion area:</label>
                    <div class="col-md-6">
                        <input type="number" name="proc-min-area" class="form-control" min="1" max="10000" value={{conf["proc-min-area"]}}>
                    </div>
                </div>
                
                <h3 class="col-md-6 col-md-offset-6"><span class='glyphicon glyphicon-cloud-upload'></span> Cloud settings</h3>
                <div class="form-group">
                    <label class="control-label col-md-6">Activate Dropbox:</label>
                    <div class="col-md-6">
                        <div class="checkbox">
                            <input type="checkbox" name="dropbox" data-toggle="toggle" data-onstyle="default" value="True" \\
                            % if conf["dropbox"]:
                                checked\\
			    % end
                            >
                        </div>
                    </div>
                </div>
                <div class="form-group">
                    <label class="control-label col-md-6">Dropbox folder:</label>
                    <div class="col-md-6">
                        <input type="text" name="dropbox-path" class="form-control" value={{conf["dropbox-path"]}}>
                    </div>
                </div>
                <div class="form-group">
                    <label class="control-label col-md-6">Minimum delay between uploads:</label>
                    <div class="col-md-6">
                        <input type="number" name="proc-min-delay" class="form-control" min="1" max="60" step="0.1" value={{conf["proc-min-delay"]}}>
                    </div>
                </div>
                
                <div class="form-group">
                    <div class="text-center">
                        <button type="submit" class="btn btn-default" style="margin-top:20px;">Save</button>
                    </div>
                </div>
                
            </form>
        </div>
    </div>
</div>

% include('temp_bootstrap_footer')

</body>
</html>

