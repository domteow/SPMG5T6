async function deleteLJ(deleteid){
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
    } catch (error) {
        
    }
}