var manager_id = sessionStorage.getItem('staff_id');
var manager_dept = sessionStorage.getItem('dept');
var contentdiv = document.getElementById('teamcont');
var searchdiv = document.getElementById('myUL');
console.log(manager_id);
$(async () => {
    console.log(manager_id);
    var serviceURL = "http://127.0.0.1:5001/get_team_members/" + manager_id
    console.log(serviceURL);
    try {
        const response = await fetch(serviceURL, { mode: "cors", method: "GET" });
        const result = await response.json();
        if (result) {
            var data = result.team_members;
            if (data == []){
                contentdiv.innerHTML = `<div class='emptyTeam'>There is currently no statistics for your team.</div>`
            }
            else{
                var content = ``;
                for (var idx in data){
                    var staff_details = data[idx];

                    // staff's details all here 
                    var staff_name = staff_details['staff_name'];
                    var course_complete = staff_details['courses_completed_count'];
                    var course_ongoing = staff_details['courses_ongoing_count'];
                    var skill_acquired = staff_details['skill_acquired_count'];
                    var skill_ongoing = staff_details['skill_ongoing_count'];
                    var staff_dept = staff_details['dept'];
                    var staff_id = staff_details['staff_id'];

                    // add staff name into the search bad 
                    searchdiv.innerHTML += `<li><a href='#${staff_id}'>${staff_name}</a></li>`;

                    // first staff in row 
                    if (idx == 0 || idx % 3 == 0){
                        content += `
                            <div class="row teamrow">
                                <button class="col-sm-4 individ" id=${staff_id} onclick='showStaffProgress(this.id)'>
                                    <div class="individualcard">
                                        <div class="personname">${staff_name}</div>
                                        <div class="personrole">${staff_dept}</div>
                                        <div class="courses">
                                            Courses:
                                        </div>
                                        <div class="container-fluid">
                                            <div class="row">
                                                <div class="col divi">
                                                    <div class="num">
                                                        ${course_ongoing}
                                                    </div>
                                                    <div class="title">
                                                        Ongoing
                                                    </div>
                                                </div>
                                                <div class="col ">
                                                    <div class="num">
                                                        ${course_complete}
                                                    </div>
                                                    <div class="title">
                                                        Completed
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                        <div class="skills">
                                            Skills:
                                        </div>
                                        <div class="container-fluid">
                                            <div class="row">
                                                <div class="col divi">
                                                    <div class="num">
                                                        ${skill_ongoing}
                                                    </div>
                                                    <div class="title">
                                                        Ongoing
                                                    </div>
                                                </div>
                                                <div class="col">
                                                    <div class="num">
                                                        ${skill_acquired}
                                                    </div>
                                                    <div class="title">
                                                        Acquired
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </button>
                        `;
                    };

                    // second staff in row 
                    if(idx == 1 || (idx-1) % 3 == 0){
                        content+= `
                            <button class="col-sm-4 individ" id=${staff_id} onclick='showStaffProgress(this.id)'>
                                <div class="individualcard">
                                    <div class="personname">${staff_name}</div>
                                    <div class="personrole">${staff_dept}</div>
                                    <div class="courses">
                                        Courses:
                                    </div>
                                    <div class="container-fluid">
                                        <div class="row">
                                            <div class="col divi">
                                                <div class="num">
                                                    ${course_ongoing}
                                                </div>
                                                <div class="title">
                                                    Ongoing
                                                </div>
                                            </div>
                                            <div class="col ">
                                                <div class="num">
                                                    ${course_complete}
                                                </div>
                                                <div class="title">
                                                    Completed
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="skills">
                                        Skills:
                                    </div>
                                    <div class="container-fluid">
                                        <div class="row">
                                            <div class="col divi">
                                                <div class="num">
                                                    ${skill_ongoing}
                                                </div>
                                                <div class="title">
                                                    Ongoing
                                                </div>
                                            </div>
                                            <div class="col">
                                                <div class="num">
                                                    ${skill_acquired}
                                                </div>
                                                <div class="title">
                                                    Acquired
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </button>
                        `;
                    }


                    // third staff in row 
                    if (idx == 2 || (idx-2) % 3 == 0 ){
                        content += `
                                <button class="col-sm-4 individ" id=${staff_id} onclick='showStaffProgress(this.id)'>
                                    <div class="individualcard">
                                        <div class="personname">${staff_name}</div>
                                        <div class="personrole">${staff_dept}</div>
                                        <div class="courses">
                                            Courses:
                                        </div>
                                        <div class="container-fluid">
                                            <div class="row">
                                                <div class="col divi">
                                                    <div class="num">
                                                        ${course_ongoing}
                                                    </div>
                                                    <div class="title">
                                                        Ongoing
                                                    </div>
                                                </div>
                                                <div class="col ">
                                                    <div class="num">
                                                        ${course_complete}
                                                    </div>
                                                    <div class="title">
                                                        Completed
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                        <div class="skills">
                                            Skills:
                                        </div>
                                        <div class="container-fluid">
                                            <div class="row">
                                                <div class="col divi">
                                                    <div class="num">
                                                        ${skill_ongoing}
                                                    </div>
                                                    <div class="title">
                                                        Ongoing
                                                    </div>
                                                </div>
                                                <div class="col">
                                                    <div class="num">
                                                        ${skill_acquired}
                                                    </div>
                                                    <div class="title">
                                                        Acquired
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </button>
                            </div>
                        `;
                    }
                }

                contentdiv.innerHTML += content;
            }
    
       } 
    }
    catch (error) {
        console.log(error);
        console.log("error");
    }
});


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

function showStaffProgress(staff_id){
    sessionStorage.setItem('view_staff', staff_id);
    location.href = './view_staff_progress.html';
}