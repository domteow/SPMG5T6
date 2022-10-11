
// THE USER WILL KEY IN THEIR STAFF ID THEN SEND 
// login() WILL TAKE THE STAFF ID AND STORE IN SESSIONSTORAGE
// BACKEND WILL TELL FRONTEND WHO THIS STAFF IS
// sessionStorage.clear();
function login(){
    var staff_id = document.getElementById('staff_ID').value;
    sessionStorage.setItem('staff_id', staff_id);
    $(async () => {
        var serviceURL = "http://127.0.0.1:5001/login/" + staff_id
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
                var staff_role = result.data.role_id;
                // console.log(staff_role);
                var f_name = result.data.staff_fname
                var l_name = result.data.staff_lname
                var full_name = f_name + " " + l_name
                var dept = result.data.dept
                sessionStorage.setItem('staff_role', staff_role)
                sessionStorage.setItem('full_name', full_name)
                sessionStorage.setItem('dept', dept)
                }
                console.log(staff_role);
                if (staff_role == 1){
                    location.href = './hr/homepage_hr.html';
                }
                if (staff_role == 2){
                    location.href = './staff/homepage_standard.html';
                }
                if(staff_role == 3){
                    location.href = './manager/homepage_manager.html';
                }
        } catch (error) {
            console.log(error)
            console.log('error')
        }
    })
}
