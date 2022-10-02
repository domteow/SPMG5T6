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


// console.log(role_id);

var role_details = JSON.parse(sessionStorage.getItem('role_details'));
var ljpsr_role_id = role_details.ljps_role.ljpsr_id;
console.log(role_details)

// Retrieving courses for each skill (dom)
staff_id = sessionStorage.getItem('staff_id')
$(async () => {
    var serviceURL = "http://127.0.0.1:5001/view_courses_under_skill/" + staff_id + '/' + ljpsr_role_id

    try {
        const response =
            await fetch(
            serviceURL, { mode: 'cors', method: 'GET' }
        );
        // console.log(response)
        const result = await response.json();
        console.log(result.data)
        if(result) {
            console.log('Courses for skill retrieved')
            new_lj_details = JSON.stringify(result.data)
            sessionStorage.setItem('new_lj_details', new_lj_details)
            var item = result.data.ljps_role;



            /* add role title */ 
            var role_name = item['role_title'];
            var title = document.getElementById('roletitle');
            title.innerText = item['role_title'];
            
            /* add role description */ 
            var description = document.getElementById('roledescription');
            // console.log(description);
            description.innerText = item['role_desc'];

            /* add skill and courses*/ 
            var skillscont = document.getElementById('skillscontainer');
            var skills = result.data.skills_with_courses;
            for (var sidx in skills){
                console.log(sidx)
                var skill = skills[sidx];
                var skillname = skill['skill_name'];
                var courses = skill['courses'];
                var skill_id = skill['skill_id'];
                skillscont.innerHTML += `
                    <div class='row skillname'>${skillname}
                        <div class='container-fluid coursecontainer' id='coursecontainer'>`; 
                for (var course_idx in courses){
                    var course = courses[course_idx];
                    var course_name = course['course_name'];
                    var course_desc = course['course_desc'];
                    var course_id = course['course_id'];
                    skillscont.innerHTML += `
                        <div class='row coursename form-check'>
                            <input class='form-check-input' type='checkbox' id=${course_id} name = 'skills' value = "${skillname}/${course_name}/${course_id}">
                            ${course_name}
                            <div class='course_desc'>${course_desc}</div>
                        </div>
                    </div>
                    </div>
                    `
                }
            }
        }
        

    } catch (error) {
        console.log(error)
        console.log('error')
    }
})



    


function getValues(){
    const allChecked = document.querySelectorAll('input[name=skills]:checked');

    // console.log(allChecked);

    // console.log(Array.from(allChecked).map(checkbox => checkbox.value));

    var checkedCourses = Array.from(allChecked).map(checkbox => checkbox.value);

    console.log(checkedCourses);

    sessionStorage.setItem('checkedCourses', checkedCourses);
    // sessionStorage.setItem('ljpsr_role_id', ljpsr_role_id);
    // sessionStorage.setItem('role_name', role_name);
    

    location.href = './confirm_LJ.html';
}

