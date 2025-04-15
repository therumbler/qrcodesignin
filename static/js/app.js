function MainApp(){
    return {
        imageUrl: '',
        isAuthorized: false,
        'codeId': 'GENERATED_UUID',
        connectToWebSocket: function(){
            let protocol = window.location.protocol === 'https:' ? 'wss://' : 'ws://';
            let url = `${protocol}${window.location.host}/ws`;
            let socket = new WebSocket(url);
            socket.onopen = function(event){
                console.log('Connected to WebSocket');
                socket.send(JSON.stringify({'action': 'create_qr_code'}))
            }
            socket.onmessage = function(event){
                let message = JSON.parse(event.data);
                this.processMessage(message);
            }.bind(this);
            socket.onerror = function(event){
                console.error('WebSocket error:', event);
            }
            socket.onclose = function(event){
                console.log('WebSocket closed:', event);
            }
        },
        processMessage: function(message){ 
            if(message.hasOwnProperty('codeId')){
                this.codeId = message.codeId;
                return
            }
            if(message.hasOwnProperty('image_url')){
                console.log('got image_url', message.image_url)
                
                this.imageUrl = message.image_url;
                // console.log('this', this);
                return
            }
            if(message.hasOwnProperty('auth')){
                console.log('got auth', message.auth)
                this.isAuthorized = message.auth;
                this.imageUrl = '';
                return
               
            }
            console.error('unhandled message', message);

        },
        init: function(){
            console.log('init')
            this.connectToWebSocket();
        }
    }
}
