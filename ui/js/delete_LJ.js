async function deleteLJ(deleteid){
    var userinput = prompt('Are you sure you want to delete this learning journey? (Y/N)')

    if(userinput.toLowerCase() == 'y') {
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
                alert('Learning Journey deleted')
                
            }
        } catch (error) {
            console.log(error)
            console.log('error')
        }
    }

}