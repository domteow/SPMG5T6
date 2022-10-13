$(async () => {
    // JANN PLEASE CHECK serviceURL
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
            // JANN PLEASE CHECK THAT THE console.log(result.data) WORKS AND IS CORRECT OUTPUT THANKS 
            // THE REST DONT NEED DO
            // console.log(result.data)
            all_courses = result.data
            all_courses = all_courses.courses;
            // console.log(all_skills);
            var searchdiv = document.getElementById('myUL');
            var coursediv = document.getElementById('allCourses');
            var courseinput = ``


            for (var course_idx in all_courses){
                var course = all_courses[course_idx];
                var course_name = course.course_name;
                var course_id = course.course_id;

                // add skill into search 
                searchdiv.innerHTML += `<li><a href='#'${course_id}>${course_name}</a></li>`;

                if (course_idx == 0 || skill_idx%2==0){
                    courseinput += `
                        <div class='row courserow'>
                            <div class='col-sm-6 coursename form-check' id=${course_id}>
                                <input class='form-check-input courseName' type='checkbox' id=${course_id} onchange="handleChange(this)"  name='courses' value =${course_id}>
                                ${course_name}
                            </div>
                        
                    `;
                }
                else{
                    courseinput += `
                            <div class='col-sm-6 coursename form-check' id=${course_id}>
                                <input class='form-check-input courseName' type='checkbox' id=${course_id} onchange="handleChange(this)"  name='courses' value =${course_id}>
                                ${course_name}
                            </div>
                        </div>
                    `;
                }
            }
            // console.log(skillinput);
            coursediv.innerHTML += courseinput;
        
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

function addCourse(){
    var skill_name = document.getElementById('skill_name').value;
    console.log(skill_name);
    var skill_desc = document.getElementById('skill_desc').value;
    console.log(skill_desc);

    const allChecked = document.querySelectorAll('input[name=courses]:checked');

    var newSkillCourses = Array.from(allChecked).map(checkbox => checkbox.value);
    console.log(newSkillCourses);
    if(newSkillCourses.length == 0) {
        alert("Please select at least one course to create your learning journey.")
    }
    else {
        sessionStorage.setItem('newSkillName', skill_name);
        sessionStorage.setItem('newSkillDesc', skill_desc);
        sessionStorage.setItem('newSkillCourses', newSkillCourses);

        // var staff_role = sessionStorage.getItem('staff_role');
        // console.log(staff_role);
        
        location.href = './edit_skills.html';
    }

}