import './UserBubble.css';
import * as Icon from 'react-bootstrap-icons';

const UserBubble = ({ userChat = {} }) => {
  return (
    <div className="user">
      <label className="user-chat">{userChat.chatEntry}</label>
      <Icon.PersonCircle color="#bde2f7" size={35} />
    </div>
  )
}

export default UserBubble;