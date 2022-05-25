$(document).ready(function () {  
    CKEDITOR.on('instanceReady', function (ev) {  
       document.getElementById(ev.editor.id + '_bottom').style.display = 'none';  
 
 
       ev.editor.on('focus', function (e) {  
          document.getElementById(ev.editor.id + '_bottom').style.display = 'block';  
 
       });  
       ev.editor.on('blur', function (e) {  
          document.getElementById(ev.editor.id + '_bottom').style.display = 'none';  
 
       });  
    });  
 });