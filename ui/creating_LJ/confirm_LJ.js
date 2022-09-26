var role_id = sessionStorage.getItem('role_id');
var selectedCourses = sessionStorage.getItem('checkedCourses');
var role_name = sessionStorage.getItem('role_name');
var course_dict = {};
var courses = selectedCourses.split(',');

document.getElementById('rolename').innerText = role_name;


// console.log(courses);

for(let i = 0; i<courses.length; i+=1){
    var course_comb = courses[i].split('/');
    // console.log(course_comb);

    if (course_comb[0] in course_dict){
        course_dict[course_comb[0]].push(course_comb[1]);
    }
    else{
        course_dict[course_comb[0]] = [course_comb[1]];
    }
}

// console.log(course_dict);

var courseskill = document.getElementById('courseskill');

for(var skill_name in course_dict){
    // console.log(skill_name);
    var courses = course_dict[skill_name];
    // console.log(courses);
    courseskill.innerHTML += `
        <div class='row skillname'> ${skill_name} <br> <ul>`; 
    for (var course in courses){
        // console.log(course)
        courseskill.innerHTML += `
        <li>${courses[course]}</li>
        `;
    }
    courseskill.innerHTML+= `</ul></div>`;
}

function confirmLJ(){
    location.href = '../staff/dashboards_standard.html';
}