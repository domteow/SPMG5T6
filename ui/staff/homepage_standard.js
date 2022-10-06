// roles = {
//     "data" : [
//         {
//         "role_name" : "accountant",
//         "role_desc": "Lorem ipsum dolor sit amet consectetur adipisicing elit. Dolorem quisquam, quod earum sapiente impedit illo, provident accusamus, doloremque ducimus laudantium eius aspernatur eum dolores. Ipsam odit a ipsa dolore ducimus.",
//         "role_id" : 1,
//         "is_complete": 0
//         },
//         {
//             "role_name" : "CEO",
//             "role_desc": "Lorem ipsum dolor sit amet consectetur adipisicing elit. Dolorem quisquam, quod earum sapiente impedit illo, provident accusamus, doloremque ducimus laudantium eius aspernatur eum dolores. Ipsam odit a ipsa dolore ducimus.",
//             "role_id" : 2,
//             "is_complete": 1
//         },
//         {
//             "role_name" : "teehee",
//             "role_desc": "Lorem ipsum dolor sit amet consectetur adipisicing elit. Dolorem quisquam, quod earum sapiente impedit illo, provident accusamus, doloremque ducimus laudantium eius aspernatur eum dolores. Ipsam odit a ipsa dolore ducimus.",
//             "role_id" : 3,
//             "is_complete": 0
//         }
//     ]
// }

var staff_id = 1
sessionStorage.setItem('staff_id', staff_id)
var place = document.getElementById('allroles');
var all_roles;

$(async () => {
    var serviceURL = "http://127.0.0.1:5001/all_roles/" + staff_id

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
            all_roles = result.data
            
            for (let role in all_roles){
                var roled = all_roles[role];
                // console.log(roled)
                var role_name = roled['role_title'];
                var role_id = roled['ljpsr_id'];
                var completed = roled['attained'];
                // console.log(role_name);
                // console.log(role_id);
                // console.log(completed);
            
                if (completed == 1){
                    /* IF THE PERSON HAS ALREADY ATTAINED ALL SKILLS REQUIRED */
                    place.innerHTML += 
                    `<div class="roleCol container-fluid">
                        <div class="row">
                            <div class="col-4 roledeets">`+ role_name + `</div>
                            <div class= 'col-4 completed'>Attained Skills Required</div>
                            <div class='col-4'><a href='#'><div class='ncompleted' id=${role_id} onclick='createLJ(this.id)'>View Role Details</div></a></div>
                        </div>
                    </div>`
                }
            
                else{
                    /* IF THE PERSON HAS NOT ATTAINED ALL SKILLS REQUIRED */
                    place.innerHTML += 
                    `<div class="roleCol container-fluid">
                        <div class="row">
                            <div class="col-4 roledeets">${role_name}</div>
                            <div class= 'col-4 completed'></div>
                            <div class='col-4'><a href='#'><div class='ncompleted' id=${role_id} onclick='createLJ(this.id)'>View Role Details</div></a></div>
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

// for (let role in all_roles){
//     var roled = all_roles[role];
//     console.log(roled)
//     var role_name = roled['role_title'];
//     var role_id = roled['ljpsr_id'];
//     var completed = roled['attained'];
//     // console.log(role_name);
//     // console.log(role_id);
//     // console.log(completed);

//     if (completed == 1){
//         /* IF THE PERSON HAS ALREADY ATTAINED ALL SKILLS REQUIRED */
//         place.innerHTML += 
//         `<div class="roleCol container-fluid">
//             <div class="row">
//                 <div class="col-4 roledeets">`+ role_name + `</div>
//                 <div class= 'col-4 completed'>Attained Skills Required</div>
//                 <div class='col-4'><a href='#'><div class='ncompleted' id=${role_id} onclick='createLJ(this.id)'>View Role Details</div></a></div>
//             </div>
//         </div>`
//     }

//     else{
//         /* IF THE PERSON HAS NOT ATTAINED ALL SKILLS REQUIRED */
//         place.innerHTML += 
//         `<div class="roleCol container-fluid">
//             <div class="row">
//                 <div class="col-4 roledeets">${role_name}</div>
//                 <div class= 'col-4 completed'></div>
//                 <div class='col-4'><a href='#'><div class='ncompleted' id=${role_id} onclick='createLJ(this.id)'>View Role Details</div></a></div>
//             </div>
//         </div>`
//     }
// }

// function createLJ(roleid){
//     sessionStorage.setItem('role_id', roleid);


//     location.href = '../creating_LJ/view_role_details.html';
// }

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
        // console.log(response)
        const result = await response.json();
        console.log(result.data)
        if(result) {
            console.log('Role selected')
            role_details = JSON.stringify(result.data)
            sessionStorage.setItem('role_details', role_details)
            location.href = '../creating_LJ/view_role_details.html';
        }
        

    } catch (error) {
        console.log(error)
        console.log('error')
    }

    // location.href = '../creating_LJ/view_role_details.html';
}