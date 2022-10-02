role_descriptions = {
    "roles_details":[
        {
            "role_name": "accountant",
            "role_desc": "Lorem ipsum dolor sit amet consectetur adipisicing elit. Dolorem quisquam, quod earum sapiente impedit illo, provident accusamus, doloremque ducimus laudantium eius aspernatur eum dolores. Ipsam odit a ipsa dolore ducimus.",
            "role_id" :1,
            "skills": [
                {
                    "skill_name": "skill1",
                    "skill_id": "skillID1",
                    "skill_desc": "skillDesc1",
                    "courses": [
                        {
                            "course_name": "course name 1",
                            "course_id" : "course id 1",
                            "course_desc": "course desc 1"
                        },
                        {
                            "course_name": "course name 2",
                            "course_id" : "course id 2",
                            "course_desc": "course desc 2"
                        }
                    ]
                }
            ]
        },
        {
            "role_name": "CEO",
            "role_desc": "Lorem ipsum dolor sit amet consectetur adipisicing elit. Dolorem quisquam, quod earum sapiente impedit illo, provident accusamus, doloremque ducimus laudantium eius aspernatur eum dolores. Ipsam odit a ipsa dolore ducimus.",
            "role_id" :2,
            "skills": [
                {
                    "skill_name": "skill1",
                    "skill_id": "skillID1",
                    "skill_desc": "skillDesc1",
                    "courses": [
                        {
                            "course_name": "course name 1",
                            "course_id" : "course id 1",
                            "course_desc": "course desc 1"
                        },
                        {
                            "course_name": "course name 2",
                            "course_id" : "course id 2",
                            "course_desc": "course desc 2"
                        },
                        {
                            "course_name": "course name 3",
                            "course_id" : "course id 3",
                            "course_desc": "course desc 3"
                        }
                    ]

                },
                {
                    "skill_name": "skill2",
                    "skill_id": "skillID2",
                    "skill_desc": "skillDesc2",
                    "courses": [
                        {
                            "course_name": "course name 1",
                            "course_id" : "course id 1",
                            "course_desc": "course desc 1"
                        },
                        {
                            "course_name": "course name 2",
                            "course_id" : "course id 2",
                            "course_desc": "course desc 2"
                        },
                        {
                            "course_name": "course name 3",
                            "course_id" : "course id 3",
                            "course_desc": "course desc 3"
                        }
                    ]

                },
                {
                    "skill_name": "skill3",
                    "skill_id": "skillID3",
                    "skill_desc": "skillDesc3",
                    "courses": [
                        {
                            "course_name": "course name 1",
                            "course_id" : "course id 1",
                            "course_desc": "course desc 1"
                        },
                        {
                            "course_name": "course name 2",
                            "course_id" : "course id 2",
                            "course_desc": "course desc 2"
                        },
                        {
                            "course_name": "course name 3",
                            "course_id" : "course id 3",
                            "course_desc": "course desc 3"
                        }
                    ]

                }
            ]
        },
        {
            "role_name": "teehee",
            "role_desc": "Lorem ipsum dolor sit amet consectetur adipisicing elit. Dolorem quisquam, quod earum sapiente impedit illo, provident accusamus, doloremque ducimus laudantium eius aspernatur eum dolores. Ipsam odit a ipsa dolore ducimus.",
            "role_id" :3,
            "skills": [
                {
                    "skill_name": "skill1",
                    "skill_id": "skillID1",
                    "skill_desc": "skillDesc1",
                    "courses": [
                        {
                            "course_name": "course name 1",
                            "course_id" : "course id 1",
                            "course_desc": "course desc 1"
                        },
                        {
                            "course_name": "course name 2",
                            "course_id" : "course id 2",
                            "course_desc": "course desc 2"
                        },
                        {
                            "course_name": "course name 3",
                            "course_id" : "course id 3",
                            "course_desc": "course desc 3"
                        }
                    ]

                },
                {
                    "skill_name": "skill2",
                    "skill_id": "skillID2",
                    "skill_desc": "skillDesc2",
                    "courses": [
                        {
                            "course_name": "course name 2",
                            "course_id" : "course id 2",
                            "course_desc": "course desc 2"
                        },
                        {
                            "course_name": "course name 3",
                            "course_id" : "course id 3",
                            "course_desc": "course desc 3"
                        }
                    ]

                }
            ]
        }
    ]
}

var role_details = role_descriptions['roles_details'];

var role_id = sessionStorage.getItem('role_id');

var role_name_div = document.getElementById('rolename');

var role_details_div = document.getElementById('roledetails');

var role_skills_list = document.getElementById('role_skills');

for (var idx in role_details){
    var item = role_details[idx];
    var itemRole_id = item["role_id"];
    var rname = item['role_name'];
    var rdeet = item['role_desc'];
    var skills = item['skills'];
    // console.log(skills);
    // console.log(rname);
    if (itemRole_id == role_id){
        role_name_div.innerHTML = `${rname}`;
        role_details_div.innerHTML = `${rdeet}`;
        for (var skill in skills){
            // console.log(skill);
            var skill_details = skills[skill];
            var skill_name = skill_details['skill_name'];
            var skill_desc = skill_details['skill_desc'];
            // console.log(skill_desc);
            role_skills_list.innerHTML += `
                <li class='skillname'>
                    ${skill_name}
                    <div class='skilldesc'>
                        ${skill_desc}
                    </div>
                </li>
            `
        }
    }
}

console.log(role_id);

function confirmCreateLJ(){
    sessionStorage.setItem('role_id', role_id);
    location.href = './creating_LJ.html';
}