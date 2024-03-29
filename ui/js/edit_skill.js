var edit_skill_id = sessionStorage.getItem("edit_skill_id");
var allcurrskills = sessionStorage.getItem('allskills').split(',');

// to add existing skill name and description into input field value
$(async () => {

    var serviceURL = "http://127.0.0.1:5001/get_all_skills_and_courses_hr";

    try {
        const response = await fetch(serviceURL, { mode: "cors", method: "GET" });
        // console.log(response)
        const result = await response.json();
        // console.log(result.data)
        if (result) {
        // console.log(result.data)
        all_skills = result.data;
        all_skills = all_skills.skills;
        // console.log(all_skills);

            for (var skill_idx in all_skills) {
                var skill_name_div = document.getElementById("skill_name");
                var skill_desc_div = document.getElementById("skill_desc");
                var skill = all_skills[skill_idx];

                var skill_name = skill["skill_name"];
                var skill_desc = skill["skill_desc"];
                var skill_id = skill["skill_id"];


                if (skill_id == edit_skill_id) {
                // console.log(skill_id);
                // console.log(edit_skill_id);

                skill_name_div.value = skill_name;
                skill_desc_div.value = skill_desc;
                sessionStorage.setItem("curr_skill_name", skill_name);
                sessionStorage.setItem("curr_skill_desc", skill_desc);
                }
            }
        }
      } 
  catch (error) {
    console.log(error);
    console.log("error");
  }
});

function searchCourse() {
  var input, filter, ul, li, a, i, txtValue;
  input = document.getElementById("courseName");
  filter = input.value.toUpperCase();
  ul = document.getElementById("myUL");
  ul.style.display = "inline";
  li = ul.getElementsByTagName("li");
  // console.log(filter);
  // console.log(filter.length);

  if (filter.length == 0) {
    ul.style.display = "none";
  } else {
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
  if (cb.checked == true) {
    // to check all checkbox with the SAME ID -> course_id
    var cbox = `input[id=${cbval}]`;
    var allCB = document.querySelectorAll(cbox);
    for (var i = 0; i < allCB.length; i++) {
      allCB[i].checked = true;
    }
  } else {
    // to uncheck all checkbox
    var cbox = `input[id=${cbval}]`;
    var allCB = document.querySelectorAll(cbox);
    for (var i = 0; i < allCB.length; i++) {
      allCB[i].checked = false;
    }
  }
}

// to add all courses available into div
$(async () => {
  var serviceURL = "http://127.0.0.1:5001/courses";

  try {
    const response = await fetch(serviceURL, { mode: "cors", method: "GET" });
    
    const result = await response.json();
    
    if (result) {
      
      all_courses = result.data;
      
      var searchdiv = document.getElementById("myUL");
      var coursediv = document.getElementById("allCourses");
      var courseinput = ``;

      for (var course_idx in all_courses) {
        var course = all_courses[course_idx];
        var course_name = course.course_name;
        var course_id = course.course_id;

        // add course into search
        searchdiv.innerHTML += `<li><a href='#${course_id}'>${course_name}</a></li>`;

        if (course_idx == 0 || course_idx % 2 == 0) {
          courseinput += `
                                <div class='row courserow'>
                                    <div class='col-sm-6 coursename form-check' id='course${course_id}'>
                                        <input class='form-check-input courseName' type='checkbox' id=${course_id} onchange="handleChange(this)"  name='courses' value =${course_id}>
                                        ${course_name}
                                    </div>
                                
                            `;
        } else {
          courseinput += `
                                    <div class='col-sm-6 coursename form-check' id='course${course_id}'>
                                        <input class='form-check-input courseName' type='checkbox' id=${course_id} onchange="handleChange(this)"  name='courses' value =${course_id}>
                                        ${course_name}
                                    </div>
                                </div>
                            `;
        }
      }
      coursediv.innerHTML += courseinput;

    }
  } catch (error) {
    console.log(error);
    console.log("error");
  }
});

// to check checkboxes of existing courses under that skill
$(async () => {
  var serviceURL =
    "http://127.0.0.1:5001//get_courses_by_skill/" + edit_skill_id;

  try {
    const response = await fetch(serviceURL, { mode: "cors", method: "GET" });
    
    const result = await response.json();
    
    if (result) {
      var courses = result.data.courses;
      curr_courses = [];
      currcourses = JSON.stringify(courses);
      sessionStorage.setItem("curr_courses", currcourses);

      for (var course_idx in courses) {
        var course = courses[course_idx];
        var course_id = course["course_id"];
        var course_checkbox = document.getElementById(course_id);
        course_checkbox.checked = true;
      }
    }
  } catch (error) {
    console.log(error);
    console.log("error");
  }
});

var nameError = document.getElementById("nameError");
var descError = document.getElementById("descError");
var courseError = document.getElementById("courseError");

async function saveSkill() {
  var skill_id = sessionStorage.getItem("edit_skill_id");
  var curr_skill_name = sessionStorage.getItem("curr_skill_name");
  var curr_skill_desc = sessionStorage.getItem("curr_skill_desc");
  var curr_courses = sessionStorage.getItem("curr_courses");
  curr_courses = JSON.parse(curr_courses);
  var error_count = 0;

  nameError.innerText = ``;
  descError.innerText = ``;
  console.log(nameError);

  // SKILL NAME
  // get value of skill name from form and compare
  var new_name = document.getElementById("skill_name").value;
  var new_skill_name = new_name.trim(' ');
  console.log(new_skill_name);
  if (new_skill_name == "") {
    error_count += 1;
    nameError.innerText += `Skill name cannot be empty.`;
  }

  // SKILL DESCRIPTION
  // get value of skill desc from form and compare
  var new_skill_desc = document.getElementById("skill_desc").value;
  if (new_skill_desc == "") {
    error_count += 1;
    descError.innerText += `Skill description cannot be empty.`;
  }

  for (var skillidx in allcurrskills){
    var skill_name = allcurrskills[skillidx];
    console.log(skill_name);
    if (new_skill_name == skill_name && skill_name != curr_skill_name){
      error_count +=1;
      nameError.innerText += `The skill ${skill_name} already exists.`;
    }
  }

  // check if new skill name and new skill desc are not empty 
  if (nameError.innerText == '') {
    $(async () => {
      var serviceURL = "http://127.0.0.1:5001/edit_skill_details";

      try {
        const response = 
          await fetch(
            serviceURL, {mode: "cors", method: "POST",
            headers: {"Content-Type": "application/json", "Access-Controlled-Allow-Origin": '*'}, 
            body: JSON.stringify({
              "skill_id": skill_id, 
              "new_skill_name": new_skill_name,
              "new_skill_desc": new_skill_desc,
            })}); 
        
        const result = await response.json(); 

        if (result) {
          update_message = result.data
        }
      } catch (error) {
          console.log(error); 
          console.log("error")
      }
    })
  }

  // SKILL COURSES
  // get values of courses in skill from form and compare
  // var courseError = document.getElementById("courseError");
  const allChecked = document.querySelectorAll("input[name=courses]:checked");
  var checkedCourses = Array.from(allChecked).map((checkbox) => checkbox.value);
  // console.log(checkedCourses);
  courseError.innerText = ``;

  if (checkedCourses.length == 0) {
    error_count += 1;
    courseError.innerHTML += `You cannot remove all courses from this skill. Please select at least one course to be added under this skill. <br>`;
    // error_msg.push("Please select at least one course to be added under this skill.");
  } else {
    var added_courses = [];
    var deleted_courses = [];
    var curr_course_ids = [];

    // to store course ID of existing courses into curr_course_ids
    for (var curr_idx in curr_courses) {
      var curr_course = curr_courses[curr_idx];
      var curr_course_id = curr_course["course_id"];
      curr_course_ids.push(curr_course_id);
    }

    for (var new_idx in checkedCourses) {
      var new_id = checkedCourses[new_idx];
      // if new id is not in curr_course ->  save to added_courses
      if (!curr_course_ids.includes(new_id)) {
        added_courses.push(new_id);
      }
    }

    for (var old_idx in curr_course_ids) {
      var old_id = curr_course_ids[old_idx];
      // if old id not in checkedCourses -> save to deleted_courses
      if (!checkedCourses.includes(old_id)) {
        deleted_courses.push(old_id);
      }
    }

    if (added_courses.length > 0) {
      
      // to input backend to add course to skill
      let serviceURL = "http://127.0.0.1:5001/add_course_to_skill";
      try {
        const response = await fetch(serviceURL, {
          mode: "cors",
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            skill_id: skill_id,
            course_arr: added_courses,
          }),
        });
        console.log(response);
        let result = await response.json();
        console.log(result);
        if (result.code === 200) {
          console.log("Courses added successfully");
        }
      } catch (error) {
        error_count += 1;
        console.log(error);
        courseError.innerHTML += `Error during addition of course: ${error} <br>`;
        // alert(`Error during addition: ${error}`);
      }
    }

    if (deleted_courses.length > 0) {
      // to input backend to delete course from skill
      console.log(deleted_courses);
      let serviceURL = "http://127.0.0.1:5001/remove_course_from_skill";
      try {
        const response = await fetch(serviceURL, {
          mode: "cors",
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            skill_id: skill_id,
            course_arr: deleted_courses,
          }),
        });

        let result = await response.json();

        if (result.code === 200) {
          console.log("Courses removed successfully");
        }
      } catch (error) {
        error_count += 1;
        console.log(error);
        courseError.innerHTML += `Error during removal of course: ${error} <br>`;
        // alert(`Error during addition: ${error}`);
      }
    }
  }

  if (error_count == 0) {
    // alert("Your changes have been saved successfully!");
    var message = new_skill_name + ' has been edited';
    localStorage.setItem('errmessage', message);
    location.href = "./skills_page.html";
  } else {
    location.href = "#top";
    // alert("Errors have been found in page.");
  }
}

