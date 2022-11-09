var edit_role_id = sessionStorage.getItem('edit_role_id');
var allRoles = sessionStorage.getItem('allroles').split(',');
// console.log(allRoles);

// to get current role name and desc
$(async () => {
    var serviceURL = "http://127.0.0.1:5001/read_all_roles"

    try {
        const response =
            await fetch(
            serviceURL, { mode: 'cors', method: 'GET' }
        );
        // console.log(response)
        const result = await response.json();
        // console.log(result.data)
        if(result) {
            var all_roles = result.data;
            for (var role_idx in all_roles){
                var role_name_div = document.getElementById('role_name');
                var role_desc_div = document.getElementById('role_desc');

                var role = all_roles[role_idx];
                var role_name = role['role_title'];
                var role_desc = role['role_desc'];
                var role_id = role['ljpsr_id'];
                var role_skills = role['skills']

                if (role_id == edit_role_id){
                    sessionStorage.setItem('curr_role_name', role_name);
                    sessionStorage.setItem('curr_role_desc', role_desc);
                    sessionStorage.setItem('curr_role_skills', JSON.stringify(role_skills));

                    role_name_div.value = role_name;
                    role_desc_div.value = role_desc;
                }
            }
            // to add all skills available into div 
            $(async () => {
                var serviceURL = "http://127.0.0.1:5001/get_all_skills_and_courses";
            
                try {
                    const response = 
                        await fetch(
                            serviceURL, { mode: "cors", method: "GET" });
                    // console.log(response)
                    const result = await response.json();
                    // console.log(result.data)
                    if (result) {
                        // console.log(result.data)
                        all_skills = result.data.skills;
                        // console.log(all_skills);
                        var searchdiv = document.getElementById("myUL");
                        var skillsdiv = document.getElementById("allSkills");
                        var skillsinput = ``;
            
                        for (var skill_idx in all_skills) {
                            var skill = all_skills[skill_idx];
                            var skill_name = skill.skill_name;
                            var skill_id = skill.skill_id;
            
                            // add skill into search
                            searchdiv.innerHTML += `<li><a href='#${skill_id}'>${skill_name}</a></li>`;
            
                            if (skill_idx == 0 || skill_idx % 2 == 0) {
                            skillsinput += `
                                            <div class='row skillrow'>
                                                <div class='col-sm-6 skillname form-check' id='skill${skill_id}'>
                                                    <input class='form-check-input skillName' type='checkbox' id=${skill_id}  name='skills' value =${skill_id}>
                                                    ${skill_name}
                                                </div>
                                            
                                        `;
                            } else {
                            skillsinput += `
                                                <div class='col-sm-6 skillname form-check' id='skill${skill_id}'>
                                                    <input class='form-check-input skillName' type='checkbox' id=${skill_id} name='skills' value =${skill_id}>
                                                    ${skill_name}
                                                </div>
                                            </div>
                                        `;
                            }
                        }
                        // console.log(skillinput);
                        skillsdiv.innerHTML += skillsinput;
            
                        var curr_role_skills = sessionStorage.getItem('curr_role_skills');
                        curr_role_skills = JSON.parse(curr_role_skills);
                        var curr_skills_id = [];
            
                        for (var skill_idx in curr_role_skills){
                            var curr_skill = curr_role_skills[skill_idx];
                            var skill_id = curr_skill['skill_id'];
                            curr_skills_id.push(skill_id);
                            var skill_checkbox = document.getElementById(skill_id);
                            skill_checkbox.checked=true;
                        }
            
            
                        // console.log(curr_skills_id);
                        sessionStorage.setItem('curr_skill_ids', JSON.stringify(curr_skills_id));       
                        }
                    } catch (error) {
                        console.log(error);
                        console.log("error");
                } 
            });
        }
    }
    catch(error){
        console.log(error)
        console.log('error')
    }
})

function searchSkill() {
    var input, filter, ul, li, a, i, txtValue;
    input = document.getElementById("skillName");
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

var nameError = document.getElementById('nameError');
var descError = document.getElementById('descError');
var skillError = document.getElementById('skillError');

// function editRole(){
//     var role_id = sessionStorage.getItem('edit_role_id');
//     var curr_role_name = sessionStorage.getItem('curr_role_name');
//     var curr_role_desc = sessionStorage.getItem('curr_role_desc');
//     var curr_skill_ids = sessionStorage.getItem('curr_skill_ids');
//     curr_skill_ids = JSON.parse(curr_skill_ids);
//     var error_count = 0;
    
//     nameError.innerText = ``;
//     descError.innerText = ``;


//     // ROLE NAME 
//     // get value of role name from form and compare 
//     var new_role_name = document.getElementById('role_name').value;
//     if (new_role_name == ''){
//         error_count += 1;
//         nameError.innerText = `Role name cannot be empty.`;
//     }

//     // ROLE DESCRIPTION 
//     // get value of role description from form and compare 
//     var new_role_desc = document.getElementById('role_desc').value;
//     if (new_role_desc == ''){
//         error_count += 1;
//         descError.innerText = `Role description cannot be empty.`;
//     }

//     // ROLE SKILLS 
//     // get values of skills in role from form and compare 
//     skillError.innerText = ``;
//     const allChecked = document.querySelectorAll("input[name=skills]:checked");
//     var checkedSkills = Array.from(allChecked).map((checkbox) => checkbox.value);
//     console.log(error_count);

//     if (checkedSkills.length == 0){
//         error_count += 1;
//         skillError.innerText = `You cannot remove all skills from this role. Please select at least one skill to be added under this role.`;
//     }
//     else{
//         var added_skills = [];
//         var deleted_skills = [];

//         for (var new_idx in checkedSkills){
//             var new_id = checkedSkills[new_idx];
//             // if new id not in curr_skill -> save to added_skills 
//             if(!curr_skill_ids.includes(parseInt(new_id))){
//                 added_skills.push(parseInt(new_id));
//             }
//         }

//         for (var old_idx in curr_skill_ids) {
//             var old_id = curr_skill_ids[old_idx];
//             // if old id not in checkedCourses -> save to deleted_courses
//             if (!checkedSkills.includes(old_id.toString())) {
//                 deleted_skills.push(old_id);
//             }
//         }

//         if (added_skills.length > 0 || deleted_skills.length > 0){

//             console.log("added_skills====",added_skills)
//             console.log("deleted_skills====", deleted_skills)
//             // bryan to add backend
//             $(async () => {
//                 console.log("new here")
//                 var serviceURL = "http://127.0.0.1:5001/edit_skills_in_ljps_role";
//                 try {
//                     const response = 
//                         await fetch(
//                             serviceURL, { mode: "cors", method: "POST", 
//                             headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": '*' },
//                             body: JSON.stringify({
//                                 "ljpsr_id" : role_id,
//                                 "added_skills" : added_skills,
//                                 "deleted_skills" : deleted_skills,
//                                 "new_role_name": new_role_name,
//                                 "new_role_desc": new_role_desc,
//                             })});
//                     const result = await response.json();
//                     if (result) {
//                         // console.log(result.data)
//                         all_skills = result.data;         
//                         }
//                     } catch (error) {
//                         console.log(error);
//                         console.log("error");
//                         error_count += 1 
//                 } 
//             })
//         }
//     }

    
//     // to edit the details 
//     // if (new_role_name != curr_role_name){
        
//         $(async () => {
//             var serviceURL = "http://127.0.0.1:5001/edit_role_details";
//             try {
//                 const response = 
//                     await fetch(
//                         serviceURL, { mode: "cors", method: "POST", 
//                         headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": '*' },
//                         body: JSON.stringify({
//                             "ljpsr_id" : role_id,
//                             "new_role_name": new_role_name,
//                             "new_role_desc": new_role_desc,
//                         })});
//                 const result = await response.json();

//                 if (response.status === 201) {
//                     console.log(error_count);
//                     console.log("Role edited.");
//                     console.log('im fked');
//                     var message = new_role_name + ' has been edited.'
//                     localStorage.setItem('errmessage', message);
//                     location.href ='./roles_page.html';
//                 } 
//                 if (response.status === 401) {
//                     console.log('huh');
//                     error_count += 1;
//                     console.log(error_count)
//                     nameError.innerText = `The role name ${new_role_name} already exists.`;
//                     location.href = '#top';
//                 }

//                 } catch (error) {
//                     console.log(error);
//                     console.log("error");
//                     error_count += 1;
//             } 
//         })
//     // }
//     console.log(nameError);

//     // console.log('hi');
//     // console.log(error_count);
//     // if (error_count == 0){
//     //     console.log('im fked');
//     //     var message = new_role_name + ' has been edited.'
//     //     localStorage.setItem('errmessage', message);
//     //     location.href ='./roles_page.html';
//     // }

//     // else{
//     //     location.href = '#top';
//     //     // alert('Errors have been found in page.');
//     // }
// }



function editRole(){
    var role_id = sessionStorage.getItem('edit_role_id');
    var curr_role_name = sessionStorage.getItem('curr_role_name');
    var curr_role_desc = sessionStorage.getItem('curr_role_desc');
    var curr_skill_ids = sessionStorage.getItem('curr_skill_ids');
    curr_skill_ids = JSON.parse(curr_skill_ids);
    var error_count = 0;
    
    nameError.innerText = ``;
    descError.innerText = ``;


    // ROLE NAME 
    // get value of role name from form and compare 
    var new_role_name = document.getElementById('role_name').value;
    if (new_role_name == ''){
        error_count += 1;
        nameError.innerText = `Role name cannot be empty.`;
    }
    // ROLE DESCRIPTION 
    // get value of role description from form and compare 
    var new_role_desc = document.getElementById('role_desc').value;
    if (new_role_desc == ''){
        error_count += 1;
        descError.innerText = `Role description cannot be empty.`;
    }

    for (var roleidx in allRoles){
        var rolename = allRoles[roleidx];
        if (new_role_name == rolename && rolename != curr_role_name ){
            error_count += 1;
            nameError.innerText += `The role ${rolename} already exists.`;
        }
    }

    if (nameError.innerText == ''){
        $(async () => {
            var serviceURL = "http://127.0.0.1:5001/edit_role_details";
            try {
                const response = 
                    await fetch(
                        serviceURL, { mode: "cors", method: "POST", 
                        headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": '*' },
                        body: JSON.stringify({
                            "ljpsr_id" : role_id,
                            "new_role_name": new_role_name,
                            "new_role_desc": new_role_desc,
                        })});
                const result = await response.json();
                if (result) {
                    // console.log(result.data)
                    update_message = result.data;         
                    }
                } catch (error) {
                    console.log(error);
                    console.log("error");
            } 
        })
    }

    // ROLE SKILLS 
    // get values of skills in role from form and compare 
    skillError.innerText = ``;
    const allChecked = document.querySelectorAll("input[name=skills]:checked");
    var checkedSkills = Array.from(allChecked).map((checkbox) => checkbox.value);
    // console.log(checkedSkills);
    if (checkedSkills.length == 0){
        error_count += 1;
        skillError.innerText = `You cannot remove all skills from this role. Please select at least one skill to be added under this role.`;
    }
    else{
        var added_skills = [];
        var deleted_skills = [];

        for (var new_idx in checkedSkills){
            var new_id = checkedSkills[new_idx];
            // if new id not in curr_skill -> save to added_skills 
            if(!curr_skill_ids.includes(parseInt(new_id))){
                added_skills.push(parseInt(new_id));
            }
        }

        for (var old_idx in curr_skill_ids) {
            var old_id = curr_skill_ids[old_idx];
            // if old id not in checkedCourses -> save to deleted_courses
            if (!checkedSkills.includes(old_id.toString())) {
                deleted_skills.push(old_id);
            }
        }

        if (added_skills.length > 0 || deleted_skills.length > 0){

            console.log("added_skills====",added_skills)
            console.log("deleted_skills====", deleted_skills)
            // bryan to add backend
            $(async () => {
                // console.log("new here")
                var serviceURL = "http://127.0.0.1:5001/edit_skills_in_ljps_role";
                try {
                    const response = 
                        await fetch(
                            serviceURL, { mode: "cors", method: "POST", 
                            headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": '*' },
                            body: JSON.stringify({
                                "ljpsr_id" : role_id,
                                "added_skills" : added_skills,
                                "deleted_skills" : deleted_skills,
                                "new_role_name": new_role_name,
                                "new_role_desc": new_role_desc,
                            })});
                    const result = await response.json();
                    if (result) {
                        // console.log(result.data)
                        all_skills = result.data;         
                        }
                    } catch (error) {
                        console.log(error);
                        console.log("error");
                } 
            })
        }
    }

    if (error_count == 0){
        var message = new_role_name + ' has been edited.'
        localStorage.setItem('errmessage', message);
        location.href ='./roles_page.html';
    }

    else{
        location.href = '#top';
        // alert('Errors have been found in page.');
    }
}