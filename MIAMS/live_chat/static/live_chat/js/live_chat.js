
let chatName = ''
let chatSocket = null
let chatWindowUrl = window.location.href
let chatRoomUuid = Math.random().toString(36).slice(2, 12)

console.log('chatuuid', chatRoomUuid)

//const csrftoken = getCookie('csrftoken');


function scrollToBottom(){
    chatLogElement.scrollTop = chatLogElement.scrollHeight
}
function getCookie(name) {
    var cookieValue = null

    if (document.cookie && document.cookie != '') {
        var cookie = document.cookie.split(';')

        for (var i = 0; i < cookie.length; i++) {
            var cookie = cookie[i].trim()

            if (cookie.substring(0, name.length+1) ==(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1))

                break
            }
        }
    }
    return cookieValue
}

function sendMessage(){
    chatSocket.send(JSON.stringify({
        'type': 'message',
        'message' : chatInputElement.value,
        'name': chatName
    }))
    chatInputElement.value = ''
}

function onChatMessage(data){
    console.log('onChatMessage', data)

    if (data.type == 'chat_message') {
        if (data.agent){

            chatLogElement.innerHTML += `<div id="chatLogElement" style="flex: 1; margin-top: 2px; display: flex; justify-content: flex-start; max-width: 300px; overflow: hidden; margin-left: auto;">
                                            <div style="flex-shrink: 0; height: 45px; width: 45px; border-radius: 50%; background-color: #ccc; text-align: center; padding-top: 10px; overflow: hidden;">${data.initials}</div>
                                            <div>
                                                <div style="background-color: #ccc; padding: 0.75rem; border-radius: 0 0.375rem 0.375rem 0; border-radius: 0 6px 6px 0;">
                                                    <p style="font-size: 0.875rem; margin: 0; color: #000000;">${data.message}</p>
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

async function joinChatRoom(){
    console.log('joinchatroom')
    chatName = chatNameElement.value

    console.log('Join as:', chatName)
    console.log('Room uuid:', chatRoomUuid)

    const data = new FormData()
    data.append('name', chatName)
    data.append('url', chatWindowUrl)
    console.log('chat name', chatName)

    await fetch(`/api/create-room/${chatRoomUuid}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken' : getCookie('csrftoken')
        },
        body: data
    })
    .then(function(res) {
        return res.json()
    })
    .then(function(data) {
        console.log('data',data)
    });

//    chatSocket = new WebSocket(`ws://${window.location.host}/ws/${chatRoomUuid}/`)
    chatSocket = new WebSocket("ws://" +'127.0.0.1:8000' + '/ws/' + chatRoomUuid + '/')
    console.log(chatSocket);
    chatSocket.onmessage = function(e) {
        console.log('onMessage')

        onChatMessage(JSON.parse(e.data))
    }

    chatSocket.onopen = function(e) {
        console.log('onOpen - chat socket was open')
        scrollToBottom()
    }

    chatSocket.onclose = function(e) {
        console.log('onClose - chat socket was closed')

    }
}
/**
*Elements
*/

const chatElement = document.querySelector('#chat')
const chatOpenElement = document.querySelector('#chat_open')
const chatJoinElement = document.querySelector('#chat_join')
const chatIconElement = document.querySelector('#chat_icon')
const chatWelcomeElement = document.querySelector('#chat_welcome')
const chatRoomElement = document.querySelector('#chat_room')
const chatNameElement = document.querySelector('#chat_name')
const chatLogElement = document.querySelector('#chat_log')
const chatInputElement = document.querySelector('#chat_message_input')
const chatSubmitElement = document.querySelector('#chat_message_submit')


chatOpenElement.onclick = function(e) {
    e.preventDefault()
        console.log('Clicked'); // Add this line to check if the event handler is triggered.
//    alert('Clicked');
    chatIconElement.style.display = 'none'
    chatWelcomeElement.style.display = 'block'

    return false
}

chatJoinElement.onclick = function(e) {
    e.preventDefault()
        console.log('Clicked'); // Add this line to check if the event handler is triggered.
//    alert('Clicked');
    chatWelcomeElement.style.display = 'none'
    chatRoomElement.style.display = 'block'
    joinChatRoom()
    return false
}

chatSubmitElement.onclick = function(e) {
    e.preventDefault()

    sendMessage()
}
