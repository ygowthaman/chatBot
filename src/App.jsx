import './App.css';
import React, { useState, useEffect } from 'react';
import ScoutBubble from './ScoutBubble';
import UserBubble from './UserBubble';

function App() {

  const [userChat, setUserChat] = useState('');
  const [messages, setMessages] = useState([{
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
      id: messages.length
    };
    messages.push(newMessage);
    setUserChat('');
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
          {messages.map((message) => {
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
