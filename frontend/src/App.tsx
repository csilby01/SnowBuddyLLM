

// App.tsx
import AppName from './components/AppName';
import Chat from './components/Chat';
import Headings from './components/Headings';
import SearchBar from './components/SearchBar';
import Button from './components/Button';
import { useState, useEffect } from 'react';
import snowLogo from '/sblogonbg.png'
import './App.css'

const App = () => {

  const [inputValue, setInputValue] = useState('');
  // State to manage chat messages
  const [chatMessages, setChatMessages] = useState<string[]>([]);

  //Ensure no messages are sent while awaiting response from Chatbot
  const [isSending, setIsSending] = useState(false);

  // Function to handle input change
  const handleInputChange = (event: React.ChangeEvent<HTMLTextAreaElement>) => {
    setInputValue(event.target.value);
  };

  // Function to handle button click
  const handleSend = async () => {
    if (inputValue.trim() === '') return;

    const userMessage = `You: ${inputValue}`;
    const newMessages = [...chatMessages, userMessage];
    setChatMessages(newMessages);


    setIsSending(true);

    try {
      const response = await fetch('http://localhost:5000/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: inputValue }),
      });

      const data = await response.json();
      const botReply = `SnowBuddy: ${data.reply}`;
      setChatMessages([...newMessages, botReply]);
    } catch (error) {
      console.error('Error:', error);
      setChatMessages([...newMessages, 'Bot: Sorry, something went wrong.']);
    }

    setInputValue('');
    setIsSending(false);
  };
  return (
    <>
      <AppName>
        <div>
          <img src={snowLogo} className="logo" alt="SnowBuddy logo"  />
        </div>
      </AppName>
      <div>
        <Headings>
          <div>
            <h3>What would you like to know about snowboard gear?</h3>
          </div>
        </Headings>
      </div>
      <div>
       <Chat>
          {/* Render chat messages */}
          {chatMessages.map((message, index) => (
            <div key={index} className = {`chat-${index % 2}`}>
              {message}
            </div>
          ))}
        </Chat>
      </div>
      <div className="searchBar-container">
        <SearchBar>
          <textarea
            className="search-input"
            placeholder="Enter your text"
            value={inputValue}
            onChange={handleInputChange}
          />
          <Button textContent="Send" handleClick={handleSend} disabled={isSending} />
        </SearchBar>
      </div>
    </>
  );
};

export default App;