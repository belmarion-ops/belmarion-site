"use strict";
(() => {
  const form=document.getElementById("private-enquiry-form");
  if(!form)return;
  const status=document.getElementById("enquiry-status");
  const button=document.getElementById("enquiry-submit");
  const openedAt=Date.now();
  const endpoint="https://nxjqyijykcnxlwoxanrb.supabase.co/functions/v1/belmarion-public-contact";
  const feedback=(message,error=false)=>{
    status.textContent=message;
    status.classList.toggle("error",error);
    status.setAttribute("role",error?"alert":"status");
  };
  form.addEventListener("submit",async(event)=>{
    event.preventDefault();
    if(!form.reportValidity())return;
    if(button.disabled)return;
    button.disabled=true;
    button.querySelector(".submit-label").textContent="SENDING";
    feedback("Sending your enquiry…");
    const f=new FormData(form);
    const payload={
      name:String(f.get("name")||""),
      email:String(f.get("email")||""),
      office:String(f.get("office")||""),
      topic:String(f.get("topic")||""),
      message:String(f.get("message")||""),
      website:String(f.get("website")||""),
      privacy_acknowledged:f.get("privacy_acknowledged")==="on",
      started_at:openedAt
    };
    const controller=new AbortController();
    const timer=setTimeout(()=>controller.abort(),16000);
    try {
      const r=await fetch(endpoint,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(payload),signal:controller.signal,credentials:"omit",cache:"no-store"});
      let body={};
      try{body=await r.json();}catch{}
      if(!r.ok || body.ok!==true)throw new Error(typeof body.message==="string"?body.message:"We could not submit your enquiry.");
      feedback("Your enquiry has been submitted. Thank you.");
      form.reset();
    }catch(error){
      feedback((error && error.name==="AbortError") ? "The connection timed out. Please contact us by email." :
        (error && typeof error.message==="string" ? error.message : "The enquiry could not be sent. Please contact us by email."),true);
    }finally {
      clearTimeout(timer);
      button.disabled=false;
      button.querySelector(".submit-label").textContent="SEND ENQUIRY";
    }
  });
})();