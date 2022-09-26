role_descriptions = {
    1: {
        'role_title': 'accountant',
        'role_description': 'counting numbers',
        'skills': {
            'skill1': ['s1c1', 's1c2', 's1c3'],
            'skill2': ['s2c1', 's2c2'],
            'skill3': ['s3c1', 's3c2']
        } 
    },
    
    2: {
        'role_title': 'cashier',
        'role_description': 'counting money',
        'skills': {
            'skill1': ['s1c1', 's1c2', 's1c3'],
            'skill2': ['s2c1', 's2c2'],
            'skill3': ['s3c1', 's3c2'],
            'skill4': ['s4c1', 's4c2']
        } 
    },

    4:{
        'role_title': 'cleaner',
        'role_description': 'clean',
        'skills': {
            'skill1': ['s1c1', 's1c2', 's1c3']
        } 
    },

    6 : {
        'role_title': 'econs person',
        'role_description': 'idk',
        'skills': {
            'skill1': ['s1c1', 's1c2'],
            'skill2': ['s2c1'],
            'skill3': ['s3c1', 's3c2'],
            'skill4': ['s4c1', 's4c2']
        } 
    }
}


var roleid = sessionStorage.getItem('roleid');
console.log(roleid);

var details = role_descriptions[roleid];

/* add role title */
var title = document.getElementById('roletitle');
title.innerText = details['role_title'];

/* add role description */
var description = document.getElementById('roledescription');
description.innerText = details['role_description'];

/* add skill & courses */ 
var skills = details['skills'];
var skillscont = document.getElementById('skillscontainer');
for (var skill in skills){
        console.log(skill);
        var courses = skills[skill];
        console.log(courses);
        skillscont.innerHTML += `
            <div class="row skillname">
                ${skill}
            <div class="container-fluid coursecontainer" id="coursecontainer">`;
            for (course in courses){
                // console.log(courses[course]);
                skillscont.innerHTML += `
                    <div class="row coursename form-check">
                        <input class='form-check-input' type="checkbox" id="${courses[course]}" name="" value=""> 
                        ${courses[course]}
                    </div>
                </div>
            </div>
        `
    }
}