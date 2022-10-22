// var learning_journeys = {
//     "data": [
//       {
//         "courses": [
//           {
//             "course_category": "Business", 
//             "course_desc": "discover foundational project management terminology", 
//             "course_id": "COURSE2", 
//             "course_name": "Foundations of Project Management", 
//             "course_status": 0, 
//             "course_type": "Internal"
//           }, 
//           {
//             "course_category": "Business", 
//             "course_desc": "be better at writing emails", 
//             "course_id": "COURSE4", 
//             "course_name": "Writing & Reasoning", 
//             "course_status": 0, 
//             "course_type": "Internal"
//           }
//         ], 
//         "journey_id": 2, 
//         "ljpsr_id": 2, 
//         "role_desc": "Project managers are accountable for planning and allocating resources, preparing budgets, monitoring progress, and keeping stakeholders informed throughout the project lifecycle", 
//         "role_title": "Project Manager", 
//         "skills": [
//           {
//             "skill_desc": "Project management is the process of leading the work of a team to achieve all project goals within the given constraints", 
//             "skill_id": 3, 
//             "skill_name": "Project Management", 
//             "status": 0
//           }, 
//           {
//             "skill_desc": "how to talk like businessman and woman", 
//             "skill_id": 7, 
//             "skill_name": "Business Communication", 
//             "status": 0
//           }
//         ], 
//         "staff_id": 1, 
//         "status": 0
//       }, 
//       {
//         "courses": [
//           {
//             "course_category": "Business", 
//             "course_desc": "you learn business strategy", 
//             "course_id": "COURSE1", 
//             "course_name": "Business Strategy", 
//             "course_status": 1, 
//             "course_type": "Internal"
//           }, 
//           {
//             "course_category": "Finance", 
//             "course_desc": "financial statements and more!", 
//             "course_id": "COURSE3", 
//             "course_name": "Accounting Fundamentals", 
//             "course_status": 0, 
//             "course_type": "Internal"
//           }
//         ], 
//         "journey_id": 3, 
//         "ljpsr_id": 1, 
//         "role_desc": "Accountants are responsible for financial audits, reconciling bank statements, and ensuring financial records are accurate throughout the year.", 
//         "role_title": "Accountant", 
//         "skills": [
//           {
//             "skill_desc": "Researching an organization and its working environment to formulate a strategy", 
//             "skill_id": 1, 
//             "skill_name": "Strategic Analysis", 
//             "status": 1
//           }, 
//           {
//             "skill_desc": "A set of tools and calculations used in determining whether a system meets certain specification requirements", 
//             "skill_id": 2, 
//             "skill_name": "Capabilities Analysis", 
//             "status": 1
//           }, 
//           {
//             "skill_desc": "beginner level accounting things", 
//             "skill_id": 6, 
//             "skill_name": "Accounting (Basics)", 
//             "status": 0
//           }
//         ], 
//         "staff_id": 1, 
//         "status": 0
//       }
//     ]
//   }


var ljpaths = JSON.parse(sessionStorage.getItem('learning_journeys'));
// console.log(ljpaths[0]); 

var courses_div = document.getElementById('courses_in_LJ');
var courseCount = 1;

var active = sessionStorage.getItem('activeLJ');
console.log(active);

function showpath(pathid){
    var original = document.getElementById(active);
    // console.log(original);

    // to chance colour 
    original.classList.remove('activepath');
    var originalprogress = document.getElementById('progressbar'+active);
    originalprogress.style.backgroundColor= '#9E82CA';
    var newpath = document.getElementById(pathid);
    newpath.classList.add('activepath');
    var newprogress = document.getElementById('progressbar'+pathid);
    newprogress.style.backgroundColor= '#FFA0A0';
    active = pathid;
    sessionStorage.removeItem('activeLJ');
    sessionStorage.setItem('activeLJ', active);

    // clear current course_div
    courses_div.innerHTML = ``;
    
    // find chosen ljpath...
    for (var paths_idx in ljpaths){
        var paths = ljpaths[paths_idx];
        var path_journey_id = paths['journey_id'];

        if (path_journey_id == pathid){
            var chosen_path_courses = paths['courses'];
            var new_course_content = ``;

            for (var newPath_course_idx in chosen_path_courses){
                var new_course_details = chosen_path_courses[newPath_course_idx];
                var new_course_name = new_course_details['course_name'];
                var new_iscomplete = new_course_details['course_status'];

                // course not completed 
                if (new_iscomplete == 0){
                    if (newPath_course_idx == 0 || newPath_course_idx % 2 == 0){
                        new_course_content += `
                        <div class="row">
                            <div class="col-sm-6 module">
                                <div class="container-fluid course">
                                    <div class="row courseinfo">
                                        <div class="col-sm-2">
                                            <img src="../img/leadership.png" alt="">
                                        </div>
                                        <div class="col-sm-6 courseName" id="courseName">
                                            ${new_course_name}
                                        </div>
                                        <div class="col-sm-4 courseNotComplete" id="notcomplete">
                                            In Progress
                                        </div>
                                    </div>
                                </div>                        
                            </div>`;
                    }
                    else{
                        new_course_content += `
                            <div class="col-sm-6 module">
                                <div class="container-fluid course">
                                    <div class="row courseinfo">
                                        <div class="col-sm-2">
                                            <img src="../img/comm.png" alt="">
                                        </div>
                                        <div class="col-sm-6 courseName" id="courseName">
                                            ${new_course_name}
                                        </div>
                                        <div class="col-sm-4 courseNotComplete" id="notcomplete">
                                            In Progress
                                        </div>
                                    </div>
                                </div>                        
                            </div>
                        </div>` 
                    }                    
                }

                // course completed (iscomplete == 1)
                else{
                    if (newPath_course_idx == 0 || newPath_course_idx % 2 == 0){
                        new_course_content += `
                        <div class="row">
                            <div class="col-sm-6 module">
                                <div class="container-fluid course">
                                    <div class="row courseinfo">
                                        <div class="col-sm-2">
                                            <img src="../img/leadership.png" alt="">
                                        </div>
                                        <div class="col-sm-6 courseName" id="courseName">
                                            ${new_course_name}
                                        </div>
                                        <div class="col-sm-4 courseComplete" id="complete">
                                            Completed
                                        </div>
                                    </div>
                                </div>                        
                            </div>`;
                    }
                    else{
                        new_course_content += `
                            <div class="col-sm-6 module">
                                <div class="container-fluid course">
                                    <div class="row courseinfo">
                                        <div class="col-sm-2">
                                            <img src="../img/comm.png" alt="">
                                        </div>
                                        <div class="col-sm-6 courseName" id="courseName">
                                            ${new_course_name}
                                        </div>
                                        <div class="col-sm-4 courseComplete" id="complete">
                                            Completed
                                        </div>
                                    </div>
                                </div>                        
                            </div>
                        </div>` 
                    } 
                }

                if(courseCount == 1){
                    courseCount+=1;
                }                
                else{
                    courseCount == 1;
                }
            }
            if (courseCount == 2){
                new_course_content += `<div class=col-sm-6></div>`;
            } 
            courses_div.innerHTML += new_course_content;
        }
        

    }


}
