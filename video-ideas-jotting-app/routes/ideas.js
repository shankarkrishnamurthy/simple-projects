const express = require('express');
const route = express.Router();
const ideaMod = require('../models/idea');

route.get('/add', function (req, res, next) {
    res.render('ideas/add');
});
route.get('/edit/:id', function (req, res, next) {
    ideaMod.find({
            _id: req.params.id
        })
        .then(ideas => {
            res.render('ideas/edit', {
                idea: ideas[0],
            });
        });
});

route.delete('/:id', (req, res) => {
    ideaMod.deleteOne({
            _id: req.params.id
        })
        .then(idea => {
            req.flash('success_msg', ' Successfully removed');
            res.redirect('/ideas');

        });
});

route.put('/:id', (req, res) => {
    ideaMod.findOne({
            _id: req.params.id
        })
        .then(idea => {
            idea.title = req.body.title;
            idea.details = req.body.details;

            idea.save()
                .then(idea => {
                    req.flash('success_msg', ' Successfully edited');
                    console.log(res.locals)
                    res.redirect('/ideas');
                });
        });
});

route.get('/', function (req, res, next) {
    ideaMod.find({})
        .sort({
            date: 'desc'
        })
        .then(idlist => {
            res.render('ideas/index', {
                ideas: idlist,
            });
        });

});

route.post('/', function (req, res, next) {
    let errors = [];
    if (!req.body.title) {
        errors.push({
            text: ' Please add title '
        });
    }
    if (!req.body.details) {
        errors.push({
            text: ' Please add details '
        });
    }
    if (errors.length > 0) {
        res.render('ideas/add', {
            errors: errors,
            title: req.body.title,
            details: req.body.details
        })
    } else {
        const nUser = {
            title: req.body.title,
            details: req.body.details
        };
        new ideaMod(nUser)
            .save()
            .then(id => {
                req.flash('success_msg', ' Successfully added');
                res.redirect('/ideas');
            })
    }
});

module.exports = route;
