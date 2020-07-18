
function divClick(){  
  
       var show="";  
       var radio_st = document.getElementsByName("type");  
       for(var i=0;i<radio_st.length;i++){  
       if(radio_st[i].checked)  
        show = radio_st[i].value;  
       }  
       
       switch (show){  
           case 'transcript':  
               document.getElementById("search_regulator_type").style.display="none";  
               document.getElementById("search_transcript_type").style.display="flex";  
                console.log(show);

               break;  
           case 'regulator':  
               document.getElementById("search_regulator_type").style.display="block";  
               document.getElementById("search_transcript_type").style.display="none";  
                console.log(show);
               break;  
           default:  
               document.getElementById("search_regulator_type").style.display="none";  
               document.getElementById("search_transcript_type").style.display="none";  
               break;                                                                
       }  
}

var st=document.querySelectorAll("input[name='type']")
st[0].addEventListener('click',divClick)
st[1].addEventListener('click',divClick)
