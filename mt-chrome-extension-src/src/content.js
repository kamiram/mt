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
        fetch('https://mailtracker.mckira.com/ext/link?' + Date.now(), opt)
          .then((response) =>{
            return response.text();
          })
          .then((text) => {
	    if(text != ""){
        	console.log('test text: ', text);
          var json = JSON.parse(text);
          var mailtrack = '';
          if(json.banner)
            mailtrack += '\n\n<br><hr>Mail track';

          if(json.url)
            mailtrack += '<img width=1 height=1 src=' + json.url + '>';
        	this.setBodyHTML(this.getHTMLContent() + mailtrack);
	    }
	    this.send();
          });
      }
    );
  });
});
