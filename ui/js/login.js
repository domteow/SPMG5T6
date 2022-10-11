
// THE USER WILL KEY IN THEIR STAFF ID THEN SEND 
// login() WILL TAKE THE STAFF ID AND STORE IN SESSIONSTORAGE
// BACKEND WILL TELL FRONTEND WHO THIS STAFF IS

function login(){
    var staff_id = document.getElementById('staff_ID').value;
    sessionStorage.setItem('staff_id', staff_id);
    var staff_role = // 1/2/3/4; 
    sessionStorage.setItem('staff_role', staff_role);
}

// BACKEND TO USE ^ staff_id TO TELL FRONTEND USER DETAILS

