const mongoose = require('mongoose');
const Schema = mongoose.Schema;

mongoose.Promise = global.Promise;
mongoose.connect('mongodb://localhost/TL1-db', { useMongoClient: true });

const TaskSchema = new Schema ({
    task: String,
    date: { 
        type: Date, 
        default: Date.now 
    }
});

const Task= mongoose.model('mytaskmodel', TaskSchema);

function list_all_tasks(req, res) {
    Task.find({}, function(err, tasks) {
        if (err)
            res.send(err);
        else
            res.json(tasks);
    })
}

function create_a_task(req, res) {
    //console.log(req.body);
    var t = new Task(req.body);
    t.save(function(err, data) {
        if (err)
            res.send(err);
        else
            res.send(data);
    });
}

function delete_a_task(req, res) {
    var id = req.params.taskId;
    console.log(id);
    Task.remove({_id: id}, function (err, task) {
        if (err)
            res.send(err);
        else
            res.json({message: 'Task successfully deleted'});
    });
    
}

//function read_a_task(req, res) {}
//function update_a_task(req, res) {}

exports.list_all_tasks = list_all_tasks;
exports.create_a_task = create_a_task;
exports.delete_a_task = delete_a_task;