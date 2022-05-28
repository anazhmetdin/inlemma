$(document).ready(function () {  
    CKEDITOR.on('instanceReady', function (ev) {  
       document.getElementById(ev.editor.id + '_bottom').style.display = 'none';  
       for (var instance in CKEDITOR.instances)
           CKEDITOR.instances[instance].setData("");
       document.getElementById('newPostBody').style.display='block' 
       document.getElementById('dummyNewPost').style.display='none' 
 
       ev.editor.on('focus', function (e) {  
          document.getElementById(ev.editor.id + '_bottom').style.display = 'block'; 
       });  
       ev.editor.on('blur', function (e) {  
          document.getElementById(ev.editor.id + '_bottom').style.display = 'none';  
 
       });  
    });  
 });