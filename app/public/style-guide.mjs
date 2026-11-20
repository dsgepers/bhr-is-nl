// All demo forms are local. Capture prevents production submission handlers.
document.querySelectorAll('.sg-main form').forEach(form=>form.addEventListener('submit',event=>{
 event.preventDefault();event.stopImmediatePropagation();
 const status=form.querySelector('[role="status"]');
 if(status)status.textContent='Style guide demo: no data was sent.';
},true));
document.querySelectorAll('[data-sg-message]').forEach(button=>button.addEventListener('click',()=>{
 document.querySelector('#sg-button-status').textContent=`${button.textContent} activated. This is a local demonstration.`;
}));
const viewport=document.querySelector('#sg-viewport');
const update=()=>{viewport.textContent=`Current viewport: ${window.innerWidth}px. ${window.innerWidth<=600?'Phone':window.innerWidth<=900?'Tablet':'Desktop'} inner-page rules.`;};
window.addEventListener('resize',update,{passive:true});update();
