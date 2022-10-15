var edit_skill_id = sessionStorage.getItem('edit_skill_id');
var skill_name_div = document.getElementById('skill_name');
var skill_desc_div = document.getElementById('skill_desc');

// to add existing skill name and description into input field value 
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

           
            

            for (var skill_idx in all_skills){
                var skill = all_skills[skill_idx];

                var skill_name = skill['skill_name'];
                var skill_desc = skill['skill_desc'];
                var skill_id = skill['skill_id'];

                if (skill_id == edit_skill_id){
                    // console.log(skill_id);
                    // console.log(edit_skill_id);

                    skill_name_div.value = skill_name;
                    skill_desc_div.value = skill_desc;
                }

            }

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
    // console.log(filter);
    // console.log(filter.length);

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

// to add all courses available into div
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
                            <div class='col-sm-6 coursename form-check' id='course${course_id}'>
                                <input class='form-check-input courseName' type='checkbox' id=${course_id} onchange="handleChange(this)"  name='courses' value =${course_id}>
                                ${course_name}
                            </div>
                        
                    `;
                }
                else{
                    courseinput += `
                            <div class='col-sm-6 coursename form-check' id='course${course_id}'>
                                <input class='form-check-input courseName' type='checkbox' id=${course_id} onchange="handleChange(this)"  name='courses' value =${course_id}>
                                ${course_name}
                            </div>
                        </div>
                    `;
                }
            }
            // console.log(skillinput);
            coursediv.innerHTML += courseinput;
        
            // console.log(searchdiv);
        }
        

    } catch (error) {
        console.log(error)
        console.log('error')
    }
})


$(async () =>{
    var serviceURL = "http://127.0.0.1:5001//get_courses_by_skill/" + edit_skill_id

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
            var courses = result.data.courses;
            // console.log(courses);

            for (var course_idx in courses){
                // console.log(course_idx);
                var course = courses[course_idx];
                var course_id = course['course_id'];
                var course_checkbox = document.getElementById(course_id);
                // console.log(course_checkbox); 
                course_checkbox.checked = true;
            }

        }
        

    } catch (error) {
        console.log(error)
        console.log('error')
    }
})
