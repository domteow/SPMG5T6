window.onload = function(){
    if(!window.location.hash) {
		window.location = window.location + '#loaded';
		window.location.reload();
	}
}

var ljpaths_div = document.getElementById('ljpaths');
var courses_div = document.getElementById('courses_in_LJ');
var courseCount = 1;
var staff_id = sessionStorage.getItem('staff_id');
var count = 1;
var first_slide = true;

var full_name = sessionStorage.getItem('full_name');
console.log(full_name);
document.getElementById('hiuser').innerHTML = 'Hi, ' + full_name;


// the data is placed in learning_journeys 
$(async () => {
    var serviceURL = "http://127.0.0.1:5001/readlj/" + staff_id

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
            learning_journeys = result.data
            // console.log(learning_journeys)
            sessionStorage.setItem('learning_journeys', JSON.stringify(learning_journeys));

            var firstLJ = learning_journeys[0];

            // this entire chunk is to display the learning journey 
            

            for (var lj_index in learning_journeys){
                // console.log(count);
                // console.log(first_slide);
                var lj_arr = learning_journeys[lj_index];
                // console.log(lj_arr);
                var journey_id = lj_arr['journey_id'];
                var role_title = lj_arr['role_title'];
                console.log(lj_index);
                if (first_slide){
                    if (lj_index==0 || lj_index%3==0){
                        // first_slide == true, count == 1, means this is the first learning journey shown = auto checked
                        sessionStorage.setItem('activeLJ', journey_id);
                        var content = `
                        <div class="carousel-item active">
                            <div class="container caroucontainer">
                                <div class="row">
                                    <div class="col">
                                        <a href="#">
                                            <div class="learningjourney activepath" id=${journey_id} onclick="showpath(this.id)">
                                                <div class="title">
                                                    <img src="../img/pathicon.png" alt=""> ${role_title}
                                                </div>
                                                <div class="progresstitle">
                                                    Progess:
                                                </div>
                                                <div class="progress" id="pathprogress">
                                                    <div class="progress-bar activeprogress" role="progressbar" id="progressbar${journey_id}" style="width: 77%" aria-valuenow="25" aria-valuemin="0" aria-valuemax="100"></div>
                                                </div>
                                            </div>
                                        </a>
                                    </div>
                        `;
                    }
                    if (lj_index==2 || (lj_index-2)%3==0){
                        content += `
                                    <div class="col">
                                        <a href="#">
                                            <div class="learningjourney" id=${journey_id} onclick="showpath(this.id)">
                                                <div class="title">
                                                    <img src="../img/pathicon.png" alt=""> ${role_title}
                                                </div>
                                                <div class="progresstitle">
                                                    Progess:
                                                </div>
                                                <div class="progress" id="pathprogress">
                                                    <div class="progress-bar" role="progressbar" id="progressbar${journey_id}" style="width: 77%" aria-valuenow="25" aria-valuemin="0" aria-valuemax="100"></div>
                                                </div>
                                            </div>
                                        </a>
                                    </div>
                                </div>
                            </div>
                        </div>                        
                        `;
                    }
                    if (lj_index == 1 || (lj_index-4)%3==0){
                        content += `
                        <div class="col">
                            <a href="#">
                                <div class="learningjourney" id=${journey_id} onclick="showpath(this.id)">
                                    <div class="title">
                                        <img src="../img/pathicon.png" alt=""> ${role_title}
                                    </div>
                                    <div class="progresstitle">
                                        Progess:
                                    </div>
                                    <div class="progress" id="pathprogress">
                                        <div class="progress-bar" role="progressbar" id="progressbar${journey_id}" style="width: 77%" aria-valuenow="25" aria-valuemin="0" aria-valuemax="100"></div>
                                    </div>
                                </div>
                            </a>
                        </div>
                        `;
                    }
                    // first_slide = false;
                    if (count <3){
                        count += 1;
                    }
                    else{
                        count == 0;
                        first_slide = false;
                    }
                }

                // not first slide 
                else{
                    // console.log(count);
                    // console.log(first_slide);
                    if (lj_index==0 || lj_index%3==0){
                        content += `
                        <div class="carousel-item">
                            <div class="container caroucontainer">
                                <div class="row">
                                    <div class="col">
                                        <a href="#">
                                            <div class="learningjourney" id=${journey_id} onclick="showpath(this.id)">
                                                <div class="title">
                                                    <img src="../img/pathicon.png" alt=""> ${role_title}
                                                </div>
                                                <div class="progresstitle">
                                                    Progess:
                                                </div>
                                                <div class="progress" id="pathprogress">
                                                    <div class="progress-bar" role="progressbar" id="progressbar${journey_id}" style="width: 77%" aria-valuenow="25" aria-valuemin="0" aria-valuemax="100"></div>
                                                </div>
                                            </div>
                                        </a>
                                    </div>
                        `;
                        // count += 1;
                    }
                    if (lj_index==2 || (lj_index-2)%3==0){
                        content += `
                                    <div class="col">
                                        <a href="#">
                                            <div class="learningjourney" id=${journey_id} onclick="showpath(this.id)">
                                                <div class="title">
                                                    <img src="../img/pathicon.png" alt=""> ${role_title}
                                                </div>
                                                <div class="progresstitle">
                                                    Progess:
                                                </div>
                                                <div class="progress" id="pathprogress">
                                                    <div class="progress-bar" role="progressbar" id="progressbar${journey_id}" style="width: 77%" aria-valuenow="25" aria-valuemin="0" aria-valuemax="100"></div>
                                                </div>
                                            </div>
                                        </a>
                                    </div>
                                </div>
                            </div>
                        </div>
                        `;
                    }
                    if (lj_index==1 || (lj_index-4)%3==0){
                        content += `
                        <div class="col">
                            <a href="#">
                                <div class="learningjourney" id=${journey_id} onclick="showpath(this.id)">
                                    <div class="title">
                                        <img src="../img/pathicon.png" alt=""> ${role_title}
                                    </div>
                                    <div class="progresstitle">
                                        Progess:
                                    </div>
                                    <div class="progress" id="pathprogress">
                                        <div class="progress-bar" role="progressbar" id="progressbar${journey_id}" style="width: 77%" aria-valuenow="25" aria-valuemin="0" aria-valuemax="100"></div>
                                    </div>
                                </div>
                            </a>
                        </div>
                        `;
                    }
                }
            }
            // end of displaying the learning journey 


            var len = learning_journeys.length;
            console.log(len);
            var remainder = len % 3;

            if (remainder == 1) {
                content+= `<div class = 'col'></div><div class = 'col'></div>`;
            }

            if (remainder == 2){
                content +=`<div class = 'col'></div>`;
            }


            console.log(content);

            ljpaths_div.innerHTML += content;


            // ^ FINISH displaying the diff paths

            // to display the courses in the FIRST PATH 
            var firstcourses = firstLJ['courses']; // returns an array [] of courses and the details
            console.log(firstcourses);
            var coursecontent =``;

            for (var course_idx in firstcourses){
                console.log(course_idx);
                console.log(courseCount);
                var course_details = firstcourses[course_idx];
                var course_name = course_details['course_name'];
                var iscomplete = course_details['course_status'];
                

                // course not completed 
                if (iscomplete == 0){
                    if (course_idx == 0 || course_idx%2 == 0){
                        coursecontent += `
                        <div class="row">
                            <div class="col-sm-6 module">
                                <div class="container-fluid course">
                                    <div class="row courseinfo">
                                        <div class="col-sm-2">
                                            <img src="../img/leadership.png" alt="">
                                        </div>
                                        <div class="col-sm-6 courseName" id="courseName">
                                            ${course_name}
                                        </div>
                                        <div class="col-sm-4 courseNotComplete" id="notcomplete">
                                            In Progress
                                        </div>
                                    </div>
                                </div>                        
                            </div>`;
                    }
                    else{
                        coursecontent += `
                            <div class="col-sm-6 module">
                                <div class="container-fluid course">
                                    <div class="row courseinfo">
                                        <div class="col-sm-2">
                                            <img src="../img/comm.png" alt="">
                                        </div>
                                        <div class="col-sm-6 courseName" id="courseName">
                                            ${course_name}
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
                    if (course_idx == 0 || course_idx%2 == 0){
                        coursecontent += `
                        <div class="row">
                            <div class="col-sm-6 module">
                                <div class="container-fluid course">
                                    <div class="row courseinfo">
                                        <div class="col-sm-2">
                                            <img src="../img/leadership.png" alt="">
                                        </div>
                                        <div class="col-sm-6 courseName" id="courseName">
                                            ${course_name}
                                        </div>
                                        <div class="col-sm-4 courseComplete" id="complete">
                                            Completed
                                        </div>
                                    </div>
                                </div>                        
                            </div>`;
                    }
                    else{
                        coursecontent += `
                            <div class="col-sm-6 module">
                                <div class="container-fluid course">
                                    <div class="row courseinfo">
                                        <div class="col-sm-2">
                                            <img src="../img/comm.png" alt="">
                                        </div>
                                        <div class="col-sm-6 courseName" id="courseName">
                                            ${course_name}
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
                if(courseCount ==2) {
                    courseCount == 1;
                }
            }
            courses_div.innerHTML += coursecontent;  
            console.log(courses_div);            
        }
        

    } catch (error) {
        console.log(error)
        console.log('error')
    }
})