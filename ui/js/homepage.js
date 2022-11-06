// var staff_id = 1
// sessionStorage.setItem('staff_id', staff_id)
var staff_id = sessionStorage.getItem('staff_id');
var place = document.getElementById('allroles');
var all_roles;
var searchopt = document.getElementById('myUL');

$(async () => {
    var serviceURL = "http://127.0.0.1:5001/all_roles/" + staff_id

    try {
        const response =
            await fetch(
            serviceURL, { mode: 'cors', method: 'GET' }
        );

        const result = await response.json();
        if(result) {
            console.log(result.data)
            all_roles = result.data
            
            for (let role in all_roles){
                var roled = all_roles[role];
                var role_name = roled['role_title'];
                var role_id = roled['ljpsr_id'];
                var completed = roled['attained'];
                var liID = '#' + role_name;

                searchopt.innerHTML += `<li><a href=${liID}>${role_name}</a></li>`;

                if (completed == 1){
                    /* IF THE PERSON HAS ALREADY ATTAINED ALL SKILLS REQUIRED */
                    place.innerHTML += 
                    `<div class="roleCol container-fluid" id=${role_name}>
                        <div class="row">
                            <div class="col-sm-6 roledeets">`+ role_name + `</div>
                            <div class= 'col-sm-3 completed'>Attained Skills Required</div>
                            <div class='col-sm-3'><a href='#'><div class='ncompleted' id=${role_id} onclick='createLJ(this.id)'>View Role Details</div></a></div>
                        </div>
                    </div>`
                }
            
                else{
                    /* IF THE PERSON HAS NOT ATTAINED ALL SKILLS REQUIRED */
                    place.innerHTML += 
                    `<div class="roleCol container-fluid" id=${role_name}>
                        <div class="row">
                            <div class="col-sm-6 roledeets">${role_name}</div>
                            <div class= 'col-sm-3 notcompleted'>Skills required not attained</div>
                            <div class='col-sm-3'><a href='#'><div class='ncompleted' id=${role_id} onclick='createLJ(this.id)'>View Role Details</div></a></div>
                        </div>
                    </div>`
                }
            }
              
        }
        

    } catch (error) {
        console.log(error)
        console.log('error')
    }
})


// get all required skills related to the selected role (dom)
async function createLJ(role_id){
    // roleid selected now becomes learning journey role id
    sessionStorage.setItem('ljpsr_id', role_id);

    var serviceURL = "http://127.0.0.1:5001/view_skills_needed_for_role/" + String(staff_id) + '/' + String(role_id)

    try {
        const response =
            await fetch(
            serviceURL, { mode: 'cors', method: 'GET' }
        );
        
        const result = await response.json();
        console.log(result.data)
        if(result) {
            console.log('Role selected')
            role_details = JSON.stringify(result.data)
            sessionStorage.setItem('role_details', role_details)
            var staff_role = sessionStorage.getItem('staff_role');
            console.log(staff_role);
            if (staff_role == 1){
                location.href = '../hr/view_role_details.html';
            }
            if(staff_role == 2){
                location.href = '../staff/view_role_details.html';
            }
            if(staff_role == 3){
                location.href = '../manager/view_role_details.html';
            }
        }
        

    } catch (error) {
        console.log(error)
        console.log('error')
    }

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