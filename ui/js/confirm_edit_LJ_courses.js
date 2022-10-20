var ljpsr_id = sessionStorage.getItem('ljpsr_id');
var selectedCourses = sessionStorage.getItem('checkedCourses');
// var role_name = sessionStorage.getItem('role_name');
var course_dict = {};
var courses = selectedCourses.split(',');
var staff_id = sessionStorage.getItem('staff_id')

// var skillarr = sessionStorage.getItem('skillarr') //array of skill IDs
new_lj_details = JSON.parse(sessionStorage.getItem('new_lj_details'))
console.log(new_lj_details)

document.getElementById('rolename').innerText = new_lj_details.ljps_role.role_title;


console.log(courses);

for(let i = 0; i<courses.length; i+=1){
    var course_comb = courses[i].split('/');
    console.log(course_comb);

    if (course_comb[0] in course_dict){
        course_dict[course_comb[0]].push({'course_id':course_comb[2],'course_name':course_comb[1]});
    }
    else{
        course_dict[course_comb[0]] = [{'course_id':course_comb[2],'course_name':course_comb[1]}];
    }
}

console.log(course_dict);
console.log(JSON.stringify(course_dict))
var courseskill = document.getElementById('courseskill');

for(var skill_name in course_dict){
    // console.log(skill_name);
    var courses = course_dict[skill_name];
    console.log(courses);
    courseskill.innerHTML += `
        <div class='row skillname'> ${skill_name} <br> <ul>`; 
    for (var course of courses){
        console.log(course)
        courseskill.innerHTML += `
        <li>${course.course_name}</li>
        `;
    }
    courseskill.innerHTML+= `</ul></div>`;
}

// function confirmLJ(){
//     location.href = '../staff/dashboard_standard.html';
// }


async function confirm_edit_LJ(){
    // creating LJ in learning_journey table
    var course_arr = JSON.stringify(course_dict)
    console.log(course_arr)
    var journey_id = sessionStorage.getItem("activeLJ")
    // var serviceURL = "http://127.0.0.1:5001/edit_LJ_courses/" + Number(journey_id) + '&' + String(course_arr)
    var serviceURL = "http://127.0.0.1:5001/edit_LJ_courses/" 

    console.log(serviceURL)

    try {
        const response =
            await fetch(
            serviceURL, { mode: 'cors', method: ['POST'],
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                "journey_id" : journey_id,
                "staff_id" : staff_id,
                // stringify course array and add here
                "course_arr" : course_arr
            })
        });
        console.log(response)
        const result = await response.json();
        console.log(result)
        if(response.status === 201 || response.status === 200) {
            console.log('Learning Journey edited')
            alert('Learning Journey edited')
        }
        

    } catch (error) {
        console.log(error)
        console.log('error')
    }


    // creating courses in lj_course table

    var staff_role = sessionStorage.getItem('staff_role');
    console.log(staff_role);
    if (staff_role == 1){
        location.href = '../hr/dashboard_hr.html';
    }
    if(staff_role == 2){
        location.href = '../staff/dashboard_standard.html';
    }
    if(staff_role == 3){
        location.href = '../manager/dashboard_manager_personal.html';
    }
    
}