import {test} from 'node:test';
import assert from 'node:assert/strict';
import {searchPages,stepTarget,cookiePreferences} from '../public/behavior.mjs';
test('search finds Dutch page titles without accents and handles empty input',()=>{
 const pages=[{title:'Industriële automatisering',url:'/expertises/industriele-automatisering'},{title:'Contact',url:'/contact'}];
 assert.deepEqual(searchPages(pages,'industriele'),[pages[0]]);
 assert.deepEqual(searchPages(pages,'  '),[]);
 assert.deepEqual(searchPages(pages,'onbekend'),[]);
});
test('form navigation stays within the available steps',()=>{
 assert.equal(stepTarget(0,-1,3),0);assert.equal(stepTarget(2,1,3),2);assert.equal(stepTarget(0,1,3),1);
});

test('cookie settings restore the previously accepted, denied or selected preferences',()=>{
 assert.deepEqual(cookiePreferences('accepted'),{analytics:true,marketing:true});
 assert.deepEqual(cookiePreferences('denied'),{analytics:false,marketing:false});
 assert.deepEqual(cookiePreferences('{"analytics":"on"}'),{analytics:true,marketing:false});
 assert.deepEqual(cookiePreferences('{"marketing":"on"}'),{analytics:false,marketing:true});
 for(const value of [null,'malformed','null','{}'])assert.deepEqual(cookiePreferences(value),{analytics:false,marketing:false});
});
