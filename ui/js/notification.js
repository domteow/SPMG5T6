var erroralert = document.getElementById('alerty');
var count = 100;
var message = localStorage.getItem('errmessage');
erroralert.innerHTML = ``;
console.log(message);
console.log(typeof(message));
if ('errmessage' in localStorage){
    console.log('hiiii');
    erroralert.style.display = 'block';
    count += 1;
    erroralert.innerHTML += `
        <div class="alert position-relative " id="${count}"> 
            <span class="closebtn" onclick="this.parentElement.style.display='none';">&times;</span>
            <div class="alert-header">
                <img src="../img/webicon.png" width="10%" class="rounded me-2" alt="...">
                <strong class="me-auto">LJPS</strong>
                <small></small>
                
            </div>
            <div class="alert-body">
                ${message}
            </div>
        </div>`;
    console.log(erroralert);
    localStorage.removeItem('errmessage');

}
