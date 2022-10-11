var full_name = sessionStorage.getItem('full_name');
var dept = sessionStorage.getItem('dept');
console.log(full_name);
console.log(dept);

document.getElementById('full_name').innerText = full_name;
document.getElementById('department').innerHTML = dept;