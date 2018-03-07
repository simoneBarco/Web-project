window.onload=function(){
   if(document.title=="Registrazione-GameSide"){
      caricamento();
      document.getElementById("in").onblur=function(){
         checkNome();
      }
      document.getElementById("ic").onblur=function(){
         checkCognome();
      }
      document.getElementById("ie").onblur=function(){
         checkEmail();
      }
      document.getElementById("ip1").onblur=function(){
         checkPw1();
      }
      document.getElementById("ip2").onblur=function(){
         checkPw2();
      }
   }
}

function checkNome(){
   var tag=document.getElementById("in");
   var dest=document.getElementById("nome");
   if(tag.value==""){
      dest.innerHTML="Campo obbligatorio!";
      dest.className="errori";
   }
   else{
      dest.innerHTML="";
      dest.className="";
   }
}

function checkCognome(){
   var tag=document.getElementById("ic");
   var dest=document.getElementById("cognome");
   if(tag.value==""){
      dest.innerHTML="Campo obbligatorio!";
      dest.className="errori";
   }
   else{
      dest.innerHTML="";
      dest.className="";
   }
}

function checkEmail(){
   var tag=document.getElementById("ie");
   var dest=document.getElementById("email");
   if(tag.value==""){
      dest.innerHTML="Campo obbligatorio!";
      dest.className="errori";
   }
   else{
      var regExp=/^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+[\.]([a-z0-9-]+[\.])*([a-z]{2,3})$/;
      if(tag.value.search(regExp)!=0){
         dest.innerHTML="E-mail non valida!";
         dest.className="errori";
      }
      else{
         dest.innerHTML="";
         dest.className="";
      }
   }

}

function checkPw1(){
   var pw1=document.getElementById("ip1");
   var dest=document.getElementById("pwd1");
   if(pw1.value==""){
      dest.innerHTML="Campo obbligatorio!";
      dest.className="errori";
   }
   else{
      dest.innerHTML="";
      dest.className="";
   }
}

function checkPw2(){
   var pw1=document.getElementById("ip1");
   var pw2=document.getElementById("ip2");
   var dest=document.getElementById("pwd2");
   if(pw1.value!=pw2.value){
      dest.innerHTML="Le password non coincidono!";
      dest.className="errori";
   }
   else{
      dest.innerHTML="";
      dest.className="";
   }
}

function caricamento(){
   var form=document.getElementById("reg");
   var arraytext = form.getElementsByTagName("input");
   for(var i=0; i<arraytext.length; i++){
      if(arraytext[i].getAttribute("type")=="text" || arraytext[i].getAttribute("type")=="password"){
         suggerimento(arraytext[i].getAttribute("id"));
         arraytext[i].className="suggerimento";
         arraytext[i].setAttribute("onfocus", "svuota(id)");
      }
   }
}

function suggerimento(id){
   var tag=document.getElementById(id);
   var sel=tag.getAttribute("id");
   if(sel=="in"){
      tag.value="Inserire nome";
   }
   if(sel=="ic"){
      tag.value="Inserire cognome";
   }
   if(sel=="ie"){
      tag.value="Inserire E-mail";
   }
   if(sel=="ip1"){
      tag.value="Inserire password";
   }
   if(sel=="ip2"){
      tag.value="Reinserire password";
   }
   if(sel=="ni"){
       tag.value="Inserire nickname";
   }
}

function svuota(stringa){
   var tag=document.getElementById(stringa);
   if(tag.className=="suggerimento"){
      tag.value="";
      tag.removeAttribute("class");
   }
}
