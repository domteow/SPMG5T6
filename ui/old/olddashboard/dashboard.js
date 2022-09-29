details = {
    1: {
        'rolename': 'CEO',
        'modules': {
            'm1' : 'Y',
            'm2' : 'Y',
            'm3' :'N',
            'm4':'Y',
            'm5': 'N'
        }
    },
    2: {
        'rolename':'manager',
        'modules':{
            'm1' : 'Y',
            'm2' : 'N',
            'm3' :'Y',
            'm4':'N',
            'm5': 'Y',
            'm6': 'N'
        }
    }
}

var parentdiv = document.getElementById('display_LJ');
for(var detail in details){
    var set = details[detail];

    var rolename = set['rolename'];
    var modules = set['modules'];
    // console.log(modules);
    var count = 0;
    var len = 0;
    for (var mod in modules){
        // console.log(modules[mod]);
        if (modules[mod] == 'Y'){
            count += 1 
        }
        len += 1;
    }
    console.log(count);
    console.log(len);
    var percentage = Math.ceil(count*100/len);
    console.log(percentage);
    parentdiv.innerHTML= `<div class="item">
    <div class="col-xs-4">
          <div class="path" id="path2" onclick="showpath(this.id)">
              <div class="pathname" id="pathname">
                  <img src="../img/pathicon.png" alt=""> ${rolename}
              </div>
              <div class="progr">
                  Progress
              </div>
              <div class="progress" id="pathprogress">
                  <div class="progress-bar" id="progressbar2" role="progressbar" style="width: ${percentage}%" aria-valuenow="25" aria-valuemin="0" aria-valuemax="100"></div>
              </div>
          </div>
      </div>
  </div>`;


}