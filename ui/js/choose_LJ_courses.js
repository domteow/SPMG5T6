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
                    console.log(course_name);
                    
                    skillscont.innerHTML += `
                        <div class='row coursename form-check'>
                            <input class='form-check-input' type='checkbox' id=${course_id} onchange="handleChange(this)"  name='skills' value = "${skillname}/${course_name}/${course_id}">
                            ${course_name}
                            <div class='course_desc'>${course_desc}</div>
                        </div>
                    </div>
                    </div>
                    `
                }
            }

            console.log(skillscont);
            
        }
        

    } catch (error) {
        console.log(error)
        console.log('error')
    }
})
    
// TO CHECK ALL THE CHECKBOXES WITH THE SAME VALUE (COURSE NAME)
function handleChange(cb) {
    var cbval = cb.id;
    if(cb.checked == true) {
        // to check all checkbox with the SAME ID -> course_id
        var cbox = `input[id=${cbval}]`
        var allCB = document.querySelectorAll(cbox);
        for (var i=0; i< allCB.length; i++){
            allCB[i].checked = true;
        }
      
    } else {
        // to uncheck all checkbox
        var cbox = `input[id=${cbval}]`
        var allCB = document.querySelectorAll(cbox);
        for (var i=0; i< allCB.length; i++){
            allCB[i].checked = false;
        }

    }
}

var errormsg = document.getElementById('nameError');

function getValues(){
    const allChecked = document.querySelectorAll('input[name=skills]:checked');

    var checkedCourses = Array.from(allChecked).map(checkbox => checkbox.value);
    console.log(checkedCourses);
    if(checkedCourses.length == 0) {
        errormsg.innerText = `Please select at least one course to create your learning journey.`;
        location.href = "#top";
    }
    else {
        sessionStorage.setItem('checkedCourses', checkedCourses);
        var staff_role = sessionStorage.getItem('staff_role');
        console.log(staff_role);
        if (staff_role == 1){
            location.href = '../hr/confirm_LJ.html';
        }
        if(staff_role == 2){
            location.href = '../staff/confirm_LJ.html';
        }
        if(staff_role == 3){
            location.href = '../manager/confirm_LJ.html';
        }  
    }
}

