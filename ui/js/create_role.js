$(async () => {
    var serviceURL = "http://127.0.0.1:5001/get_all_skills_and_courses"

    try {
        const response =
            await fetch(
            serviceURL, { mode: 'cors', method: 'GET' }
        );
        const result = await response.json();
        
        if(result) {
            all_skills = result.data
            all_skills = all_skills.skills;

            var searchdiv = document.getElementById('myUL');
            var skilldiv = document.getElementById('allSkills');
            var skillinput = ``

            for (var skill_idx in all_skills){
                var skill = all_skills[skill_idx];
                var skill_name = skill.skill_name;
                var skill_id = skill.skill_id;

                // add skill into search 
                searchdiv.innerHTML += `<li><a href='#${skill_id}'>${skill_name}</a></li>`;

                if (skill_idx == 0 || skill_idx%2==0){
                    skillinput += `
                        <div class='row skillrow'>
                            <div class='col-sm-6 skillname form-check' id=${skill_id}>
                                <input class='form-check-input skillName' type='checkbox' id=${skill_id}   name='skills' value =${skill_id}>
                                ${skill_name}
                            </div>
                        
                    `;
                }
                else{
                    skillinput += `
                            <div class='col-sm-6 skillname form-check' id=${skill_id}>
                                <input class='form-check-input skillName' type='checkbox' id=${skill_id}   name='skills' value =${skill_id}>
                                ${skill_name}
                            </div>
                        </div>
                    `;
                }
            }
            skilldiv.innerHTML += skillinput;
        }
        
    } catch (error) {
        console.log(error)
        console.log('error')
    }
})

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

var nameError = document.getElementById('nameError');
var descError = document.getElementById('descError');
var skillError = document.getElementById('skillError');

async function addRole(){
    nameError.innerText = ``;
    descError.innerText = ``;
    skillError.innerText = ``;

    var serviceURL = "http://127.0.0.1:5001/create_role"

    var new_name = document.getElementById('role_name').value;
    var role_name = new_name.trim(' ');
    var role_desc = document.getElementById('role_desc').value;
    var error = 0;

    const allChecked = document.querySelectorAll('input[name=skills]:checked');

    var newRoleSkills = Array.from(allChecked).map(checkbox => checkbox.value);
    
    if (role_name == "") {
        nameError.innerText = `Role name cannot be empty.`;
        error += 1;
    }

    if (role_desc == ""){
        descError.innerText = `Role description cannot be empty.`;
        error += 1;
    }

    if(newRoleSkills.length == 0) {
        skillError.innerText = `Please select at least one skill to create the role.`;
        error += 1;
    }
    if((role_name != '') & (role_desc != '') & (newRoleSkills.length > 0)) {
        sessionStorage.setItem('newRoleName', role_name);
        sessionStorage.setItem('newRoleDesc', role_desc);
        sessionStorage.setItem('newRoleSkills', newRoleSkills);
        try {
            const response =
                await fetch(
                serviceURL, { mode: 'cors', method: 'POST',
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    "newRoleName" : role_name,
                    "newRoleDesc" : role_desc,
                    // stringify course array and add here
                    "newRoleSkills" : JSON.stringify(newRoleSkills)
                })
            });
            console.log(response)
            const result = await response.json();
            console.log(result)
            if(response.status === 201) {
                console.log('Creation successful');
            } else if (response.status === 401) {
                nameError.innerText = `The role name ${role_name} already exists`;
                error += 1
            }
            
    
        } catch (error) {
            console.log(error)
            console.log('error')
        }

    
    }
    if (error > 0){
        location.href = '#top';
        // alert('Errors have been found in creating the role.')
    }

    else{
        var message = 'The role ' + role_name + ' has been successfully created.'
        localStorage.setItem('errmessage', message);
        location.href = './roles_page.html';
    }

}