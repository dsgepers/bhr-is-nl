export function selectedProjectGroup(search){const value=new URLSearchParams(search).get('filter_projectgroup[]');return ['1','2','3'].includes(value)?value:null}
export function projectGalleryIndex(index,delta,count){return count>0?Math.max(0,Math.min(count-1,index+delta)):0}
