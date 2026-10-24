'use strict';
(() => {
  const endpoint='https://nxjqyijykcnxlwoxanrb.supabase.co/functions/v1/belmarion-office-handoff';
  const token=new URLSearchParams(window.location.hash.slice(1)).get('t') || '';
  const form=document.getElementById('confirm-form');
  const button=document.getElementById('confirm-button');
  const detail=document.getElementById('detail');
  const error=document.getElementById('error');
  const heading=document.querySelector('h1');
  const status=document.getElementById('receipt-status');

  const message=(text,kind='info')=>{
    status.hidden=false;
    status.textContent=text;
    status.style.color=kind==='error'?'#f2b4a8':'#c6c2b9';
  };
  const showSuccess=()=>{
    form.hidden=true; error.hidden=true;
    heading.textContent='Acknowledgement Received.';
    detail.textContent='Thank you for confirming handover.';
    document.getElementById('close-page').hidden=false;
    status.hidden=true;
    button.disabled=false;
    window.history.replaceState(null,'',window.location.pathname);
  };
  const showFailure=()=>{
    button.disabled=false;
    button.textContent='TRY AGAIN';
    message('We could not confirm the result. Please try again, or contact Belmarion for assistance.','error');
  };
  const requestStatus=async()=>{
    const u=endpoint+'?receipt_status=1&t='+encodeURIComponent(token);
    const res=await fetch(u,{method:'GET',mode:'cors',credentials:'omit',cache:'no-store',referrerPolicy:'no-referrer',headers:{'Accept':'application/json'}});
    if(!res.ok) throw new Error('Receipt status unavailable');
    const data=await res.json();
    return data?.acknowledged===true;
  };

  if(!/^[a-f0-9]{64}$/i.test(token)){
    error.hidden=false;
    detail.hidden=true;
    return;
  }
  document.getElementById('token').value=token;
  form.hidden=false;
  message('Checking the existing receipt record…');

  requestStatus().then(done=>{
    if(done) showSuccess();
    else status.hidden=true;
  }).catch(()=>{status.hidden=true;});

  form.addEventListener('submit',async(event)=>{
    event.preventDefault();
    if(button.disabled)return;
    button.disabled=true;
    button.textContent='CONFIRMING RECEIPT…';
    error.hidden=true;
    message('Checking confirmation with Belmarion…');
    try{
      const res=await fetch(endpoint,{
        method:'POST',
        mode:'cors',
        credentials:'omit',
        cache:'no-store',
        referrerPolicy:'no-referrer',
        headers:{'Accept':'application/json'},
        body:new URLSearchParams({token,action:'acknowledge'})
      });
      if(!res.ok)throw new Error('Acknowledgement request unsuccessful');
      const result=await res.json();
      if(result?.acknowledged!==true)throw new Error('Receipt not confirmed');
      showSuccess();
    }catch(_error){
      // Recover from a network interruption after the backend has saved receipt.
      try{if(await requestStatus()){showSuccess();return;}}catch(_statusError){}
      showFailure();
    }
  });
})();

