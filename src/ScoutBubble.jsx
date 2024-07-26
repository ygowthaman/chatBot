import './ScoutBubble.css';

const ScoutBubble = ({ scoutChat = {} }) => {
  return (
    <div className="scout" key={scoutChat.id}>
      <img src='./logo.png'></img>
      <label className="scout-chat">{scoutChat.chatEntry}</label>
    </div>
  )
}

export default ScoutBubble;