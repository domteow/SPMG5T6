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

for (let role in roles){
    console.log(role);
    var completed = roles[role];
    console.log(completed);
    if (completed =='Y'){
        place.innerHTML += `<div class="roleCol container-fluid">
        <div class="row">
            <div class="col-8 roledeets">`+ role + `</div>
            <div class="col-4 completed">
                Attained Skills Required
            </div>
        </div>`
    }
    else{
        place.innerHTML += `<div class="roleCol container-fluid">
        <div class="row">
            <div class="col-8 roledeets">`+ role + `</div>
            <div class="col-4 ncompleted">
                Take Skills Required
            </div>
        </div>`
    }
}

