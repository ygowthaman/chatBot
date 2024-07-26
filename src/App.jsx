import './App.css';
import React, { useState, useEffect } from 'react';
import ScoutBubble from './ScoutBubble';
import UserBubble from './UserBubble';

function App() {

  const [userChat, setUserChat] = useState('');
  const [chatArray, setchatArray] = useState([{
    userMessage: false,
    chatEntry: 'Hello! I am the Netscout Assistant! How can I help you?',
    id: 1
  }]);
  const [currentTime, setCurrentTime] = useState(0);

  useEffect(() => {
    fetch('/time').then(res => res.json()).then(data => {
      setCurrentTime(data.time);
    });
  }, []);

  function handleSubmit(e) {
    e.preventDefault();
    if (!userChat) { return; }
    const newMessage = {
      userMessage: true,
      chatEntry: userChat,
      id: chatArray.length + 1
    };
    chatArray.push(newMessage);
    setUserChat('');

    postChatEntry(newMessage);
  }

  async function postChatEntry(message) {
    const request = new Request("/chat", {
      method: "POST",
      body: JSON.stringify({ message: message.chatEntry }),
      headers: {
        "Content-Type": "application/json",
      },
    });

    chatArray.push({
      userMessage: false,
      chatEntry: '...',
      id: chatArray.length + 1
    });

    let resMessage = '';
    const response = await fetch(request);
    const jsonResponse = await response.json();
    if (jsonResponse.success) {
      const streamResponse = await fetch("/stream")
      const streamResponseText = await streamResponse.text();
      if (streamResponseText.includes("\\")) {
        var validJSONString = streamResponseText.replace(/'/g, '"')
        var parsedResponse = JSON.parse(validJSONString);
        chatArray.pop();
        resMessage = parsedResponse;
      }
      else {
        chatArray.pop();
        resMessage = streamResponseText;
      }
      console.log(chatArray[chatArray.length - 1].chatEntry);
      const deepCopy = [...chatArray]
      deepCopy.push({
        userMessage: false,
        chatEntry: streamResponseText,
        id: chatArray.length + 1
      })
      setchatArray(deepCopy);
    }
  }

  return (
    <div className="App" style={{
      backgroundImage: `url("${process.env.PUBLIC_URL + '/network-mesh.png'}")`
    }} >
      <header className="App-header">
        <img src='./netscout-logo.png'></img>
        <span>ChatBOT</span>
        <span>{currentTime}</span>
      </header>
      <section className="d-flex flex-column align-items-center">
        <div className="chat-history">
          {chatArray.map((message) => {
            if (message.userMessage) {
              return (
                <UserBubble userChat={message} key={message.id} />
              );
            } else {
              return (
                <ScoutBubble scoutChat={message} key={message.id} />
              );
            }
          })}
        </div>
        <form className="d-flex flex-row bd-highlight mb-3 form-section" onSubmit={handleSubmit}>
          <input
            className="form-control"
            id="chatbotTextarea"
            rows="1"
            value={userChat}
            onChange={(e) => setUserChat(e.target.value)}></input>
          <button className="btn btn-primary">Ask</button>
        </form>
      </section>
    </div>
  );
}

export default App;
