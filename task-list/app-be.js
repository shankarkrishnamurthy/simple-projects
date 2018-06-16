const express = require('express'), app = express();
const bodyParser = require('body-parser');
const Task = require('./task');
const path = require('path');

var port = process.env.PORT || 5432;

// necessary middle ware
//app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());
app.use(express.static(path.join(__dirname, 'public')));

// todo List Routes
app.route('/tasks')
    .get(Task.list_all_tasks)
    .post(Task.create_a_task);

app.route('/tasks/:taskId')
    .delete(Task.delete_a_task)
//    .get(Task.read_a_task)
//    .put(Task.update_a_task)

// listen on our port
app.listen(port);


