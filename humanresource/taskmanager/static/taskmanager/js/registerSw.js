const registerSw = async() => {
    if('serviceWorker' in navigator){
        const reg = await navigator.serviceWorker.register('sw.js');
        initialiseState(reg)
    }else{
        showNotAllowed("Huwezi tuma push notification.. ☹️😢")
    }
};

const initialiseState = (reg) => {
    if(!reg.showNotification){
        showNotAllowed("Notifications haiko supported ☹️😢");
        return
    }
    if(Notification.permission == 'denied'){
        showNotAllowed('Nimekataa hakuna kuona notifications ☹️🤔');
        return
    }
    if(!'PushManager' in window){
        showNotAllowed('Push isn\'t allowed in your browser 🤔 🤔');
        return
    }
    subscirbe(reg)
}

const showNotAllowed = (message) => {
    const button = document.querySelector;
    button.innerHTML = `${message}`;
    button.setAttribute('disabled','true' );
}


function urlB64ToUint8Array(base64String){
    const padding = '='.repeat((4-base64String.length % 4) % 4);
    const base64 = (base64String + padding)
                    .replace(/\-/g,'+')
                    .replace(/_/g,'/');
    const rawData = window.atob(base64);
    const outputArray = new Uint8Array(rawData.length);
    const outputData = outputArray.map((output,index) => rawData.charCodeAt(index));

    return outputData;
}

const subscirbe = async (reg) => {
    const subscription = await reg.pushManager.getSubscription();
    if(subscription){
        sendSubData(subscription);
        return;
    }
    const vapidMeta = document.querySelector('meta[name="vapid-key"]');
    const key = vapidMeta.content;
    const options = {
        userVisibleOnly: true,
        applicationServerKey: urlB64ToUint8Array(
            'BE-PoVEuQGI-OUPkpphW1ivIj2A6SskYXRn9v7cJk6bMDr8BAXVIqqg478x3OMh8ON-tkp-vlHW7-y3NwxYle9o'
        )
    };

    const sub = await reg.pushManager.subscribe(options);
    sendSubData(sub)
}

const sendSubData = async(subscription) => {
    const browser = navigator.userAgent.match(/(firefox|msie|chrome|safari|trident)/ig)[0].toLowerCase();
    const data = {
        status_type:'subscribe',
        subscription:subscription.toJSON(),
        browser:browser,
    };

    const res = await fetch('/webpush/save_information',{
        method:'POST',
        body:JSON.stringify(data),
        headers:{
            'content-type':'application/json'
        },
        credentials:"include"
    });

    handleResponse(res);
};

const handleResponse = (res) => {
    console.log(res.status);
};

registerSw()
