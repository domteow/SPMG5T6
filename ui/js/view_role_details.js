// Retrieving and populating required skills for selected role (dom)

var role_details = JSON.parse(sessionStorage.getItem('role_details'));
console.log(role_details)
var ljpsr_role_id = role_details.ljps_role.ljpsr_id;

var role_name_div = document.getElementById('rolename');

var role_details_div = document.getElementById('roledetails');

var role_skills_list = document.getElementById('role_skills');



var rname = role_details.ljps_role.role_title;
var rdeet = role_details.ljps_role.role_desc;
var skills = role_details.skills;

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

console.log(ljpsr_role_id);

function confirmCreateLJ(){
    sessionStorage.setItem('ljpsr_role_id', ljpsr_role_id);
    var staff_role = sessionStorage.getItem('staff_role');
    console.log(staff_role);
    if (staff_role == 1){
        location.href = '../hr/choose_LJ_courses.html';
    }
    if(staff_role == 2){
        location.href = '../staff/choose_LJ_courses.html';
    }
    if(staff_role == 3){
        location.href = '../manager/choose_LJ_courses.html';
    }
}