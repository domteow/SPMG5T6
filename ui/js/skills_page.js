function editSkill(skill_id){
    sessionStorage.setItem('edit_skill_id', skill_id);
    location.href = './edit_skill.html';
}

$(async () => {
    var serviceURL = "http://127.0.0.1:5001/get_all_skills_and_courses"

    try {
        const response =
            await fetch(
            serviceURL, { mode: 'cors', method: 'GET' }
        );
        // console.log(response)
        const result = await response.json();
        // console.log(result.data)
        if(result) {
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
                                        <select class="form-select" aria-label="Default select example">
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
                                    <button class="col-sm-2 editskill" id="${skill_id}" onclick="editSkill(this.id)">
                                        Edit
                                    </button>
                                    <div class="col-sm-2 isactivediv">
                                        <select class="form-select" aria-label="Default select example">
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

