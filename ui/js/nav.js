function openNav() {
    document.getElementById("mySidebar").style.width = "225px";
    document.getElementById("navmenu").style.marginLeft = "225px";
    document.getElementById('navey').innerHTML = '';
}

function closeNav() {
    document.getElementById("mySidebar").style.width = "0";
    document.getElementById("navmenu").style.marginLeft= "0";
    document.getElementById('navey').innerHTML = `<button class="openbtn" id="navey" onclick="openNav()"><img src="../img/menu icon.png" alt=""></button>`;
    
}

var wid = window.screen.width;
if (wid >= 768){
    // document.getElementById('navey').innerHTML = '';
    document.getElementById('close').innerHTML= '';
    openNav();
}
else{
    document.getElementById('navey').innerHTML = `<button class="openbtn" id="navey" onclick="openNav()"><img src="../img/menu icon.png" alt=""></button>`;
    closeNav();
}
