var ljpaths = JSON.parse(sessionStorage.getItem('learning_journeys'));
var staff_id =sessionStorage.getItem('staff_id')
// console.log(ljpaths[0]); 

var courses_div = document.getElementById('courses_in_LJ');
var courseCount = 1;

var active = sessionStorage.getItem('activeLJ');
console.log(active);

function showpath(pathid){
    var original = document.getElementById(active);
    console.log(original);

    // to chance colour 
    original.classList.remove('activepath');
    var originalprogress = document.getElementById('progressbar'+active);
    originalprogress.style.backgroundColor= '#9E82CA';
    console.log(original);
    var newpath = document.getElementById(pathid);
    console.log(newpath);
    newpath.classList.add('activepath');
    var newprogress = document.getElementById('progressbar'+pathid);
    newprogress.style.backgroundColor= '#FFA0A0';
    active = pathid;
    sessionStorage.removeItem('activeLJ');
    sessionStorage.setItem('activeLJ', active);

    // to change delete button 
    var deletebutton = document.getElementById('deletelj');
    deletebutton.innerHTML = `<div onclick='deleteLJ(this.id)' id='delete/${pathid}' class='deletelj'>Delete Learning Journey</div>`;

    // clear current course_div
    courses_div.innerHTML = ``;
    
    $(async () => {

        var serviceURL = "http://127.0.0.1:5001/get_courses_of_lj/" + staff_id + "&" + pathid
    
        try {
            const response = await fetch(serviceURL, { mode: "cors", method: "GET" });
            // console.log(response)
            const result = await response.json();
            // console.log(result.data)
            if (result) {
            // console.log(result.data)
            var chosen_path_courses = result.data
            var new_course_content = ``;
            
            for (var newPath_course_idx in chosen_path_courses){
                var new_course_details = chosen_path_courses[newPath_course_idx];
                var new_course_name = new_course_details['course_name'];
                var new_iscomplete = new_course_details['course_status'];

                // course not completed 
                if (new_iscomplete == 0){
                    if (newPath_course_idx == 0 || newPath_course_idx % 2 == 0){
                        new_course_content += `
                        <div class="row lrow">
                            <div class="col-sm-6 module">
                                <div class="container-fluid course">
                                    <div class="row courseinfo">
                                        <div class="col-2 clogo">
                                            <img src="../img/leadership.png" alt="">
                                        </div>
                                        <div class="col-6 courseName" id="courseName">
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
                                        <div class="col-2 clogo">
                                            <img src="../img/comm.png" alt="">
                                        </div>
                                        <div class="col-6 courseName" id="courseName">
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
                        <div class="row lrow">
                            <div class="col-sm-6 module">
                                <div class="container-fluid course">
                                    <div class="row courseinfo">
                                        <div class="col-2 clogo">
                                            <img src="../img/leadership.png" alt="">
                                        </div>
                                        <div class="col-6 courseName" id="courseName">
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
                                        <div class="col-2 clogo">
                                            <img src="../img/comm.png" alt="">
                                        </div>
                                        <div class="col-6 courseName" id="courseName">
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
      catch (error) {
        console.log(error);
        console.log("error");
      }
    });
    // find chosen ljpath...
    // for (var paths_idx in ljpaths){
    //     var paths = ljpaths[paths_idx];
    //     var path_journey_id = paths['journey_id'];

    //     if (path_journey_id == pathid){
    //         var chosen_path_courses = paths['courses'];
    //         var new_course_content = ``;

    //         for (var newPath_course_idx in chosen_path_courses){
    //             var new_course_details = chosen_path_courses[newPath_course_idx];
    //             var new_course_name = new_course_details['course_name'];
    //             var new_iscomplete = new_course_details['course_status'];

    //             // course not completed 
    //             if (new_iscomplete == 0){
    //                 if (newPath_course_idx == 0 || newPath_course_idx % 2 == 0){
    //                     new_course_content += `
    //                     <div class="row lrow">
    //                         <div class="col-sm-6 module">
    //                             <div class="container-fluid course">
    //                                 <div class="row courseinfo">
    //                                     <div class="col-sm-2">
    //                                         <img src="../img/leadership.png" alt="">
    //                                     </div>
    //                                     <div class="col-sm-6 courseName" id="courseName">
    //                                         ${new_course_name}
    //                                     </div>
    //                                     <div class="col-sm-4 courseNotComplete" id="notcomplete">
    //                                         In Progress
    //                                     </div>
    //                                 </div>
    //                             </div>                        
    //                         </div>`;
    //                 }
    //                 else{
    //                     new_course_content += `
    //                         <div class="col-sm-6 module">
    //                             <div class="container-fluid course">
    //                                 <div class="row courseinfo">
    //                                     <div class="col-sm-2">
    //                                         <img src="../img/comm.png" alt="">
    //                                     </div>
    //                                     <div class="col-sm-6 courseName" id="courseName">
    //                                         ${new_course_name}
    //                                     </div>
    //                                     <div class="col-sm-4 courseNotComplete" id="notcomplete">
    //                                         In Progress
    //                                     </div>
    //                                 </div>
    //                             </div>                        
    //                         </div>
    //                     </div>` 
    //                 }                    
    //             }

    //             // course completed (iscomplete == 1)
    //             else{
    //                 if (newPath_course_idx == 0 || newPath_course_idx % 2 == 0){
    //                     new_course_content += `
    //                     <div class="row lrow">
    //                         <div class="col-sm-6 module">
    //                             <div class="container-fluid course">
    //                                 <div class="row courseinfo">
    //                                     <div class="col-sm-2">
    //                                         <img src="../img/leadership.png" alt="">
    //                                     </div>
    //                                     <div class="col-sm-6 courseName" id="courseName">
    //                                         ${new_course_name}
    //                                     </div>
    //                                     <div class="col-sm-4 courseComplete" id="complete">
    //                                         Completed
    //                                     </div>
    //                                 </div>
    //                             </div>                        
    //                         </div>`;
    //                 }
    //                 else{
    //                     new_course_content += `
    //                         <div class="col-sm-6 module">
    //                             <div class="container-fluid course">
    //                                 <div class="row courseinfo">
    //                                     <div class="col-sm-2">
    //                                         <img src="../img/comm.png" alt="">
    //                                     </div>
    //                                     <div class="col-sm-6 courseName" id="courseName">
    //                                         ${new_course_name}
    //                                     </div>
    //                                     <div class="col-sm-4 courseComplete" id="complete">
    //                                         Completed
    //                                     </div>
    //                                 </div>
    //                             </div>                        
    //                         </div>
    //                     </div>` 
    //                 } 
    //             }

    //             if(courseCount == 1){
    //                 courseCount+=1;
    //             }                
    //             else{
    //                 courseCount == 1;
    //             }
    //         }
    //         if (courseCount == 2){
    //             new_course_content += `<div class=col-sm-6></div>`;
    //         } 
    //         courses_div.innerHTML += new_course_content;
        // }
        

    // }


}

// function to edit courses in learning journey (dom)
// click on edit learning journey button to use this
async function edit_LJ() {
    
    // use staff_id to retrieve ljpsr_id
    var serviceURL = "http://127.0.0.1:5001/readlj/" + Number(staff_id)

    try {
        const response =
            await fetch(
            serviceURL, { mode: 'cors', method: 'GET' }
        );
        // console.log(response)
        const result = await response.json();
        console.log(result.data)
        
        if(result) {
            console.log(result);

            var active_lj = sessionStorage.getItem('activeLJ');
            console.log(active_lj);

            for (LJ of result.data) {
                console.log(LJ)


                console.log(active);
                if(LJ.journey_id == active_lj) {
                    console.log(active)
                    var ljpsr_id = LJ.ljpsr_id
                    console.log(ljpsr_id)
                    sessionStorage.setItem('ljpsr_id',ljpsr_id)
                }
            }
           
        }
        

    } catch (error) {
        console.log(error)
        console.log('error')
    }



    var active_lj_id_now = sessionStorage.getItem('activeLJ');
    console.log(active_lj_id_now);
    sessionStorage.setItem('activeLJ', active_lj_id_now);

    var ljpsr_id_selected = sessionStorage.getItem('ljpsr_id');
    sessionStorage.setItem('edit_ljpsr_id', ljpsr_id_selected);

    sessionStorage.setItem('staff_id', staff_id)
    staff_role = sessionStorage.getItem('staff_role')
    if (staff_role == 1){
        location.href = './edit_LJ_courses.html';
    }
    if (staff_role == 2 || staff_role == 4){
        location.href = './edit_LJ_courses.html';
    }
    if(staff_role == 3){
        location.href = './edit_LJ_courses.html';
    }

    
}