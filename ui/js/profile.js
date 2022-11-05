var staff_id = sessionStorage.getItem('staff_id');
var namediv = document.getElementById('name');
var emaildiv = document.getElementById('email');
var skilldiv = document.getElementById('skills');
console.log(staff_id);

$(async() => {
    var serviceURL = "http://127.0.0.1:5001/get_personal_attained_skills/" + staff_id

    try{
        const response = 
            await fetch(serviceURL, {mode:'cors', method: 'GET'});
        
        const result = await response.json();
        if(result){
            var data = result.data;
            
            // display personal information
            var staff_name = data['staff_details']['staff_fname'] + data['staff_details']['staff_lname'];
            var staff_email = data['staff_details']['email'];
            var staff_dept = data['staff_details']['dept'];
            namediv.innerHTML = `${staff_name}<span class='depty'>${staff_dept}</span>`;
            emaildiv.innerText = staff_email; 

            // display skills
            var allSkills = data['completed_skills'];
           
            if (allSkills.length > 0){
                document.getElementById('noValue').style.display = 'none';
                for (var idx in allSkills){
                    var skilldeets = allSkills[idx];
                    var skill_name = skilldeets['skill_name'];
                    skilldiv.innerHTML+= `
                        <div class='row skillrow'>
                            <div class='col-9 skillname'>
                                ${skill_name}
                            </div>
                            <div class='col-3'>
                                <div class='attained'>
                                    Attained
                                </div>
                            </div>
                        </div>
                    `;                    
                }
            }
        }
    }

    catch(error){
        console.log(error);
        console.log('error');
    }

})