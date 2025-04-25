// import { useState } from 'react'
// import snowLogo from '/sblogonbg.png'
// import './App.css'

// function App() {
//   const [count, setCount] = useState(0)

//   return (
//     <>
//       <div>
//         <img src={snowLogo} className="logo" alt="SnowBuddy logo"  />
//       </div>
//       <div className="card">
//         <button onClick={() => setCount((count) => count + 1)}>
//           count is not {count - 1}
//         </button>
//       </div>
//     </>
//   )
// }

// export default App

// App.tsx
import AppName from './components/AppName';
import Chat from './components/Chat';
import Headings from './components/Headings';
import SearchBar from './components/SearchBar';
import Button from './components/Button';
import { useState } from 'react';
import snowLogo from '/sblogonbg.png'
import './App.css'

const App = () => {
  // const handleSearch = () => {
  //   alert('Search button clicked!');
  // };
  // State to manage the input value
  const [inputValue, setInputValue] = useState('');
  // State to manage chat messages
  const [chatMessages, setChatMessages] = useState<string[]>([]);

  // Function to handle input change
  const handleInputChange = (event: React.ChangeEvent<HTMLTextAreaElement>) => {
    setInputValue(event.target.value);
  };

  // Function to handle button click
  const handleSend = () => {
    if (inputValue.trim() === '') return;
    // Add the input value to the chat messages
    setChatMessages([...chatMessages, inputValue]);
    // Clear the input field
    setInputValue('');
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
      <div className="chat-container">
       <Chat>
          {/* Render chat messages */}
          {chatMessages.map((message, index) => (
            <div key={index} className="chat-message">
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
          <Button textContent="Send" handleClick={handleSend} />
        </SearchBar>
      </div>
    </>
  );
};

export default App;