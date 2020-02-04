//registering an event listener for the push event
self.addEventListener('push',function(event){
    const eventInfo = event.data.text();
    const data = JSON.parse(eventInfo);
    const head = data.head || 'New Notification';
    const body = data.body || 'Default content Notification didn\'t have one';

    //keep service worker alive till notification is created
    event.waitUntil(
        self.registration.showNotification(head,{
            body:body,
            icon:'https://i.imgur.com/MZM3K5w.png'
        })
    );
});