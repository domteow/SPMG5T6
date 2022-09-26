roles = {
    'audit': 'Y',
    'accountant': 'N',
    'cashier' : 'N',
    'CEO' : 'Y',
    'cleaner' : 'N',
    'developer' : 'Y',
    'econs person' :' N',
    'frontend developer' : 'Y',
    'manager' : 'Y'
}

var place = document.getElementById('allroles');
var role_id = 0;
for (let role in roles){
    console.log(role);
    var completed = roles[role];
    console.log(completed);

    if (completed =='Y'){
        /* IF THE PERSON HAS ALREADY ATTAINED ALL SKILLS REQUIRED */
        place.innerHTML += `<div class="roleCol container-fluid">
        <div class="row">
            <div class="col-4 roledeets">`+ role + `</div>
            <div class= 'col-4 completed'>Attained Skills Required</div>
            <div class="col-4 ncompleted" id=${role_id} onclick='createLJ(this.id)'>
            Take Skills Required
            </div>
        </div></div>`
    }
    else{
        /* IF THE PERSON HAS NOT ATTAINED ALL SKILLS REQUIRED */
        place.innerHTML += `<div class="roleCol container-fluid">
        <div class="row">
            <div class="col-4 roledeets">${role}</div>
            <div class= 'col-4 completed'></div>
            <div class="col-4 ncompleted" id=${role_id} onclick='createLJ(this.id)'>
                Take Skills Required
            </div>
        </div></div>`
    }
    role_id += 1;
}

function createLJ(roleid){
    sessionStorage.setItem('roleid', roleid);
    location.href = '../creating_LJ/creating_LJ.html';
}

