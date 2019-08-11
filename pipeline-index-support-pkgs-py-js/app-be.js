const express = require('express'), app = express();
const bodyParser = require('body-parser');
const path = require('path');

var port = process.env.PORT || 2567;

app.use(bodyParser.json());

app.route('/vet').post(check_sr);
app.route('/:sr').post(save_content);

app.listen(port);

var srlist = []


// main functions
function save_content(req,res) {
    res.send({ 'SR': 'OK' });
}

function check_sr(req, res) {
    var present;
    var dirty = 0;
    console.log(req.body)
    present = ('SR' in req.body && req.body['SR'] in srlist)
    //srlist[req.body['SR']] = 0;
    res.status(200).send({ 'present': present && !dirty, 'SR' : req.body['SR'] })
}

