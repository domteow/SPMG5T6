roles = {
    "data" : [
        {
        "role_name" : "accountant",
        "role_desc": "Lorem ipsum dolor sit amet consectetur adipisicing elit. Dolorem quisquam, quod earum sapiente impedit illo, provident accusamus, doloremque ducimus laudantium eius aspernatur eum dolores. Ipsam odit a ipsa dolore ducimus.",
        "role_id" : 1,
        "is_complete": 0
        },
        {
            "role_name" : "CEO",
            "role_desc": "Lorem ipsum dolor sit amet consectetur adipisicing elit. Dolorem quisquam, quod earum sapiente impedit illo, provident accusamus, doloremque ducimus laudantium eius aspernatur eum dolores. Ipsam odit a ipsa dolore ducimus.",
            "role_id" : 2,
            "is_complete": 1
        },
        {
            "role_name" : "teehee",
            "role_desc": "Lorem ipsum dolor sit amet consectetur adipisicing elit. Dolorem quisquam, quod earum sapiente impedit illo, provident accusamus, doloremque ducimus laudantium eius aspernatur eum dolores. Ipsam odit a ipsa dolore ducimus.",
            "role_id" : 3,
            "is_complete": 0
        }
    ]
}

var place = document.getElementById('allroles');
var all_roles = roles['data'];

for (let role in all_roles){
    var roled = all_roles[role];
    
    var role_name = roled['role_name'];
    var role_id = roled['role_id'];
    var completed = roled['is_complete'];
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

function createLJ(roleid){
    sessionStorage.setItem('role_id', roleid);
    location.href = '../creating_LJ/view_role_details.html';
}
