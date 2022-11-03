function openNav() {
    document.getElementById("mySidebar").style.width = "225px";
    document.getElementById("navmenu").style.marginLeft = "225px";
    document.getElementById('navey').innerHTML = '';
}

function closeNav() {
    document.getElementById("mySidebar").style.width = "0";
    document.getElementById("navmenu").style.marginLeft= "0";
    document.getElementById('navey').innerHTML = `<button class="openbtn" id="navey" onclick="openNav()"><img src="../img/menu icon.png" alt=""></button>`;
    
}

var wid = window.screen.width;
if (wid >= 768){
    // document.getElementById('navey').innerHTML = '';
    document.getElementById('close').innerHTML= '';
    openNav();
}
else{
    document.getElementById('navey').innerHTML = `<button class="openbtn" id="navey" onclick="openNav()"><img src="../img/menu icon.png" alt=""></button>`;
    closeNav();
}

var full_name = sessionStorage.getItem('full_name');
var dept = sessionStorage.getItem('dept');
var full_name_div = document.getElementById('user_name');
var dept_div = document.getElementById('dept');
full_name_div.innerText = full_name;
dept_div.innerText = dept;

var staff_id_check = sessionStorage.getItem('staff_id');
var staff_role = sessionStorage.getItem('staff_role');

console.log(staff_id_check);
// if no staff_id is inputed 
if (staff_id_check == null){
    window.confirm('Please login first in order to access this page.')
    {
    window.location.href='../login.html';
    };
}

// if staff_id is input check role_id instead and match to url 
var currURL = window.location.href;
var urlSplit= currURL.split('/');
var urlRole = urlSplit.at(-2);
if((staff_role == 1) && (urlRole != 'hr')){
    window.confirm('You do not have access to this page. Please re-login.')
    {
    window.location.href='../login.html';
    };
}

if((staff_role == 3) && (urlRole != 'manager')){
    window.confirm('You do not have access to this page. Please re-login.')
    {
    window.location.href='../login.html';
    };
}

if((staff_role == 2) | (staff_role == 4)){
    if(urlRole != 'staff'){
        window.confirm('You do not have access to this page. Please re-login.')
    {
        window.location.href='../login.html';
    };
    }
}