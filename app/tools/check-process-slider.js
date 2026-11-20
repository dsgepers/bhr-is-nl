// Run on /expertises or /afspraak-maken at 1920px after page modules load.
// It checks the actual carousel controls and image, then returns to step one.
(async()=>{
 const root=document.querySelector('[data-carousel="steps"]');
 const image=root.querySelector('.parity-step-photo,.secondary-photo');
 const previous=root.querySelector('[data-carousel-direction="-1"]');
 const next=root.querySelector('[data-carousel-direction="1"]');
 root.scrollIntoView({block:'center'});previous.click();previous.click();
 const expected=['437_dsc02673.webp','438_dsc02665.webp','624_dsc01086.webp'];
 const results=[];
 const check=async index=>{
  await new Promise(resolve=>setTimeout(resolve,350));
  await Promise.race([image.decode().catch(()=>{}),new Promise(resolve=>setTimeout(resolve,2000))]);
  const actual=image.getAttribute('src').split('/').pop();
  const card=root.querySelector('.parity-step,.secondary-step'),p=image.getBoundingClientRect(),c=card.getBoundingClientRect();
  const overlap=Math.min(p.right,c.right)-Math.max(p.left,c.left);
  const point={x:(Math.max(p.left,c.left)+Math.min(p.right,c.right))/2,y:(Math.max(p.top,c.top)+Math.min(p.bottom,c.bottom))/2};
  const photoOnTop=overlap<=0||document.elementFromPoint(point.x,point.y)===image;
  results.push({step:index+1,actual,expected:expected[index],pass:actual===expected[index]&&image.naturalWidth>0&&photoOnTop,loaded:image.complete&&image.naturalWidth>0,photoOnTop});
 };
 await check(0);next.click();await check(1);next.click();await check(2);
 previous.click();await check(1);previous.click();await check(0);
 return {pass:results.every(result=>result.pass),width:innerWidth,results};
})()
