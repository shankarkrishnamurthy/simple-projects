const express = require('express');
const route = express.Router();
const ideaMod = require('../models/idea');
const {
    ensureAuthenticated
} = require('../helpers/auth');

route.get('/add', ensureAuthenticated, function (req, res, next) {
    res.render('ideas/add');
});
route.get('/edit/:id', ensureAuthenticated, function (req, res, next) {
    ideaMod.find({
            _id: req.params.id,
            user: req.user._id,
        })
        .then(ideas => {
            if (ideas.length == 0) {
                req.flash('error_msg', 'Document not found');
                res.redirect('/ideas');
            } else {
                res.render('ideas/edit', {
                    idea: ideas[0],
                });
            }
        });
});

route.delete('/:id', ensureAuthenticated, (req, res) => {
    ideaMod.deleteOne({
            _id: req.params.id,
            user: req.user._id,

        })
        .then(idea => {
            req.flash('success_msg', ' Successfully removed');
            res.redirect('/ideas');
        })
        .catch(err => {
            req.flash('error_msg', 'Document not found');
            res.redirect('/ideas');
        });
});

route.put('/:id', ensureAuthenticated, (req, res) => {
    ideaMod.findOne({
            _id: req.params.id,
            user: req.user._id,
        })
        .then(idea => {
            idea.title = req.body.title;
            idea.details = req.body.details;

            idea.save()
                .then(idea => {
                    req.flash('success_msg', ' Successfully edited');
                    res.redirect('/ideas');
                });
        });
});

route.get('/', ensureAuthenticated, function (req, res, next) {
    ideaMod.find({
            user: req.user._id
        })
        .sort({
            date: 'desc'
        })
        .then(idlist => {
            res.render('ideas/index', {
                ideas: idlist,
            });
        });

});

route.post('/', ensureAuthenticated, function (req, res, next) {
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
            details: req.body.details,
            user: req.user._id
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
