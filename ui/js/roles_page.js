function editRole(role_id){
    sessionStorage.setItem('edit_role_id', role_id);
    location.href = './edit_role.html';
}

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
            var searchdiv = document.getElementById('myUL');
            var rolesdiv = document.getElementById('existingRoles');
            var rolesdiv_content = ``;

            for (var role_idx in all_roles){
                var role = all_roles[role_idx];

                var role_name = role['role_title'];
                var role_desc = role['role_desc'];
                var role_id = role['ljpsr_id'];
                var active = role['active'];
                var role_skills = role['skills'];
                var skill_content = ``;

                searchdiv.innerHTML += `<li><a href='#${role_name}'>${role_name}</a></li>`;

                for (var skill_idx in role_skills){
                    var skill = role_skills[skill_idx];
                    var skill_name = skill['skill_name'];

                    skill_content += `<li class='role_desc_text'>${skill_name}</li>`;
                }

                if (active == 1 ){
                    rolesdiv_content += `
                    <div class="accordion-item" id="${role_name}">
                            <div class="container-fluid">
                                <div class="row">
                                    <div class="col-sm-8">
                                        <div id="role-head-1">
                                            <button class="accordion-button collapsed roleTitle" type="button" data-bs-toggle="collapse" data-bs-target="#role-${role_id}" aria-expanded="false" aria-controls="panelsStayOpen-collapseTwo">
                                                ${role_name}   
                                            </button>
                                        </div>
                                    </div>
                                    <button class="col-6 col-md-2 editrole" id="${role_id}" onclick="editRole(this.id)">
                                        Edit
                                    </button>
                                    <div class="col-6 col-md-2 isactivediv">
                                        <select class="form-select" name="${role_id}/${role_name}" aria-label="Default select example" onchange='deleterole(this)'>
                                            <option value="1" selected>Active</option>
                                            <option value="0">Inactive</option>
                                        </select>
                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col">
                                        <div id="role-${role_id}" class="accordion-collapse collapse" aria-labelledby="role-${role_id}">
                                            <div class="accordion-body">
                                                <div class='role_desc_title'>
                                                    Description: 
                                                </div>
                                                <div class='role_desc_text'>
                                                    ${role_desc}
                                                </div>
                                                <div class='role_desc_title'>
                                                    Skills:
                                                </div>
                                                <div class='role_desc_text'>
                                                    <ul>
                                                        ${skill_content}
                                                    </ul>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    `;
                }

                else{
                    rolesdiv_content += `
                        <div class="accordion-item" id="${role_name}">
                            <div class="container-fluid">
                                <div class="row">
                                    <div class="col-sm-8">
                                        <div id="role-head-1">
                                            <button class="accordion-button collapsed roleTitle" type="button" data-bs-toggle="collapse" data-bs-target="#role-${role_id}" aria-expanded="false" aria-controls="panelsStayOpen-collapseTwo">
                                                ${role_name}   
                                            </button>
                                        </div>
                                    </div>
                                    <button class="col-6 col-md-2 editrole" id="${role_id}" onclick="editRole(this.id)">
                                        Edit
                                    </button>
                                    <div class="col-6 col-md-2 isactivediv">
                                        <select class="form-select" name="${role_id}/${role_name}" aria-label="Default select example" onchange='deleterole(this)'>
                                            <option value="1">Active</option>
                                            <option value="0" selected>Inactive</option>
                                        </select>
                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col">
                                        <div id="role-${role_id}" class="accordion-collapse collapse" aria-labelledby="role-${role_id}">
                                            <div class="accordion-body">
                                                <div class='role_desc_title'>
                                                     Description: 
                                                </div>
                                                <div class='role_desc_text'>
                                                    ${role_desc}
                                                </div>
                                                <div class='role_desc_title'>
                                                    Skills:
                                                </div>
                                                <div class='role_desc_text'>
                                                    <ul>
                                                        ${skill_content}
                                                    </ul>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    `;
                }


            }

            rolesdiv.innerHTML += rolesdiv_content


        }
        

    } catch (error) {
        console.log(error)
        console.log('error')
    }
})

var erroralert = document.getElementById('alerts');
erroralert.innerHTML = ``;

function deleterole(activeCheck){
    var isactive = activeCheck.value;
    var values = activeCheck.name;
    var roleid = values.split("/")[0]
    var role_name = values.split("/")[1]

    
    // insert backend here to delete role (kelvvvvvvvvvv) 
    $(async () => {
        var serviceURL = "http://127.0.0.1:5001/delete_role/" + roleid + "&" + isactive + "&" + role_name
        try {
            const response =
                await fetch(
                serviceURL, { mode: 'cors', method: 'GET' }
            );
            // console.log(response)
            const result = await response.json();
            // console.log(result.data)
            if(result) {
                console.log('User data retrieved')
                new_lj_details = JSON.stringify(result.data)
                var message = result.data.message;
                // console.log(staff_role);
                // alert(message)
                erroralert.style.display = 'block';
                erroralert.innerHTML += `
                    <div class="alert position-relative " id="alert"> 
                    <span class="closebtn" onclick="this.parentElement.style.display='none';">&times;</span>
                        <div class="alert-header">
                            <img src="../img/webicon.png" width="10%" class="rounded me-2" alt="...">
                            <strong class="me-auto">LJPS</strong>
                            <small></small>
                            
                        </div>
                        <div class="alert-body">
                            ${message}
                        </div>
                    </div>`;

            

            }
        } catch (error) {
            console.log(error)
            erroralert.innerHTML += `
                    <div class="alert position-relative " id="alert"> 
                        <div class="alert-header">
                            <img src="../img/webicon.png" width="10%" class="rounded me-2" alt="...">
                            <strong class="me-auto">LJPS</strong>
                            <small></small>
                            <span class="closebtn" onclick="this.parentElement.style.display='none';">&times;</span>
                        </div>
                        <div class="alert-body">
                            ${error}
                        </div>
                    </div>`;
        }
    })
}


