var active = 1;
console.log('test');
function showpath(pathid){
    var original = document.getElementById(active);
    original.classList.remove('activepath');
    var originalprogress = document.getElementById('progressbar'+active);
    originalprogress.style.backgroundColor= '#9E82CA';
    var newpath = document.getElementById(pathid);
    newpath.classList.add('activepath');
    var newprogress = document.getElementById('progressbar'+pathid);
    newprogress.style.backgroundColor= '#FFA0A0';
    active = pathid;
}