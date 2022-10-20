$(async () => {
    var serviceURL = "http://127.0.0.1:5001/skills"

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
            // console.log(skillinput);
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

// function handleChange(cb) {
//     var cbval = cb.id;
//     if(cb.checked == true) {
//         // to check all checkbox with the SAME ID -> course_id
//         var cbox = `input[id=${cbval}]`
//         var allCB = document.querySelectorAll(cbox);
//         for (var i=0; i< allCB.length; i++){
//             allCB[i].checked = true;
//         }
      
//     } else {
//         // to uncheck all checkbox
//         var cbox = `input[id=${cbval}]`
//         var allCB = document.querySelectorAll(cbox);
//         for (var i=0; i< allCB.length; i++){
//             allCB[i].checked = false;
//         }

//     }
// }

async function addRole(){
    var serviceURL = "http://127.0.0.1:5001/create_role"
    var role_name = document.getElementById('role_name').value;
    console.log(role_name);
    var role_desc = document.getElementById('role_desc').value;
    console.log(role_desc);

    const allChecked = document.querySelectorAll('input[name=skills]:checked');

    var newRoleSkills = Array.from(allChecked).map(checkbox => checkbox.value);
    console.log(newRoleSkills);
        if (role_name == "") {
            alert("Role name cannot be empty.")
        }
        else if (role_desc == ""){
            alert("Role description cannot be empty.")
        }
        else if(newRoleSkills.length == 0) {
            alert("Please select at least one skill to add to your role.")
        }
        else {
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
                    alert("The role " + role_name + " has been successfully created")
                    var message = 'The role' + role_name + 'has been successfully created.'
                    localStorage.setItem('errmessage', message);
                    location.href = './roles_page.html';
                } else if (response.status === 401) {
                    alert("The role name " + role_name + " already exists");
                }
                
        
            } catch (error) {
                console.log(error)
                console.log('error')
            }
            // var staff_role = sessionStorage.getItem('staff_role');
            // console.log(staff_role);

        }

}