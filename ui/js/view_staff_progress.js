var staff_id = sessionStorage.getItem('view_staff');

var coursesdiv = document.getElementById('courses');
var skillsdiv = document.getElementById('skills');

var staffname = document.getElementById('name');
var staffemail = document.getElementById('email');
var staffdept = document.getElementById('dept');

// display all completed courses of staff (SA-12 BRUNO USER STORY)
$(async () => {
    var serviceURL = "http://127.0.0.1:5001/get_completed_course_of_staff/" + staff_id 

    try {
        const response = await fetch(serviceURL, { mode: "cors", method: "GET" });
        const result = await response.json();
        if (result){
            var data = result;
            var completed_courses = data['completed_courses'];
            
            if(completed_courses.length > 0){
                document.getElementById('courseNoVal').style.display = 'none';
                for(var idx in completed_courses){
                    var coursedeets = completed_courses[idx];
                    var course_name = coursedeets['course_name'];

                    coursesdiv.innerHTML += `
                        <div class = 'row coursesrow'>
                            <div class = 'col-9 ctitle'>
                                ${course_name}
                            </div>
                            <div class = 'col-3 statusdiv'>
                                <div class='completed'>
                                    Completed
                                </div>
                            </div>
                        </div>
                    `;
                }
            }            
        }
    }

    catch (error){
        console.log(error);
        console.log('error');
    }
});


// display all ongoing courses of staff (SA-10 BRUNO'S USER STORY)
$(async () => {
    var serviceURL = "http://127.0.0.1:5001/get_ongoing_course_of_staff/" + staff_id 

    try {
        const response = await fetch(serviceURL, { mode: "cors", method: "GET" });
        const result = await response.json();
        if (result){
            var data = result;
            var ongoing_courses = data['ongoing_courses'];
            var staffdata = result['staff_details'];
            var staff_name = staffdata['staff_fname'] + ' ' + staffdata['staff_lname'];
            var staff_email = staffdata['email'];
            var staff_dept = staffdata['dept'];

            staffname.innerHTML = `${staff_name} <span class="staffDept" id="dept">${staff_dept}</span>`;
            staffemail.innerText = staff_email;
            staffdept.innerHTML = `<div>${staff_dept}</div>`;
            
            if(ongoing_courses.length > 0){
                document.getElementById('courseNoVal').style.display = 'none';
                for(var idx in ongoing_courses){
                    var coursedeets = ongoing_courses[idx];
                    var course_name = coursedeets['course_name'];

                    coursesdiv.innerHTML += `
                        <div class = 'row coursesrow'>
                            <div class = 'col-9 ctitle'>
                                ${course_name}
                            </div>
                            <div class = 'col-3 statusdiv'>
                                <div class='ongoing'>
                                    Ongoing
                                </div>
                            </div>
                        </div>
                    `;
                }
            }            
        }
    }

    catch (error){
        console.log(error);
        console.log('error');
    }
});

// display all ongoing skills of staff (SA-23 BRYAN USER STORY)
$(async () => {
    var serviceURL = "http://127.0.0.1:5001/get_in_progress_skills_of_staff/" + staff_id

    try {
        const response = await fetch(serviceURL, { mode: "cors", method: "GET" });
        const result = await response.json();
        if (result){
            var data = result['data'];
            var ongoing_skills = data['in_progress_skills'];
            
            if (ongoing_skills.length > 0){
                document.getElementById('skillNoVal').style.display = 'none';
                for (var idx in ongoing_skills){
                    var skilldeets = ongoing_skills[idx];
                    var skill_name = skilldeets['skill_name'];

                    skillsdiv.innerHTML += `
                        <div class='row coursesrow'>
                            <div class='col-9 ctitle'>
                                ${skill_name}
                            </div>
                            <div class='col-3 statusdiv'>
                            <div class='ongoing'>
                                Ongoing
                            </div>
                            </div>
                        </div>
                    `;
                }
            }
        }
    }

    catch (error){
        console.log(error);
        console.log('error');
    }
})

// display all completed skills of staff (SA-18 BRYAN USER STORY)
$(async () => {
    var serviceURL = "http://127.0.0.1:5001/get_attained_skills_of_staff/" + staff_id

    try {
        const response = await fetch(serviceURL, { mode: "cors", method: "GET" });
        const result = await response.json();
        if (result){
            var data = result['data'];
            var attained_skills = data['attained_skills'];
            
            if (attained_skills.length > 0){
                document.getElementById('skillNoVal').style.display = 'none';
                for (var idx in attained_skills){
                    var skilldeets = attained_skills[idx];
                    var skill_name = skilldeets['skill_name'];

                    skillsdiv.innerHTML += `
                        <div class='row coursesrow'>
                            <div class='col-9 ctitle'>
                                ${skill_name}
                            </div>
                            <div class='col-3 statusdiv'>
                                <div class='completed'>
                                    Attained
                                </div>
                            </div>
                        </div>
                    `;
                }
            }
        }
    }

    catch (error){
        console.log(error);
        console.log('error');
    }
})