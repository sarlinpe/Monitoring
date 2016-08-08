<!--
Copyright (c) 2016, Paul-Edouard Sarlin
All rights reserved.

Project:     Autonomous Monitoring System
File:        temp_bootstrap_home.tpl
Date:        2016-08-08
Author:      Paul-Edouard Sarlin
Website:	 https://github.com/skydes/monitoring
-->

<!DOCTYPE html>
<html lang="en">
<head>
    <title>Monitoring homepage</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
    <script src="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js"></script>

    <style>
        .img-box {
            text-align: center;
            padding-top: 10px;
            padding-bottom: 15px;
            font-family: courier;
        }
        % include('temp_bootstrap_banner_css', active=conf["capture"])
        % include('temp_bootstrap_footer_css')
    </style>
</head>

<body>

% include('temp_bootstrap_banner', conf=conf, parent="home")

<div class="container-fluid”>
    <div class="row">
    % for img in frames_list:
        <div class="col-md-6 img-box">
            <h3>{{img[1]}}</h3>
            <img class="img-responsive img-thumbnail" src="{{img[0]}}" alt="Image">
        </div>
    % end
    </div>
</div>

% include('temp_bootstrap_footer')

</body>
</html>

