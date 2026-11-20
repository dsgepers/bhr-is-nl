import {formAccessKey,formDefinitions} from './public/config.js';
const escape=value=>String(value).replace(/[&<>"']/g,char=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]));

// Buttons remain disabled until JavaScript supplies an absolute, deployment-aware thank-you URL.
export function formStart(kind,classes='',attributes=''){
 if(!Object.hasOwn(formDefinitions,kind))throw Error(`Unknown form: ${kind}`);
 const definition=formDefinitions[kind];
 const fields=`<input type="hidden" name="access_key" value="${escape(formAccessKey)}"><input type="hidden" name="subject" value="${escape(definition.subject)}"><input type="hidden" name="redirect" value="">`;
 const trap='<input type="checkbox" name="botcheck" class="honeypot" style="display:none" tabindex="-1" autocomplete="off" aria-hidden="true">';
 return `<form class="${kind==='newsletter'?'':'static-form '}${classes}" data-form-submit="${kind}" ${attributes} action="https://api.web3forms.com/submit" method="post" enctype="multipart/form-data">${fields}<input type="hidden" name="pagina" value="">${trap}<noscript><p>Schakel JavaScript in om dit formulier te gebruiken, of <a href="mailto:info@bhr-is.nl">mail naar info@bhr-is.nl</a>.</p></noscript>`;
}
