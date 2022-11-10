$(async () => {
    var serviceURL = "http://127.0.0.1:5001/courses"

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
            all_courses = result.data
            // console.log(all_skills);
            var searchdiv = document.getElementById('myUL');
            var coursediv = document.getElementById('allCourses');
            var courseinput = ``


            for (var course_idx in all_courses){
                var course = all_courses[course_idx];
                var course_name = course.course_name;
                var course_id = course.course_id;
                // console.log(course_name);
                // console.log(course_id);

                // add course into search 
                searchdiv.innerHTML += `<li><a href='#${course_id}'>${course_name}</a></li>`;

                if (course_idx == 0 ||course_idx%2==0){
                    courseinput += `
                        <div class='row courserow'>
                            <div class='col-sm-6 coursename form-check' id=${course_id}>
                                <input class='form-check-input courseName' type='checkbox' id=${course_id}  name='courses' value =${course_id}>
                                ${course_name}
                            </div>
                        
                    `;
                }
                else{
                    courseinput += `
                            <div class='col-sm-6 coursename form-check' id=${course_id}>
                                <input class='form-check-input courseName' type='checkbox' id=${course_id} name='courses' value =${course_id}>
                                ${course_name}
                            </div>
                        </div>
                    `;
                }
            }
            coursediv.innerHTML += courseinput;
        
            console.log(searchdiv);
        }
        

    } catch (error) {
        console.log(error)
        console.log('error')
    }
})

function searchCourse() {
    var input, filter, ul, li, a, i, txtValue;
    input = document.getElementById("courseName");
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

var nameError = document.getElementById('nameError');
var descError = document.getElementById('descError');
var courseError = document.getElementById('courseError');


async function addCourse(){
    nameError.innerText = ``;
    descError.innerText = ``;
    courseError.innerText = ``;

    var serviceURL = "http://127.0.0.1:5001/create_skill"

    var new_name = document.getElementById('skill_name').value;
    var skill_name = new_name.trim(' ');
    var skill_desc = document.getElementById('skill_desc').value;
    var error = 0;
    const allChecked = document.querySelectorAll('input[name=courses]:checked');

    var newSkillCourses = Array.from(allChecked).map(checkbox => checkbox.value);
    console.log(newSkillCourses);

    if (skill_name == "") {
        nameError.innerText = `Skill name cannot be empty.`;
        error += 1 
    }

    if (skill_desc == "") {
        descError.innerText = `Skill description cannot be empty.`;
        error += 1 
    }

    if (newSkillCourses.length == 0) {
        courseError.innerText = `Please select at least one course to create the skill.`;
        error += 1 
    }

    if((skill_name != '') & (skill_desc != '') & (newSkillCourses.length > 0)) {
        sessionStorage.setItem('newSkillName', skill_name);
        sessionStorage.setItem('newSkillDesc', skill_desc);
        sessionStorage.setItem('newSkillCourses', newSkillCourses);

        try {
            const response = 
                await fetch(
                    serviceURL, 
                    {
                        mode: 'cors', method: 'POST', 
                        headers: {"Content-Type": "application/json"}, 
                        body: JSON.stringify({
                            "newSkillName": skill_name, 
                            "newSkillDesc": skill_desc, 
                            "newSkillCourses": JSON.stringify(newSkillCourses)
                        })
                    }
                );
            
            
            const result = await response.json(); 
            

            if (response.status == 201) {
                console.log("Skill created.")
            } else if (response.status === 401) {
                nameError.innerText = `The skill name ${skill_name} already exists.`;
                error += 1 
            }
            
        } 

        catch (error) {
            console.log(error)
            console.log("error")
        }
        
    }

    if (error > 0) {
        location.href = "#top";
        // alert("Errors have been found in creating the skill.");
        console.log(error);
    }
    else{
        console.log(error);
        var message = "The skill " + skill_name + " has been successfully created.";
        localStorage.setItem('errmessage', message);
        location.href = './skills_page.html';
    }
}