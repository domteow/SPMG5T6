// Instantiate the Bootstrap carousel
$('.multi-item-carousel').carousel({
  interval: false
});
  
// for every slide in carousel, copy the next slide's item in the slide.
// Do the same for the next, next item.
$('.multi-item-carousel .item').each(function(){
  var next = $(this).next();
  if (!next.length) {
    next = $(this).siblings(':first');
  }
  next.children(':first-child').clone().appendTo($(this));

  if (next.next().length>0) {
    next.next().children(':first-child').clone().appendTo($(this));
  } else {
      $(this).siblings(':first').children(':first-child').clone().appendTo($(this));
  }
});

var active = 'path1';
var test = document.getElementById(active);
console.log(test);
console.log(active);

var active = 1;
console.log('test');
function showpath(pathid){
    var original = document.getElementById(active);
    original.classList.remove('activecarou');
    var originalprogress = document.getElementById('progressbar'+active);
    originalprogress.style.backgroundColor= '#9E82CA';
    var newpath = document.getElementById(pathid);
    newpath.classList.add('activecarou');
    var newprogress = document.getElementById('progressbar'+pathid);
    newprogress.style.backgroundColor= '#FFA0A0';
    active = pathid;
}
