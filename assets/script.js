var startProductBarPos=-1;
window.onscroll=function(){
  var bar = document.getElementById('nav');
  if(startProductBarPos<0)startProductBarPos=findPosY(bar);

  if(pageYOffset>startProductBarPos){
    bar.classList.add("nav_sticky")
  }else{
    bar.classList.remove("nav_sticky")
  }

};

function findPosY(obj) {
  var curtop = 0;
  if (typeof (obj.offsetParent) != 'undefined' && obj.offsetParent) {
    while (obj.offsetParent) {
      curtop += obj.offsetTop;
      obj = obj.offsetParent;
    }
    curtop += obj.offsetTop;
  }
  else if (obj.y)
    curtop += obj.y;
  return curtop;
}