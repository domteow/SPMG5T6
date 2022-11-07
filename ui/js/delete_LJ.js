async function deleteLJ(deleteid){
    var userinput = prompt('Are you sure you want to delete this learning journey? (Y/N)')

    if(userinput.toLowerCase() == 'y') {
        var confirm_delete = true
        var lj_id = deleteid.split('/')[1];
        console.log(lj_id);
    
        //  delete LJ 
        var serviceURL = "http://127.0.0.1:5001/delete_LJ/"
    
        try {
            const response = await fetch(serviceURL,
                { mode: 'cors', method: ['DELETE'],
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({
                    "journey_id" : lj_id
                })});
    
            console.log(response)
            if(response.status === 201 || response.status === 200) {
                console.log('Learning Journey deleted')
                // alert('Learning Journey deleted')
                
            }
        } catch (error) {
            console.log(error)
            console.log('error')
        }
    }
    var staff_role = sessionStorage.getItem('staff_role');
    console.log(staff_role);
    if (confirm_delete) {
        if (staff_role == 1){
            var message = 'Learning Journey deleted.';
            localStorage.setItem('errmessage', message);
            sessionStorage.setItem('refresh', 'Y');
            location.href = '../hr/dashboard_hr.html';
        }
        if(staff_role == 2){
            var message = 'Learning Journey deleted.';
            localStorage.setItem('errmessage', message);
            sessionStorage.setItem('refresh', 'Y');
            location.href = '../staff/dashboard_standard.html';
        }
        if(staff_role == 3){
            var message = 'Learning Journey deleted.';
            localStorage.setItem('errmessage', message);
            sessionStorage.setItem('refresh', 'Y');
            location.href = '../manager/dashboard_manager_personal.html';
        }        
    }
    

}