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
            // console.log(skillinput);
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

// function handleChange(cb) {
//     var cbval = cb.id;
//     if(cb.checked == true) {
//         // to check all checkbox with the SAME ID -> course_id
//         var cbox = `input[id=${cbval}]`
//         var allCB = document.querySelectorAll(cbox);
//         for (var i=0; i< allCB.length; i++){
//             allCB[i].checked = true;
//         }
      
//     } else {
//         // to uncheck all checkbox
//         var cbox = `input[id=${cbval}]`
//         var allCB = document.querySelectorAll(cbox);
//         for (var i=0; i< allCB.length; i++){
//             allCB[i].checked = false;
//         }

//     }
// }

async function addCourse(){
    var serviceURL = "http://127.0.0.1:5001/create_skill"
    var skill_name = document.getElementById('skill_name').value;
    console.log(skill_name);
    var skill_desc = document.getElementById('skill_desc').value;
    console.log(skill_desc);

    const allChecked = document.querySelectorAll('input[name=courses]:checked');

    var newSkillCourses = Array.from(allChecked).map(checkbox => checkbox.value);
    console.log(newSkillCourses);

    if (skill_name == "") {
        alert("Skill name cannot be empty.")
    }

    else if (skill_desc == "") {
        alert("Skill description cannot be empty.")
    }

    else if (newSkillCourses.length == 0) {
        alert("Please select at least one course to create your learning journey.")
    }

    else {
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
            
            console.log(response)
            const result = await response.json(); 
            console.log(result)

            if (response.status == 201) {
                console.log("Skill created.")
                var message = "The skill " + skill_name + " has been successfully created.";
                localStorage.setItem('errmessage', message);
                location.href = './skills_page.html';
            } else if (response.status === 401) {
                alelrt("The skill name " + skill_name + " already exists.")
            }
            
        } 

        catch (error) {
            console.log(error)
            console.log("error")
        }
        
        // var staff_role = sessionStorage.getItem('staff_role');
        // console.log(staff_role);   
    }
}