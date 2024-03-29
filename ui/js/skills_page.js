function editSkill(skill_id){
    sessionStorage.setItem('edit_skill_id', skill_id);
    location.href = './edit_skill.html';
}

$(async () => {
    var serviceURL = "http://127.0.0.1:5001/get_all_skills_and_courses_hr"

    try {
        const response =
            await fetch(
            serviceURL, { mode: 'cors', method: 'GET' }
        );
        // console.log(response)
        const result = await response.json();
        // console.log(result.data)
        if(result) {
            var allskills = []

            // console.log(result.data)
            all_skills = result.data
            all_skills = all_skills.skills;
            // console.log(all_skills);

            var searchdiv = document.getElementById('myUL');
            var skillsdiv = document.getElementById('existingSkills');
            var skilldiv_content = ``;
            

            for (var skill_idx in all_skills){
                var skill = all_skills[skill_idx];

                var skill_name = skill['skill_name'];
                var skill_desc = skill['skill_desc'];
                var skill_id = skill['skill_id'];
                var active = skill['active'];
                var skill_courses = skill['courses'];
                var course_content = ``;
                allskills.push(skill_name);
                

                searchdiv.innerHTML += `<li><a href="#${skill_name}">${skill_name}</a></li>`;

                for (var course_idx in skill_courses){
                    var course = skill_courses[course_idx];
                    var course_name = course['course_name'];
                    course_content += `<li class='skill_desc_text'>${course_name}</li>`;
                }

                if (active == 1){
                    skilldiv_content += `
                        <div class="accordion-item" id="${skill_name}">
                            <div class="container-fluid">
                                <div class="row">
                                    <div class="col-sm-8">
                                        <div id="skill-head-1">
                                            <button class="accordion-button collapsed skillTitle" type="button" data-bs-toggle="collapse" data-bs-target="#skill-${skill_id}" aria-expanded="false" aria-controls="panelsStayOpen-collapseTwo">
                                                ${skill_name}   
                                            </button>
                                        </div>
                                    </div>
                                    <button class="col-6 col-md-2 editskill" id="${skill_id}" onclick="editSkill(this.id)">
                                        Edit
                                    </button>
                                    
                                    <div class="col-6 col-md-2 isactivediv">
                                        <select class="form-select" name='${skill_id}/${skill_name}' onchange='deleteskill(this)' aria-label="Default select example">
                                            <option value="1" selected>Active</option>
                                            <option value="0">Inactive</option>
                                        </select>
                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col">
                                        <div id="skill-${skill_id}" class="accordion-collapse collapse" aria-labelledby="skill-${skill_id}">
                                            <div class="accordion-body">
                                                <div class='skill_desc_title'>
                                                    Description: 
                                                </div>
                                                <div class='skill_desc_text'>
                                                    ${skill_desc}
                                                </div>
                                                <div class='skill_desc_title'>
                                                    Courses:
                                                </div>
                                                <div class='skill_desc_text'>
                                                    <ul>
                                                        ${course_content}
                                                    </ul>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    `;
                }

                else{
                    skilldiv_content += `
                        <div class="accordion-item" id="${skill_name}">
                            <div class="container-fluid">
                                <div class="row">
                                    <div class="col-sm-8">
                                        <div id="skill-head-1">
                                            <button class="accordion-button collapsed skillTitle" type="button" data-bs-toggle="collapse" data-bs-target="#skill-${skill_id}" aria-expanded="false" aria-controls="panelsStayOpen-collapseTwo">
                                                ${skill_name}   
                                            </button>
                                        </div>
                                    </div>
                                    <button class="col-6 col-md-2 editskill" id="${skill_id}" onclick="editSkill(this.id)">
                                        Edit
                                    </button>
                                    <div class="col-6 col-md-2 isactivediv">
                                        <select class="form-select" name='${skill_id}/${skill_name}' onchange='deleteskill(this)' aria-label="Default select example">
                                            <option value="1">Active</option>
                                            <option value="0" selected>Inactive</option>
                                        </select>
                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col">
                                        <div id="skill-${skill_id}" class="accordion-collapse collapse" aria-labelledby="skill-${skill_id}">
                                            <div class="accordion-body">
                                                <div class='skill_desc_title'>
                                                    Description: 
                                                </div>
                                                <div class='skill_desc_text'>
                                                    ${skill_desc}
                                                </div>
                                                <div class='skill_desc_title'>
                                                    Courses:
                                                </div>
                                                <div >
                                                    <ul>
                                                        ${course_content}
                                                    </ul>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    `;
                }


            }

            skillsdiv.innerHTML += skilldiv_content;

            sessionStorage.setItem('allskills', allskills);
        }
        

    } catch (error) {
        console.log(error)
        console.log('error')
    }
})

function searchRole() {
    var input, filter, ul, li, a, i, txtValue;
    input = document.getElementById("roleName");
    filter = input.value.toUpperCase();
    ul = document.getElementById("myUL");
    ul.style.display='inline';
    li = ul.getElementsByTagName("li");
    console.log(filter);
    console.log(filter.length);

    if(filter.length == 0){
        ul.style.display = 'none';
    }
    else{

        for (i = 0; i < li.length; i++) {
            a = li[i].getElementsByTagName("a")[0];
            txtValue = a.textContent || a.innerText;
            if (txtValue.toUpperCase().indexOf(filter) > -1) {
                li[i].style.display = "";
            } else {
                li[i].style.display = "none";
            }
        }
    }
}

var erroralert = document.getElementById('alerts');
erroralert.innerHTML = ``;
var count = 100;
function deleteskill(activeCheck){
    var skilldeets = activeCheck.name;
    var skill_id = skilldeets.split('/')[0];
    var skill_name = skilldeets.split('/')[1];
    var isactive = activeCheck.value;
    // insert backend here to delete skill (jann)

    $(async () => {
        
        var serviceURL = "http://127.0.0.1:5001/delete_skill/" + skill_id + "&" + isactive + "&" + skill_name

        try {
            const response = 
                await fetch(
                    serviceURL, {mode: 'cors', method: 'GET'}
                ); 

            const result = await response.json()

            if (result) {
                console.log('User data retrieved.')
                new_skill_details = JSON.stringify(result.data)

                var message = result.message; 
                erroralert.style.display = 'block';
                    count += 1;
                    erroralert.innerHTML += `
                        <div class="alert position-relative " id="${count}"> 
                            <span class="closebtn" onclick="this.parentElement.style.display='none';">&times;</span>
                            <div class="alert-header">
                                <img src="../img/webicon.png" width="10%" class="rounded me-2" alt="...">
                                <strong class="me-auto">LJPS</strong>
                                <small></small>
                                
                            </div>
                            <div class="alert-body">
                                ${message}
                            </div>
                        </div>`;
            }
        } catch (error) {
            console.log(error)
            console.log('error')
            erroralert.innerHTML += `
                    <div class="alert position-relative " id="alert"> 
                        <span class="closebtn" onclick="this.parentElement.style.display='none';">&times;</span>
                        <div class="alert-header">
                            <img src="../img/webicon.png" width="10%" class="rounded me-2" alt="...">
                            <strong class="me-auto">LJPS</strong>
                            <small></small>
                            
                        </div>
                        <div class="alert-body">
                            ${error}
                        </div>
                    </div>`;
        }
    })
    // setTimeout(function() {
    //     var div = document.getElementById(count);
    //     console.log(div);
    //     div.style.display ='none';
    // }, 1500);
}