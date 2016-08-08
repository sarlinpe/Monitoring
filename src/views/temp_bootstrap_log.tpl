<!--
Copyright (c) 2016, Paul-Edouard Sarlin
All rights reserved.

Project:     Autonomous Monitoring System
File:        temp_bootstrap_log.tpl
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

% include('temp_bootstrap_banner', conf=conf, parent="log")

<div class="container">
    <div class="row">
        <pre>
            <samp>
                {{"\n"+file.read()}}
            </samp>
        </pre>
    </div>
</div>

% include('temp_bootstrap_footer')

</body>
</html>

