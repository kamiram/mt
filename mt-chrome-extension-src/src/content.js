import * as InboxSDK from '@inboxsdk/core';

InboxSDK.load(2, "sdk_MailTracking_5d204ff84a").then((sdk) => {
  sdk.Compose.registerComposeViewHandler((composeView) => {
    var ready2go = false;
    composeView.on('presending',
      function(event) {
        if(ready2go){
          console.info('tracking canceled');
          return;
        }
        console.info('process tracking: ', sdk.User.getEmailAddress(), sdk.User);
//        chrome.identity.getProfileUserInfo((userInfo) => {
//            console.info(userInfo);
//        });
        event.cancel();
        const to = this.getToRecipients();
        var tostr = '';
        for(var i = 0; i < to.length; i++){
          tostr += to[i].emailAddress + ' ';
        }
        const opt = {
          method: 'POST',
          // mode: 'no-cors',
          body: JSON.stringify(
              {
              "mail_from": this.getFromContact().emailAddress,
              "mail_to": tostr,
              "topic": this.getSubject()
            }
          ),
          headers: {
            'Content-Type': 'text/plain'
          }
        };
        ready2go = true;
        fetch('https://mailtracker.mckira.com/link?' + Date.now(), opt)
          .then((response) =>{
            return response.text();
          })
          .then((text) => {
            const mailtrack = '\n\n<br><hr>Mail track <img width=1 height=1 src=' + text + '>';
            this.setBodyHTML(this.getHTMLContent() + mailtrack);
            this.send();
          });
      }
    );
  });
});
