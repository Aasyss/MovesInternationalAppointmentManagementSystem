console.log("main admin")


const chatRoom = document.querySelector('#room_uuid').textContent.replaceAll('"','')

let chatSocket = null

const chatLogElement = document.querySelector('#chat_log')
const chatInputElement = document.querySelector('#chat_message_input')
const chatSubmitElement = document.querySelector('#chat_message_submit')

chatSocket = new WebSocket("ws://" +'127.0.0.1:8000' + '/ws/' + chatRoom + '/')

function scrollToBottom(){
    chatLogElement.scrollTop = chatLogElement.scrollHeight
}

function sendMessage(){
    chatSocket.send(JSON.stringify({
        'type': 'message',
        'message' : chatInputElement.value,
        'name': document.querySelector('#user_name').textContent.replaceAll('"',''),
        'agent': document.querySelector('#user_id').textContent.replaceAll('"',''),
    }))
    chatInputElement.value = ''
}

function onChatMessage(data){
    console.log('onChatMessage', data)

    if (data.type == 'chat_message') {
        if (!data.agent){

            chatLogElement.innerHTML += `<div id="chatLogElement" style="flex: 1; margin-top: 2px; display: flex; justify-content: flex-start; max-width: 300px; overflow: hidden; margin-left: auto;">
                                            <div style="flex-shrink: 0; height: 45px; width: 45px; border-radius: 50%; background-color: #ccc; text-align: center; padding-top: 10px; overflow: hidden;">${data.initials}</div>
                                            <div>
                                                <div style="background-color: #3b82f6; padding: 0.75rem; border-radius: 0 0.375rem 0.375rem 0; border-radius: 0 6px 6px 0;">
                                                    <p style="font-size: 0.875rem; margin: 0; color: #fff;">${data.message}</p>
                                                </div>
                                                <span style="font-size: 0.75rem; color: #6b7280; margin: 0; align-self: flex-end;">${data.created_at} ago</span>
                                            </div>
                                        </div>`

        }else {
            chatLogElement.innerHTML += `<div id="chatLogElement" style="flex: 1; margin-top: 2px; display: flex; justify-content: flex-end; max-width: 300px; overflow: hidden; margin-left: auto;">
                                            <div>
                                                <div style="background-color: #3b82f6; padding: 0.75rem; border-radius: 0 0.375rem 0.375rem 0; border-radius: 0 6px 6px 0;">
                                                    <p style="font-size: 0.875rem; margin: 0; color: #fff;">${data.message}</p>
                                                </div>
                                                <span style="font-size: 0.75rem; color: #6b7280; margin: 0; align-self: flex-end;">${data.created_at} ago</span>
                                            </div>
                                            <div style="flex-shrink: 0; height: 45px; width: 45px; border-radius: 50%; background-color: #ccc; text-align: center; padding-top: 10px; overflow: hidden;">${data.initials}</div>

                                        </div>`

            }
    }
    scrollToBottom()
}



chatSocket.onmessage = function(e) {
    console.log('on message')
    onChatMessage(JSON.parse(e.data))
}

chatSocket.onclose = function(e){
    console.log('on close')
}

chatSocket.onopen = function(e) {
    console.log('on open')
    scrollToBottom()
}

chatSubmitElement.onclick = function(e) {
    e.preventDefault()

    sendMessage()
}


