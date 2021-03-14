#!/usr/bin/node
/*
    Description: Simple Temperature tracking tool for winter weather
    Author: Shankar K (Oct 2017)
*/

var https = require("request");

var url = "https://developer-api.nest.com";
var path = '/devices/thermostats';
var contenttype = 'application/json';

//REAL
// var accesstoken = ' **** https://developers.nest.com/guides/api/how-to-auth#exchange-authorization-code-for-an-access-token *** ';
//var deviceid = ['zN2I-rK4gVoHdkur-zzVorAmRwxi1amd', 'sGKXgmos9X4y4BMPt4iFcLAmRwxi1amd'];

var auth = 'Bearer ' + accesstoken;

var options = {
    headers : {
        'content-type' : contenttype,
        'Authorization': auth
    },
};
var therm = {}

function process(therm) {
    console.log(JSON.stringify(therm, null, 4))
    const funproperties = [
        'name',
        'humidity',
        'temperature_scale',
        'target_temperature_f',
        'ambient_temperature_f',
        'hvac_mode'
    ];

    //validate
    for (v of funproperties) {
        if (!therm.hasOwnProperty(v)) {
            throw 'CHECK: api seems to have changed.' +  v + " Not available";
        }
        //console.log(v + '   : ' + therm[v]);
    }

    if ((therm['hvac_mode'] !== 'heat' &&
        therm['hvac_mode'] !== 'eco') ||
        therm['temperature_scale'] !== 'F') {
        throw "CHECK: Scale and Mode are not expected";
    }
    
    var tt = therm['target_temperature_f'];
    var at = therm['ambient_temperature_f'];
    var hu = therm['humidity'];
    
    if (tt < 60 || tt > 100 || 
       at < 60 || at > 100 ||
       hu < 20 || hu > 70) {
        throw "CHECK: Temperature/Humidity not in expected range ";
    }
    
    var nd = new Date();
    var s = nd.toLocaleDateString() + ' ' +
            nd.toLocaleTimeString('en-US', {hour12: false});
    
    var out = s+' '+therm['name']+' HU '+hu+' AT '+at+' TT '+tt;
    console.log(out);
    
}

for (dev of deviceid) {
    options.url = url + path + '/' + dev;
    https.get(options, (err, res, body) => {
        try {
        if (err || res.statusCode != 200) {
            console.log(err);
            throw "CHECK: cannot get response";
        }

        //console.log(res);
        process(JSON.parse(body));
        }
        catch (err) {
            console.log('Error: ' + err);
        }
    });
}

// Catch the throws and send emails (later)



