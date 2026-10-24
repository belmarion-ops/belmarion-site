'use strict';
(async()=>{
 const endpoint='https://nxjqyijykcnxlwoxanrb.supabase.co/functions/v1/belmarion-office-handoff';
 const token=new URLSearchParams(location.hash.slice(1)).get('t')||'';
 const status=document.getElementById('status');
 if(!/^[a-f0-9]{64}$/i.test(token)){status.textContent='The private link is missing or invalid. Reopen your handover email.';return;}
 try{
  const res=await fetch(endpoint+'?reference=1&t='+encodeURIComponent(token),{cache:'no-store',credentials:'omit',referrerPolicy:'no-referrer',headers:{Accept:'application/json'}});
  if(!res.ok)throw new Error('unavailable');
  const result=await res.json();const r=result.reference;
  if(!r||typeof r.experience!=='string'||!r.experience)throw new Error('reference_missing');
  for(const key of ['experience','location','duration','condition','physical']){
   if(typeof r[key]!=='string')throw new Error('reference_invalid');
   document.getElementById(key).textContent=r[key];
  }
  document.getElementById('vector-title').textContent=r.title;
  const url=endpoint+'?t='+encodeURIComponent(token);
  document.getElementById('open-pdf').href=url;
  document.getElementById('pdf').src=url;
  document.getElementById('content').hidden=false;status.hidden=true;
 }catch{status.textContent='These arrangement details are unavailable or the private link has expired. Reopen the handover email, retry, or contact Belmarion.';}
})();
