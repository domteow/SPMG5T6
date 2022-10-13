$(async () => {
    var serviceURL = "http://127.0.0.1:5001/skills"

    try {
        const response =
            await fetch(
            serviceURL, { mode: 'cors', method: 'GET' }
        );
        // console.log(response)
        const result = await response.json();
        // console.log(result.data)
        if(result) {
            console.log(result.data)
            all_skills = result.data
        
        }
        

    } catch (error) {
        console.log(error)
        console.log('error')
    }
})
















function addRole(){
    var role_name = document.getElementById('role_name').value;
    console.log(role_name);
    var role_desc = document.getElementById('role_desc').value;
    console.log(role_desc);
}